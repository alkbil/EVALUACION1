"""
Sistema de Memoria de Corto Plazo
Mantiene contexto de la conversación actual usando LangChain Memory
"""

from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class ShortTermMemory:
    """
    Gestiona la memoria de corto plazo (sesión actual)
    Mantiene contexto para referencias anafóricas y continuidad conversacional
    """
    
    def __init__(
        self,
        memory_type: str = "buffer",
        openai_api_key: Optional[str] = None,
        max_token_limit: int = 2000
    ):
        """
        Inicializa el sistema de memoria de corto plazo
        
        Args:
            memory_type: Tipo de memoria ("buffer" o "summary")
            openai_api_key: API key para memoria tipo summary
            max_token_limit: Límite de tokens para la memoria
        """
        self.memory_type = memory_type
        self.max_token_limit = max_token_limit
        
        if memory_type == "buffer":
            # Memoria buffer: mantiene todos los mensajes
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="output"
            )
        elif memory_type == "summary":
            # Memoria summary: resume conversaciones largas
            if not openai_api_key:
                raise ValueError("openai_api_key requerido para memoria tipo summary")
            
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.1,
                openai_api_key=openai_api_key
            )
            
            self.memory = ConversationSummaryMemory(
                llm=llm,
                memory_key="chat_history",
                return_messages=True,
                output_key="output"
            )
        else:
            raise ValueError(f"Tipo de memoria no soportado: {memory_type}")
        
        # Metadata adicional
        self.session_start = datetime.now()
        self.message_count = 0
        
        print(f"✅ Memoria de corto plazo inicializada (tipo: {memory_type})")
    
    def add_message(self, user_message: str, agent_response: str):
        """
        Agrega un intercambio de mensajes a la memoria
        
        Args:
            user_message: Mensaje del usuario
            agent_response: Respuesta del agente
        """
        self.memory.save_context(
            {"input": user_message},
            {"output": agent_response}
        )
        self.message_count += 1
    
    def get_context(self) -> str:
        """
        Obtiene el contexto actual de la conversación
        
        Returns:
            String con el historial formateado
        """
        memory_vars = self.memory.load_memory_variables({})
        chat_history = memory_vars.get("chat_history", [])
        
        if not chat_history:
            return ""
        
        # Formatear historial
        formatted = []
        for msg in chat_history:
            if hasattr(msg, 'type'):
                role = "Usuario" if msg.type == "human" else "Asistente"
                content = msg.content
            else:
                role = "Mensaje"
                content = str(msg)
            
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)
    
    def get_messages(self) -> List[Dict[str, str]]:
        """
        Obtiene los mensajes en formato de lista de diccionarios
        
        Returns:
            Lista de mensajes [{role, content}]
        """
        memory_vars = self.memory.load_memory_variables({})
        chat_history = memory_vars.get("chat_history", [])
        
        messages = []
        for msg in chat_history:
            if hasattr(msg, 'type'):
                role = "user" if msg.type == "human" else "assistant"
                content = msg.content
                messages.append({"role": role, "content": content})
        
        return messages
    
    def get_last_n_messages(self, n: int = 5) -> List[Dict[str, str]]:
        """
        Obtiene los últimos N mensajes
        
        Args:
            n: Número de mensajes a recuperar
        
        Returns:
            Lista de últimos N mensajes
        """
        all_messages = self.get_messages()
        return all_messages[-n:] if len(all_messages) > n else all_messages
    
    def clear(self):
        """Limpia la memoria de la sesión actual"""
        self.memory.clear()
        self.message_count = 0
        self.session_start = datetime.now()
        print("🔄 Memoria de corto plazo limpiada")
    
    def get_session_info(self) -> Dict[str, Any]:
        """
        Obtiene información de la sesión actual
        
        Returns:
            Dict con metadata de la sesión
        """
        duration = (datetime.now() - self.session_start).total_seconds()
        
        return {
            "session_start": self.session_start.isoformat(),
            "duration_seconds": duration,
            "message_count": self.message_count,
            "memory_type": self.memory_type,
            "has_context": self.message_count > 0
        }
    
    def extract_user_preferences(self) -> Dict[str, List[str]]:
        """
        Extrae preferencias del usuario de la conversación
        
        Returns:
            Dict con categorías de preferencias identificadas
        """
        context = self.get_context().lower()
        
        preferences = {
            "categorias_interes": [],
            "restricciones": [],
            "ocasiones": [],
            "presupuesto": []
        }
        
        # Detectar categorías de interés
        if "vegano" in context or "vegana" in context:
            preferences["categorias_interes"].append("Productos veganos")
        if "sin azúcar" in context or "diabético" in context:
            preferences["categorias_interes"].append("Productos sin azúcar")
        if "cuadrada" in context:
            preferences["categorias_interes"].append("Tortas cuadradas")
        if "circular" in context:
            preferences["categorias_interes"].append("Tortas circulares")
        
        # Detectar restricciones
        if "alérgico" in context or "alergia" in context:
            preferences["restricciones"].append("Alergias alimentarias")
        if "vegetariano" in context:
            preferences["restricciones"].append("Vegetariano")
        
        # Detectar ocasiones
        if "cumpleaños" in context:
            preferences["ocasiones"].append("Cumpleaños")
        if "boda" in context or "matrimonio" in context:
            preferences["ocasiones"].append("Boda")
        if "aniversario" in context:
            preferences["ocasiones"].append("Aniversario")
        
        # Detectar presupuesto
        if "económico" in context or "barato" in context:
            preferences["presupuesto"].append("Económico")
        elif "premium" in context or "lujo" in context:
            preferences["presupuesto"].append("Premium")
        
        return preferences


