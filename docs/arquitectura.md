# 🏗️ Arquitectura del Agente Inteligente

## 📐 Vista General

El sistema implementa una arquitectura **ReAct (Reasoning + Acting)** con los siguientes componentes principales:

## 1. Capas Arquitectónicas

### 📱 Capa de Presentación (UI)
- **Tecnología**: Streamlit
- **Archivo**: `app_agent.py`
- **Responsabilidades**:
  - Renderizar interfaz de chat
  - Mostrar panel de control
  - Visualizar proceso de razonamiento
  - Recoger input del usuario
  - Mostrar métricas en tiempo real

### 🤖 Capa de Agente (Orquestación)
- **Tecnología**: LangChain Agents
- **Archivo**: `src/agent/agent_executor.py`
- **Responsabilidades**:
  - Ciclo ReAct (Thought/Action/Observation)
  - Selección de herramientas
  - Gestión de iteraciones
  - Manejo de errores
  - Tracking de ejecución

### 🛠️ Capa de Herramientas (Tools)
- **Tecnología**: LangChain BaseTool
- **Archivo**: `src/agent/tools.py`
- **Herramientas**:
  1. **SearchProductsTool**: Búsqueda en catálogo
  2. **CalculateDiscountTool**: Cálculo de descuentos
  3. **CheckInventoryTool**: Verificación de stock
  4. **CustomerHistoryTool**: Historial del cliente

### 💾 Capa de Memoria (Memory)
- **Tecnologías**: LangChain Memory + ChromaDB
- **Archivos**: `src/memory/`
- **Componentes**:
  - **Short Term**: ConversationBufferMemory (sesión)
  - **Long Term**: ChromaDB + Embeddings (persistente)
  - **Context**: Referencias anafóricas

### 📊 Capa de Datos (Data)
- **Tecnología**: JSON, CSV, Markdown
- **Directorio**: `data/`
- **Fuentes**:
  - productos.json (catálogo)
  - faqs.json (preguntas frecuentes)
  - politicas_descuentos.md (reglas)
  - clientes_ejemplos.csv (clientes)
  - historial_ejemplos.csv (conversaciones)

---

## 2. Flujo de Datos

### Flujo Principal de una Consulta

```
┌─────────────┐
│   USUARIO   │
│  "Consulta" │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  STREAMLIT UI (app_agent.py)        │
│  • Captura input                    │
│  • Muestra "thinking" animation     │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  SHORT TERM MEMORY                  │
│  • Recupera contexto de sesión      │
│  • Formatea historial               │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  AGENT EXECUTOR                     │
│  ┌───────────────────────────────┐  │
│  │ CICLO ReAct (max 10 iter)     │  │
│  │                               │  │
│  │ 1. THOUGHT                    │  │
│  │    ↓                          │  │
│  │ 2. ACTION (select tool)       │  │
│  │    ↓                          │  │
│  │ 3. OBSERVATION (tool result)  │  │
│  │    ↓                          │  │
│  │ 4. ¿Necesita más info?        │  │
│  │    ├─ SÍ: volver a paso 1     │  │
│  │    └─ NO: generar respuesta   │  │
│  └───────────────────────────────┘  │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  TOOLS (según necesidad)            │
│  • search_products                  │
│  • calculate_discount               │
│  • check_inventory                  │
│  • customer_history                 │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  DATA LAYER                         │
│  • Productos JSON                   │
│  • Políticas MD                     │
│  • ChromaDB (historial)             │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  RESPONSE GENERATION                │
│  • Final Answer                     │
│  • Execution Trace                  │
│  • Metadata (time, tools used)      │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  MEMORY STORAGE                     │
│  • Short Term: agregar a buffer     │
│  • Long Term: guardar en ChromaDB   │
│  • Logger: registrar en archivo     │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  STREAMLIT UI                       │
│  • Mostrar respuesta                │
│  • Renderizar badges de tools       │
│  • Mostrar métricas                 │
│  • Expandible: ver razonamiento     │
└─────────────────────────────────────┘
```

