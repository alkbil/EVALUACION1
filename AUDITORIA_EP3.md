# 🔍 AUDITORÍA EP3 - OBSERVABILIDAD Y MONITOREO
**Proyecto:** Agente Inteligente Pastelería 1000 Sabores  
**Fecha:** 26 Noviembre 2025  
**Evaluación:** EP3 - Implementación de Observabilidad

---

## 1. RESUMEN EJECUTIVO

### 📊 Evaluación General
Tu proyecto tiene una **base sólida de EP2** (agente con herramientas y memoria), pero **NO cumple con los requisitos de EP3** en su estado actual. Necesitas implementar componentes específicos de observabilidad que actualmente están ausentes.

### ✅ Fortalezas
- Agente funcional con 4 herramientas
- Sistema de logging básico implementado
- ExecutionTracker capturando estadísticas
- Memoria dual operativa

### ❌ Debilidades Críticas
- **Sin dashboard visual** (IE5 - 15% perdido)
- **Sin métricas de precisión/consistencia** (IE1 - 15% perdido)
- **Sin métricas de recursos** (IE2 - parcial)
- **Sin análisis de patrones/anomalías** (IE4 - 10% perdido)
- **Sin protocolos de seguridad documentados** (IE6 - parcial)
- **Sin recomendaciones basadas en datos** (IE7 - 10% perdido)
- **Sin informe técnico con evidencia visual** (IE8 - 5% perdido)

### 📈 Nota Proyectada Actual
**35-40/100 (2.5-3.0/7.0)** ⚠️ INSUFICIENTE

### 🎯 Nota Proyectada con Mejoras
**90-100/100 (6.5-7.0/7.0)** ✅ MUY BUEN DESEMPEÑO

---

## 2. EVALUACIÓN POR INDICADOR

### **IE1: Métricas de Precisión, Consistencia y Errores (15%)**

📊 **Nivel alcanzado:** ❌ **No logrado (0%)**

**Estado actual:**
- ✅ Tienes `ExecutionTracker` que cuenta ejecuciones
- ✅ Registras errores en logs
- ❌ **NO hay métrica de precisión** (% respuestas correctas)
- ❌ **NO hay métrica de consistencia** (coherencia en respuestas similares)
- ❌ **NO hay cálculo de frecuencia de errores** (errores/100 consultas)

**Código actual:**
```python
# En logger.py líneas 190-223
def get_statistics(self):
    # Solo cuenta: total, successful, success_rate
    # FALTA: precisión, consistencia, error_frequency
```

**Lo que necesitas:**

1. **Crear `src/monitoring/metrics.py`:**
```python
class ObservabilityMetrics:
    def __init__(self):
        self.total_queries = 0
        self.correct_responses = 0
        self.consistency_scores = []
        self.errors = []
    
    def calculate_precision(self):
        """Precisión = respuestas correctas / total"""
        if self.total_queries == 0:
            return 0
        return (self.correct_responses / self.total_queries) * 100
    
    def calculate_consistency(self, query, response):
        """Mide coherencia comparando con respuestas previas similares"""
        # Usar embeddings para comparar similitud
        pass
    
    def calculate_error_frequency(self):
        """Errores por cada 100 consultas"""
        if self.total_queries == 0:
            return 0
        return (len(self.errors) / self.total_queries) * 100
```

2. **Integrar en `app_agent.py`:**
```python
# Después de cada query, evaluar:
metrics.total_queries += 1
if user_validates_response():  # Thumbs up/down
    metrics.correct_responses += 1
```

**Impacto:** +15% si implementas correctamente

---

### **IE2: Métricas de Latencia y Uso de Recursos (15%)**

📊 **Nivel alcanzado:** ⚠️ **Aceptable (60% = 9/15 puntos)**

**Estado actual:**
- ✅ Mides tiempo de ejecución (`execution_time`)
- ❌ **NO mides uso de RAM**
- ❌ **NO mides uso de CPU**
- ❌ **NO mides tokens consumidos**
- ❌ **NO contextualizas** (promedio, máx, mín)

**Código actual:**
```python
# En agent_executor.py línea 171
result["execution_time"] = time.time() - start_time
# SOLO tiempo, falta RAM, CPU, tokens
```

**Lo que necesitas:**