class ConversationContext:
    """
    Gestiona el contexto extendido de la conversación
    Permite referencias anafóricas ("esa torta", "la anterior", etc.)
    """
    
    def __init__(self):
        self.last_product_mentioned = None
        self.last_products_shown = []
        self.last_calculation = None
        self.current_topic = None
        
    def update_product_context(self, products: List[Dict[str, Any]]):
        """Actualiza el contexto de productos mostrados"""
        if products:
            self.last_product_mentioned = products[0]
            self.last_products_shown = products
    
    def update_calculation_context(self, calculation: Dict[str, Any]):
        """Actualiza el contexto de cálculos realizados"""
        self.last_calculation = calculation
    
    def update_topic(self, topic: str):
        """Actualiza el tema actual de conversación"""
        self.current_topic = topic
    
    def resolve_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        """
        Resuelve referencias anafóricas
        
        Args:
            reference: Referencia del usuario ("esa", "la anterior", etc.)
        
        Returns:
            Producto o información referenciada
        """
        reference_lower = reference.lower()
        
        if reference_lower in ["esa", "ese", "esa torta", "ese producto"]:
            return self.last_product_mentioned
        elif reference_lower in ["la anterior", "el anterior", "la que mencionaste"]:
            return self.last_product_mentioned
        elif reference_lower in ["la primera", "el primero"]:
            return self.last_products_shown[0] if self.last_products_shown else None
        elif reference_lower in ["la última", "el último"]:
            return self.last_products_shown[-1] if self.last_products_shown else None
        
        return None
    
    def get_context_summary(self) -> str:
        """Obtiene resumen del contexto actual"""
        summary = []
        
        if self.last_product_mentioned:
            summary.append(f"Último producto: {self.last_product_mentioned.get('nombre', 'N/A')}")
        
        if self.last_products_shown:
            summary.append(f"Productos mostrados: {len(self.last_products_shown)}")
        
        if self.current_topic:
            summary.append(f"Tema actual: {self.current_topic}")
        
        return " | ".join(summary) if summary else "Sin contexto"
    
    def clear(self):
        """Limpia el contexto"""
        self.last_product_mentioned = None
        self.last_products_shown = []
        self.last_calculation = None
        self.current_topic = None


# ==================== FUNCIÓN HELPER ====================

def create_short_term_memory(
    memory_type: str = "buffer",
    openai_api_key: Optional[str] = None
) -> ShortTermMemory:
    """
    Factory function para crear memoria de corto plazo
    
    Args:
        memory_type: Tipo de memoria ("buffer" o "summary")
        openai_api_key: API key si se usa summary
    
    Returns:
        Instancia de ShortTermMemory
    """
    return ShortTermMemory(
        memory_type=memory_type,
        openai_api_key=openai_api_key
    )
