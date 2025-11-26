"""
Detector de Anomalías y Patrones Avanzado
IE4: Identificación de Patrones y Anomalías
IE7: Propuestas de Mejora basadas en datos
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict


class AnomalyDetector:
    """
    Detección avanzada de anomalías usando estadísticas
    """
    
    def __init__(self):
        self.data_points = defaultdict(list)
        self.baselines = {}
    
    def add_measurement(self, metric_name: str, value: float, timestamp: datetime = None):
        """Agrega una medición a las series de tiempo"""
        if timestamp is None:
            timestamp = datetime.now()
        
        self.data_points[metric_name].append({
            'value': value,
            'timestamp': timestamp
        })
    
    def calculate_baseline(self, metric_name: str, window_size: int = 100):
        """
        Calcula línea base estadística para un métrica
        Usa media y desviación estándar
        """
        if metric_name not in self.data_points:
            return None
        
        values = [dp['value'] for dp in self.data_points[metric_name][-window_size:]]
        
        if len(values) < 2:
            return None
        
        self.baselines[metric_name] = {
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'median': np.median(values)
        }
        
        return self.baselines[metric_name]
    
    def detect_spike(self, metric_name: str, threshold_std: float = 3.0) -> List[Dict]:
        """
        Detecta spikes en una métrica
        Spike = valor > media + (threshold_std * desv_std)
        """
        if metric_name not in self.baselines:
            self.calculate_baseline(metric_name)
        
        if metric_name not in self.baselines:
            return []
        
        baseline = self.baselines[metric_name]
        mean = baseline['mean']
        std = baseline['std']
        
        threshold = mean + (threshold_std * std)
        
        spikes = []
        for dp in self.data_points[metric_name]:
            if dp['value'] > threshold:
                spikes.append({
                    'value': dp['value'],
                    'timestamp': dp['timestamp'],
                    'deviation': (dp['value'] - mean) / std if std > 0 else 0,
                    'severity': 'HIGH' if dp['value'] > mean + (4 * std) else 'MEDIUM'
                })
        
        return spikes
    
    def detect_drift(self, metric_name: str, window_size: int = 50) -> Dict[str, Any]:
        """
        Detecta degradación gradual en una métrica (drift)
        Compara primera mitad vs segunda mitad
        """
        if metric_name not in self.data_points:
            return {}
        
        values = [dp['value'] for dp in self.data_points[metric_name][-window_size:]]
        
        if len(values) < 4:
            return {}
        
        mid = len(values) // 2
        first_half = values[:mid]
        second_half = values[mid:]
        
        mean_first = np.mean(first_half)
        mean_second = np.mean(second_half)
        
        drift_percentage = ((mean_second - mean_first) / mean_first * 100) if mean_first != 0 else 0
        
        return {
            'metric': metric_name,
            'mean_first_half': mean_first,
            'mean_second_half': mean_second,
            'drift_percentage': drift_percentage,
            'direction': 'IMPROVING' if drift_percentage < -5 else ('DEGRADING' if drift_percentage > 5 else 'STABLE'),
            'severity': 'HIGH' if abs(drift_percentage) > 20 else ('MEDIUM' if abs(drift_percentage) > 10 else 'LOW')
        }
    
    def get_anomaly_summary(self) -> Dict[str, Any]:
        """Resumen completo de anomalías detectadas"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'metrics_monitored': len(self.data_points),
            'spikes': {},
            'drifts': {},
            'critical_issues': []
        }
        
        for metric_name in self.data_points.keys():
            # Detectar spikes
            spikes = self.detect_spike(metric_name)
            if spikes:
                summary['spikes'][metric_name] = spikes
                high_severity_spikes = [s for s in spikes if s['severity'] == 'HIGH']
                if high_severity_spikes:
                    summary['critical_issues'].append(
                        f"Spike detected in {metric_name}: {high_severity_spikes[-1]['value']:.2f}"
                    )
            
            # Detectar drift
            drift = self.detect_drift(metric_name)
            if drift and drift['severity'] != 'LOW':
                summary['drifts'][metric_name] = drift
                if drift['severity'] == 'HIGH':
                    summary['critical_issues'].append(
                        f"Significant drift in {metric_name}: {drift['drift_percentage']:.1f}% {drift['direction']}"
                    )
        
        return summary


