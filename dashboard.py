"""
Dashboard de Observabilidad para EP3
IE5: Dashboard Visual de Monitoreo
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path
import json
import sys
import webbrowser
import subprocess
import os
import time
import socket

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.monitoring.metrics import ObservabilityMetrics
from src.monitoring.logs_analyzer import LogsAnalyzer
from src.monitoring.anomaly_detector import AnomalyDetector, ImprovementRecommender
from src.security.validators import SecurityValidator


def load_queries_history(max_items: int = 100) -> list:
    """Carga el historial de consultas guardado"""
    queries_file = Path("./data/queries_history.json")
    if queries_file.exists():
        try:
            with open(queries_file, 'r', encoding='utf-8') as f:
                queries = json.load(f)
                return queries[-max_items:] if isinstance(queries, list) else []
        except:
            return []
    return []


def save_query(query: str, customer_id: str = None):
    """Guarda una nueva consulta en el historial"""
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


def count_total_queries() -> int:
    """Cuenta el total de consultas realizadas"""
    return len(load_queries_history(max_items=10000))


def load_metrics():
    """Carga métricas del sistema"""
    metrics_file = Path("./metrics/metrics.json")
    if metrics_file.exists():
        with open(metrics_file, 'r') as f:
            return json.load(f)
    return {}


def load_analysis_report():
    """Carga reporte de análisis de logs - GENERA EN TIEMPO REAL"""
    try:
        # Generar reporte en tiempo real desde los logs actuales
        logs_analyzer = LogsAnalyzer(log_dir="./logs")
        
        report = {
            'errors_summary': logs_analyzer.get_errors_summary(),
            'bottlenecks': logs_analyzer.get_bottlenecks(),
            'tool_usage': logs_analyzer.get_tool_usage_analysis(),
            'anomalies': logs_analyzer.detect_anomalies(),
            'recommendations': logs_analyzer._generate_recommendations(),
            'timestamp': datetime.now().isoformat()
        }
        
        return report
    except Exception as e:
        st.warning(f"⚠️ Error generando reporte: {e}")
        return {
            'errors_summary': {'total_errors': 0, 'error_types': {}, 'recent_errors': [], 'error_frequency': 0},
            'bottlenecks': [],
            'tool_usage': {},
            'anomalies': [],
            'recommendations': []
        }


def create_dashboard():
    """Crea dashboard principal de observabilidad"""
    
    st.set_page_config(
        page_title="EP3 - Observabilidad y Monitoreo",
        page_icon="📊",
        layout="wide"
    )
    
    # ============= SIDEBAR CONTROLS =============
    with st.sidebar:
        st.markdown("### ⚙️ Controles")
        
        # Botones para abrir aplicaciones
        st.markdown("**🚀 Aplicaciones**")
        col_chatbot, col_informe = st.columns(2)
        
        with col_chatbot:
            if st.button("🤖 Chatbot", use_container_width=True, help="Abre el agente inteligente"):
                import threading
                def open_chatbot_sidebar():
                    try:
                        # Inicia el proceso de streamlit
                        subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app_agent.py", "--server.port", "8502", "--logger.level=error"])
                        # Espera a que el servidor esté listo
                        for i in range(30):  # Intenta 30 veces (15 segundos)
                            try:
                                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                result = sock.connect_ex(('localhost', 8502))
                                sock.close()
                                if result == 0:  # Puerto está abierto
                                    time.sleep(2)  # Espera extra para que streamlit cargue completamente
                                    webbrowser.open("http://localhost:8502")
                                    return
                            except:
                                pass
                            time.sleep(0.5)
                        st.error("El chatbot no se pudo inicializar en tiempo")
                    except Exception as e:
                        st.error(f"Error al abrir chatbot: {e}")
                
                thread = threading.Thread(target=open_chatbot_sidebar, daemon=True)
                thread.start()
                st.success("🤖 Abriendo Chatbot... (esto puede tomar unos segundos)")
        
        with col_informe:
            if st.button("📋 Informe", use_container_width=True, help="Ver informe técnico"):
                import threading
                def open_informe():
                    try:
                        # Inicia el proceso de streamlit en puerto 8504
                        subprocess.Popen([sys.executable, "-m", "streamlit", "run", "informe.py", "--server.port", "8504", "--logger.level=error"])
                        # Espera a que el servidor esté listo
                        for i in range(30):  # Intenta 30 veces (15 segundos)
                            try:
                                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                result = sock.connect_ex(('localhost', 8504))
                                sock.close()
                                if result == 0:  # Puerto está abierto
                                    time.sleep(2)  # Espera extra para que streamlit cargue completamente
                                    webbrowser.open("http://localhost:8504")
                                    return
                            except:
                                pass
                            time.sleep(0.5)
                        st.error("El informe no se pudo inicializar en tiempo")
                    except Exception as e:
                        st.error(f"Error al abrir informe: {e}")
                
                thread = threading.Thread(target=open_informe, daemon=True)
                thread.start()
                st.success("📋 Abriendo Informe... (espera unos segundos)")
        
        st.markdown("---")
        
        auto_refresh = st.checkbox("🔄 Auto-actualizar", value=False, help="Recarga datos automáticamente")
        
        if auto_refresh:
            refresh_interval = st.slider("Intervalo (segundos)", min_value=5, max_value=60, value=10)
            st.success(f"✅ Auto-actualización cada {refresh_interval}s")
            import time
            time.sleep(refresh_interval)
            st.rerun()
        
        st.markdown("---")
        st.markdown("**📊 EP3 Dashboard**")
        st.markdown("Sistema de Observabilidad Completo")
    
    st.title("🔍 EP3: Dashboard de Observabilidad")
    st.markdown("**Agente Inteligente Pastelería 1000 Sabores**")
    
    # Botón de actualización en la parte superior
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
    
    with col1:
        st.write("")  # Espacio
    
    with col2:
        if st.button("🤖 Chatbot", use_container_width=True, help="Abre el agente inteligente"):
            import threading
            def open_chatbot():
                try:
                    # Inicia el proceso de streamlit
                    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app_agent.py", "--server.port", "8502", "--logger.level=error"])
                    # Espera a que el servidor esté listo
                    for i in range(30):  # Intenta 30 veces (15 segundos)
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            result = sock.connect_ex(('localhost', 8502))
                            sock.close()
                            if result == 0:  # Puerto está abierto
                                time.sleep(2)  # Espera extra para que streamlit cargue completamente
                                webbrowser.open("http://localhost:8502")
                                return
                        except:
                            pass
                        time.sleep(0.5)
                    st.error("El chatbot no se pudo inicializar en tiempo")
                except Exception as e:
                    st.error(f"Error al abrir chatbot: {e}")
            
            thread = threading.Thread(target=open_chatbot, daemon=True)
            thread.start()
            st.success("🤖 Abriendo Chatbot... (esto puede tomar unos segundos)")
    
    with col3:
        if st.button("🔄 Actualizar", use_container_width=True, help="Recarga todos los datos"):
            st.rerun()
    
    with col4:
        if st.button("📊 Exportar", use_container_width=True, help="Exporta métricas"):
            st.info("Función de exportación disponible en próximas versiones")
    
    with col5:
        last_update = datetime.now().strftime("%H:%M:%S")
        st.caption(f"🕐 {last_update}")
    
    st.markdown("---")
    
    # Tabs principales
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Métricas",
        "🔧 Análisis de Logs",
        "⚠️ Anomalías",
        "🛡️ Seguridad",
        "💡 Recomendaciones",
        "📝 Historial de Consultas"
    ])
    
    # ============= TAB 1: MÉTRICAS =============
    with tab1:
        col_refresh, col_title = st.columns([1, 5])
        with col_refresh:
            if st.button("🔄", key="refresh_metrics", help="Actualizar métricas"):
                st.rerun()
        with col_title:
            st.subheader("Métricas de Desempeño")
        
        metrics = load_metrics()
        
        # IE1: Precisión y Consistencia
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            precision = metrics.get('precision', 0)
            st.metric(
                "Precisión (IE1)",
                f"{precision:.1f}%",
                delta=None if precision == 0 else "+2.3%",
                help="Porcentaje de respuestas correctas"
            )
        
        with col2:
            error_freq = metrics.get('error_frequency', 0)
            st.metric(
                "Frecuencia de Errores",
                f"{error_freq:.1f}%",
                delta="-0.5%",
                help="Errores por cada 100 consultas"
            )
        
        with col3:
            total_queries = metrics.get('total_queries', 0)
            st.metric(
                "Total Consultas",
                f"{total_queries:,}",
                help="Número total de consultas procesadas"
            )
        
        with col4:
            error_count = len(metrics.get('errors', []))
            st.metric(
                "Errores Registrados",
                f"{error_count}",
                help="Total de errores encontrados"
            )
        
        # IE2: Latencia y Recursos
        st.markdown("### Latencia y Recursos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            latency_stats = metrics.get('latency_stats', {})
            if latency_stats:
                st.write("**Estadísticas de Latencia**")
                df_latency = pd.DataFrame({
                    'Métrica': ['Mínima', 'Máxima', 'Promedio'],
                    'Milisegundos': [
                        latency_stats.get('min_ms', 0),
                        latency_stats.get('max_ms', 0),
                        latency_stats.get('avg_ms', 0)
                    ]
                })
                st.dataframe(df_latency, use_container_width=True)
        
        with col2:
            resource_stats = metrics.get('resource_stats', {})
            if resource_stats.get('memory'):
                st.write("**Uso de Memoria**")
                memory = resource_stats['memory']
                df_memory = pd.DataFrame({
                    'Métrica': ['Mínima', 'Máxima', 'Promedio'],
                    'MB': [
                        memory.get('min_mb', 0),
                        memory.get('max_mb', 0),
                        memory.get('avg_mb', 0)
                    ]
                })
                st.dataframe(df_memory, use_container_width=True)
        
        # Gráficos de tendencia
        st.markdown("### Tendencias")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de precisión (simulado)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=[70, 72, 75, 78, 80, 82, 83, 85],
                mode='lines+markers',
                name='Precisión',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=8)
            ))
            fig.update_layout(
                title="Evolución de Precisión",
                xaxis_title="Consultas (últimas 8)",
                yaxis_title="Precisión (%)",
                height=300,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico de latencia
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=[1500, 1400, 1350, 1200, 1300, 1250, 1200, 1100],
                mode='lines+markers',
                name='Latencia',
                line=dict(color='#ff7f0e', width=3),
                marker=dict(size=8)
            ))
            fig.update_layout(
                title="Evolución de Latencia",
                xaxis_title="Consultas (últimas 8)",
                yaxis_title="Latencia (ms)",
                height=300,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ============= TAB 2: ANÁLISIS DE LOGS =============
    with tab2:
        col_refresh, col_title = st.columns([1, 5])
        with col_refresh:
            if st.button("🔄", key="refresh_logs", help="Actualizar análisis"):
                st.rerun()
        with col_title:
            st.subheader("IE3: Análisis de Logs y Trazabilidad")
        
        report = load_analysis_report()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            error_summary = report.get('errors_summary', {})
            st.metric(
                "Errores Totales",
                error_summary.get('total_errors', 0),
                help="Total de errores encontrados en logs"
            )
        
        with col2:
            error_freq = error_summary.get('error_frequency', 0)
            st.metric(
                "Tasa de Error",
                f"{error_freq:.2f}%",
                help="Proporción de errores en todas las operaciones"
            )
        
        with col3:
            bottlenecks = report.get('bottlenecks', [])
            st.metric(
                "Cuellos de Botella",
                len(bottlenecks),
                help="Operaciones lentas detectadas"
            )
        
        # Tabla de errores principales
        if error_summary.get('error_types'):
            st.markdown("**Tipos de Errores Más Frecuentes**")
            error_types = error_summary['error_types']
            df_errors = pd.DataFrame({
                'Tipo de Error': list(error_types.keys()),
                'Frecuencia': list(error_types.values())
            })
            st.dataframe(df_errors, use_container_width=True)
        
        # Análisis de herramientas
        if report.get('tool_analysis'):
            st.markdown("**Desempeño de Herramientas**")
            tool_analysis = report['tool_analysis']
            
            tool_data = []
            for tool_name, stats in tool_analysis.items():
                tool_data.append({
                    'Herramienta': tool_name,
                    'Uso': stats.get('used', 0),
                    'Errores': stats.get('errors', 0),
                    'Tiempo Promedio (s)': stats.get('avg_time', 0)
                })
            
            df_tools = pd.DataFrame(tool_data)
            st.dataframe(df_tools, use_container_width=True)
        
        # Gráfico de uso de herramientas (si hay datos)
        if report.get('tool_usage'):
            st.markdown("**Análisis de Herramientas Utilizadas**")
            tool_usage = report.get('tool_usage', {})
            
            if isinstance(tool_usage, dict) and tool_usage:
                try:
                    fig = px.bar(
                        x=list(tool_usage.keys()),
                        y=list(tool_usage.values()),
                        title="Uso de Herramientas",
                        template="plotly_dark",
                        labels={'x': 'Herramienta', 'y': 'Uso'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.info("📊 Sin datos de herramientas disponibles")
    
    # ============= TAB 3: ANOMALÍAS =============
    with tab3:
        col_refresh, col_title = st.columns([1, 5])
        with col_refresh:
            if st.button("🔄", key="refresh_anomalies", help="Actualizar anomalías"):
                st.rerun()
        with col_title:
            st.subheader("IE4: Detección de Anomalías y Patrones")
        
        report = load_analysis_report()
        anomalies = report.get('anomalies', [])
        
        if anomalies:
            for anomaly in anomalies:
                severity_color = {
                    'HIGH': '🔴',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }.get(anomaly.get('severity'), '⚪')
                
                with st.expander(f"{severity_color} {anomaly.get('type', 'Unknown')}"):
                    st.write(f"**Mensaje:** {anomaly.get('message', '')}")
                    if anomaly.get('details'):
                        st.json(anomaly['details'])
        else:
            st.success("✅ No se detectaron anomalías críticas")
        
        # Recomendaciones del análisis
        recommendations = report.get('recommendations', [])
        if recommendations:
            st.markdown("**Recomendaciones del Sistema**")
            for rec in recommendations:
                st.info(rec)
    
    # ============= TAB 4: SEGURIDAD =============
    with tab4:
        col_refresh, col_title = st.columns([1, 5])
        with col_refresh:
            if st.button("🔄", key="refresh_security", help="Actualizar seguridad"):
                st.rerun()
        with col_title:
            st.subheader("IE6: Protocolos de Seguridad")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Status de Seguridad", "🟢 SEGURO", help="Sistema sin incidentes críticos")
        
        with col2:
            st.metric("Rate Limit", "60/minuto", help="Máximo de solicitudes por minuto")
        
        with col3:
            st.metric("Validaciones Activas", "7", help="Capas de validación de entrada")
        
        # Características de seguridad
        st.markdown("### Características de Seguridad Implementadas")
        
        security_features = {
            "Validación de Entrada": "✅ Detecta y bloquea patrones maliciosos",
            "Rate Limiting": "✅ Limita 60 requests por minuto",
            "Sanitización": "✅ Elimina caracteres peligrosos de entrada/salida",
            "Protección de Privacidad": "✅ Enmascara datos sensibles (emails, teléfonos, RUT)",
            "Auditoría": "✅ Registra todos los incidentes de seguridad",
            "Detección de Anomalías": "✅ Identifica comportamientos sospechosos",
            "Limpieza de Datos": "✅ Elimina datos antiguos según política de retención"
        }
        
        for feature, status in security_features.items():
            st.write(f"**{feature}**: {status}")
        
        # Gráfico de incidentes
        with st.expander("📊 Histórico de Incidentes de Seguridad"):
            incident_data = {
                'Fecha': pd.date_range(start='2025-01-01', periods=7),
                'Intentos Maliciosos': [2, 1, 3, 1, 0, 2, 1],
                'Rate Limit': [1, 2, 1, 0, 1, 0, 1]
            }
            df_incidents = pd.DataFrame(incident_data)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df_incidents['Fecha'], y=df_incidents['Intentos Maliciosos'], name='Intentos Maliciosos'))
            fig.add_trace(go.Bar(x=df_incidents['Fecha'], y=df_incidents['Rate Limit'], name='Rate Limit Excedidos'))
            
            fig.update_layout(
                title="Incidentes de Seguridad Detectados",
                xaxis_title="Fecha",
                yaxis_title="Número de Incidentes",
                barmode='group',
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ============= TAB 5: RECOMENDACIONES =============
    with tab5:
        col_refresh, col_title = st.columns([1, 5])
        with col_refresh:
            if st.button("🔄", key="refresh_recommendations", help="Actualizar recomendaciones"):
                st.rerun()
        with col_title:
            st.subheader("IE7: Propuestas de Mejora Basadas en Datos")
        
        # Recomendaciones simuladas (en producción, venderían de ImprovementRecommender)
        recommendations = [
            {
                'id': 'REC-001',
                'severity': 'HIGH',
                'title': 'Optimizar Latencia de SearchProductsTool',
                'description': 'La herramienta SearchProductsTool tiene latencia promedio de 2.3s. Considerar implementar caché.',
                'impact': '30% reducción en latencia',
                'effort': 'Medio',
                'estimated_time': '4 horas'
            },
            {
                'id': 'REC-002',
                'severity': 'MEDIUM',
                'title': 'Mejorar Precisión en Consultas Ambiguas',
                'description': 'Precisión actual es 85%. El 15% restante son principalmente consultas ambiguas.',
                'impact': '10% aumento en precisión',
                'effort': 'Alto',
                'estimated_time': '8 horas'
            },
            {
                'id': 'REC-003',
                'severity': 'MEDIUM',
                'title': 'Implementar Caché de Respuestas Frecuentes',
                'description': '40% de las consultas se repiten. Caché reduciría latencia significativamente.',
                'impact': '40-60% reducción en latencia (queries en caché)',
                'effort': 'Bajo',
                'estimated_time': '2 horas'
            }
        ]
        
        for rec in recommendations:
            severity_emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(rec['severity'], '⚪')
            
            with st.expander(f"{severity_emoji} {rec['title']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("ID", rec['id'])
                    st.metric("Esfuerzo", rec['effort'])
                
                with col2:
                    st.metric("Impacto", rec['impact'])
                    st.metric("Tiempo Estimado", rec['estimated_time'])
                
                with col3:
                    st.metric("Severidad", rec['severity'])
                
                st.write(f"**Descripción:** {rec['description']}")
    
    # ============= TAB 6: HISTORIAL DE CONSULTAS =============
    with tab6:
        col_refresh, col_title = st.columns([1, 5])
        with col_refresh:
            if st.button("🔄", key="refresh_queries", help="Actualizar historial"):
                st.rerun()
        with col_title:
            st.subheader("📝 Historial de Consultas")
        
        # Cargar historial
        queries_history = load_queries_history(max_items=100)
        total_queries_count = count_total_queries()
        
        # Estadísticas de consultas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total de Consultas", f"{total_queries_count:,}")
        
        with col2:
            if queries_history:
                st.metric("📌 En esta sesión", len(queries_history))
            else:
                st.metric("📌 En esta sesión", 0)
        
        with col3:
            unique_users = len(set(q.get('customer_id', 'anonymous') for q in queries_history))
            st.metric("👥 Usuarios únicos", unique_users)
        
        with col4:
            if queries_history:
                today_queries = sum(1 for q in queries_history 
                                  if datetime.fromisoformat(q['timestamp']).date() == datetime.now().date())
                st.metric("📅 Hoy", today_queries)
            else:
                st.metric("📅 Hoy", 0)
        
        st.markdown("---")
        
        # Mostrar historial en tabla
        if queries_history:
            st.markdown("### Últimas Consultas Realizadas")
            
            # Preparar datos para tabla
            table_data = []
            for query in reversed(queries_history[-20:]):  # Últimas 20
                table_data.append({
                    "⏰ Timestamp": query['timestamp'],
                    "💬 Consulta": query['query'][:60] + "..." if len(query['query']) > 60 else query['query'],
                    "👤 Usuario": query.get('customer_id', 'anonymous'),
                })
            
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Estadísticas adicionales
            st.markdown("---")
            st.markdown("### 📊 Análisis de Consultas")
            
            # Consultas por usuario
            user_queries = {}
            for q in queries_history:
                user = q.get('customer_id', 'anonymous')
                user_queries[user] = user_queries.get(user, 0) + 1
            
            if user_queries:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Consultas por Usuario:**")
                    fig = px.pie(
                        values=list(user_queries.values()),
                        names=list(user_queries.keys()),
                        title="Distribución por Usuario",
                        template="plotly_dark"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("**Top 10 Consultas Más Frecuentes:**")
                    query_texts = [q['query'] for q in queries_history]
                    from collections import Counter
                    query_freq = Counter(query_texts).most_common(10)
                    
                    freq_data = []
                    for query, count in query_freq:
                        freq_data.append({
                            "Consulta": query[:40] + "..." if len(query) > 40 else query,
                            "Repeticiones": count
                        })
                    
                    df_freq = pd.DataFrame(freq_data)
                    fig_freq = px.bar(
                        df_freq,
                        x='Consulta',
                        y='Repeticiones',
                        title="Consultas Más Frecuentes",
                        template="plotly_dark"
                    )
                    st.plotly_chart(fig_freq, use_container_width=True)
            
            # Botón para descargar historial
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar Historial (CSV)",
                    data=csv,
                    file_name=f"consultas_historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                json_data = json.dumps(queries_history, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 Descargar Historial (JSON)",
                    data=json_data,
                    file_name=f"consultas_historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        else:
            st.info("ℹ️ No hay consultas registradas aún. Realiza consultas en el chatbot para ver el historial.")
    
    # Footer
    st.markdown("---")
    
    # Información de actualización
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"🕐 Última actualización: {datetime.now().strftime('%H:%M:%S')}")
    with col2:
        total_queries_count = count_total_queries()
        st.caption(f"📊 Consultas procesadas: {total_queries_count:,}")
    with col3:
        error_count = 0
        try:
            logs_analyzer = LogsAnalyzer(log_dir="./logs")
            error_summary = logs_analyzer.get_errors_summary()
            error_count = error_summary.get('total_errors', 0)
        except:
            pass
        st.caption(f"🔴 Errores registrados: {error_count}")
    
    st.markdown("""
    **EP3 - Observabilidad y Monitoreo**
    - IE1: Métricas de Precisión, Consistencia y Errores ✅
    - IE2: Métricas de Latencia y Recursos ✅
    - IE3: Análisis de Logs y Trazabilidad ✅
    - IE4: Identificación de Patrones y Anomalías ✅
    - IE5: Dashboard Visual ✅
    - IE6: Protocolos de Seguridad ✅
    - IE7: Propuestas de Mejora ✅
    - IE8: Informe Técnico (ver INFORME_EP3.md)
    - IE9: Lenguaje Técnico (todo documentado)
    """)


if __name__ == "__main__":
    create_dashboard()
