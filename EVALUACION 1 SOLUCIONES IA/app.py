import streamlit as st
import pandas as pd
from src.data_loader import PasteleriaDataLoader
from src.rag_engine import PasteleriaRAGEngine
from src.discount_calculator import DiscountCalculator
import os
from dotenv import load_dotenv

# Configuración inicial
load_dotenv()
st.set_page_config(
    page_title="Chatbot Pastelería 1000 Sabores", 
    page_icon="🍰", 
    layout="wide",
    initial_sidebar_state="expanded"
)

class PasteleriaChatbotApp:
    def __init__(self):
        self.data_loader = PasteleriaDataLoader()
        self.rag_engine = PasteleriaRAGEngine()
        self.discount_calculator = DiscountCalculator()
        self.inicializado = False
        
    def inicializar_sistema(self):
        """Inicializa todos los componentes del sistema"""
        try:
            # Cargar datos de la pastelería
            productos = self.data_loader.cargar_productos()
            politicas = self.data_loader.cargar_politicas()
            faqs = self.data_loader.cargar_faqs()
            
            # Combinar todos los documentos
            todos_documentos = productos + politicas + faqs
            
            # Inicializar motor RAG con los documentos
            self.rag_engine.cargar_documentos(todos_documentos)
            
            self.inicializado = True
            return True
        except Exception as e:
            st.error(f"❌ Error inicializando sistema: {str(e)}")
            return False

def main():
    st.title("🍰 Chatbot Pastelería 1000 Sabores")
    st.markdown("### ¡Bienvenido a nuestros 50 años de tradición dulce! 🎉")
    st.markdown("---")
    
    # Inicializar sistema
    if 'app' not in st.session_state:
        st.session_state.app = PasteleriaChatbotApp()
        st.session_state.messages = []
        st.session_state.inicializado = False
    
    # Sidebar con información de la pastelería
    with st.sidebar:
        st.info("🔧 **Modo:** Simulado Inteligente")
        st.success("✅ Sistema optimizado para evaluación")
        
        st.markdown("""
        **🎉 50 años de tradición**  
        **🏆 Récord Guinness 1995**  
        **📍 Chile**  
        **🎓 Convenio con Duoc UC**
        """)
        
        st.markdown("---")
        st.subheader("🎁 Promociones Activas")
        st.info(st.session_state.app.discount_calculator.explicar_descuentos())
        
        st.markdown("---")
        st.subheader("📦 Categorías")
        categorias = st.session_state.app.data_loader.obtener_categorias()
        for cat in categorias:
            st.write(f"• {cat}")
        
        st.markdown("---")
        st.subheader("⚙️ Configuración")
        top_k = st.slider("Documentos a recuperar:", 1, 5, 3)
    
    # Área principal del chat
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Historial de mensajes
        st.subheader("💬 Conversación")
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
                if message.get("documentos"):
                    with st.expander("📚 Fuentes utilizadas"):
                        for i, doc in enumerate(message["documentos"]):
                            st.write(f"**Fuente {i+1}:** {doc[:150]}...")
        
        # Input de consulta
        query = st.chat_input("Escribe tu pregunta sobre productos, descuentos o promociones...")
        
        if query:
            # Mostrar mensaje del usuario
            with st.chat_message("user"):
                st.write(query)
            
            # Procesar consulta
            if not st.session_state.inicializado:
                with st.spinner("🔄 Inicializando sistema..."):
                    st.session_state.inicializado = st.session_state.app.inicializar_sistema()
            
            if st.session_state.inicializado:
                with st.chat_message("assistant"):
                    with st.spinner("🔍 Buscando en nuestra pastelería..."):
                        respuesta, documentos, metricas = st.session_state.app.rag_engine.consultar(query, top_k)
                        
                        # Mostrar respuesta
                        st.write(respuesta)
                        
                        # Mostrar métricas
                        col_met1, col_met2, col_met3 = st.columns(3)
                        with col_met1:
                            st.metric("📊 Docs encontrados", metricas["documentos_encontrados"])
                        with col_met2:
                            st.metric("⭐ Relevancia", f"{metricas['score_promedio']:.2f}")
                        with col_met3:
                            st.metric("📏 Longitud", metricas["longitud_respuesta"])
                
                # Guardar en historial
                st.session_state.messages.append({
                    "role": "user", 
                    "content": query
                })
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": respuesta,
                    "documentos": documentos,
                    "metricas": metricas
                })
            else:
                st.error("❌ El sistema no pudo inicializarse correctamente")
    
    with col2:
        st.subheader("🔍 Consultas Rápidas")
        st.info("💡 Haz clic en cualquier ejemplo:")
        
        ejemplos = [
            "¿Qué tortas cuadradas tienen?",
            "Descuento para mayores de 50 años",
            "Productos veganos disponibles", 
            "¿Cómo personalizo una torta?",
            "Promoción FELICES50",
            "¿Tienen envíos a regiones?",
            "Tortas para cumpleaños estudiantiles",
            "Productos sin azúcar"
        ]
        
        for ejemplo in ejemplos:
            if st.button(f"• {ejemplo}", key=ejemplo, use_container_width=True):
                # Simular que el usuario escribió esto
                st.session_state.ejemplo_query = ejemplo
                st.rerun()
        
        st.markdown("---")
        st.subheader("📞 Contacto")
        st.write("📧 contacto@1000sabores.cl")
        st.write("📞 +56 9 1234 5678")
        st.write("🕒 Lunes a Domingo: 8:00 - 20:00 hrs")

if __name__ == "__main__":
    main()