"""
Módulo de Métricas de Observabilidad
Calcula: Precisión, Consistencia, Latencia, Recursos, Errores
"""

import time
import psutil
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
from pathlib import Path


class ObservabilityMetrics:
    """
    Sistema de métricas para monitorear el desempeño del agente
    IE1: Métricas de Precisión, Consistencia y Errores
    IE2: Métricas de Latencia y Recursos
    """
    
    def __init__(self, metrics_file: str = "./metrics/metrics.json"):
        """Inicializa el sistema de métricas"""
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Métricas básicas
        self.total_queries = 0
        self.correct_responses = 0
        self.consistency_scores = []
        self.errors = []
        self.executions = []
        
        # Métricas por tipo de consulta
        self.queries_by_type = defaultdict(lambda: {"total": 0, "correct": 0})
        
        # Métricas de recursos
        self.latencies = []
        self.memory_usage = []
        self.cpu_usage = []
        self.tokens_used = []
        
        # Cargar métricas existentes
        self._load_metrics()
    
    def _load_metrics(self):
        """Carga métricas previas si existen"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.total_queries = data.get('total_queries', 0)
                    self.correct_responses = data.get('correct_responses', 0)
                    self.executions = data.get('executions', [])
                    self.errors = data.get('errors', [])
            except:
                pass
    
    def _save_metrics(self):
        """Persiste las métricas a disco"""
        metrics_data = {
            'timestamp': datetime.now().isoformat(),
            'total_queries': self.total_queries,
            'correct_responses': self.correct_responses,
            'precision': self.calculate_precision(),
            'error_frequency': self.calculate_error_frequency(),
            'executions': self.executions[-100:],  # Últimas 100
            'errors': self.errors[-50:],  # Últimos 50 errores
        }
        
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, ensure_ascii=False, indent=2)
    
    # ============= IE1: PRECISIÓN, CONSISTENCIA, ERRORES =============
    
    def calculate_precision(self) -> float:
        """Precisión = respuestas correctas / total consultas"""
        if self.total_queries == 0:
            return 0.0
        return round((self.correct_responses / self.total_queries) * 100, 2)
    
    def calculate_consistency(self, response_a: str, response_b: str) -> float:
        """
        Mide consistencia entre dos respuestas similares
        Usa token overlap como métrica simple
        0.0 = completamente diferente, 100.0 = idénticas
        """
        tokens_a = set(response_a.lower().split())
        tokens_b = set(response_b.lower().split())
        
        if len(tokens_a) == 0 or len(tokens_b) == 0:
            return 0.0
        
        intersection = len(tokens_a & tokens_b)
        union = len(tokens_a | tokens_b)
        
        return round((intersection / union) * 100, 2)
    
    def calculate_error_frequency(self) -> float:
        """Errores por cada 100 consultas"""
        if self.total_queries == 0:
            return 0.0
        return round((len(self.errors) / self.total_queries) * 100, 2)
    
    def record_query(self, query: str, query_type: str = "general"):
        """Registra inicio de una consulta"""
        self.total_queries += 1
        self.queries_by_type[query_type]["total"] += 1
        
        return {
            'query_id': self.total_queries,
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'type': query_type
        }
    
    def record_response(
        self,
        query_id: int,
        response: str,
        is_correct: bool = None,
        query_type: str = "general"
    ):
        """Registra una respuesta evaluada"""
        if is_correct:
            self.correct_responses += 1
            self.queries_by_type[query_type]["correct"] += 1
        
        self.executions.append({
            'query_id': query_id,
            'correct': is_correct,
            'timestamp': datetime.now().isoformat(),
            'response_length': len(response)
        })
        
        self._save_metrics()
    
    def record_error(self, error_type: str, error_message: str, context: Dict = None):
        """Registra un error ocurrido"""
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'message': error_message,
            'context': context or {}
        }
        
        self.errors.append(error_record)
        self._save_metrics()
    
    # ============= IE2: LATENCIA Y RECURSOS =============
    
    def measure_resources(
        self,
        execution_time: float,
        tokens_prompt: int = 0,
        tokens_response: int = 0
    ) -> Dict[str, Any]:
        """
        Mide recursos utilizados en una ejecución
        """
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / (1024 * 1024)
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        resource_data = {
            'timestamp': datetime.now().isoformat(),
            'latency_ms': round(execution_time * 1000, 2),
            'memory_mb': round(memory_mb, 2),
            'cpu_percent': cpu_percent,
            'tokens_prompt': tokens_prompt,
            'tokens_response': tokens_response,
            'tokens_total': tokens_prompt + tokens_response
        }
        
        # Guardar en listas
        self.latencies.append(resource_data['latency_ms'])
        self.memory_usage.append(memory_mb)
        self.cpu_usage.append(cpu_percent)
        self.tokens_used.append(tokens_prompt + tokens_response)
        
        return resource_data
    
    def get_latency_stats(self) -> Dict[str, float]:
        """Estadísticas de latencia"""
        if not self.latencies:
            return {}
        
        return {
            'min_ms': min(self.latencies),
            'max_ms': max(self.latencies),
            'avg_ms': round(sum(self.latencies) / len(self.latencies), 2),
            'total_queries': len(self.latencies)
        }
    
    def get_resource_stats(self) -> Dict[str, Any]:
        """Estadísticas de recursos"""
        stats = {}
        
        if self.memory_usage:
            stats['memory'] = {
                'min_mb': min(self.memory_usage),
                'max_mb': max(self.memory_usage),
                'avg_mb': round(sum(self.memory_usage) / len(self.memory_usage), 2)
            }
        
        if self.cpu_usage:
            stats['cpu'] = {
                'min_percent': min(self.cpu_usage),
                'max_percent': max(self.cpu_usage),
                'avg_percent': round(sum(self.cpu_usage) / len(self.cpu_usage), 2)
            }
        
        if self.tokens_used:
            stats['tokens'] = {
                'total': sum(self.tokens_used),
                'avg_per_query': round(sum(self.tokens_used) / len(self.tokens_used), 2),
                'queries': len(self.tokens_used)
            }
        
        return stats
    
    # ============= ESTADÍSTICAS GENERALES =============
    
    def get_summary(self) -> Dict[str, Any]:
        """Resumen completo de métricas"""
        return {
            'total_queries': self.total_queries,
            'precision': self.calculate_precision(),
            'error_frequency': self.calculate_error_frequency(),
            'error_count': len(self.errors),
            'error_types': Counter([e['type'] for e in self.errors]),
            'latency_stats': self.get_latency_stats(),
            'resource_stats': self.get_resource_stats(),
            'top_errors': self._get_top_errors(5),
            'queries_by_type': dict(self.queries_by_type)
        }
    
    def _get_top_errors(self, top_n: int = 5) -> List[Dict]:
        """Retorna los N errores más frecuentes"""
        error_types = Counter([e['type'] for e in self.errors])
        return [
            {'type': error_type, 'count': count}
            for error_type, count in error_types.most_common(top_n)
        ]
    
    def export_metrics(self, output_file: str = "./metrics/export.json"):
        """Exporta todas las métricas a un archivo"""
        summary = self.get_summary()
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        return output_path
