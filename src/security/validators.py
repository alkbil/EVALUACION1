"""
Módulo de Seguridad y Validación
IE6: Protocolos de Seguridad
"""

import re
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from collections import defaultdict
import logging


class SecurityValidator:
    """
    IE6: Implementa protocolos de seguridad para el agente
    - Validación de entrada
    - Sanitización de datos
    - Rate limiting
    - Protección de privacidad
    """
    
    def __init__(self, max_requests_per_minute: int = 60):
        """Inicializa validador de seguridad"""
        self.logger = logging.getLogger(__name__)
        self.max_requests_per_minute = max_requests_per_minute
        self.request_history = defaultdict(list)
        self.security_incidents = []
        
        # Patrones maliciosos
        self.malicious_patterns = [
            r'(\bsql\b|\bselect\b|\bdrop\b|\binsert\b|\bupdate\b)',  # SQL injection
            r'(<script|javascript:|onerror|onclick)',  # XSS
            r'(\.\./|\.\.\\)',  # Path traversal
            r'(eval\(|exec\(|\$\{|@)',  # Code injection
        ]
    
    # ============= VALIDACIÓN DE ENTRADA =============
    
    def validate_input(self, user_input: str, input_type: str = "query") -> Tuple[bool, str]:
        """
        Valida entrada del usuario
        Retorna: (es_válida, mensaje_error)
        """
        # Validación 1: Longitud
        if len(user_input) == 0:
            return False, "Empty input"
        if len(user_input) > 10000:
            return False, "Input exceeds maximum length (10000 characters)"
        
        # Validación 2: Detección de patrones maliciosos
        is_malicious, threat_type = self._detect_malicious_input(user_input)
        if is_malicious:
            self._log_security_incident("malicious_input", threat_type, user_input)
            return False, f"Suspicious input detected: {threat_type}"
        
        # Validación 3: Caracteres permitidos (según tipo)
        if input_type == "query":
            # Permitir más caracteres en consultas normales
            if not re.match(r'^[a-zA-Z0-9\s\.,¿?¡!áéíóúñ\-()]+$', user_input):
                return False, "Input contains invalid characters"
        
        # Validación 4: Rate limiting
        if not self._check_rate_limit():
            self._log_security_incident("rate_limit", "exceeded", user_input)
            return False, "Too many requests. Please try again later."
        
        return True, "Valid input"
    
    def _detect_malicious_input(self, user_input: str) -> Tuple[bool, str]:
        """Detecta patrones maliciosos"""
        user_input_lower = user_input.lower()
        
        for i, pattern in enumerate(self.malicious_patterns):
            if re.search(pattern, user_input_lower):
                threat_types = [
                    "SQL_Injection",
                    "XSS_Attack",
                    "Path_Traversal",
                    "Code_Injection"
                ]
                return True, threat_types[min(i, len(threat_types) - 1)]
        
        return False, ""
    
    # ============= SANITIZACIÓN DE DATOS =============
    
    def sanitize_input(self, user_input: str) -> str:
        """
        Sanitiza entrada del usuario (elimina caracteres peligrosos)
        NOTA: Mantiene contenido legítimo
        """
        # Remover caracteres de control
        sanitized = re.sub(r'[\x00-\x1F\x7F]', '', user_input)
        
        # Remover scripts comunes
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)
        
        # Normalizar espacios
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        return sanitized
    
    def sanitize_response(self, response: str) -> str:
        """Sanitiza respuesta antes de enviarla al usuario"""
        # Similar a sanitize_input pero más permisivo
        sanitized = re.sub(r'[\x00-\x1F\x7F]', '', response)
        return sanitized
    
    # ============= RATE LIMITING =============
    
    def _check_rate_limit(self, user_id: str = "anonymous") -> bool:
        """Verifica si el usuario ha excedido rate limit"""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # Limpiar requests antiguos
        self.request_history[user_id] = [
            req_time for req_time in self.request_history[user_id]
            if req_time > minute_ago
        ]
        
        # Verificar límite
        if len(self.request_history[user_id]) >= self.max_requests_per_minute:
            return False
        
        # Agregar nuevo request
        self.request_history[user_id].append(now)
        return True
    
    def get_rate_limit_status(self, user_id: str = "anonymous") -> Dict[str, Any]:
        """Obtiene estado actual del rate limit"""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        recent_requests = [
            req_time for req_time in self.request_history[user_id]
            if req_time > minute_ago
        ]
        
        return {
            'user_id': user_id,
            'requests_this_minute': len(recent_requests),
            'limit': self.max_requests_per_minute,
            'remaining': max(0, self.max_requests_per_minute - len(recent_requests)),
            'reset_seconds': 60
        }
    
    # ============= PROTECCIÓN DE PRIVACIDAD =============
    
    def mask_sensitive_data(self, text: str, data_type: str = "general") -> str:
        """Enmascara datos sensibles en texto"""
        # Email
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        
        # Números de tarjeta (16 dígitos)
        text = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '[CARD]', text)
        
        # Teléfono
        text = re.sub(r'\b\d{9,11}\b', '[PHONE]', text)
        
        # RUT (patrón chileno)
        text = re.sub(r'\b\d{1,2}\.\d{3}\.\d{3}[-k]\b', '[RUT]', text, flags=re.IGNORECASE)
        
        return text
    
    def hash_sensitive_value(self, value: str) -> str:
        """Hashea un valor sensible para almacenamiento seguro"""
        return hashlib.sha256(value.encode()).hexdigest()[:16]
    
    # ============= AUDITORÍA DE SEGURIDAD =============
    
    def _log_security_incident(self, incident_type: str, details: str, context: str = ""):
        """Registra un incidente de seguridad"""
        incident = {
            'timestamp': datetime.now().isoformat(),
            'type': incident_type,
            'details': details,
            'context': context[:100],  # Limitar contexto
            'severity': self._calculate_severity(incident_type)
        }
        
        self.security_incidents.append(incident)
        self.logger.warning(f"SECURITY INCIDENT: {incident_type} - {details}")
    
    def _calculate_severity(self, incident_type: str) -> str:
        """Calcula severidad de un incidente"""
        critical = ['malicious_input', 'sql_injection', 'code_injection']
        high = ['xss', 'path_traversal', 'auth_failure']
        
        if incident_type in critical:
            return 'CRITICAL'
        elif incident_type in high:
            return 'HIGH'
        else:
            return 'MEDIUM'
    
    def get_security_report(self) -> Dict[str, Any]:
        """Genera reporte de seguridad"""
        recent_incidents = self.security_incidents[-100:]
        
        incident_count = defaultdict(int)
        for incident in recent_incidents:
            incident_count[incident['type']] += 1
        
        critical_incidents = [i for i in recent_incidents if i['severity'] == 'CRITICAL']
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_incidents': len(recent_incidents),
            'critical_incidents': len(critical_incidents),
            'incident_types': dict(incident_count),
            'recent_incidents': recent_incidents[-10:],
            'security_status': 'SECURE' if len(critical_incidents) == 0 else 'AT_RISK'
        }


class PrivacyProtector:
    """
    Implementa políticas de privacidad y protección de datos
    """
    
    def __init__(self):
        self.data_retention_days = 30
        self.logged_data_access = []
    
    def should_retain_data(self, timestamp: datetime) -> bool:
        """Determina si se debe retener un dato basado en edad"""
        age = datetime.now() - timestamp
        return age.days < self.data_retention_days
    
    def cleanup_old_data(self, data_list: List[Dict], timestamp_field: str = 'timestamp') -> List[Dict]:
        """Limpia datos antiguos según política de retención"""
        current_time = datetime.now()
        cutoff_date = current_time - timedelta(days=self.data_retention_days)
        
        cleaned = []
        for item in data_list:
            try:
                item_date = datetime.fromisoformat(item[timestamp_field])
                if item_date > cutoff_date:
                    cleaned.append(item)
            except:
                cleaned.append(item)
        
        return cleaned
    
    def log_data_access(self, user_id: str, data_type: str, action: str):
        """Registra acceso a datos para auditoría"""
        self.logged_data_access.append({
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'data_type': data_type,
            'action': action
        })
    
    def get_privacy_audit_log(self) -> List[Dict]:
        """Retorna log de acceso a datos"""
        return self.logged_data_access[-100:]
