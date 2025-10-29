"""
Agente Executor - Orquestador principal del sistema inteligente
Implementa arquitectura ReAct (Reasoning + Acting) con LangChain
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from typing import List, Dict, Any, Optional, Tuple
import json
from datetime import datetime
import os

from .tools import initialize_tools
from .prompts import AGENT_SYSTEM_PROMPT
from .demo_llm import DemoPasteleriaLLM


class PasteleriaAgentExecutor:
    """
    Orquestador principal del agente inteligente de Pastelería 1000 Sabores
    Gestiona herramientas, decisiones y flujo de conversación
    """
    
    def __init__(
        self, 
        data_loader, 
        discount_calculator,
        openai_api_key: str,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.3,
        max_iterations: int = 10,
        verbose: bool = True
    ):
        """
        Inicializa el agente con todas sus dependencias
        
        Args:
            data_loader: Instancia de PasteleriaDataLoader
            discount_calculator: Instancia de DiscountCalculator
            openai_api_key: API Key de OpenAI
            model_name: Modelo a usar (gpt-3.5-turbo o gpt-4)
            temperature: Control de creatividad (0.0-1.0)
            max_iterations: Máximo de iteraciones del agente
            verbose: Si True, muestra logs detallados
        """
        self.data_loader = data_loader
        self.discount_calculator = discount_calculator
        self.verbose = verbose
        
        # Detectar modo DEMO o usar API
        use_demo = os.getenv("USE_DEMO_MODE", "false").lower() == "true"
        
        if use_demo or openai_api_key == "DEMO_MODE":
            # Usar LLM Demo (sin consumir API)
            print("🎭 Usando MODO DEMO (sin consumir API)")
            self.llm = DemoPasteleriaLLM()
        else:
            # Detectar si usar GitHub Models o OpenAI
            github_token = os.getenv("GITHUB_TOKEN")
            github_base_url = os.getenv("GITHUB_BASE_URL", "https://models.inference.ai.azure.com")
            
            if github_token and not openai_api_key.startswith("sk-"):
                # Usar GitHub Models (GRATIS)
                print("🔄 Usando GitHub Models (gratis)")
                self.llm = ChatOpenAI(
                    model="gpt-4o",
                    temperature=temperature,
                    api_key=github_token,
                    base_url=github_base_url
                )
            else:
                # Usar OpenAI
                print("🔄 Usando OpenAI API")
                self.llm = ChatOpenAI(
                    model=model_name,
                    temperature=temperature,
                    openai_api_key=openai_api_key
                )
        
        # Inicializar herramientas
        self.tools = initialize_tools(data_loader, discount_calculator)
        
        # Crear el prompt del agente
        self.prompt = self._create_agent_prompt()
        
        # Crear el agente ReAct
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Crear el executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            max_iterations=max_iterations,
            verbose=verbose,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
        
        # Tracking de ejecución
        self.execution_log = []
        
        print(f"✅ Agente inteligente inicializado con {len(self.tools)} herramientas")
        print(f"🤖 Modelo: {model_name} | Temperatura: {temperature}")
    
    def _create_agent_prompt(self) -> PromptTemplate:
        """Crea el prompt template para el agente ReAct"""
        
        template = AGENT_SYSTEM_PROMPT + """

Tienes acceso a las siguientes herramientas:

{tools}

Usa el siguiente formato:

Pregunta: la consulta del cliente que debes responder
Thought: siempre debes pensar qué hacer
Action: la acción a tomar, debe ser una de [{tool_names}]
Action Input: el input de la acción
Observation: el resultado de la acción
... (este Thought/Action/Action Input/Observation puede repetirse N veces)
Thought: Ahora sé la respuesta final
Final Answer: la respuesta final al cliente

¡Importante! Siempre usa el formato exacto arriba.

Pregunta: {input}

