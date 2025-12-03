# Script para ejecutar las aplicaciones del Proyecto EP3

# Activar ambiente virtual
Write-Host "Activando ambiente virtual..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   EP3 - Sistema de Observabilidad" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Selecciona una opcion:`n"
Write-Host "1 - Menu Principal (recomendado)" -ForegroundColor Yellow
Write-Host "2 - Dashboard de Observabilidad" -ForegroundColor Yellow
Write-Host "3 - Chatbot (Agente Inteligente)" -ForegroundColor Yellow
Write-Host "4 - Informe Tecnico" -ForegroundColor Yellow
Write-Host "5 - Salir`n"

$choice = Read-Host "Ingresa tu opcion (1-5)"

switch ($choice) {
    "1" {
        Write-Host "`nAbriendo Menu Principal..." -ForegroundColor Green
        python -m streamlit run menu_principal.py
    }
    "2" {
        Write-Host "`nAbriendo Dashboard..." -ForegroundColor Green
        python -m streamlit run dashboard.py
    }
    "3" {
        Write-Host "`nAbriendo Chatbot..." -ForegroundColor Green
        python -m streamlit run app_agent.py
    }
    "4" {
        Write-Host "`nAbriendo Informe..." -ForegroundColor Green
        python -m streamlit run informe.py
    }
    "5" {
        Write-Host "`nSaliendo..." -ForegroundColor Yellow
        exit
    }
    default {
        Write-Host "`nOpcion invalida. Por favor intenta de nuevo." -ForegroundColor Red
    }
}