```python
import psutil
import tiktoken

class ResourceMetrics:
    def measure_resources(self, query, response):
        return {
            'latency_ms': execution_time * 1000,
            'memory_mb': psutil.Process().memory_info().rss / 1024 / 1024,
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'tokens_prompt': len(tiktoken.encode(query)),
            'tokens_response': len(tiktoken.encode(response)),
            'tokens_total': tokens_prompt + tokens_response
        }
```

**Impacto:** +6% (llegarías a 15/15)

---

### **IE3: Análisis de Logs y Trazabilidad (15%)**

📊 **Nivel alcanzado:** ⚠️ **Buen desempeño (80% = 12/15 puntos)**

**Estado actual:**
- ✅ Sistema de logging implementado (`logger.py`)
- ✅ Logs capturan query, tools, observations
- ✅ Logs almacenados en archivos
- ⚠️ Logs en texto plano (no JSON estructurado)
- ❌ **NO hay análisis de logs** (identificación de errores/cuellos de botella)
- ❌ **NO documentas hallazgos** en informe

**Lo que necesitas:**

1. **Cambiar formato a JSON** (línea 52 de logger.py):
```python
formatter = logging.Formatter(
    '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
```

2. **Crear análisis de logs:**
```python
def analyze_logs(log_file):
    """Identifica errores y cuellos de botella"""
    errors = []
    slow_queries = []
    
    with open(log_file) as f:
        for line in f:
            log = json.loads(line)
            if log['level'] == 'ERROR':
                errors.append(log)
            if 'execution_time' in log and log['execution_time'] > 5:
                slow_queries.append(log)
    
    return {
        'total_errors': len(errors),
        'error_types': Counter([e['message'] for e in errors]),
        'bottlenecks': slow_queries
    }
```

**Impacto:** +3% (llegarías a 15/15)

---

### **IE4: Identificación de Patrones y Anomalías (10%)**

📊 **Nivel alcanzado:** ❌ **No logrado (0%)**

**Estado actual:**
- ❌ **NO hay análisis de patrones**
- ❌ **NO hay detección de anomalías**
- ❌ **NO hay propuestas de mejora basadas en datos**

**Lo que necesitas:**

```python
def identify_patterns(executions):
    """Analiza logs para encontrar patrones"""
    
    # Patrón 1: Errores por tipo de consulta
    error_by_query_type = {}
    
    # Patrón 2: Latencia por número de herramientas
    latency_by_tools = {}
    
    # Patrón 3: Horarios pico
    queries_by_hour = {}
    
    # Anomalías
    anomalies = []
    avg_latency = mean([e['duration'] for e in executions])
    for e in executions:
        if e['duration'] > avg_latency * 3:  # 3x promedio
            anomalies.append({
                'type': 'high_latency',
                'query': e['query'],
                'latency': e['duration']
            })
    
    return {
        'patterns': {...},
        'anomalies': anomalies,
        'recommendations': [
            "Implementar caché para consultas frecuentes",
            "Optimizar herramientas lentas"
        ]
    }
```

**Documentar en informe:**
- "El 80% de errores ocurren con consultas de productos veganos"
- "Latencia aumenta 3x cuando se usan 3+ herramientas"
- "Picos de uso entre 12-14hrs"

**Impacto:** +10%

---

### **IE5: Dashboard Visual de Monitoreo (15%)**

📊 **Nivel alcanzado:** ❌ **No logrado (0%)**

**Estado actual:**
- ❌ **NO existe dashboard dedicado**
- ⚠️ Tienes métricas básicas en sidebar de `app_agent.py`
- ❌ **NO hay visualizaciones** (gráficos de línea, barras)
- ❌ **NO es interactivo**

**Lo que necesitas:**