Thought: {agent_scratchpad}
"""
        
        return PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad"],
            partial_variables={
                "tools": self._format_tools_description(),
                "tool_names": ", ".join([tool.name for tool in self.tools])
            }
        )
    
    def _format_tools_description(self) -> str:
        """Formatea la descripción de las herramientas disponibles"""
        descriptions = []
        for tool in self.tools:
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)
    
    def execute(
        self, 
        query: str, 
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta el agente para responder una consulta
        
        Args:
            query: Consulta del cliente
            chat_history: Historial de conversación (opcional)
        
        Returns:
            Dict con la respuesta y metadata de ejecución
        """
        start_time = datetime.now()
        
        try:
            # Preparar input con contexto
            agent_input = {
                "input": query
            }
            
            # Si hay historial, agregarlo al contexto
            if chat_history:
                context = self._format_chat_history(chat_history)
                agent_input["input"] = f"Contexto previo: {context}\n\nPregunta actual: {query}"
            
            # Ejecutar el agente
            result = self.agent_executor.invoke(agent_input)
            
            # Extraer información de la ejecución
            output = result.get("output", "")
            intermediate_steps = result.get("intermediate_steps", [])
            
            # Procesar pasos intermedios
            execution_trace = self._process_intermediate_steps(intermediate_steps)
            
            # Calcular tiempo de ejecución
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Construir respuesta
            response = {
                "success": True,
                "answer": output,
                "execution_trace": execution_trace,
                "tools_used": [step["tool"] for step in execution_trace],
                "execution_time": execution_time,
                "iterations": len(intermediate_steps),
                "timestamp": datetime.now().isoformat()
            }
            
            # Log de ejecución
            self.execution_log.append({
                "query": query,
                "response": response,
                "timestamp": datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            error_trace = traceback.format_exc()
            
            # Imprimir error detallado en consola
            print("❌ ERROR EN AGENT EXECUTOR:")
            print(f"Tipo: {type(e).__name__}")
            print(f"Mensaje: {error_msg}")
            print(f"Trace:\n{error_trace}")
            
            error_response = {
                "success": False,
                "answer": self._generate_error_response(str(e)),
                "error": str(e),
                "error_trace": error_trace,
                "execution_trace": [],
                "tools_used": [],
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
            
            return error_response
    
    def _process_intermediate_steps(
        self, 
        intermediate_steps: List[Tuple[AgentAction, str]]
    ) -> List[Dict[str, Any]]:
        """
        Procesa los pasos intermedios de ejecución del agente
        
        Args:
            intermediate_steps: Lista de tuplas (acción, observación)
        
        Returns:
            Lista de diccionarios con información estructurada
        """
        trace = []
        
        for idx, (action, observation) in enumerate(intermediate_steps, 1):
            step_info = {
                "step": idx,
                "thought": getattr(action, 'log', '').split('Action:')[0].replace('Thought:', '').strip(),
                "tool": action.tool,
                "tool_input": action.tool_input,
                "observation": observation[:500] + "..." if len(observation) > 500 else observation
            }
            trace.append(step_info)
        
        return trace
    
    def _format_chat_history(self, chat_history: List[Dict[str, str]]) -> str:
        """Formatea el historial de chat para contexto"""
        formatted = []
        for msg in chat_history[-5:]:  # Últimos 5 mensajes
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted.append(f"{role.capitalize()}: {content}")
        return "\n".join(formatted)
    
    def _generate_error_response(self, error: str) -> str:
        """Genera una respuesta amigable ante errores"""
        return f"""
        Lo siento, tuve un problema procesando tu consulta. 😔
        
        Pero no te preocupes, déjame intentar ayudarte de otra forma:
        
        - Puedes reformular tu pregunta de manera más específica
        - Puedo mostrarte nuestro catálogo completo
        - O puedes preguntarme por categorías específicas (tortas, postres, productos veganos, etc.)
        
        ¿Cómo te gustaría continuar? 🍰
        """
    
    def get_execution_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de uso del agente
        
        Returns:
            Dict con métricas de ejecución
        """
        if not self.execution_log:
            return {
                "total_queries": 0,
                "avg_execution_time": 0,
                "success_rate": 0,
                "most_used_tools": []
            }
        
        total_queries = len(self.execution_log)
        successful = sum(1 for log in self.execution_log if log["response"]["success"])
        
        all_tools = []
        total_time = 0
        
        for log in self.execution_log:
            total_time += log["response"]["execution_time"]
            all_tools.extend(log["response"]["tools_used"])
        
        # Contar herramientas más usadas
        tool_counts = {}
        for tool in all_tools:
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        most_used = sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_queries": total_queries,
            "successful_queries": successful,
            "success_rate": (successful / total_queries * 100) if total_queries > 0 else 0,
            "avg_execution_time": total_time / total_queries if total_queries > 0 else 0,
            "most_used_tools": most_used[:3],
            "total_tool_calls": len(all_tools)
        }
    
    def reset_log(self):
        """Reinicia el log de ejecución"""
        self.execution_log = []
        print("🔄 Log de ejecución reiniciado")


# ==================== FUNCIÓN HELPER ====================

def create_agent(
    data_loader,
    discount_calculator,
    openai_api_key: str,
    **kwargs
) -> PasteleriaAgentExecutor:
    """
    Factory function para crear el agente
    
    Args:
        data_loader: Instancia de PasteleriaDataLoader
        discount_calculator: Instancia de DiscountCalculator
        openai_api_key: API Key de OpenAI
        **kwargs: Argumentos adicionales para el agente
    
    Returns:
        Instancia configurada de PasteleriaAgentExecutor
    """
    return PasteleriaAgentExecutor(
        data_loader=data_loader,
        discount_calculator=discount_calculator,
        openai_api_key=openai_api_key,
        **kwargs
    )