---

## 3. Arquitectura ReAct Detallada

### Ciclo Reasoning + Acting

```
┌─────────────────────────────────────────────────────────┐
│                    REACT LOOP                           │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │  ITERATION N                                   │   │
│  │                                                │   │
│  │  1️⃣ THOUGHT (Reasoning)                       │   │
│  │     ┌──────────────────────────────────────┐  │   │
│  │     │ LLM analiza:                         │  │   │
│  │     │ • Qué necesita el usuario            │  │   │
│  │     │ • Qué información tengo              │  │   │
│  │     │ • Qué tool usar next                 │  │   │
│  │     └──────────────────────────────────────┘  │   │
│  │                    ↓                           │   │
│  │  2️⃣ ACTION (Acting)                           │   │
│  │     ┌──────────────────────────────────────┐  │   │
│  │     │ Ejecutar herramienta:                │  │   │
│  │     │ • search_products(...)               │  │   │
│  │     │ • calculate_discount(...)            │  │   │
│  │     │ • check_inventory(...)               │  │   │
│  │     │ • customer_history(...)              │  │   │
│  │     └──────────────────────────────────────┘  │   │
│  │                    ↓                           │   │
│  │  3️⃣ OBSERVATION (Result)                      │   │
│  │     ┌──────────────────────────────────────┐  │   │
│  │     │ Resultado de la herramienta          │  │   │
│  │     │ • Productos encontrados              │  │   │
│  │     │ • Precio calculado                   │  │   │
│  │     │ • Stock disponible                   │  │   │
│  │     │ • Historial recuperado               │  │   │
│  │     └──────────────────────────────────────┘  │   │
│  │                    ↓                           │   │
│  │  4️⃣ DECISION                                  │   │
│  │     ┌──────────────────────────────────────┐  │   │
│  │     │ ¿Tengo suficiente info?              │  │   │
│  │     │                                      │  │   │
│  │     │ SÍ → FINAL ANSWER                    │  │   │
│  │     │ NO → NEXT ITERATION                  │  │   │
│  │     └──────────────────────────────────────┘  │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
│  Max Iterations: 10                                 │
│  Early Stopping: Si encuentra respuesta completa   │
└─────────────────────────────────────────────────────┘
```

### Ejemplo de Trace Real

```json
{
  "query": "Torta vegana para 15 personas",
  "iterations": 3,
  "trace": [
    {
      "step": 1,
      "thought": "Necesito buscar tortas veganas",
      "action": "search_products",
      "input": {"query": "vegana"},
      "observation": "Encontradas 2 tortas veganas: PV001, PV002"
    },
    {
      "step": 2,
      "thought": "Debo verificar capacidad para 15 personas",
      "action": "check_inventory",
      "input": {"product_code": "PV001", "capacity_needed": 15},
      "observation": "PV001 sirve para 12 personas. Necesitas 2 unidades"
    },
    {
      "step": 3,
      "thought": "Calcular precio para 2 unidades",
      "action": "calculate_discount",
      "input": {"product_code": "PV001", "quantity": 2},
      "observation": "2x PV001 = $104,000 sin descuentos"
    }
  ],
  "final_answer": "Para 15 personas recomiendo 2 tortas veganas PV001..."
}
```

---

## 4. Sistema de Memoria Dual

### Memoria de Corto Plazo (Short Term)

```
┌─────────────────────────────────────────┐
│  ConversationBufferMemory              │
│                                         │
│  Almacena:                              │
│  ┌─────────────────────────────────┐   │
│  │ Message 1: User + Assistant     │   │
│  │ Message 2: User + Assistant     │   │
│  │ Message 3: User + Assistant     │   │
│  │ ...                             │   │
│  │ Message N: User + Assistant     │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Características:                       │
│  • Se limpia al reiniciar sesión        │
│  • Mantiene contexto para referencias   │
│  • Permite "esa torta", "la anterior"   │
│  • Extrae preferencias en tiempo real   │
└─────────────────────────────────────────┘
```

