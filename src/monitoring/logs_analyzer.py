"""
Analizador de Logs y Trazabilidad
IE3: Análisis de Logs y Trazabilidad
IE4: Identificación de Patrones y Anomalías (parcial)
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import Counter, defaultdict
import re


class LogsAnalyzer:
    """
    Analiza logs generados por el agente para:
    - Identificar errores y cuellos de botella
    - Detectar patrones en consultas
    - Encontrar anomalías
    """
    
    def __init__(self, log_dir: str = "./logs"):
        """Inicializa el analizador"""
        self.log_dir = Path(log_dir)
        self.logs = []
        self._load_logs()
    
    def _load_logs(self):
        """Carga todos los logs disponibles"""
        if not self.log_dir.exists():
            return
        
        for log_file in self.log_dir.glob("*.log"):
            self._parse_log_file(log_file)
    
    def _parse_log_file(self, log_file: Path):
        """
        Parsea un archivo de log
        Formato esperado: "TIMESTAMP | LEVEL | MESSAGE"
        """
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parsear línea del log
                    parts = line.split(" | ", 2)
                    if len(parts) >= 3:
                        log_entry = {
                            'timestamp': parts[0],
                            'level': parts[1],
                            'message': parts[2],
                            'file': log_file.name
                        }
                        
                        # Extraer tipo de evento (QUERY, TOOL, ERROR, etc.)
                        if ' | ' in parts[2]:
                            event_type = parts[2].split(' | ')[0]
                            log_entry['event_type'] = event_type
                        
                        self.logs.append(log_entry)
        except Exception as e:
            logging.warning(f"Error parsing log {log_file}: {e}")
    
    # ============= IE3: ANÁLISIS DE LOGS =============
    
    def get_errors_summary(self) -> Dict[str, Any]:
        """Resumen de todos los errores encontrados"""
        errors = [log for log in self.logs if log['level'] == 'ERROR']
        
        error_types = defaultdict(list)
        for error in errors:
            msg = error['message']
            # Extraer tipo de error
            match = re.search(r'(\w+Error|\w+Exception)', msg)
            error_type = match.group(1) if match else 'Unknown'
            error_types[error_type].append(error)
        
        return {
            'total_errors': len(errors),
            'error_types': {k: len(v) for k, v in error_types.items()},
            'recent_errors': errors[-10:],  # Últimos 10
            'error_frequency': len(errors) / max(len(self.logs), 1) * 100
        }
    
    def get_bottlenecks(self, threshold_ms: float = 5000) -> List[Dict]:
        """
        Identifica operaciones lentas (cuellos de botella)
        Threshold por defecto: 5 segundos
        """
        bottlenecks = []
        
        for log in self.logs:
            # Buscar logs que contengan tiempo de ejecución
            match = re.search(r'execution_time[":]*\s*(\d+\.?\d*)', log['message'])
            if match:
                exec_time_ms = float(match.group(1)) * 1000
                if exec_time_ms > threshold_ms:
                    bottlenecks.append({
                        'timestamp': log['timestamp'],
                        'execution_time_ms': exec_time_ms,
                        'message': log['message'][:100],
                        'severity': 'HIGH' if exec_time_ms > threshold_ms * 2 else 'MEDIUM'
                    })
        
        return sorted(bottlenecks, key=lambda x: x['execution_time_ms'], reverse=True)
    
    def get_tool_usage_analysis(self) -> Dict[str, Any]:
        """Analiza qué herramientas se usan más y cuál es su éxito"""
        tool_logs = [log for log in self.logs if 'TOOL' in log.get('event_type', '')]
        
        tool_stats = defaultdict(lambda: {'used': 0, 'errors': 0, 'avg_time': 0})
        tool_times = defaultdict(list)
        
        for log in tool_logs:
            # Extraer nombre de herramienta
            match = re.search(r'TOOL \| Name: (\w+)', log['message'])
            if match:
                tool_name = match.group(1)
                tool_stats[tool_name]['used'] += 1
                
                # Contar errores
                if log['level'] == 'ERROR':
                    tool_stats[tool_name]['errors'] += 1
                
                # Guardar tiempos
                time_match = re.search(r'time[":]*\s*(\d+\.?\d*)', log['message'])
                if time_match:
                    tool_times[tool_name].append(float(time_match.group(1)))
        
        # Calcular tiempos promedio
        for tool_name, times in tool_times.items():
            if times:
                tool_stats[tool_name]['avg_time'] = round(sum(times) / len(times), 3)
        
        return dict(tool_stats)
    
    # ============= IE4: PATRONES Y ANOMALÍAS =============
    
    def identify_patterns(self) -> Dict[str, Any]:
        """Identifica patrones en las consultas y respuestas"""
        patterns = {
            'query_types': defaultdict(int),
            'common_errors': Counter(),
            'peak_usage_times': defaultdict(int),
            'user_patterns': defaultdict(int)
        }
        
        query_logs = [log for log in self.logs if log.get('event_type') == 'QUERY']
        
        for log in query_logs:
            # Extraer hora
            try:
                timestamp = datetime.fromisoformat(log['timestamp'])
                hour = timestamp.hour
                patterns['peak_usage_times'][f"Hour_{hour:02d}"] += 1
            except:
                pass
            
            # Clasificar tipo de consulta
            msg = log['message'].lower()
            if 'producto' in msg or 'search' in msg:
                patterns['query_types']['product_search'] += 1
            elif 'descuento' in msg or 'discount' in msg:
                patterns['query_types']['discount'] += 1
            elif 'inventario' in msg or 'inventory' in msg:
                patterns['query_types']['inventory'] += 1
            elif 'historial' in msg or 'history' in msg:
                patterns['query_types']['customer_history'] += 1
            else:
                patterns['query_types']['other'] += 1
        
        return {
            'query_types': dict(patterns['query_types']),
            'peak_usage_times': dict(sorted(patterns['peak_usage_times'].items())),
            'total_queries_analyzed': len(query_logs)
        }
    
    def detect_anomalies(self) -> List[Dict]:
        """
        Detecta anomalías en el comportamiento del agente
        Ejemplos: spike de errores, latencias inusuales, patrones raros
        """
        anomalies = []
        
        # Anomalía 1: Spike de errores
        error_logs = [log for log in self.logs if log['level'] == 'ERROR']
        if len(error_logs) > len(self.logs) * 0.1:  # >10% errores
            anomalies.append({
                'type': 'high_error_rate',
                'severity': 'HIGH',
                'message': f'Error rate too high: {len(error_logs) / len(self.logs) * 100:.1f}%',
                'details': {
                    'error_count': len(error_logs),
                    'total_logs': len(self.logs),
                    'percentage': round(len(error_logs) / max(len(self.logs), 1) * 100, 2)
                }
            })
        
        # Anomalía 2: Patrones inusuales en tipos de consultas
        patterns = self.identify_patterns()
        query_types = patterns['query_types']
        if query_types:
            total = sum(query_types.values())
            for query_type, count in query_types.items():
                if count > total * 0.7:  # Un tipo domina >70%
                    anomalies.append({
                        'type': 'query_type_imbalance',
                        'severity': 'MEDIUM',
                        'message': f'Unusual concentration in query type: {query_type}',
                        'details': {
                            'query_type': query_type,
                            'percentage': round(count / total * 100, 2)
                        }
                    })
        
        # Anomalía 3: Cuellos de botella frecuentes
        bottlenecks = self.get_bottlenecks(threshold_ms=3000)
        if len(bottlenecks) > 5:
            anomalies.append({
                'type': 'frequent_bottlenecks',
                'severity': 'MEDIUM',
                'message': f'Frequent slow operations detected ({len(bottlenecks)} operations >3s)',
                'details': {
                    'bottleneck_count': len(bottlenecks),
                    'slowest': bottlenecks[0]['execution_time_ms'] if bottlenecks else 0
                }
            })
        
        return anomalies
    
    def generate_report(self, output_file: str = "./logs/analysis_report.json") -> Path:
        """Genera reporte completo de análisis"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_logs': len(self.logs),
            'errors_summary': self.get_errors_summary(),
            'tool_analysis': self.get_tool_usage_analysis(),
            'patterns': self.identify_patterns(),
            'anomalies': self.detect_anomalies(),
            'bottlenecks': self.get_bottlenecks(threshold_ms=3000),
            'recommendations': self._generate_recommendations()
        }
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return output_path
    
    def _generate_recommendations(self) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        errors = self.get_errors_summary()
        if errors['error_frequency'] > 5:
            recommendations.append(
                "⚠️ Error rate is above 5%. Review error logs and implement error handling improvements."
            )
        
        bottlenecks = self.get_bottlenecks()
        if bottlenecks:
            recommendations.append(
                f"⚡ Found {len(bottlenecks)} slow operations. Consider optimizing tool execution or caching."
            )
        
        tool_analysis = self.get_tool_usage_analysis()
        for tool, stats in tool_analysis.items():
            if stats['used'] > 0 and stats['errors'] / stats['used'] > 0.1:
                recommendations.append(
                    f"🔧 Tool '{tool}' has high error rate ({stats['errors']}/{stats['used']}). Review implementation."
                )
        
        if not recommendations:
            recommendations.append("✅ System is performing well. No critical issues detected.")
        
        return recommendations
