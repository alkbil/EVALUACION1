# Agente Inteligente - Pastelería 1000 Sabores

## Descripción del Proyecto

Sistema de **agente inteligente conversacional** desarrollado con arquitectura **ReAct (Reasoning + Acting)** para la Pastelería 1000 Sabores. El sistema utiliza **LangChain** para orquestación de herramientas, **memoria dual** (corto y largo plazo), y proporciona respuestas contextuales e inteligentes sobre productos, descuentos y servicios.

### Objetivos Cumplidos

**Orquestación de Agente con Herramientas (20%)**
- 4 herramientas especializadas implementadas con LangChain
- Arquitectura ReAct para razonamiento autónomo
- Logging completo de decisiones y ejecuciones

**Sistema de Memoria (20%)**
- Memoria de corto plazo con ConversationBufferMemory
- Memoria de largo plazo con ChromaDB y embeddings
- Recuperación de contexto y preferencias de conversaciones previas

**Planificación y Toma de Decisiones (20%)**
- Lógica adaptativa según perfil del cliente
- Manejo de casos simples, medios y complejos
- Priorización inteligente de tareas

**Mejoras al Aplicativo Streamlit (40%)**
- Panel lateral con estado del agente y herramientas
- Visualización del proceso de razonamiento
- Métricas en tiempo real
- Interfaz moderna y profesional

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI (app_agent.py)              │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │  Chat UI   │  │ Sidebar Info │  │ Thinking Visualizer │ │
│  └────────────┘  └──────────────┘  └─────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
                ┌────────────▼────────────┐
                │  AGENT EXECUTOR         │
                │  (ReAct Architecture)   │
                │  - Reasoning Loop       │
                │  - Tool Selection       │
                │  - Decision Making      │
                └────────┬────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌────▼─────┐ ┌───────▼────────┐
│   TOOLS (4)    │ │  MEMORY  │ │    LOGGER      │
│ • Search       │ │  • Short │ │  • Trace       │
│ • Discount     │ │  • Long  │ │  • Metrics     │
│ • Inventory    │ │  • Vector│ │  • Errors      │
│ • History      │ │          │ │                │
└────────────────┘ └──────────┘ └────────────────┘
         │              │              │
         └──────────────┼──────────────┘
                        │
               ┌────────▼────────┐
               │   DATA LAYER    │
               │  • Products     │
               │  • Policies     │
               │  • FAQs         │
               │  • ChromaDB     │
               └─────────────────┘
```

---

## Estructura del Proyecto

```
EVALUACION 1 SOLUCIONES IA/
├── app_agent.py                    # Aplicación principal mejorada
├── app.py                          # Aplicación original (RAG básico)
├── requirements.txt                # Dependencias actualizadas
├── .env.example                    # Template de configuración
├── README.md                       # Documentación original
├── README_AGENT.md                 # Este archivo (agente)
│
├── src/
│   ├── agent/                      # MÓDULO DE AGENTE
│   │   ├── __init__.py
│   │   ├── agent_executor.py       # Orquestador principal (ReAct)
│   │   ├── tools.py                # 4 herramientas especializadas
│   │   └── prompts.py              # Templates de prompts
│   │
│   ├── memory/                     # MÓDULO DE MEMORIA
│   │   ├── __init__.py
│   │   ├── short_term.py           # Memoria de sesión (Buffer)
│   │   └── long_term.py            # Memoria persistente (ChromaDB)
│   │
│   ├── utils/                      # UTILIDADES
│   │   ├── __init__.py
│   │   └── logger.py               # Sistema de logging
│   │
│   └── [módulos existentes...]     # data_loader, discount_calculator, etc.
│
├── data/                           # DATOS
│   ├── productos.json
│   ├── faqs.json
│   ├── politicas_descuentos.md
│   ├── clientes_ejemplos.csv
│   ├── historial_ejemplos.csv
│   └── chroma_db/                  # Base de datos vectorial (generada)
│
├── docs/                           # DOCUMENTACIÓN
│   ├── arquitectura.md
│   ├── ejemplos_uso.md
│   └── diagrams/
│
├── tests/                          # PRUEBAS
│   └── test_agent.py
│
└── logs/                           # LOGS (generado)
    └── agent_*.log