**Crear `dashboard.py`:**
```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.monitoring.metrics import load_metrics

st.set_page_config(page_title="Dashboard Observabilidad", layout="wide")

st.title("📊 Dashboard de Observabilidad - Agente IA")

# === PANEL 1: KPIs PRINCIPALES ===
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Consultas", metrics['total_queries'])
with col2:
    st.metric("Precisión", f"{metrics['precision']:.1f}%")
with col3:
    st.metric("Latencia Promedio", f"{metrics['avg_latency']:.0f}ms")
with col4:
    st.metric("Tasa de Error", f"{metrics['error_rate']:.1f}%")

# === PANEL 2: GRÁFICO DE LATENCIA EN EL TIEMPO ===
st.subheader("⏱️ Latencia en el Tiempo")
df_latency = pd.DataFrame(metrics['latency_history'])
fig = px.line(df_latency, x='timestamp', y='latency_ms', 
              title='Evolución de Latencia')
st.plotly_chart(fig, use_container_width=True)

# === PANEL 3: USO DE RECURSOS ===
col1, col2 = st.columns(2)
with col1:
    st.subheader("💾 Uso de Memoria")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=metrics['memory_mb'],
        title={'text': "RAM (MB)"},
        gauge={'axis': {'range': [None, 1000]}}
    ))
    st.plotly_chart(fig)

with col2:
    st.subheader("🔥 Uso de CPU")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=metrics['cpu_percent'],
        title={'text': "CPU (%)"},
        gauge={'axis': {'range': [None, 100]}}
    ))
    st.plotly_chart(fig)

# === PANEL 4: DISTRIBUCIÓN DE ERRORES ===
st.subheader("❌ Tipos de Errores")
df_errors = pd.DataFrame(metrics['error_types'].items(), 
                         columns=['Tipo', 'Frecuencia'])
fig = px.bar(df_errors, x='Tipo', y='Frecuencia')
st.plotly_chart(fig, use_container_width=True)

# === PANEL 5: HERRAMIENTAS MÁS USADAS ===
st.subheader("🔧 Herramientas Más Usadas")
df_tools = pd.DataFrame(metrics['tool_usage'].items(),
                        columns=['Herramienta', 'Usos'])
fig = px.pie(df_tools, values='Usos', names='Herramienta')
st.plotly_chart(fig)
```

**Ejecutar:**
```bash
streamlit run dashboard.py
```

**Capturar screenshots:**
1. Vista completa del dashboard
2. Gráfico de latencia
3. Métricas de recursos
4. Distribución de errores
5. Herramientas más usadas

**Impacto:** +15% (CRÍTICO)

---

### **IE6: Protocolos de Seguridad y Uso Responsable (10%)**

📊 **Nivel alcanzado:** ⚠️ **Aceptable (60% = 6/10 puntos)**

**Estado actual:**
- ✅ API key en `.env` (no en código)
- ❌ **NO hay validación de inputs**
- ❌ **NO hay rate limiting**
- ❌ **NO hay anonimización en logs**
- ❌ **NO hay documentación de seguridad**

**Lo que necesitas:**

1. **Validación de inputs** (`src/security/validator.py`):
```python
def validate_input(query: str) -> bool:
    if len(query) > 500:
        return False
    
    # Detectar inyecciones
    dangerous_patterns = [
        "ignore previous",
        "system:",
        "<script>",
        "DROP TABLE"
    ]
    for pattern in dangerous_patterns:
        if pattern.lower() in query.lower():
            return False
    return True
```

2. **Rate limiting** (`src/security/rate_limiter.py`):
```python
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests=10, window_minutes=1):
        self.requests = {}
        self.max_requests = max_requests
        self.window = timedelta(minutes=window_minutes)
    
    def is_allowed(self, user_id):
        now = datetime.now()
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Limpiar requests antiguos
        self.requests[user_id] = [
            t for t in self.requests[user_id]
            if now - t < self.window
        ]
        
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        self.requests[user_id].append(now)
        return True
```

3. **Documentar en informe:**
```markdown
## Protocolos de Seguridad

### A) Seguridad
- ✅ API keys protegidas en .env
- ✅ Validación de inputs (max 500 chars, sin inyecciones)
- ✅ Rate limiting (10 requests/minuto)

### B) Privacidad
- ✅ Logs anonimizan IDs de usuario
- ✅ No se guardan datos sensibles sin encriptar

### C) Ética
- ✅ Disclaimer sobre uso de IA
- ✅ Transparencia sobre limitaciones

### D) Cumplimiento
- ✅ Términos de uso claros
- ✅ Política de retención de datos (30 días)
```

**Impacto:** +4% (llegarías a 10/10)

---

### **IE7: Propuesta de Mejoras y Optimización (10%)**

📊 **Nivel alcanzado:** ❌ **No logrado (0%)**

**Estado actual:**
- ❌ **NO hay recomendaciones documentadas**
- ❌ **NO están basadas en datos observados**

**Lo que necesitas:**

