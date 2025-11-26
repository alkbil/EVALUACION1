"""
Aplicación Streamlit mejorada con Agente Inteligente
Incluye visualización de herramientas, memoria y proceso de razonamiento
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from pathlib import Path
import os
import json
from dotenv import load_dotenv
import time

# Importar componentes existentes
from src.data_loader import PasteleriaDataLoader
from src.discount_calculator import DiscountCalculator

# Importar componentes del agente
from src.agent import create_agent
from src.memory import create_short_term_memory, create_long_term_memory, ConversationContext
from src.utils import create_logger, create_tracker

# Configuración inicial
load_dotenv()
st.set_page_config(
    page_title="🤖 Agente Inteligente - Pastelería 1000 Sabores", 
    page_icon="🍰", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la UI y arreglar visibilidad del texto
st.markdown("""
<style>
    /* Arreglar visibilidad del texto en mensajes del chat */
    .stChatMessage {
        background-color: #f0f2f6 !important;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    
    .stChatMessage p, .stChatMessage div {
        color: #000000 !important;
    }
    
    /* Mensajes del usuario con fondo azul claro */
    [data-testid="stChatMessageContent"] {
        color: #000000 !important;
    }
    
    /* Asegurar que todo el texto sea visible */
    .stMarkdown, .stMarkdown p, .stMarkdown div {
        color: #262730 !important;
    }
    
    .tool-badge {
        display: inline-block;
        padding: 4px 8px;
        margin: 2px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    
    .tool-search { background-color: #e3f2fd; color: #1976d2; }
    .tool-discount { background-color: #e8f5e9; color: #388e3c; }
    .tool-inventory { background-color: #fff3e0; color: #f57c00; }
    .tool-history { background-color: #f3e5f5; color: #7b1fa2; }
    
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .thinking-animation {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)


# ============= FUNCIONES AUXILIARES PARA GUARDAR CONSULTAS =============

def save_query_to_history(query: str, customer_id: str = None):
    """Guarda una consulta en el historial"""
    queries_file = Path("./data/queries_history.json")
    queries_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Cargar historial existente
        if queries_file.exists():
            with open(queries_file, 'r', encoding='utf-8') as f:
                queries = json.load(f)
        else:
            queries = []
        
        # Agregar nueva consulta
        query_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "customer_id": customer_id or "anonymous"
        }
        queries.append(query_entry)
        
        # Guardar
        with open(queries_file, 'w', encoding='utf-8') as f:
            json.dump(queries, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"⚠️ Error guardando consulta: {e}")


class IntelligentPasteleriaApp:
    """
    Aplicación principal con agente inteligente integrado
    """
    
    def __init__(self):
        self.data_loader = PasteleriaDataLoader()
        self.discount_calculator = DiscountCalculator()
        self.agent = None
        self.short_term_memory = None
        self.long_term_memory = None
        self.conversation_context = ConversationContext()
        self.logger = None
        self.tracker = create_tracker()
        self.initialized = False
    
    def initialize_system(self, api_key: str):
        """Inicializa todos los componentes del sistema"""
        try:
            with st.spinner("🔄 Inicializando agente inteligente..."):
                # Inicializar logger
                self.logger = create_logger(console_output=False)
                self.logger.logger.info("=== INICIANDO SISTEMA DE AGENTE INTELIGENTE ===")
                
                # Detectar si es GitHub Token o OpenAI Key
                github_token = os.getenv("GITHUB_TOKEN")
                use_github = github_token and api_key == github_token
                
                if use_github:
                    st.write("🌟 Usando GitHub Models (GRATIS)")
                else:
                    st.write("🔑 Usando OpenAI API")
                
                # Inicializar memorias
                st.write("💾 Configurando sistema de memoria...")
                self.short_term_memory = create_short_term_memory(
                    memory_type="buffer",
                    openai_api_key=api_key
                )
                
                self.long_term_memory = create_long_term_memory(
                    persist_directory="./data/chroma_db"
                )
                
                # Inicializar agente
                st.write("🤖 Creando agente con herramientas...")
                self.agent = create_agent(
                    data_loader=self.data_loader,
                    discount_calculator=self.discount_calculator,
                    openai_api_key=api_key,
                    model_name="gpt-4o" if use_github else "gpt-3.5-turbo",
                    temperature=0.3,
                    max_iterations=10,
                    verbose=False
                )
                
                self.initialized = True
                st.success("✅ Sistema de agente inteligente inicializado correctamente")
                
                return True
                
        except Exception as e:
            st.error(f"❌ Error inicializando sistema: {str(e)}")
            self.logger.log_error(str(e)) if self.logger else None
            return False
    
    def process_query(self, query: str, customer_id: str = None):
        """Procesa una consulta usando el agente inteligente"""
        try:
            # Log de la consulta
            self.logger.log_query(query, customer_id or "anonymous")
            
            # Iniciar tracking
            self.tracker.start_execution(query)
            
            # Obtener contexto de memoria de corto plazo
            chat_history = self.short_term_memory.get_messages()
            
            # Ejecutar agente
            result = self.agent.execute(query, chat_history)
            
            # Guardar en memoria
            answer = result.get("answer", "")
            self.short_term_memory.add_message(query, answer)
            
            # Guardar en memoria de largo plazo
            metadata = {
                "customer_id": customer_id or "anonymous",
                "tools_used": result.get("tools_used", []),
                "execution_time": result.get("execution_time", 0)
            }
            self.long_term_memory.store_conversation(query, answer, metadata)
            
            # Completar tracking
            self.tracker.finish_execution(
                result=answer,
                error=None if result.get("success") else result.get("error")
            )
            
            # Log de respuesta
            self.logger.log_answer(answer)
            self.logger.log_execution_trace(result.get("execution_trace", []))
            
            return result
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            error_trace = traceback.format_exc()
            self.logger.log_error(f"{error_msg}\n{error_trace}")
            self.tracker.finish_execution(result="", error=error_msg)
            
            # Mostrar error detallado en desarrollo
            print("❌ ERROR DETALLADO:")
            print(error_trace)
            
            return {
                "success": False,
                "answer": f"❌ **Error técnico detectado:**\n\n```\n{error_msg}\n```\n\n💡 **Detalles**: Revisa la consola para más información.",
                "execution_trace": [],
                "tools_used": [],
                "error": error_msg,
                "error_trace": error_trace
            }


def render_sidebar(app: IntelligentPasteleriaApp):
    """Renderiza el sidebar con información del sistema"""
    with st.sidebar:
        st.title("🤖 Panel de Control")
        
        # Estado del sistema
        st.subheader("⚙️ Estado del Sistema")
        if app.initialized:
            st.success("✅ Agente activo")
            
            # Información de sesión
            if app.short_term_memory:
                session_info = app.short_term_memory.get_session_info()
                st.metric("💬 Mensajes en sesión", session_info["message_count"])
                st.metric("⏱️ Duración sesión", f"{session_info['duration_seconds']:.0f}s")
        else:
            st.warning("⏸️ Sistema no inicializado")
        
        st.markdown("---")
        
        # Herramientas disponibles
        st.subheader("🛠️ Herramientas Disponibles")
        
        tools_info = {
            "search_products": {"name": "Búsqueda de Productos", "icon": "🔍", "color": "#1976d2"},
            "calculate_discount": {"name": "Calcular Descuentos", "icon": "💰", "color": "#388e3c"},
            "check_inventory": {"name": "Verificar Inventario", "icon": "📦", "color": "#f57c00"},
            "customer_history": {"name": "Historial Cliente", "icon": "👤", "color": "#7b1fa2"}
        }
        
        for tool_id, info in tools_info.items():
            st.markdown(f"""
            <div style="padding: 8px; margin: 4px 0; background-color: {info['color']}20; 
                        border-left: 3px solid {info['color']}; border-radius: 4px;">
                <b>{info['icon']} {info['name']}</b>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Información de la pastelería
        st.subheader("🍰 Sobre Nosotros")
        st.info("""
        **🎉 50 años de tradición**  
        **🏆 Récord Guinness 1995**  
        **📍 Chile**  
        **🎓 Convenio con Duoc UC**
        """)
        
        st.markdown("---")
        
        # Promociones activas
        st.subheader("🎁 Promociones Activas")
        st.success("""
        **👴 Mayores 50 años:** 50% OFF  
        **🎓 Código FELICES50:** 10% OFF  
        **🎂 Estudiantes DUOC:** Torta GRATIS
        """)
        
        st.markdown("---")
        
        # Estadísticas
        if app.initialized and app.agent:
            st.subheader("📊 Estadísticas de Uso")
            stats = app.agent.get_execution_statistics()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Consultas", stats.get("total_queries", 0))
            with col2:
                st.metric("Éxito", f"{stats.get('success_rate', 0):.0f}%")
            
            if stats.get("most_used_tools"):
                st.write("**Herramientas más usadas:**")
                for tool, count in stats.get("most_used_tools", [])[:3]:
                    st.write(f"• {tool}: {count}x")
        
        st.markdown("---")
        
        # Botón de reinicio
        if st.button("🔄 Reiniciar Sesión", use_container_width=True):
            if app.short_term_memory:
                app.short_term_memory.clear()
            app.conversation_context.clear()
            st.session_state.messages = []
            st.rerun()


def render_thinking_process(execution_trace):
    """Renderiza el proceso de pensamiento del agente"""
    if not execution_trace:
        return
    
    with st.expander("🧠 Ver proceso de razonamiento del agente", expanded=False):
        for step in execution_trace:
            step_num = step.get("step", 0)
            thought = step.get("thought", "")
            tool = step.get("tool", "")
            observation = step.get("observation", "")
            
            st.markdown(f"### 📍 Paso {step_num}")
            
            if thought:
                st.markdown(f"**💭 Pensamiento:**")
                st.info(thought)
            
            if tool:
                tool_icons = {
                    "search_products": "🔍",
                    "calculate_discount": "💰",
                    "check_inventory": "📦",
                    "customer_history": "👤"
                }
                icon = tool_icons.get(tool, "🔧")
                st.markdown(f"**{icon} Acción:** `{tool}`")
            
            if observation:
                st.markdown(f"**👁️ Observación:**")
                st.success(observation)
            
            st.markdown("---")


def render_tools_used(tools_used):
    """Renderiza badges de herramientas usadas"""
    if not tools_used:
        return
    
    st.markdown("**🔧 Herramientas utilizadas:**")
    
    tool_styles = {
        "search_products": ("🔍 Búsqueda", "tool-search"),
        "calculate_discount": ("💰 Descuentos", "tool-discount"),
        "check_inventory": ("📦 Inventario", "tool-inventory"),
        "customer_history": ("👤 Historial", "tool-history")
    }
    
    badges_html = ""
    for tool in set(tools_used):  # Eliminar duplicados
        label, css_class = tool_styles.get(tool, (tool, "tool-badge"))
        badges_html += f'<span class="tool-badge {css_class}">{label}</span>'
    
    st.markdown(badges_html, unsafe_allow_html=True)


def render_metrics(result):
    """Renderiza métricas de ejecución"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "⏱️ Tiempo",
            f"{result.get('execution_time', 0):.2f}s"
        )
    
    with col2:
        st.metric(
            "🔄 Iteraciones",
            result.get('iterations', 0)
        )
    
    with col3:
        st.metric(
            "✅ Estado",
            "Éxito" if result.get('success') else "Error"
        )


def main():
    # Título principal
    st.title("🤖 Agente Inteligente - Pastelería 1000 Sabores")
    st.markdown("### Sistema avanzado con arquitectura ReAct y memoria conversacional")
    st.markdown("---")
    
    # Inicializar app en session state
    if 'app' not in st.session_state:
        st.session_state.app = IntelligentPasteleriaApp()
        st.session_state.messages = []
        st.session_state.customer_id = None
    
    app = st.session_state.app
    
    # Configuración inicial: API Key
    if not app.initialized:
        st.success("🎭 **MODO DEMO DISPONIBLE** - ¡Prueba el sistema sin consumir API!")
        
        # Botón de MODO DEMO destacado
        if st.button("🎭 INICIAR MODO DEMO (Sin límites, perfecto para presentaciones)", type="primary", use_container_width=True):
            st.session_state.customer_id = None
            app.initialize_system("DEMO_MODE")
            st.rerun()
        
        st.markdown("---")
        
        # Verificar si hay GitHub Token en .env
        github_token = os.getenv("GITHUB_TOKEN")
        
        if github_token:
            st.info("🌟 **GitHub Models detectado** - Modelos GPT-4 gratis (50 requests/día)")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if st.button("🌟 Usar GitHub Models", use_container_width=True):
                    st.session_state.customer_id = None
                    app.initialize_system(github_token)
                    st.rerun()
            
            with col2:
                st.markdown("**O usa tu API Key de OpenAI:**")
        else:
            st.info("💡 También puedes usar tu propia API Key de OpenAI")
        
        with st.form("api_key_form"):
            api_key = st.text_input(
                "🔑 OpenAI API Key",
                type="password",
                help="Tu API key de OpenAI (comienza con sk-...)"
            )
            
            customer_id = st.text_input(
                "👤 ID de Cliente (opcional)",
                placeholder="ej: cliente123",
                help="Para personalizar experiencia y recuperar historial"
            )
            
            submitted = st.form_submit_button("🚀 Inicializar con OpenAI")
            
            if submitted and api_key:
                st.session_state.customer_id = customer_id if customer_id else None
                app.initialize_system(api_key)
                st.rerun()
        
        # Mostrar información mientras no esté inicializado
        st.info("""
        ### 🎯 Características del Agente Inteligente:
        
        - **🧠 Arquitectura ReAct**: Razonamiento + Actuación
        - **🛠️ 4 Herramientas Especializadas**: Búsqueda, Descuentos, Inventario, Historial
        - **💾 Memoria Dual**: Corto plazo (sesión) y largo plazo (persistente)
        - **📊 Trazabilidad Completa**: Visualización de decisiones del agente
        - **⚡ Respuestas Inteligentes**: Adaptadas al contexto y preferencias
        
        ---
        
        ### 🎭 Modo DEMO:
        - ✅ Sin consumir API (perfecto para presentaciones)
        - ✅ Respuestas inteligentes simuladas
        - ✅ Todas las herramientas funcionan
        - ✅ Visualización completa del proceso ReAct
        - ✅ Sin límites de uso
        """)

        
        return
    
    # Renderizar sidebar
    render_sidebar(app)
    
    # Área principal de chat
    st.subheader("💬 Conversación con el Agente")
    
    # Mostrar historial de mensajes
    for idx, message in enumerate(st.session_state.messages):
        role = message["role"]
        content = message["content"]
        
        with st.chat_message(role):
            st.markdown(content)
            
            # Si es respuesta del asistente, mostrar información adicional
            if role == "assistant" and "result" in message:
                result = message["result"]
                
                # Herramientas usadas
                if result.get("tools_used"):
                    render_tools_used(result["tools_used"])
                
                # Métricas
                render_metrics(result)
                
                # Proceso de razonamiento
                if result.get("execution_trace"):
                    render_thinking_process(result["execution_trace"])
    
    # Input de consulta
    query = st.chat_input("💬 Escribe tu consulta... (ej: /error para simular error)")
    
    if query:
        # Verificar comandos especiales
        if query.strip().lower() == "/error":
            # Simular un error para testing - registrarlo en el logger
            st.session_state.messages.append({
                "role": "user",
                "content": query
            })
            
            with st.chat_message("user"):
                st.markdown(f"```\n{query}\n```")
            
            # Registrar el error en el sistema de logging
            error_msg = "ValueError: División por cero en cálculo de descuento"
            error_trace = """  File 'discount_calculator.py', line 142, in calculate
    percentage = amount / total_items  # Error aquí"""
            
            try:
                # Si hay logger, escribir en él
                if app.logger:
                    app.logger.logger.error(f"ERROR | {error_msg}\nTraceback:\n{error_trace}")
                
                # Mostrar en la UI
                with st.chat_message("assistant"):
                    st.error("❌ **ERROR SIMULADO PARA TESTING**")
                    st.markdown(f"""
                    **Detalles del error:**
                    - **Tipo**: ValueError
                    - **Módulo**: discount_calculator.py
                    - **Línea**: 142
                    - **Mensaje**: {error_msg}
                    
                    ```python
                    Traceback (most recent call last):
                      File "discount_calculator.py", line 142, in calculate
                        percentage = amount / total_items  # Error aquí
                    ValueError: {error_msg}
                    ```
                    
                    **✅ Este error ha sido registrado en los logs del sistema.**
                    **Actualiza el dashboard para ver el error reflejado.**
                    """)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"ERROR: {error_msg}"
                    })
            except Exception as e:
                st.error(f"Error al registrar el fallo: {e}")
            
            st.rerun()
        
        elif query.strip().lower() == "/help":
            # Mostrar comandos disponibles
            st.info("""
            **Comandos disponibles:**
            - `/error` - Simula un error para ver cómo se captura en el dashboard
            - `/help` - Muestra esta ayuda
            - `/reset` - Limpia el historial de mensajes
            """)
        
        elif query.strip().lower() == "/reset":
            # Limpiar historial
            st.session_state.messages = []
            st.success("✅ Historial limpiado")
            st.rerun()
        
        else:
            # Consulta normal
            # GUARDAR CONSULTA EN HISTORIAL
            save_query_to_history(query, st.session_state.customer_id)
            
            # Agregar mensaje del usuario
            st.session_state.messages.append({
                "role": "user",
                "content": query
            })
            
            # Mostrar mensaje del usuario
            with st.chat_message("user"):
                st.markdown(query)
            
            # Procesar con el agente
            with st.chat_message("assistant"):
                with st.status("🤖 Agente pensando...", expanded=True) as status:
                    st.write("🔄 Analizando consulta...")
                    time.sleep(0.5)
                    
                    st.write("🛠️ Seleccionando herramientas...")
                    time.sleep(0.5)
                    
                    st.write("💭 Razonando y ejecutando...")
                    
                    # Ejecutar agente
                    result = app.process_query(
                        query,
                        customer_id=st.session_state.customer_id
                    )
                    
                    status.update(label="✅ Respuesta generada", state="complete")
                
                # Mostrar respuesta
                answer = result.get("answer", "")
                st.markdown(answer)
                
                # Herramientas usadas
                if result.get("tools_used"):
                    render_tools_used(result["tools_used"])
                
                # Métricas
                render_metrics(result)
                
                # Proceso de razonamiento
                if result.get("execution_trace"):
                    render_thinking_process(result["execution_trace"])
            
            # Agregar respuesta al historial
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "result": result
            })
            
            st.rerun()
    
    # Sección de consultas rápidas
    st.markdown("---")
    st.subheader("💡 Consultas Rápidas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    ejemplos = [
        ("🔍 Ver productos", "Muéstrame todas las tortas de chocolate disponibles"),
        ("💰 Calcular precio", "¿Cuánto cuesta una torta vegana para 15 personas?"),
        ("🎁 Ver descuentos", "Tengo 55 años, ¿qué descuentos aplican para mí?"),
        ("📦 Verificar stock", "¿Tienen disponible la torta cuadrada de frutas?"),
        ("🌱 Opciones veganas", "Quiero ver todos los productos veganos"),
        ("💝 Cumpleaños DUOC", "Soy estudiante DUOC, ¿puedo obtener torta gratis?"),
        ("🎂 Para evento", "Necesito una torta para 30 personas en una boda"),
        ("❓ Personalización", "¿Puedo personalizar las tortas con mensajes?")
    ]
    
    for idx, (titulo, ejemplo) in enumerate(ejemplos):
        col = [col1, col2, col3, col4][idx % 4]
        with col:
            if st.button(titulo, key=f"ejemplo_{idx}", use_container_width=True):
                st.session_state.ejemplo_seleccionado = ejemplo
                st.rerun()
    
    # Si hay ejemplo seleccionado, procesarlo
    if 'ejemplo_seleccionado' in st.session_state:
        query = st.session_state.ejemplo_seleccionado
        del st.session_state.ejemplo_seleccionado
        
        # Agregar y procesar
        st.session_state.messages.append({"role": "user", "content": query})
        
        result = app.process_query(query, st.session_state.customer_id)
        answer = result.get("answer", "")
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "result": result
        })
        
        st.rerun()


if __name__ == "__main__":
    main()