```

---

## Instalación y Ejecución

### 1️ Requisitos Previos

- **Python 3.8+** instalado
- **pip** actualizado
- **Cuenta de OpenAI** con API Key activa

### 2️ Instalación

```bash
# Navegar al directorio
cd "EVALUACION 1 SOLUCIONES IA"

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows PowerShell:
venv\Scripts\activate
# Windows CMD:
venv\Scripts\activate.bat
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3️ Configuración

```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env y agregar tu API Key de OpenAI
# OPENAI_API_KEY=sk-tu-api-key-aqui
```

### 4️ Ejecutar la Aplicación

```bash
# Iniciar aplicación con agente inteligente (NUEVA VERSIÓN)
streamlit run app_agent.py

# La aplicación se abrirá en http://localhost:8501
```

---

## Características Principales

### Sistema de Agente con ReAct

El agente sigue un ciclo de **Pensamiento → Acción → Observación**:

```
Usuario: "Quiero una torta vegana para 15 personas con descuento"

Thought: Necesito buscar tortas veganas primero
Action: search_products(query="torta vegana")
Observation: Encontré 2 productos veganos...

Thought: Ahora debo verificar capacidad para 15 personas
Action: check_inventory(product_code="PV001", capacity_needed=15)
Observation: La torta XL sirve para 15-20 personas...

Thought: Necesito calcular el precio con posibles descuentos
Action: calculate_discount(product_code="PV001", quantity=1)
Observation: Precio: $52,000...

Final Answer: [Respuesta completa al cliente con opciones y precios]
```

### 4 Herramientas Especializadas

#### 1. **SearchProductsTool** 
```python
# Busca productos en el catálogo
# Filtra por categoría y precio
# Retorna información detallada
search_products(
    query="torta chocolate",
    category="veganos",  # opcional
    max_price=50000      # opcional
)
```

#### 2. **CalculateDiscountTool**
```python
# Calcula descuentos aplicables
# Soporta múltiples tipos de promoción
calculate_discount(
    product_code="TC001",
    customer_age=55,           # opcional
    promo_code="FELICES50",    # opcional
    customer_email="@duoc.cl", # opcional
    quantity=1
)
```

#### 3. **CheckInventoryTool** 
```python
# Verifica disponibilidad
# Estima capacidad de porciones
check_inventory(
    product_code="PV001",
    capacity_needed=15  # opcional
)
```

#### 4. **CustomerHistoryTool** 
```python
# Consulta historial del cliente
# Identifica preferencias recurrentes
customer_history(
    customer_id="cliente123",  # opcional
    customer_email="user@mail" # opcional
)
```

### Sistema de Memoria Dual

#### Memoria de Corto Plazo (ConversationBufferMemory)
- Mantiene contexto de la sesión actual
- Permite referencias anafóricas ("esa torta", "la anterior")
- Extrae preferencias en tiempo real
- Se limpia al reiniciar sesión

#### Memoria de Largo Plazo (ChromaDB + Embeddings)
- Almacena conversaciones con embeddings multilíngües
- Recupera contexto de interacciones previas
- Identifica patrones de compra del cliente
- Persiste entre sesiones

### Visualización Avanzada

- **Panel de Control**: Estado del sistema y herramientas disponibles
- **Proceso de Razonamiento**: Expandible paso a paso (Thought/Action/Observation)
- **Badges de Herramientas**: Visualización coloreada de tools usadas
- **Métricas en Tiempo Real**: Tiempo de ejecución, iteraciones, estado
- **Estadísticas de Uso**: Consultas totales, tasa de éxito, herramientas más usadas

---

## Ejemplos de Uso

### Caso 1: Consulta Simple
```
Usuario: "¿Qué tortas de chocolate tienen?"

Agente:
→ Thought: El cliente busca productos de chocolate
→ Action: search_products(query="chocolate")
→ Observation: Encontré 3 tortas de chocolate...
→ Final Answer: [Lista de 3 tortas con precios y descripciones]

Herramientas usadas: 🔍 Búsqueda
Tiempo: 2.3s | Iteraciones: 1
```

### Caso 2: Consulta con Cálculo
```
Usuario: "¿Cuánto cuesta la torta TC001 para una persona de 55 años?"

Agente:
→ Thought: Necesito el producto TC001 y calcular descuento por edad
→ Action: search_products(query="TC001")
→ Observation: TC001 es Torta Cuadrada de Chocolate, $45,000
→ Thought: Cliente de 55 años califica para descuento 50%
→ Action: calculate_discount(product_code="TC001", customer_age=55)
→ Observation: Precio final $22,500 con 50% descuento
→ Final Answer: [Respuesta con desglose completo]

Herramientas usadas: 🔍 Búsqueda | 💰 Descuentos
Tiempo: 3.8s | Iteraciones: 2
```