En el informe, incluir sección:

```markdown
## 5. RECOMENDACIONES DE MEJORA

### Recomendación 1: Implementar Caché de Respuestas
**Problema detectado:**
- Métrica: 40% de consultas son repetidas
- Dato: Latencia promedio 2.5s para queries idénticas

**Propuesta:**
Implementar cache con TTL de 1 hora para consultas frecuentes

**Impacto esperado:**
- Reducir latencia en 60% para queries cacheadas
- Ahorrar 30% en costos de tokens
- Mejorar experiencia de usuario

**Prioridad:** Alta  
**Esfuerzo:** Medio (4 horas)

---

### Recomendación 2: Optimizar Prompts
**Problema detectado:**
- Métrica: Consumo promedio 1200 tokens/query
- Dato: Prompt system tiene 800 tokens

**Propuesta:**
Reducir prompt system de 800 a 400 tokens

**Impacto esperado:**
- Reducir costos en 25%
- Reducir latencia en 15%

**Prioridad:** Alta  
**Esfuerzo:** Bajo (2 horas)

---

### Recomendación 3: Paralelizar Herramientas
**Problema detectado:**
- Métrica: Queries con 3 herramientas tardan 8s
- Dato: Herramientas son independientes

**Propuesta:**
Ejecutar herramientas en paralelo con asyncio

**Impacto esperado:**
- Reducir latencia en 50% para queries complejas

**Prioridad:** Media  
**Esfuerzo:** Alto (8 horas)
```

**Impacto:** +10%

---

### **IE8: Informe con Evidencia Visual (5%)**

📊 **Nivel alcanzado:** ❌ **No logrado (0%)**

**Estado actual:**
- ❌ **NO existe informe técnico**
- ❌ **NO hay capturas del dashboard**
- ❌ **NO hay gráficos**

**Lo que necesitas:**

**Crear `docs/INFORME_EP3.pdf` (máx 5 páginas):**

```markdown
# INFORME TÉCNICO EP3
## Implementación de Observabilidad - Agente IA

### 1. Introducción
[Descripción del proyecto y objetivos EP3]

### 2. Métricas Implementadas

#### 2.1 Métricas de Precisión
[Captura del dashboard mostrando precisión: 87.5%]
[Gráfico de evolución de precisión en el tiempo]

#### 2.2 Métricas de Latencia
[Captura del gráfico de latencia]
- Promedio: 2.3s
- Máximo: 8.1s
- Mínimo: 0.8s

#### 2.3 Métricas de Recursos
[Captura de gauges de RAM y CPU]
- RAM promedio: 245 MB
- CPU promedio: 12%
- Tokens promedio: 1200/query

### 3. Análisis de Logs
[Captura de logs estructurados]
[Tabla con tipos de errores y frecuencia]

### 4. Patrones Identificados
[Gráfico mostrando errores por tipo de consulta]
[Gráfico de latencia vs número de herramientas]

### 5. Dashboard Visual
[Captura completa del dashboard]
[Descripción de cada panel]

### 6. Protocolos de Seguridad
[Diagrama de flujo de validación]
[Tabla de medidas implementadas]

### 7. Recomendaciones
[Lista de 5 recomendaciones con impacto]

### 8. Conclusiones
[Resumen de logros y próximos pasos]

### 9. Referencias (APA)
- LangChain Documentation (2024)
- Streamlit Documentation (2024)
- OpenAI API Reference (2024)
- Plotly Python Graphing Library (2024)
- Python Logging Documentation (2024)
```

**Capturas obligatorias (mínimo 8):**
1. Dashboard completo
2. Panel de KPIs
3. Gráfico de latencia
4. Métricas de recursos
5. Distribución de errores
6. Herramientas más usadas
7. Ejemplo de logs JSON
8. Tabla de recomendaciones

**Impacto:** +5%

---

### **IE9: Lenguaje Técnico y Argumentación (5%)**

📊 **Nivel alcanzado:** ⚠️ **Buen desempeño (80% = 4/5 puntos)**

**Estado actual:**
- ✅ Código bien documentado
- ✅ Comentarios técnicos apropiados
- ⚠️ Falta informe con argumentación

**Lo que necesitas:**

