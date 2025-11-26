# 📊 GUÍA DE OBSERVABILIDAD EP3

## Documento de Monitoreo y Análisis

**Proyecto:** Agente Inteligente Pastelería 1000 Sabores  
**Evaluación:** EP3 - Observabilidad y Monitoreo  
**Fecha:** 2025-01-26  

---

## 1. INTRODUCCIÓN

La observabilidad es la capacidad de entender el estado interno de un sistema mediante sus outputs externos (logs, métricas, eventos). EP3 implementa un sistema completo de observabilidad con:

- **Métricas:** Mediciones numéricas del comportamiento
- **Logs:** Eventos detallados del sistema
- **Trazabilidad:** Seguimiento de requests end-to-end
- **Dashboards:** Visualización en tiempo real
- **Alertas:** Notificaciones de anomalías

---

## 2. ARQUITECTURA DE OBSERVABILIDAD

### 2.1 Capas de Recolección

```
┌─────────────────────────────────────┐
│     Aplicación (app_agent.py)       │
│  - Ejecuta queries del usuario      │
└──────────┬──────────────────────────┘
           │
    ┌──────┴──────┬──────────┬────────┐
    │             │          │        │
    v             v          v        v
┌────────┐  ┌────────┐ ┌──────────┐ ┌──────────┐
│Métricas│  │  Logs  │ │ Security │ │ Anomalías│
│        │  │        │ │          │ │          │
└────────┘  └────────┘ └──────────┘ └──────────┘
    │             │          │        │
    └──────┬──────┴──────────┴────────┘
           │
           v
    ┌─────────────────┐
    │ Storage         │
    ├─────────────────┤
    │metrics.json     │
    │logs/*.log       │
    │analysis.json    │
    └─────────────────┘
           │
           v
    ┌──────────────────┐
    │ Dashboard.py     │
    │ Visualización    │
    └──────────────────┘
```

### 2.2 Flujo de Datos

```
User Query
    ↓
[SecurityValidator]
    ├─ validate_input()
    ├─ sanitize_input()
    └─ check_rate_limit()
    ↓
[PasteleriaAgentExecutor]
    ├─ Herramientas
    ├─ Memory
    └─ [ObservabilityMetrics]
        ├─ record_query()
        ├─ record_response()
        ├─ measure_resources()
        └─ save_metrics()
    ↓
[LogsAnalyzer] (async)
    ├─ parse_logs()
    ├─ get_errors_summary()
    ├─ get_bottlenecks()
    └─ generate_report()
    ↓
[AnomalyDetector]
    ├─ detect_spike()
    ├─ detect_drift()
    └─ classify_severity()
    ↓
[ImprovementRecommender]
    ├─ check_precision()
    ├─ check_latency()
    ├─ check_errors()
    └─ generate_recommendations()
    ↓
[Dashboard.py]
    ├─ Visualiza métricas
    ├─ Muestra anomalías
    ├─ Sugiere mejoras
    └─ Reporta seguridad
```

---

## 3. COMPONENTES PRINCIPALES

### 3.1 ObservabilityMetrics (IE1, IE2)

**Ubicación:** `src/monitoring/metrics.py`

**Responsabilidades:**
- Medir precisión de respuestas
- Calcular latencia y recursos
- Registrar errores
- Persistir datos

**Métodos Principales:**

```python
# IE1: Precisión y Consistencia
calculate_precision()       # % respuestas correctas
calculate_consistency()     # Coherencia entre respuestas
calculate_error_frequency() # Errores por 100 queries

# IE2: Latencia y Recursos
measure_resources()    # Latencia, memoria, CPU, tokens
get_latency_stats()   # Min, max, average
get_resource_stats()  # Memory, CPU, tokens

# Almacenamiento
export_metrics()      # Exporta a JSON
```

**Uso:**

```python
from src.monitoring.metrics import ObservabilityMetrics

metrics = ObservabilityMetrics()

# Registrar query
query_id = metrics.record_query("¿Cuánto cuesta la torta?")

# Ejecutar...
execution_time = 1.2  # segundos

# Registrar resultado
metrics.record_response(query_id, "La torta cuesta $15.000", is_correct=True)
metrics.measure_resources(execution_time, tokens_prompt=50, tokens_response=120)

# Ver estadísticas
summary = metrics.get_summary()
print(f"Precisión: {summary['precision']}%")
print(f"Errores: {summary['error_frequency']}%")
```

### 3.2 LogsAnalyzer (IE3, IE4)

**Ubicación:** `src/monitoring/logs_analyzer.py`

**Responsabilidades:**
- Parsear logs del sistema
- Identificar errores y patrones
- Detectar anomalías
- Generar reportes

**Métodos Principales:**

```python
# IE3: Análisis de Logs
get_errors_summary()      # Resumen de errores
get_bottlenecks()         # Operaciones lentas
get_tool_usage_analysis() # Desempeño de herramientas

# IE4: Patrones y Anomalías
identify_patterns()       # Patrones de uso
detect_anomalies()        # Anomalías detectadas
```

