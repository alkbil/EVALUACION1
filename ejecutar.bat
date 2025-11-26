@echo off
REM Script para ejecutar las aplicaciones del Proyecto EP3
REM Menú interactivo para seleccionar qué ejecutar

echo.
echo ========================================
echo    EP3 - Sistema de Observabilidad
echo ========================================
echo.
echo Selecciona una opcion:
echo.
echo 1) Abrir MENU PRINCIPAL (recomendado)
echo 2) Abrir DASHBOARD de Observabilidad
echo 3) Abrir CHATBOT (Agente Inteligente)
echo 4) Abrir INFORME Tecnico
echo 5) Salir
echo.

set /p choice="Ingresa tu opcion (1-5): "

if "%choice%"=="1" (
    echo Abriendo Menu Principal...
    python -m streamlit run menu_principal.py
) else if "%choice%"=="2" (
    echo Abriendo Dashboard...
    python -m streamlit run dashboard.py
) else if "%choice%"=="3" (
    echo Abriendo Chatbot...
    python -m streamlit run app_agent.py
) else if "%choice%"=="4" (
    echo Abriendo Informe...
    python -m streamlit run informe.py
) else if "%choice%"=="5" (
    echo Saliendo...
    exit /b 0
) else (
    echo Opcion invalida. Por favor intenta de nuevo.
    pause
    goto :start
)

pause