En el informe, usar terminología técnica:
- ✅ Observabilidad, métricas, KPIs
- ✅ Latencia, throughput, overhead
- ✅ Trazabilidad, logging, debugging
- ✅ Anomalías, patrones, outliers
- ✅ Escalabilidad, sostenibilidad

**Ejemplo de argumentación:**
```markdown
La implementación de caché de respuestas se fundamenta en el análisis 
de logs que reveló que el 40% de las consultas son repetidas (patrón 
identificado mediante análisis de embeddings con similitud >0.95). 
Esta optimización reduciría la latencia promedio de 2.5s a 1.0s 
(mejora del 60%), disminuyendo el overhead de llamadas a la API de 
OpenAI y mejorando el throughput del sistema de 24 a 60 queries/minuto.
```

**Impacto:** +1% (llegarías a 5/5)

---

## 3. TABLA RESUMEN DE CUMPLIMIENTO

| Indicador | Peso | Actual | Nivel | Con Mejoras | Puntos Actuales | Puntos Posibles |
|-----------|------|--------|-------|-------------|-----------------|-----------------|
| IE1: Métricas Precisión | 15% | ❌ | 0% | ✅ 100% | 0 | 15 |
| IE2: Métricas Latencia | 15% | ⚠️ | 60% | ✅ 100% | 9 | 15 |
| IE3: Análisis Logs | 15% | ⚠️ | 80% | ✅ 100% | 12 | 15 |
| IE4: Patrones/Anomalías | 10% | ❌ | 0% | ✅ 100% | 0 | 10 |
| IE5: Dashboard Visual | 15% | ❌ | 0% | ✅ 100% | 0 | 15 |
| IE6: Seguridad | 10% | ⚠️ | 60% | ✅ 100% | 6 | 10 |
| IE7: Recomendaciones | 10% | ❌ | 0% | ✅ 100% | 0 | 10 |
| IE8: Informe Visual | 5% | ❌ | 0% | ✅ 100% | 0 | 5 |
| IE9: Lenguaje Técnico | 5% | ⚠️ | 80% | ✅ 100% | 4 | 5 |
| **TOTAL** | **100%** | | **31%** | **100%** | **31** | **100** |

**📊 Nota proyectada actual:** 31/100 (2.2/7.0) ⚠️ **REPROBADO**  
**📊 Nota proyectada con mejoras:** 100/100 (7.0/7.0) ✅ **EXCELENTE**

---

## 4. PROBLEMAS CRÍTICOS

### 🚨 CRÍTICO (afecta 45% de la nota):
1. **NO existe dashboard visual** → Pérdida de 15%
2. **NO hay métricas de precisión/consistencia** → Pérdida de 15%
3. **NO hay análisis de patrones** → Pérdida de 10%
4. **NO hay informe técnico** → Pérdida de 5%

### ⚠️ IMPORTANTE (afecta 25%):
5. **Métricas de recursos incompletas** → Pérdida de 6%
6. **Logs no estructurados (JSON)** → Pérdida de 3%
7. **Sin recomendaciones documentadas** → Pérdida de 10%
8. **Seguridad parcial** → Pérdida de 4%
9. **Sin validación de inputs** → Pérdida de 2%

### 💡 MENOR (afecta 5%):
10. **Lenguaje técnico mejorable en informe** → Pérdida de 1%

---

## 5. QUICK WINS (Mejoras Rápidas <4h)

| # | Mejora | Tiempo | Impacto | Archivos |
|---|--------|--------|---------|----------|
| 1 | Logs en formato JSON | 1h | +3% (IE3) | `logger.py` línea 52 |
| 2 | Validación de inputs | 2h | +2% (IE6) | Crear `src/security/validator.py` |
| 3 | Métricas de tokens | 1h | +2% (IE2) | `agent_executor.py` |
| 4 | Rate limiting básico | 2h | +2% (IE6) | Crear `src/security/rate_limiter.py` |
| 5 | Documentar seguridad | 1h | +2% (IE6) | Informe sección 6 |

**Total Quick Wins:** 7 horas → +11% en la nota

---

## 6. PLAN DE ACCIÓN PRIORIZADO

### **Semana 1 (20 horas):**

**Prioridad 1: Dashboard Visual** (8h) → +15%
- Crear `dashboard.py` con Streamlit + Plotly
- 5 paneles: KPIs, Latencia, Recursos, Errores, Herramientas
- Capturar 8 screenshots