**Uso:**

```python
from src.monitoring.logs_analyzer import LogsAnalyzer

analyzer = LogsAnalyzer(log_dir="./logs")

# Obtener resumen de errores
errors = analyzer.get_errors_summary()
print(f"Total errores: {errors['total_errors']}")
print(f"Tasa de error: {errors['error_frequency']}%")

# Identificar cuellos de botella
bottlenecks = analyzer.get_bottlenecks(threshold_ms=5000)
for bn in bottlenecks:
    print(f"Operación lenta: {bn['message']} ({bn['execution_time_ms']}ms)")

# Generar reporte completo
report_path = analyzer.generate_report()
print(f"Reporte guardado en: {report_path}")
```

### 3.3 AnomalyDetector (IE4, IE7)

**Ubicación:** `src/monitoring/anomaly_detector.py`

**Responsabilidades:**
- Detectar spikes en métricas
- Identificar degradación (drift)
- Generar recomendaciones

**Métodos Principales:**

```python
# Detección
detect_spike(metric_name)     # Picos inusuales
detect_drift(metric_name)     # Degradación gradual
get_anomaly_summary()         # Resumen de anomalías

# Recomendaciones (IE7)
generate_recommendations()    # Mejoras priorizadas
```

**Uso:**

```python
from src.monitoring.anomaly_detector import AnomalyDetector, ImprovementRecommender
import json

detector = AnomalyDetector()

# Simular mediciones
detector.add_measurement("latency", 1200)  # 1.2s
detector.add_measurement("latency", 1150)
detector.add_measurement("latency", 5500)  # Spike!

# Calcular baseline
detector.calculate_baseline("latency")

# Detectar spikes
spikes = detector.detect_spike("latency", threshold_std=3.0)
for spike in spikes:
    print(f"Spike detectado: {spike['value']}ms (desviación: {spike['deviation']}σ)")

# Generar recomendaciones
with open("metrics/metrics.json") as f:
    metrics = json.load(f)

recommender = ImprovementRecommender(metrics, {}, [])
recommendations = recommender.generate_recommendations()

for rec in recommendations:
    print(f"[{rec['severity']}] {rec['title']}")
    print(f"  Acciones: {rec['actions']}")
```

### 3.4 SecurityValidator (IE6)

**Ubicación:** `src/security/validators.py`

**Responsabilidades:**
- Validar entrada del usuario
- Sanitizar datos
- Rate limiting
- Auditar incidentes

**Métodos Principales:**

```python
validate_input(query)         # Valida entrada
sanitize_input(query)         # Sanitiza peligrosos
check_rate_limit()           # Verifica límite
mask_sensitive_data()        # Enmascara privados
get_security_report()        # Reporte de incidentes
```

**Uso:**

```python
from src.security.validators import SecurityValidator

security = SecurityValidator(max_requests_per_minute=60)

# Validar entrada
query = "¿Cuánto cuesta la torta?"
is_valid, message = security.validate_input(query)

if is_valid:
    # Sanitizar
    safe_query = security.sanitize_input(query)
    
    # Procesar...
    response = "La torta cuesta $15.000"
    
    # Sanitizar output
    safe_response = security.sanitize_response(response)
    
    # Registrar acceso
    security.log_data_access("user123", "product_query", "READ")
else:
    print(f"Entrada rechazada: {message}")

# Ver reporte de seguridad
report = security.get_security_report()
print(f"Incidentes críticos: {report['critical_incidents']}")
```

---

## 4. DASHBOARD DE OBSERVABILIDAD

### 4.1 Ejecutar Dashboard

```bash
streamlit run dashboard.py
```

### 4.2 Tabs del Dashboard

| Tab | Indicador | Contenido |
|-----|-----------|----------|
| 📈 Métricas | IE1, IE2 | Precisión, latencia, recursos |
| 🔧 Logs | IE3 | Errores, herramientas, patrones |
| ⚠️ Anomalías | IE4 | Spikes, drift, recomendaciones |
| 🛡️ Seguridad | IE6 | Incidentes, features, histórico |
| 💡 Mejoras | IE7 | Recomendaciones priorizadas |

### 4.3 Métricas Mostradas

**Tab Métricas:**
- Precisión (IE1): % respuestas correctas
- Error Frequency (IE1): Errores por 100 queries
- Latencia Promedio (IE2): Tiempo promedio de respuesta
- Memoria (IE2): GB usados
- CPU (IE2): % utilización
- Gráficos de tendencia

**Tab Logs:**
- Total de errores
- Tipos de errores más frecuentes
- Cuellos de botella detectados
- Uso por herramienta
- Distribución de tipos de queries

**Tab Anomalías:**
- Spikes detectados
- Drift en métricas
- Patrones anormales
- Recomendaciones automáticas

**Tab Seguridad:**
- Status: 🟢 SEGURO / 🔴 EN RIESGO
- Rate limit actual
- Capas de validación activas
- Gráfico de incidentes históricos

