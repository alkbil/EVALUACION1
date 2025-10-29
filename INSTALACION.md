# 🚀 Guía de Instalación y Ejecución Rápida

## ⚡ Inicio Rápido (5 minutos)

### Paso 1: Requisitos Previos
- ✅ Python 3.8 o superior instalado
- ✅ Conexión a Internet
- ✅ API Key de OpenAI ([Obtener aquí](https://platform.openai.com/api-keys))

### Paso 2: Instalación

```bash
# 1. Abrir PowerShell en la carpeta del proyecto
cd "C:\Users\Pc\Desktop\EVALUACION 1 SOLUCIONES IA"

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
.\venv\Scripts\activate

# 4. Actualizar pip
python -m pip install --upgrade pip

# 5. Instalar dependencias
pip install -r requirements.txt
```

⏱️ **Tiempo estimado**: 3-5 minutos (dependiendo de conexión)

### Paso 3: Configuración

```bash
# 1. Copiar template de configuración
copy .env.example .env

# 2. Abrir .env con notepad
notepad .env

# 3. Pegar tu API Key de OpenAI
# OPENAI_API_KEY=sk-tu-api-key-aqui
```

### Paso 4: Ejecutar Aplicación

```bash
# Ejecutar agente inteligente (RECOMENDADO)
streamlit run app_agent.py
```

🎉 **¡Listo!** La aplicación se abrirá en `http://localhost:8501`

---

## 🎮 Primer Uso

### 1. Pantalla de Bienvenida
Al abrir la aplicación verás:
- Campo para ingresar API Key de OpenAI
- Campo opcional para Customer ID
- Botón "🚀 Inicializar Sistema"

### 2. Inicialización
1. Pega tu API Key (sk-...)
2. (Opcional) Ingresa un Customer ID
3. Clic en "Inicializar Sistema"
4. Espera 5-10 segundos
5. Verás ✅ "Sistema inicializado"

### 3. Primera Consulta

Prueba con un ejemplo simple:

```
"¿Qué tortas de chocolate tienen?"
```

El agente:
- 🔍 Buscará en el catálogo
- 🤖 Mostrará su proceso de razonamiento
- ✅ Responderá con opciones disponibles

### 4. Explorar Funcionalidades

**Consultas Rápidas**: Usa los 8 botones de ejemplo en la parte inferior

**Ver Razonamiento**: Expande "🧠 Ver proceso de razonamiento del agente"

**Estadísticas**: Revisa el panel lateral

---

## 📋 Ejemplos de Consultas

### Nivel Básico
```
- "¿Qué productos veganos tienen?"
- "Muéstrame tortas cuadradas"
- "¿Tienen envíos a regiones?"
```

### Nivel Intermedio
```
- "¿Cuánto cuesta la torta TC001 para una persona de 55 años?"
- "Quiero una torta personalizada, ¿cómo funciona?"
- "¿Qué descuentos hay disponibles?"
```

### Nivel Avanzado
```
- "Necesito una torta vegana para 25 personas en una boda, tengo código FELICES50"
- "Soy estudiante de DUOC y cumplo años, ¿puedo obtener torta gratis?"
- "Dame opciones de tortas sin azúcar con descuento para mayores de 50 años"
```

---

## 🔧 Solución de Problemas Comunes

### ❌ Error: "Python no se reconoce..."
**Solución**: Instalar Python desde [python.org](https://python.org) y marcar "Add to PATH"

### ❌ Error: "pip no se reconoce..."
**Solución**:
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### ❌ Error al instalar dependencias
**Solución**:
```bash
# Instalar dependencias una por una
pip install streamlit
pip install langchain langchain-openai
pip install chromadb
pip install sentence-transformers
```

### ❌ "Module not found" al ejecutar
**Solución**: Verificar que el entorno virtual está activado
```bash
# Debe aparecer (venv) al inicio del prompt
(venv) PS C:\Users\...> 
```

### ❌ Error: "OpenAI API key not found"
**Solución**: 
1. Verificar que `.env` existe en la carpeta raíz
2. Abrir `.env` y verificar que contiene `OPENAI_API_KEY=sk-...`
3. Reiniciar la aplicación

### ❌ "ChromaDB connection failed"
**Solución**:
```bash
# Eliminar base de datos corrupta
rmdir /s data\chroma_db

# La app creará una nueva automáticamente
```

### ❌ Agente muy lento
**Solución**:
- Verificar conexión a Internet
- Revisar cuota de OpenAI
- Reducir `max_iterations` en código a 5

### ❌ Rate limit exceeded
**Solución**:
- Esperar 20-30 segundos entre consultas
- Verificar plan de OpenAI (free tier tiene límites estrictos)
- Considerar upgrade a plan pagado

---

## 📊 Verificar Instalación

### Test 1: Verificar Python
```bash
python --version
# Debe mostrar: Python 3.8.x o superior
```

### Test 2: Verificar pip
```bash
pip --version
# Debe mostrar versión de pip
```

### Test 3: Verificar dependencias instaladas
```bash
pip list
# Debe mostrar streamlit, langchain, chromadb, etc.
```

### Test 4: Ejecutar tests
```bash
python -m pytest tests/test_agent.py -v
# Debe mostrar tests pasando
```

---

## 🎯 Siguiente Paso: Personalización

Una vez que funcione, puedes:

1. **Cambiar modelo de OpenAI** (en `.env`):
```bash
OPENAI_MODEL=gpt-4  # Usar GPT-4 en lugar de 3.5
```

2. **Ajustar temperatura** (más creativo vs determinístico):
```bash
OPENAI_TEMPERATURE=0.7  # Más creativo (default 0.3)
```

3. **Cambiar tipo de memoria**:
```bash
SHORT_TERM_MEMORY_TYPE=summary  # Resumen vs buffer completo
```

---

## 📞 Soporte

Si sigues teniendo problemas:

1. **Revisar logs**: Carpeta `logs/agent_*.log`
2. **Verificar documentación**: `README_AGENT.md`
3. **Revisar arquitectura**: `docs/arquitectura.md`

---

## ✅ Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` creado con API Key
- [ ] Aplicación ejecutándose (`streamlit run app_agent.py`)
- [ ] Sistema inicializado correctamente
- [ ] Primera consulta exitosa

---

**🎉 ¡Felicitaciones! Tu agente inteligente está listo para usar.**

*¿Listo para endulzar vidas con IA? 🍰🤖*