**Prioridad 2: Métricas de Precisión** (4h) → +15%
- Crear `src/monitoring/metrics.py`
- Implementar: precision, consistency, error_frequency
- Integrar en `app_agent.py`

**Prioridad 3: Análisis de Patrones** (4h) → +10%
- Función `identify_patterns()` en `metrics.py`
- Detectar: errores por tipo, latencia por herramientas, horarios pico
- Documentar 3 patrones + 3 anomalías

**Prioridad 4: Quick Wins** (4h) → +11%
- Logs JSON
- Validación inputs
- Rate limiting
- Métricas tokens

**Total Semana 1:** +51% → Nota sube a 82/100 (5.7/7.0)

---

### **Semana 2 (12 horas):**

**Prioridad 5: Informe Técnico** (6h) → +5%
- Crear `docs/INFORME_EP3.pdf` (5 páginas)
- Incluir 8 capturas del dashboard
- 5 referencias APA

**Prioridad 6: Recomendaciones** (3h) → +10%
- Documentar 5 recomendaciones basadas en datos
- Formato: Problema → Propuesta → Impacto → Prioridad

**Prioridad 7: Completar Métricas de Recursos** (2h) → +6%
- Agregar: RAM, CPU, tokens
- Contextualizar: promedio, máx, mín

**Prioridad 8: Pulir Lenguaje Técnico** (1h) → +1%
- Revisar informe con terminología apropiada
- Argumentar con datos

**Total Semana 2:** +22% → Nota sube a 104/100 (7.0/7.0) ✅

---

### **Semana 3 (8 horas):**

**Revisión Final:**
- Testing completo del dashboard
- Verificar todas las capturas
- Revisar informe (ortografía, formato)
- Preparar presentación
- Backup del proyecto

---

## 7. ESTRUCTURA DE ARCHIVOS REQUERIDA

```
EVALUACION 1 SOLUCIONES IA/
├── dashboard.py                    ⚠️ CREAR (CRÍTICO)
├── app_agent.py                    ✅ Existe (modificar)
├── README.md                       ⚠️ Actualizar
├── requirements.txt                ⚠️ Agregar: plotly, psutil
│
├── src/
│   ├── monitoring/                 ⚠️ CREAR CARPETA
│   │   ├── __init__.py
│   │   ├── metrics.py              ⚠️ CREAR (CRÍTICO)
│   │   └── analyzer.py             ⚠️ CREAR
│   │
│   ├── security/                   ⚠️ CREAR CARPETA
│   │   ├── __init__.py
│   │   ├── validator.py            ⚠️ CREAR
│   │   └── rate_limiter.py         ⚠️ CREAR
│   │
│   ├── utils/
│   │   └── logger.py               ✅ Existe (modificar a JSON)
│   │
│   └── [resto de archivos]         ✅ Mantener
│
├── docs/
│   ├── INFORME_EP3.pdf             ⚠️ CREAR (CRÍTICO)
│   ├── screenshots/                ⚠️ CREAR CARPETA
│   │   ├── dashboard_full.png
│   │   ├── kpis.png
│   │   ├── latency_chart.png
│   │   ├── resources.png
│   │   ├── errors.png
│   │   ├── tools.png
│   │   ├── logs_json.png
│   │   └── recommendations.png
│   │
│   └── [archivos existentes]       ✅ Mantener
│
├── data/
│   └── metrics/                    ⚠️ CREAR CARPETA
│       ├── metrics_history.json
│       └── patterns_analysis.json
│
└── logs/                           ✅ Existe
    └── [archivos .log]             ✅ Cambiar a .json
```

---

## 8. CÓDIGO ESENCIAL A IMPLEMENTAR

### **1. dashboard.py** (CRÍTICO - 15%)

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from pathlib import Path

st.set_page_config(
    page_title="Dashboard Observabilidad",
    page_icon="📊",
    layout="wide"
)

# Cargar métricas
def load_metrics():
    with open('data/metrics/metrics_history.json') as f:
        return json.load(f)

metrics = load_metrics()

# === TÍTULO ===
st.title("📊 Dashboard de Observabilidad - Agente IA Pastelería 1000 Sabores")
st.markdown("---")

# === PANEL 1: KPIs ===
st.header("📈 Indicadores Clave de Rendimiento (KPIs)")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Consultas",
        metrics['total_queries'],
        delta=f"+{metrics['queries_today']} hoy"
    )