### Caso 3: Consulta Compleja
```
Usuario: "Necesito una torta vegana para boda de 25 personas, tengo código FELICES50"

Agente:
→ Thought: Consulta compleja, necesito buscar veganas, verificar capacidad y calcular
→ Action: search_products(query="vegana")
→ Observation: 2 opciones veganas encontradas
→ Thought: Debo verificar si sirven para 25 personas
→ Action: check_inventory(product_code="PV001", capacity_needed=25)
→ Observation: Necesitarías 2 unidades o una torta XL personalizada
→ Thought: Ahora calcular precio con código promocional
→ Action: calculate_discount(product_code="PV001", promo_code="FELICES50", quantity=2)
→ Observation: 2 unidades con 10% descuento = $93,600
→ Final Answer: [Recomendación detallada con opciones y precios]

Herramientas usadas: 🔍 Búsqueda | 📦 Inventario | 💰 Descuentos
Tiempo: 5.2s | Iteraciones: 3
```

---

## Guía de Uso de la Interfaz

### 1. Inicialización
1. Ejecutar `streamlit run app_agent.py`
2. Ingresar tu **OpenAI API Key** (sk-...)
3. (Opcional) Ingresar **Customer ID** para personalización
4. Clic en **"🚀 Inicializar Sistema"**
5. Esperar confirmación ✅

### 2. Panel Lateral (Sidebar)
- **Estado del Sistema**: Verde = activo
- **Herramientas Disponibles**: 4 tools con íconos
- **Estadísticas**: Métricas en tiempo real
- **Promociones**: Descuentos activos
- **Botón Reiniciar**: Limpia memoria y sesión

### 3. Área de Chat
- **Input**: Escribe tu consulta abajo
- **Mensajes**: Historial completo
- **Badges**: Herramientas usadas (coloreadas)
- **Métricas**: Tiempo, iteraciones, estado
- **Expansible**: Ver razonamiento paso a paso

### 4. Consultas Rápidas
- 8 botones con ejemplos preconfigurados
- Clic en cualquiera para autocompletar
- Ideal para demostración rápida

---

## Métricas y Evaluación

El sistema registra automáticamente:

| Métrica | Descripción |
|---------|-------------|
| **Total de consultas** | Número de queries procesadas |
| **Tasa de éxito** | % de ejecuciones exitosas |
| **Herramientas más usadas** | Ranking de tools invocadas |
| **Tiempo promedio** | Segundos por respuesta |
| **Iteraciones promedio** | Pasos del ciclo ReAct |

### Acceso a Estadísticas

```python
# Programáticamente
stats = agent.get_execution_statistics()
print(stats)

# En la UI
Ver panel lateral → Sección " Estadísticas de Uso"
```

---

## Solución de Problemas Comunes

### Error: "No module named 'langchain'"
```bash
pip install --upgrade langchain langchain-openai langchain-community
```

### Error: "OpenAI API key not found"
```bash
# Verificar que .env existe y contiene:
OPENAI_API_KEY=sk-tu-api-key-real-aqui

# O ingrésala directamente en la UI al inicializar
```

### Error: "ChromaDB connection failed"
```bash
# Reinstalar ChromaDB
pip uninstall chromadb -y
pip install chromadb>=0.4.22

# Eliminar directorio corrupto
rm -rf data/chroma_db
# La app creará uno nuevo automáticamente
```

### Agente toma demasiado tiempo
```python
# Ajustar en src/agent/agent_executor.py
max_iterations=5  # Reducir de 10 a 5

# O usar temperatura más baja
temperature=0.1   # Más determinístico
```

### Error: "Rate limit exceeded"
```
- Esperar 20 segundos entre consultas
- Verificar cuota de tu cuenta OpenAI
- Considerar upgrade a plan pagado
```

---

## Configuración Avanzada

### Cambiar Modelo de OpenAI

En `.env`:
```bash
OPENAI_MODEL=gpt-4  # Cambiar de gpt-3.5-turbo a gpt-4
```

O programáticamente en `app_agent.py`:
```python
agent = create_agent(
    ...,
    model_name="gpt-4",
    temperature=0.2
)
```