**Tab Mejoras:**
- Recomendaciones con severidad
- Descripción de problema
- Acciones sugeridas
- Impacto estimado
- Esfuerzo requerido

---

## 5. EJEMPLOS DE USO

### 5.1 Integración en app_agent.py

```python
import streamlit as st
from src.monitoring.metrics import ObservabilityMetrics
from src.security.validators import SecurityValidator

# Inicializar
metrics = ObservabilityMetrics()
security = SecurityValidator()

# Interfaz
st.title("Agente Inteligente")

user_query = st.text_input("¿En qué te puedo ayudar?")

if user_query:
    # Validar seguridad
    is_valid, msg = security.validate_input(user_query)
    if not is_valid:
        st.error(f"❌ {msg}")
        st.stop()
    
    # Registrar métrica
    query_id = metrics.record_query(user_query, query_type="general")
    
    # Ejecutar (pseudo-código)
    import time
    start = time.time()
    response = agent.execute(user_query)
    exec_time = time.time() - start
    
    # Registrar resultado
    metrics.record_response(query_id, response, is_correct=True)
    metrics.measure_resources(exec_time, tokens_prompt=100, tokens_response=50)
    
    # Mostrar
    st.write(response)
    
    # Mostrar métricas
    with st.expander("📊 Métricas"):
        summary = metrics.get_summary()
        col1, col2, col3 = st.columns(3)
        col1.metric("Precisión", f"{summary['precision']:.1f}%")
        col2.metric("Errores", f"{summary['error_frequency']:.1f}%")
        col3.metric("Latencia", f"{exec_time:.2f}s")
```

### 5.2 Análisis Manual de Logs

```bash
# 1. Generar reporte
python -c "
from src.monitoring.logs_analyzer import LogsAnalyzer
analyzer = LogsAnalyzer('./logs')
report_path = analyzer.generate_report()
print(f'Reporte guardado en: {report_path}')
"

# 2. Ver reporte
cat ./logs/analysis_report.json | jq '.'

# 3. Ver solo errores
cat ./logs/analysis_report.json | jq '.errors_summary'
```

### 5.3 Detección de Anomalías

```python
from src.monitoring.anomaly_detector import AnomalyDetector
import json

# Cargar métricas históricas
with open("metrics/metrics.json") as f:
    metrics_data = json.load(f)

# Crear detector
detector = AnomalyDetector()

# Simular series de tiempo (en producción, serían datos reales)
latencies = [1200, 1150, 1180, 1200, 5200, 1250, 1200, 1150]
for lat in latencies:
    detector.add_measurement("latency", lat)

# Detectar anomalías
summary = detector.get_anomaly_summary()

print("=== RESUMEN DE ANOMALÍAS ===")
print(f"Métricas monitoreadas: {summary['metrics_monitored']}")
print(f"Spikes detectados: {len(summary['spikes'])}")
print(f"Drifts detectados: {len(summary['drifts'])}")
print(f"\nProblemas críticos:")
for issue in summary['critical_issues']:
    print(f"  - {issue}")
```

---

## 6. INTERPRETACIÓN DE MÉTRICAS

### 6.1 Precisión (IE1)

```
< 70%  : 🔴 CRÍTICO - Revisar algoritmo
70-80% : 🟠 BAJO   - Mejorar prompts
80-90% : 🟡 MEDIO  - Aceptable
> 90%  : 🟢 ALTO   - Excelente
```

### 6.2 Latencia (IE2)

```
< 500ms   : 🟢 EXCELENTE - Muy rápido
500ms-2s  : 🟢 BUENO     - Aceptable
2s-5s     : 🟡 LENTO     - Revisar optimizaciones
> 5s      : 🔴 CRÍTICO   - Optimizar urgente
```

### 6.3 Error Frequency (IE1)

```
< 1%      : 🟢 EXCELENTE
1-5%      : 🟡 ACEPTABLE
5-10%     : 🟠 MEDIOCRE  - Revisar
> 10%     : 🔴 CRÍTICO   - Actuar inmediatamente
```

---

## 7. TROUBLESHOOTING

### Problema: No se guardan métricas

```python
# Verificar que directorio existe
import os
os.makedirs("./metrics", exist_ok=True)
os.makedirs("./logs", exist_ok=True)

# Verificar permisos de escritura
import pathlib
pathlib.Path("./metrics/test.txt").write_text("test")
```

### Problema: Dashboard no muestra datos

```bash
# Verificar que archivos existen
ls -la ./metrics/
ls -la ./logs/

# Regenerar análisis
python -c "
from src.monitoring.logs_analyzer import LogsAnalyzer
analyzer = LogsAnalyzer()
analyzer.generate_report()
"
```

---

## 8. MEJORES PRÁCTICAS

✅ Monitorear regularmente el dashboard  
✅ Revisar recomendaciones semanalmente  
✅ Investigar anomalías dentro de 24h  
✅ Implementar mejoras de alto impacto primero  
✅ Documentar cambios y sus efectos  
✅ Mantener histórico de métricas  

---

**Guía v1.0 | 2025-01-26**