class ImprovementRecommender:
    """
    IE7: Genera recomendaciones de mejora basadas en datos
    """
    
    def __init__(self, metrics_summary: Dict, logs_analysis: Dict, anomalies: List):
        self.metrics = metrics_summary
        self.logs = logs_analysis
        self.anomalies = anomalies
        self.recommendations = []
    
    def generate_recommendations(self) -> List[Dict[str, Any]]:
        """Genera recomendaciones priorizadas"""
        self.recommendations = []
        
        self._check_precision()
        self._check_latency()
        self._check_errors()
        self._check_resources()
        self._check_tool_performance()
        
        # Ordenar por impacto (CRITICAL > HIGH > MEDIUM > LOW)
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        self.recommendations.sort(key=lambda x: severity_order.get(x['severity'], 4))
        
        return self.recommendations
    
    def _check_precision(self):
        """Recomienda mejoras basadas en precisión"""
        precision = self.metrics.get('precision', 0)
        
        if precision < 70:
            self.recommendations.append({
                'id': 'REC-001',
                'category': 'Accuracy',
                'severity': 'CRITICAL',
                'title': 'Improve Response Precision',
                'description': f'Current precision is {precision}%. This is below acceptable threshold.',
                'actions': [
                    '1. Review failed queries and their contexts',
                    '2. Improve prompt engineering for ambiguous queries',
                    '3. Add validation layer for response plausibility',
                    '4. Train on more edge cases'
                ],
                'estimated_impact': '15-20% improvement in precision'
            })
        elif precision < 85:
            self.recommendations.append({
                'id': 'REC-002',
                'category': 'Accuracy',
                'severity': 'HIGH',
                'title': 'Fine-tune Response Quality',
                'description': f'Current precision is {precision}%. Room for improvement.',
                'actions': [
                    '1. Analyze failure patterns',
                    '2. Enhance tool integration',
                    '3. Implement response ranking'
                ],
                'estimated_impact': '5-10% improvement'
            })
    
    def _check_latency(self):
        """Recomienda mejoras basadas en latencia"""
        latency_stats = self.metrics.get('latency_stats', {})
        avg_latency = latency_stats.get('avg_ms', 0)
        
        if avg_latency > 5000:
            self.recommendations.append({
                'id': 'REC-003',
                'category': 'Performance',
                'severity': 'HIGH',
                'title': 'Optimize Query Latency',
                'description': f'Average latency is {avg_latency:.0f}ms. Users experience slow responses.',
                'actions': [
                    '1. Profile bottleneck tools',
                    '2. Implement caching for frequent queries',
                    '3. Optimize data retrieval (indices)',
                    '4. Consider model optimization (quantization)'
                ],
                'estimated_impact': '30-50% latency reduction'
            })
        elif avg_latency > 2000:
            self.recommendations.append({
                'id': 'REC-004',
                'category': 'Performance',
                'severity': 'MEDIUM',
                'title': 'Reduce Response Time',
                'description': f'Average latency is {avg_latency:.0f}ms.',
                'actions': [
                    '1. Implement response caching',
                    '2. Parallelize tool execution where possible'
                ],
                'estimated_impact': '20-30% latency reduction'
            })
    
    def _check_errors(self):
        """Recomienda mejoras basadas en tasa de errores"""
        error_frequency = self.metrics.get('error_frequency', 0)
        
        if error_frequency > 10:
            self.recommendations.append({
                'id': 'REC-005',
                'category': 'Reliability',
                'severity': 'CRITICAL',
                'title': 'Fix System Errors',
                'description': f'Error frequency is {error_frequency:.1f}%. System is unreliable.',
                'actions': [
                    '1. Debug most common error types',
                    '2. Add input validation',
                    '3. Implement graceful error handling',
                    '4. Add retry logic for transient failures'
                ],
                'estimated_impact': 'System stability'
            })
    
    def _check_resources(self):
        """Recomienda mejoras basadas en consumo de recursos"""
        resource_stats = self.metrics.get('resource_stats', {})
        memory = resource_stats.get('memory', {})
        
        if memory.get('avg_mb', 0) > 500:
            self.recommendations.append({
                'id': 'REC-006',
                'category': 'Resources',
                'severity': 'MEDIUM',
                'title': 'Reduce Memory Footprint',
                'description': f'Average memory usage is {memory.get("avg_mb", 0):.0f}MB.',
                'actions': [
                    '1. Profile memory usage by component',
                    '2. Optimize embeddings storage',
                    '3. Implement memory pooling',
                    '4. Lazy-load heavy models'
                ],
                'estimated_impact': '20-30% memory reduction'
            })
    
    def _check_tool_performance(self):
        """Recomienda mejoras basadas en desempeño de herramientas"""
        # Este análisis usaría logs_analysis si estuviera disponible
        pass
