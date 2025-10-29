# 🍰 Chatbot Pastelería 1000 Sabores

## 📋 Descripción del Proyecto
Sistema de chatbot inteligente para Pastelería 1000 Sabores implementado con arquitectura RAG (Retrieval-Augmented Generation) que permite responder consultas de clientes sobre productos, promociones y servicios de la pastelería.

## 🎯 Objetivos
- Automatizar atención al cliente para consultas frecuentes
- Proporcionar información precisa sobre productos y promociones  
- Reducir tiempos de respuesta de 24h a menos de 1 minuto
- Mantener 100% de trazabilidad en las respuestas

## 📁 Estructura del Proyecto
EVALUACION 1 SOLUCIONES IA/
├── app.py # Aplicación principal Streamlit
├── src/ # Módulos de código fuente
│ ├── data_loader.py # Cargador de datos de la pastelería
│ ├── rag_engine.py # Motor RAG principal
│ ├── discount_calculator.py # Calculadora de descuentos
│ ├── prompt_manager.py # Gestión de prompts optimizados
│ └── evaluation.py # Sistema de evaluación de respuestas
├── data/ # Datos de la pastelería
│ └── productos.json # Catálogo y políticas
├── requirements.txt # Dependencias del proyecto
├── .env.example # Template de variables de entorno
└── README.md # Este archivo

## 🚀 Instalación y Ejecución

### 1. Clonar o descargar el proyecto
```bash
# Descargar todos los archivos en la carpeta "EVALUACION 1 SOLUCIONES IA"

pip install -r requirements.txt

# Copiar el archivo de ejemplo
cp .env.example .env

### **2. Agregar sección "Uso" con ejemplos:**
```markdown
## 💡 Uso del Sistema

### Ejemplos de consultas:
- "¿Qué tortas cuadradas tienen?"
- "Descuento para mayores de 50 años"
- "Productos veganos disponibles"
- "¿Cómo personalizo una torta?"
- "Promoción FELICES50"

## 🔧 Tecnologías Utilizadas

- **Streamlit**: Interfaz de usuario web
- **Python 3.8+**: Lenguaje de programación
- **Scikit-learn**: Cálculo de similitudes vectoriales
- **LangChain**: Framework para aplicaciones con LLM

# 🍰 Chatbot Pastelería 1000 Sabores

## 📋 Descripción del Proyecto
Sistema de chatbot inteligente para Pastelería 1000 Sabores implementado con arquitectura RAG (Retrieval-Augmented Generation) que permite responder consultas de clientes sobre productos, promociones y servicios de la pastelería.

## 🎯 Objetivos
- Automatizar atención al cliente para consultas frecuentes
- Proporcionar información precisa sobre productos y promociones  
- Reducir tiempos de respuesta de 24h a menos de 1 minuto
- Mantener 100% de trazabilidad en las respuestas

## 🏗️ Arquitectura del Sistema

Sistema RAG Completo:
Consulta → Embeddings → Búsqueda Semántica → Contexto → Generación → Respuesta → Evaluación