### Memoria de Largo Plazo (Long Term)

```
┌─────────────────────────────────────────┐
│  ChromaDB + Embeddings                  │
│                                         │
│  Pipeline:                              │
│  ┌─────────────────────────────────┐   │
│  │ 1. Conversación completa        │   │
│  │    User: "..."                  │   │
│  │    Assistant: "..."             │   │
│  └──────────┬──────────────────────┘   │
│             ↓                           │
│  ┌─────────────────────────────────┐   │
│  │ 2. Generar Embedding            │   │
│  │    Sentence Transformer         │   │
│  │    (multilingual MiniLM)        │   │
│  └──────────┬──────────────────────┘   │
│             ↓                           │
│  ┌─────────────────────────────────┐   │
│  │ 3. Guardar en ChromaDB          │   │
│  │    + Metadata:                  │   │
│  │      - customer_id              │   │
│  │      - timestamp                │   │
│  │      - tools_used               │   │
│  └──────────┬──────────────────────┘   │
│             ↓                           │
│  ┌─────────────────────────────────┐   │
│  │ 4. Similarity Search            │   │
│  │    Recuperar conversaciones     │   │
│  │    similares (k=3)              │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Características:                       │
│  • Persiste entre sesiones              │
│  • Búsqueda semántica eficiente         │
│  • Recuperación por customer_id         │
│  • Análisis de preferencias             │
└─────────────────────────────────────────┘
```

---

## 5. Herramientas (Tools)

### Estructura de una Tool

```python
class MyTool(BaseTool):
    # Identificador único
    name: str = "my_tool"
    
    # Descripción para el LLM
    description: str = """
    Qué hace esta herramienta...
    Cuándo usarla...
    """
    
    # Schema de inputs
    args_schema: Type[BaseModel] = MyToolInput
    
    # Implementación
    def _run(self, **kwargs) -> str:
        # Lógica de la herramienta
        return result
```

### Interacción entre Tools y Agent

```
Agent Executor
      │
      ├─ Analiza query
      │
      ├─ Selecciona tool(s)
      │
      ├─ Prepara inputs
      │
      ▼
┌─────────────────────┐
│  TOOL DISPATCHER    │
└─────────┬───────────┘
          │
    ┌─────┴─────┬─────────┬─────────┐
    │           │         │         │
    ▼           ▼         ▼         ▼
┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐
│Search │  │Discount│ │Inventory│ │History│
└───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘
    │          │          │          │
    └──────────┴──────────┴──────────┘
               │
               ▼
         Result to Agent
```

---

## 6. Sistema de Logging

### Niveles de Logging

```
┌─────────────────────────────────────┐
│  LOGGER HIERARCHY                   │
│                                     │
│  DEBUG                              │
│    ↓                                │
│  INFO      ← Default                │
│    ↓                                │
│  WARNING                            │
│    ↓                                │
│  ERROR                              │
│    ↓                                │
│  CRITICAL                           │
└─────────────────────────────────────┘
```

### Qué se Registra

```
┌──────────────────────────────────────────┐
│  QUERY         │ Consulta del usuario    │
├──────────────────────────────────────────┤
│  THOUGHT       │ Razonamiento del agente │
├──────────────────────────────────────────┤
│  TOOL          │ Herramienta ejecutada   │
├──────────────────────────────────────────┤
│  OBSERVATION   │ Resultado de la tool    │
├──────────────────────────────────────────┤
│  ANSWER        │ Respuesta final         │
├──────────────────────────────────────────┤
│  ERROR         │ Errores y excepciones   │
├──────────────────────────────────────────┤
│  METRICS       │ Tiempos y estadísticas  │
├──────────────────────────────────────────┤
│  MEMORY        │ Operaciones de memoria  │
└──────────────────────────────────────────┘
```

---

## 7. Patrones de Diseño Utilizados

### Factory Pattern
```python
# Creación de componentes
agent = create_agent(...)
memory = create_short_term_memory(...)
logger = create_logger(...)
```

