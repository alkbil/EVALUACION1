# 🚀 GUÍA DE INTEGRACIÓN EP3

## Cómo Integrar Observabilidad en app_agent.py

**Proyecto:** Agente Inteligente Pastelería 1000 Sabores  
**Objetivo:** Implementar monitoreo completo de EP3  

---

## 1. INSTALACIÓN DE DEPENDENCIAS

```bash
# Instalar paquetes faltantes para EP3
pip install psutil>=5.9.0  # Para medir recursos
pip install plotly>=5.18.0  # Para gráficos
```

### requirements.txt actualizado:
```
# EP3: Observabilidad
psutil>=5.9.0
plotly>=5.18.0
```

---

## 2. ESTRUCTURA DE DIRECTORIOS (VERIFICAR)

```
proyecto/
├── src/
│   ├── monitoring/          ✅ NUEVO
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   ├── logs_analyzer.py
│   │   └── anomaly_detector.py
│   │
│   ├── security/            ✅ NUEVO
│   │   ├── __init__.py
│   │   └── validators.py
│   │
│   └── [EP2 modules]
│
├── dashboard.py             ✅ NUEVO
├── informe.py               ✅ NUEVO
│
├── docs/
│   ├── security_protocols.md      ✅ NUEVO
│   ├── observability_guide.md     ✅ NUEVO
│   └── [otros docs]
│
├── metrics/                 ✅ NUEVO (auto-creado)
│   └── metrics.json
│
└── logs/                    ✅ NUEVO (auto-creado)
    ├── agent_*.log
    └── analysis_report.json
```

---

## 3. MODIFICACIÓN MINIMALISTA DE app_agent.py

**Estrategia:** Integración no invasiva (máximo 30 líneas de código nuevo)

### Opción A: Integración Básica (RECOMENDADO)

```python
# Al inicio del archivo (después de imports)
import time
from src.monitoring.metrics import ObservabilityMetrics
from src.security.validators import SecurityValidator

# Inicializar (una sola vez)
metrics = ObservabilityMetrics()
security = SecurityValidator(max_requests_per_minute=60)

# Encontrar esta sección en app_agent.py:
# def run_agent():
#     query = st.text_input("¿En qué te puedo ayudar?")
#     if query:
#         # AÑADIR AQUÍ:

if query:
    # --- NUEVA INTEGRACIÓN EP3 ---
    # 1. Validar seguridad (IE6)
    is_valid, msg = security.validate_input(query)
    if not is_valid:
        st.error(f"❌ {msg}")
        st.stop()
    
    # 2. Registrar query (IE1)
    query_id = metrics.record_query(query, query_type="agent")
    
    # 3. Medir tiempo
    start_time = time.time()
    
    # --- CÓDIGO EXISTENTE DE EJECUCIÓN ---
    result = agent_executor.execute(query)
    
    # --- NUEVA INTEGRACIÓN EP3 ---
    # 4. Registrar resultado (IE1, IE2)
    exec_time = time.time() - start_time
    metrics.record_response(query_id, result['output'], is_correct=True)
    metrics.measure_resources(exec_time, tokens_prompt=100, tokens_response=50)
    
    # 5. Mostrar resultado (código existente)
    st.write(result['output'])
    
    # 6. Mostrar métricas opcionales
    with st.expander("📊 Métricas de Observabilidad"):
        summary = metrics.get_summary()
        col1, col2, col3 = st.columns(3)
        col1.metric("Precisión", f"{summary['precision']:.1f}%")
        col2.metric("Errores", f"{summary['error_frequency']:.1f}%")
        col3.metric("Latencia", f"{exec_time*1000:.0f}ms")
```

### Opción B: Integración Completa

```python
# Misma que Opción A + estos dos botones en sidebar

if st.sidebar.button("📊 Abrir Dashboard"):
    st.switch_page("pages/dashboard.py")

if st.sidebar.button("📋 Ver Informe EP3"):
    st.switch_page("pages/informe.py")
```

---

## 4. EJECUTAR SISTEMA COMPLETO

### Opción 1: Solo app_agent.py con integración

```bash
streamlit run app_agent.py
```

### Opción 2: Dashboard independiente

```bash
streamlit run dashboard.py
```

### Opción 3: Informe técnico

```bash
streamlit run informe.py
```

### Opción 4: Todo en una app multi-página (RECOMENDADO)

```
proyecto/
├── app_agent.py (main)
├── pages/
│   ├── 01_dashboard.py
│   ├── 02_informe.py
│   └── 03_recomendaciones.py
└── ...
```

Luego ejecutar:
```bash
streamlit run app_agent.py
```

---

## 5. FLUJO DE DATOS COMPLETO