### Ajustar Memoria

```python
# Memoria tipo resumen (para conversaciones largas)
memory = create_short_term_memory(
    memory_type="summary",  # Cambiar de "buffer"
    openai_api_key=api_key
)
```

### Personalizar Prompts

Editar `src/agent/prompts.py`:
```python
AGENT_SYSTEM_PROMPT = """
Tu prompt personalizado aquí...
"""
```

---

## Testing

### Ejecutar Tests Básicos

```bash
# Tests del agente
python -m pytest tests/test_agent.py -v

# Tests con coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Manual de Herramientas

```python
from src.agent import initialize_tools
from src.data_loader import PasteleriaDataLoader
from src.discount_calculator import DiscountCalculator

# Inicializar
data_loader = PasteleriaDataLoader()
calculator = DiscountCalculator()
tools = initialize_tools(data_loader, calculator)

# Probar search_products
search_tool = tools[0]
result = search_tool._run(query="chocolate")
print(result)

# Probar calculate_discount
discount_tool = tools[1]
result = discount_tool._run(
    product_code="TC001",
    customer_age=55
)
print(result)
```

---

## Documentación Adicional

- **[Arquitectura Detallada](docs/arquitectura.md)**: Diagramas y flujos
- **[Ejemplos Completos](docs/ejemplos_uso.md)**: Casos de uso extendidos
- **[Diagramas Visuales](docs/diagrams/)**: Orquestación y memoria

---

## Información Académica

### Cumplimiento de Requisitos

| Requisito | Peso | Implementación | Estado |
|-----------|------|----------------|--------|
| **Orquestación con Herramientas** | 20% | 4 tools + ReAct + logging | ✅ 100% |
| **Sistema de Memoria** | 20% | Corto plazo + Largo plazo + Vector store | ✅ 100% |
| **Planificación y Decisiones** | 20% | Lógica adaptativa + 3 niveles complejidad | ✅ 100% |
| **Mejoras Streamlit** | 40% | UI moderna + Panel + Visualización | ✅ 100% |

### Características Destacadas

- **Arquitectura ReAct Completa**: Thought/Action/Observation loop
- **4 Herramientas Funcionales**: Todas integradas y testeadas
- **Memoria Dual Operativa**: Buffer + ChromaDB con embeddings
- **UI Profesional**: Panel lateral, métricas, visualización de razonamiento
- **Código Limpio**: Documentado, modular, siguiendo mejores prácticas
- **Logging Completo**: Trazabilidad de todas las decisiones
- **Tests Implementados**: Validación de funcionalidad
- **Documentación Exhaustiva**: README, diagramas, ejemplos

---

## Contacto y Soporte

**Pastelería 1000 Sabores**
- Email: contacto@1000sabores.cl
- Teléfono: +56 9 1234 5678
- Web: www.1000sabores.cl
- Horario: Lunes a Domingo, 8:00 - 20:00 hrs

**Soporte Técnico del Proyecto**
- Issues: GitHub Issues
- Docs: `/docs` directory
- Tests: `/tests` directory

---

## Licencia

Este proyecto es un trabajo académico desarrollado para evaluación en **Duoc UC**.  
Asignatura: Soluciones de Inteligencia Artificial  
Año: 2025

---

## Agradecimientos

- **LangChain** - Framework de agentes y orquestación
- **OpenAI** - Modelos de lenguaje GPT
- **Streamlit** - Plataforma de UI interactiva
- **ChromaDB** - Vector store para memoria de largo plazo
- **Sentence Transformers** - Embeddings multilíngües
- **Duoc UC** - Oportunidad académica y formación

---

## Roadmap Futuro

Posibles mejoras futuras:

- [ ] Integración con WhatsApp/Telegram
- [ ] Sistema de recomendaciones con ML
- [ ] Panel de administración para configuración
- [ ] A/B testing de prompts
- [ ] Analytics dashboard con Plotly
- [ ] Soporte multiidioma (inglés, francés)
- [ ] Integración con sistema de pagos
- [ ] API REST para terceros

---

**¡Gracias por usar nuestro Agente Inteligente!**

*Desarrollado con amor para Pastelería 1000 Sabores*  
*50 años endulzando vidas - Ahora con IA Avanzada*

---

**Versión**: 2.0.0 (Agente Inteligente)  
**Última actualización**: Octubre 2025  
**Autor**: Estudiante Duoc UC - Soluciones IA
