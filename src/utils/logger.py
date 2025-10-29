"""
Sistema de logging para el agente inteligente
Registra todas las acciones, decisiones y herramientas usadas
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)


class AgentLogger:
    """
    Logger especializado para el agente inteligente
    Registra decisiones, uso de herramientas y métricas
    """
    
    def __init__(
        self,
        log_dir: str = "./logs",
        log_level: int = logging.INFO,
        console_output: bool = True
    ):
        """
        Inicializa el sistema de logging
        
        Args:
            log_dir: Directorio para guardar logs
            log_level: Nivel de logging
            console_output: Si True, también imprime en consola
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurar logger
        self.logger = logging.getLogger("PasteleriaAgent")
        self.logger.setLevel(log_level)
        
        # Archivo de log con timestamp
        log_file = self.log_dir / f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Handler para archivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        
        # Handler para consola (opcional)
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        self.console_output = console_output
        
        print(f"📝 Logger inicializado: {log_file}")
    
    def log_query(self, query: str, user_id: str = "anonymous"):
        """Registra una consulta del usuario"""
        self.logger.info(f"QUERY | User: {user_id} | Query: {query}")
        if self.console_output:
            print(f"{Fore.CYAN}📥 CONSULTA: {query}{Style.RESET_ALL}")
    
    def log_thought(self, thought: str):
        """Registra un pensamiento del agente"""
        self.logger.info(f"THOUGHT | {thought}")
        if self.console_output:
            print(f"{Fore.YELLOW}💭 PENSAMIENTO: {thought}{Style.RESET_ALL}")
    
    def log_tool_call(self, tool_name: str, tool_input: Dict[str, Any]):
        """Registra el uso de una herramienta"""
        self.logger.info(f"TOOL | Name: {tool_name} | Input: {json.dumps(tool_input, ensure_ascii=False)}")
        if self.console_output:
            print(f"{Fore.MAGENTA}🔧 HERRAMIENTA: {tool_name}{Style.RESET_ALL}")
            print(f"   Input: {tool_input}")
    
    def log_observation(self, observation: str):
        """Registra la observación resultante de una herramienta"""
        truncated = observation[:200] + "..." if len(observation) > 200 else observation
        self.logger.info(f"OBSERVATION | {truncated}")
        if self.console_output:
            print(f"{Fore.GREEN}👁️ OBSERVACIÓN: {truncated}{Style.RESET_ALL}")
    
    def log_answer(self, answer: str):
        """Registra la respuesta final del agente"""
        self.logger.info(f"ANSWER | {answer}")
        if self.console_output:
            print(f"{Fore.BLUE}✅ RESPUESTA FINAL{Style.RESET_ALL}")
    
    def log_error(self, error: str, context: Dict[str, Any] = None):
        """Registra un error"""
        self.logger.error(f"ERROR | {error} | Context: {context}")
        if self.console_output:
            print(f"{Fore.RED}❌ ERROR: {error}{Style.RESET_ALL}")
    
    def log_execution_trace(self, trace: List[Dict[str, Any]]):
        """Registra el trace completo de ejecución"""
        self.logger.info(f"EXECUTION_TRACE | Steps: {len(trace)}")
        
        for step in trace:
            self.logger.info(f"  Step {step.get('step')}: {step.get('tool')} -> {step.get('observation')[:100]}")
        
        if self.console_output:
            print(f"{Fore.CYAN}📊 TRACE DE EJECUCIÓN: {len(trace)} pasos{Style.RESET_ALL}")
    
    def log_metrics(self, metrics: Dict[str, Any]):
        """Registra métricas de rendimiento"""
        self.logger.info(f"METRICS | {json.dumps(metrics, ensure_ascii=False)}")
        if self.console_output:
            print(f"{Fore.GREEN}📈 MÉTRICAS:{Style.RESET_ALL}")
            for key, value in metrics.items():
                print(f"   {key}: {value}")
    
    def log_memory_operation(self, operation: str, details: str):
        """Registra operaciones de memoria"""
        self.logger.info(f"MEMORY | {operation} | {details}")
        if self.console_output:
            print(f"{Fore.MAGENTA}💾 MEMORIA: {operation}{Style.RESET_ALL}")


class ExecutionTracker:
    """
    Rastrea la ejecución del agente para análisis y debugging
    """
    
    def __init__(self):
        self.executions = []
        self.current_execution = None
    
    def start_execution(self, query: str):
        """Inicia el rastreo de una nueva ejecución"""
        self.current_execution = {
            "query": query,
            "start_time": datetime.now(),
            "steps": [],
            "tools_used": [],
            "result": None,
            "error": None
        }
    
    def add_step(
        self,
        step_num: int,
        thought: str,
        tool: str,
        tool_input: Any,
        observation: str
    ):
        """Agrega un paso de ejecución"""
        if self.current_execution:
            self.current_execution["steps"].append({
                "step": step_num,
                "thought": thought,
                "tool": tool,
                "tool_input": tool_input,
                "observation": observation,
                "timestamp": datetime.now().isoformat()
            })
            
            if tool not in self.current_execution["tools_used"]:
                self.current_execution["tools_used"].append(tool)
    
    def finish_execution(self, result: str, error: str = None):
        """Finaliza el rastreo de la ejecución actual"""
        if self.current_execution:
            self.current_execution["result"] = result
            self.current_execution["error"] = error
            self.current_execution["end_time"] = datetime.now()
            self.current_execution["duration"] = (
                self.current_execution["end_time"] - 
                self.current_execution["start_time"]
            ).total_seconds()
            
            self.executions.append(self.current_execution)
            self.current_execution = None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de todas las ejecuciones"""
        if not self.executions:
            return {"total_executions": 0}
        
        total_executions = len(self.executions)
        successful = sum(1 for e in self.executions if e.get("error") is None)
        
        all_tools = []
        total_steps = 0
        total_duration = 0
        
        for execution in self.executions:
            all_tools.extend(execution.get("tools_used", []))
            total_steps += len(execution.get("steps", []))
            total_duration += execution.get("duration", 0)
        
        # Contar herramientas más usadas
        tool_counts = {}
        for tool in all_tools:
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        return {
            "total_executions": total_executions,
            "successful": successful,
            "success_rate": (successful / total_executions * 100),
            "avg_steps": total_steps / total_executions,
            "avg_duration": total_duration / total_executions,
            "most_used_tools": sorted(
                tool_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }
    
    def export_to_json(self, filename: str):
        """Exporta todas las ejecuciones a JSON"""
        output = {
            "export_date": datetime.now().isoformat(),
            "total_executions": len(self.executions),
            "executions": [
                {
                    **e,
                    "start_time": e["start_time"].isoformat(),
                    "end_time": e["end_time"].isoformat()
                }
                for e in self.executions
            ],
            "statistics": self.get_statistics()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Ejecuciones exportadas a {filename}")


# ==================== FUNCIONES HELPER ====================

def create_logger(
    log_dir: str = "./logs",
    console_output: bool = True
) -> AgentLogger:
    """
    Factory function para crear un logger
    
    Args:
        log_dir: Directorio de logs
        console_output: Si mostrar en consola
    
    Returns:
        Instancia de AgentLogger
    """
    return AgentLogger(
        log_dir=log_dir,
        console_output=console_output
    )


def create_tracker() -> ExecutionTracker:
    """
    Factory function para crear un execution tracker
    
    Returns:
        Instancia de ExecutionTracker
    """
    return ExecutionTracker()