```
Usuario abre app_agent.py
    ↓
Escribe query
    ↓
[SecurityValidator] ← 🛡️ IE6
    ├─ validate_input()
    ├─ check_rate_limit()
    └─ si falla → RECHAZAR
    ↓
[ObservabilityMetrics] ← 📊 IE1
    ├─ record_query()
    └─ query_id = ...
    ↓
[time.time()] → start
    ↓
[PasteleriaAgentExecutor]
    ├─ Ejecuta herramientas
    ├─ Memory
    └─ Genera respuesta
    ↓
[time.time()] → exec_time
    ↓
[ObservabilityMetrics] ← 📊 IE1, IE2
    ├─ record_response()
    ├─ measure_resources()
    ├─ save_metrics()
    └─ json: metrics/metrics.json
    ↓
[Logger] (logger.py)
    ├─ Escribe log
    └─ logs/agent_*.log
    ↓
[Mostrar en UI]
    ├─ Response
    ├─ Metrics (expandible)
    └─ Botones de acceso a Dashboard
    ↓
[Background async] (si se ejecuta)
    ├─ [LogsAnalyzer] ← 📊 IE3
    │  └─ generate_report()
    │     logs/analysis_report.json
    │
    ├─ [AnomalyDetector] ← 📊 IE4
    │  └─ detect_anomalies()
    │
    └─ [ImprovementRecommender] ← 💡 IE7
       └─ generate_recommendations()
    ↓
[Dashboard.py]
    ├─ Lee metrics.json
    ├─ Lee analysis_report.json
    ├─ Visualiza todo
    └─ Muestra recomendaciones
```

---

## 6. VALIDACIÓN DE INTEGRACIÓN

### Checklist:

- [ ] `src/monitoring/` existe con 3 archivos
- [ ] `src/security/` existe con validators.py
- [ ] `dashboard.py` existe en raíz
- [ ] `informe.py` existe en raíz
- [ ] `docs/security_protocols.md` existe
- [ ] `docs/observability_guide.md` existe
- [ ] Ejecutar: `streamlit run app_agent.py`
- [ ] Ver métrica de precisión en UI
- [ ] Ejecutar: `streamlit run dashboard.py`
- [ ] Ver 5 tabs en dashboard
- [ ] Ver botón "Abrir Dashboard" en sidebar (si integración completa)

---

## 7. PRIMERA EJECUCIÓN

### Paso 1: Instalar dependencias

```bash
pip install -r requirements.txt
pip install psutil plotly
```

### Paso 2: Ejecutar app

```bash
streamlit run app_agent.py
```

### Paso 3: Hacer queries

```
Query 1: "¿Cuánto cuesta la torta de chocolate?"
Query 2: "¿Hay promociones?"
Query 3: "¿Cuánto ha costado la torta antes?"
...
```

### Paso 4: Ver métricas

- Expandir sección "📊 Métricas de Observabilidad"
- Ver Precisión, Errores, Latencia

### Paso 5: Abrir dashboard

```bash
# En otra terminal
streamlit run dashboard.py
```

### Paso 6: Revisar análisis

- Tab "📈 Métricas": ver histórico
- Tab "🔧 Logs": ver análisis
- Tab "⚠️ Anomalías": detectar problemas
- Tab "🛡️ Seguridad": ver incidentes
- Tab "💡 Mejoras": ver recomendaciones

---

## 8. VERIFICAR ARCHIVOS GENERADOS

Después de ejecutar, verificar:

```bash
# Métricas
ls -la metrics/
cat metrics/metrics.json

# Logs
ls -la logs/
head -20 logs/agent_*.log
cat logs/analysis_report.json

# Documentación
ls -la docs/
cat docs/security_protocols.md
cat docs/observability_guide.md
```

---

## 9. SOLUCIÓN DE PROBLEMAS

### Error: "ModuleNotFoundError: No module named 'monitoring'"

**Causa:** Falta `from src.monitoring import ...`

**Solución:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
```

### Error: "permission denied" en metrics.json

**Solución:**
```bash
chmod 777 metrics/
chmod 777 logs/
```

### Dashboard no muestra datos

**Solución:**
```bash
# Regenerar análisis
python -c "
from src.monitoring.logs_analyzer import LogsAnalyzer
analyzer = LogsAnalyzer()
analyzer.generate_report()
"
```

---

## 10. PRÓXIMOS PASOS

1. **Ejecutar sistema** y validar que todo funciona
2. **Hacer varias queries** para generar datos
3. **Revisar dashboard** y anomalías
4. **Implementar recomendaciones** prioritarias
5. **Documentar mejoras** realizadas
6. **Repetir** semanalmente

---

**Guía v1.0 | 2025-01-26**