with col2:
    st.metric(
        "Precisión",
        f"{metrics['precision']:.1f}%",
        delta=f"{metrics['precision_delta']:+.1f}%"
    )

with col3:
    st.metric(
        "Latencia Promedio",
        f"{metrics['avg_latency']:.0f}ms",
        delta=f"{metrics['latency_delta']:+.0f}ms",
        delta_color="inverse"
    )

with col4:
    st.metric(
        "Tasa de Error",
        f"{metrics['error_rate']:.1f}%",
        delta=f"{metrics['error_delta']:+.1f}%",
        delta_color="inverse"
    )

with col5:
    st.metric(
        "Tokens/Query",
        f"{metrics['avg_tokens']:.0f}",
        delta=f"{metrics['tokens_delta']:+.0f}"
    )

st.markdown("---")

# === PANEL 2: LATENCIA ===
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("⏱️ Evolución de Latencia")
    df_latency = pd.DataFrame(metrics['latency_history'])
    fig = px.line(
        df_latency,
        x='timestamp',
        y='latency_ms',
        title='Latencia en el Tiempo',
        labels={'latency_ms': 'Latencia (ms)', 'timestamp': 'Fecha/Hora'}
    )
    fig.add_hline(
        y=metrics['avg_latency'],
        line_dash="dash",
        annotation_text="Promedio"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Estadísticas")
    st.metric("Promedio", f"{metrics['avg_latency']:.0f}ms")
    st.metric("Máximo", f"{metrics['max_latency']:.0f}ms")
    st.metric("Mínimo", f"{metrics['min_latency']:.0f}ms")
    st.metric("Desv. Estándar", f"{metrics['std_latency']:.0f}ms")

st.markdown("---")

# === PANEL 3: RECURSOS ===
st.subheader("💻 Uso de Recursos del Sistema")
col1, col2, col3 = st.columns(3)

with col1:
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=metrics['current_memory_mb'],
        delta={'reference': metrics['avg_memory_mb']},
        title={'text': "Memoria RAM (MB)"},
        gauge={
            'axis': {'range': [None, 1000]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 500], 'color': "lightgray"},
                {'range': [500, 750], 'color': "yellow"},
                {'range': [750, 1000], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 800
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=metrics['current_cpu_percent'],
        delta={'reference': metrics['avg_cpu_percent']},
        title={'text': "CPU (%)"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "red"}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=metrics['current_tokens'],
        delta={'reference': metrics['avg_tokens']},
        title={'text': "Tokens Consumidos"},
        gauge={
            'axis': {'range': [None, 4000]},
            'bar': {'color': "purple"}
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# === PANEL 4: ERRORES ===
col1, col2 = st.columns(2)

with col1:
    st.subheader("❌ Distribución de Errores")
    df_errors = pd.DataFrame(
        metrics['error_types'].items(),
        columns=['Tipo de Error', 'Frecuencia']
    )
    fig = px.bar(
        df_errors,
        x='Tipo de Error',
        y='Frecuencia',
        color='Frecuencia',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📉 Errores en el Tiempo")
    df_errors_time = pd.DataFrame(metrics['errors_history'])
    fig = px.line(
        df_errors_time,
        x='timestamp',
        y='error_count',
        title='Frecuencia de Errores'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# === PANEL 5: HERRAMIENTAS ===
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔧 Herramientas Más Usadas")
    df_tools = pd.DataFrame(
        metrics['tool_usage'].items(),
        columns=['Herramienta', 'Usos']
    )
    fig = px.pie(
        df_tools,
        values='Usos',
        names='Herramienta',
        hole=0.3
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("⏱️ Latencia por Herramienta")
    df_tool_latency = pd.DataFrame(metrics['tool_latency'])
    fig = px.bar(
        df_tool_latency,
        x='tool',
        y='avg_latency_ms',
        color='avg_latency_ms',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# === PANEL 6: PATRONES Y ANOMALÍAS ===
st.subheader("🔍 Patrones y Anomalías Detectadas")

tab1, tab2 = st.tabs(["Patrones", "Anomalías"])

with tab1:
    for pattern in metrics['patterns']:
        st.info(f"**{pattern['title']}**: {pattern['description']}")

with tab2:
    for anomaly in metrics['anomalies']:
        st.warning(f"**{anomaly['type']}**: {anomaly['description']}")
```

### **2. src/monitoring/metrics.py** (CRÍTICO - 15%)

```python
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import numpy as np

class ObservabilityMetrics:
    def __init__(self, data_dir='data/metrics'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.total_queries = 0
        self.correct_responses = 0
        self.consistency_scores = []
        self.errors = []
        self.latencies = []
        self.resource_usage = []
        self.tool_usage = {}
    
    def record_query(
        self,
        query: str,
        response: str,
        is_correct: bool,
        latency_ms: float,
        memory_mb: float,
        cpu_percent: float,
        tokens: int,
        tools_used: List[str],
        error: str = None
    ):
        """Registra una query completa con todas sus métricas"""
        self.total_queries += 1
        
        if is_correct:
            self.correct_responses += 1
        
        if error:
            self.errors.append({
                'timestamp': datetime.now().isoformat(),
                'error': error,
                'query': query
            })
        
        self.latencies.append({
            'timestamp': datetime.now().isoformat(),
            'latency_ms': latency_ms
        })
        
        self.resource_usage.append({
            'timestamp': datetime.now().isoformat(),
            'memory_mb': memory_mb,
            'cpu_percent': cpu_percent,
            'tokens': tokens
        })
        
        for tool in tools_used:
            self.tool_usage[tool] = self.tool_usage.get(tool, 0) + 1
    
    def calculate_precision(self) -> float:
        """Precisión = respuestas correctas / total"""
        if self.total_queries == 0:
            return 0.0
        return (self.correct_responses / self.total_queries) * 100
    
    def calculate_error_frequency(self) -> float:
        """Errores por cada 100 consultas"""
        if self.total_queries == 0:
            return 0.0
        return (len(self.errors) / self.total_queries) * 100
    
    def get_latency_stats(self) -> Dict:
        """Estadísticas de latencia"""
        if not self.latencies:
            return {}
        
        values = [l['latency_ms'] for l in self.latencies]
        return {
            'avg': np.mean(values),
            'max': np.max(values),
            'min': np.min(values),
            'std': np.std(values)
        }
    
    def export_metrics(self):
        """Exporta métricas a JSON para el dashboard"""
        latency_stats = self.get_latency_stats()
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'total_queries': self.total_queries,
            'precision': self.calculate_precision(),
            'error_rate': self.calculate_error_frequency(),
            'avg_latency': latency_stats.get('avg', 0),
            'max_latency': latency_stats.get('max', 0),
            'min_latency': latency_stats.get('min', 0),
            'std_latency': latency_stats.get('std', 0),
            'latency_history': self.latencies,
            'error_types': self._count_error_types(),
            'tool_usage': self.tool_usage,
            'resource_usage': self.resource_usage
        }
        
        output_file = self.data_dir / 'metrics_history.json'
        with open(output_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        return metrics
    
    def _count_error_types(self) -> Dict:
        """Cuenta tipos de errores"""
        error_types = {}
        for error in self.errors:
            error_type = error['error'].split(':')[0]
            error_types[error_type] = error_types.get(error_type, 0) + 1
        return error_types
```

---

## 9. RECOMENDACIONES FINALES

### ✅ **Fortalezas del Proyecto:**
- Agente ReAct bien implementado (EP2)
- Código modular y organizado
- Sistema de logging funcional
- Memoria dual operativa

### 🎯 **Áreas de Oportunidad:**
- **Observabilidad**: Implementar dashboard y métricas completas
- **Documentación**: Crear informe técnico con evidencia visual
- **Análisis**: Identificar patrones y proponer mejoras basadas en datos

### 💡 **Consejo Final:**
**Prioriza el dashboard (IE5 - 15%)** y **métricas de precisión (IE1 - 15%)**. Estos dos componentes te dan 30% de la nota y son los más visibles en la presentación. Con 12 horas de trabajo enfocado, puedes pasar de 31% a 61% (4.3/7.0 = APROBADO).

Luego, en la segunda semana, completa el informe y recomendaciones para llegar a 90-100%.

---

**📊 NOTA FINAL PROYECTADA CON PLAN COMPLETO: 95-100/100 (6.7-7.0/7.0)**

¿Listo para empezar? Te recomiendo comenzar por el dashboard. ¿Quieres que te ayude a implementarlo? 🚀
