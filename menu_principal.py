"""
Menú de Inicio - Selector de Aplicaciones EP3
Permite elegir entre Dashboard, Chatbot e Informe
"""

import streamlit as st
from datetime import datetime
import webbrowser
import subprocess
import sys
import time
import threading
import socket

st.set_page_config(
    page_title="EP3 - Menú Principal",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Menú Principal EP3")
st.markdown("**Agente Inteligente Pastelería 1000 Sabores**")
st.markdown("---")

st.markdown("""
### Bienvenido al sistema completo de observabilidad

Elige una opción para comenzar:
""")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 🤖 Chatbot")
        st.markdown("""
        Interactúa con el Agente Inteligente
        
        **Características:**
        - Búsqueda de productos
        - Cálculo de descuentos
        - Consultas de inventario
        - Histórico de clientes
        """)
        
        if st.button("Abrir Chatbot", key="btn_chatbot", use_container_width=True):
            def open_chatbot():
                try:
                    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app_agent.py", "--server.port", "8502", "--logger.level=error"])
                    for i in range(30):
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            result = sock.connect_ex(('localhost', 8502))
                            sock.close()
                            if result == 0:
                                time.sleep(2)
                                webbrowser.open("http://localhost:8502")
                                return
                        except:
                            pass
                        time.sleep(0.5)
                    st.error("El chatbot no se pudo inicializar en tiempo")
                except Exception as e:
                    st.error(f"Error: {e}")
            
            thread = threading.Thread(target=open_chatbot, daemon=True)
            thread.start()
            st.success("🤖 Abriendo Chatbot... (espera unos segundos)")

with col2:
    with st.container(border=True):
        st.markdown("### 📊 Dashboard")
        st.markdown("""
        Monitoreo en tiempo real
        
        **Características:**
        - Métricas de precisión
        - Análisis de logs
        - Detección de anomalías
        - Protocolos de seguridad
        """)
        
        if st.button("Abrir Dashboard", key="btn_dashboard", use_container_width=True):
            def open_dashboard():
                try:
                    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "dashboard.py", "--server.port", "8503", "--logger.level=error"])
                    for i in range(30):
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            result = sock.connect_ex(('localhost', 8503))
                            sock.close()
                            if result == 0:
                                time.sleep(2)
                                webbrowser.open("http://localhost:8503")
                                return
                        except:
                            pass
                        time.sleep(0.5)
                    st.error("El dashboard no se pudo inicializar en tiempo")
                except Exception as e:
                    st.error(f"Error: {e}")
            
            thread = threading.Thread(target=open_dashboard, daemon=True)
            thread.start()
            st.success("📊 Abriendo Dashboard... (espera unos segundos)")

with col3:
    with st.container(border=True):
        st.markdown("### 📋 Informe")
        st.markdown("""
        Documentación técnica completa
        
        **Características:**
        - Resumen ejecutivo
        - Evaluación por indicador
        - Implementación técnica
        - Conclusiones
        """)
        
        if st.button("Ver Informe", key="btn_informe", use_container_width=True):
            def open_informe():
                try:
                    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "informe.py", "--server.port", "8504", "--logger.level=error"])
                    for i in range(30):
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            result = sock.connect_ex(('localhost', 8504))
                            sock.close()
                            if result == 0:
                                time.sleep(2)
                                webbrowser.open("http://localhost:8504")
                                return
                        except:
                            pass
                        time.sleep(0.5)
                    st.error("El informe no se pudo inicializar en tiempo")
                except Exception as e:
                    st.error(f"Error: {e}")
            
            thread = threading.Thread(target=open_informe, daemon=True)
            thread.start()
            st.success("📋 Abriendo Informe... (espera unos segundos)")

st.markdown("---")

# Estadísticas rápidas
st.markdown("### 📈 Estado del Sistema")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Status", "🟢 Activo", help="Sistema operativo")

with col2:
    st.metric("Hora", datetime.now().strftime("%H:%M:%S"), help="Hora del servidor")

with col3:
    st.metric("Versión", "1.0", help="Versión del sistema")

st.markdown("---")

st.info("""
💡 **Nota:** Cada aplicación se abre en una pestaña separada con su propio puerto:
- **Menú**: Puerto 8501
- **Chatbot**: Puerto 8502
- **Dashboard**: Puerto 8503
- **Informe**: Puerto 8504
""")

st.markdown("""
---
**EP3 - Sistema de Observabilidad y Monitoreo**  
Proyecto: Agente Inteligente Pastelería 1000 Sabores  
Evaluación: DUOC UC - ISY0101
""")