### Strategy Pattern
```python
# Diferentes estrategias de memoria
if memory_type == "buffer":
    memory = ConversationBufferMemory(...)
elif memory_type == "summary":
    memory = ConversationSummaryMemory(...)
```

### Observer Pattern
```python
# Logger observa todas las operaciones
logger.log_query(query)
logger.log_tool_call(tool, input)
logger.log_answer(answer)
```

---

## 8. Consideraciones de Rendimiento

### Optimizaciones Implementadas

1. **Lazy Loading**: Componentes se cargan solo cuando se necesitan
2. **Caching**: Productos y datos estáticos en memoria
3. **Límite de Iteraciones**: Max 10 para evitar loops infinitos
4. **Early Stopping**: Termina cuando tiene respuesta completa
5. **Embeddings Precomputados**: ChromaDB indexa vectores
6. **Streaming**: UI actualiza progresivamente

### Bottlenecks Potenciales

- 🔴 **OpenAI API**: Rate limits y latencia
- 🟡 **ChromaDB**: Primera carga de embeddings
- 🟢 **Streamlit**: Re-renders frecuentes

### Mitigaciones

```python
# Rate limiting
time.sleep(0.5)  # Entre requests

# Caching de embeddings
@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(...)

# Reducir temperatura para respuestas más rápidas
temperature=0.1  # vs 0.3 o 0.7
```

---

## 9. Seguridad y Privacidad

### Medidas Implementadas

- ✅ API Keys en variables de entorno (.env)
- ✅ No se hardcodean credenciales
- ✅ Logs no incluyen información sensible
- ✅ ChromaDB local (no cloud)
- ✅ Datos de clientes encriptados en repo

### Mejores Prácticas

```python
# ❌ MAL
openai_key = "sk-abc123..."

# ✅ BIEN
openai_key = os.getenv("OPENAI_API_KEY")
```

---

## 10. Extensibilidad

### Agregar Nueva Herramienta

```python
# 1. Crear Input Schema
class NewToolInput(BaseModel):
    param1: str = Field(description="...")

# 2. Crear Tool Class
class NewTool(BaseTool):
    name = "new_tool"
    description = "..."
    args_schema = NewToolInput
    
    def _run(self, param1: str) -> str:
        # Implementación
        return result

# 3. Registrar en initialize_tools()
def initialize_tools(...):
    tools = [
        SearchProductsTool(...),
        # ... otras tools
        NewTool(...)  # ← Agregar aquí
    ]
    return tools
```

### Agregar Nuevo Tipo de Memoria

```python
# src/memory/custom_memory.py
class CustomMemory:
    def __init__(self, ...):
        # Setup
        pass
    
    def store(self, ...):
        # Guardar
        pass
    
    def retrieve(self, ...):
        # Recuperar
        pass
```

---

## 11. Deployment (Futuro)

### Opciones de Deployment

```
┌──────────────────────────────────────┐
│  LOCAL (Actual)                      │
│  • streamlit run app_agent.py        │
│  • localhost:8501                    │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│  STREAMLIT CLOUD                     │
│  • streamlit.io deployment           │
│  • Automático desde GitHub           │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│  DOCKER CONTAINER                    │
│  • dockerfile + docker-compose       │
│  • Portable y escalable              │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│  KUBERNETES                          │
│  • Pods + Services                   │
│  • Alta disponibilidad               │
└──────────────────────────────────────┘
```

---

## 🎓 Resumen Académico

Esta arquitectura implementa:

✅ **Separation of Concerns**: Cada capa tiene responsabilidad única  
✅ **Modularity**: Componentes intercambiables  
✅ **Scalability**: Fácil agregar herramientas/memoria  
✅ **Maintainability**: Código limpio y documentado  
✅ **Testability**: Componentes aislados para testing  
✅ **Observability**: Logging completo para debugging

---

**Versión**: 2.0.0  
**Última actualización**: Octubre 2025
