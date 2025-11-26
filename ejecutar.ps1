# Script para ejecutar las aplicaciones del Proyecto EP3
# Menú interactivo para seleccionar qué ejecutar

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   EP3 - Sistema de Observabilidad" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Selecciona una opción:`n"
Write-Host "1) Abrir MENU PRINCIPAL (recomendado)" -ForegroundColor Yellow
Write-Host "2) Abrir DASHBOARD de Observabilidad" -ForegroundColor Yellow
Write-Host "3) Abrir CHATBOT (Agente Inteligente)" -ForegroundColor Yellow
Write-Host "4) Abrir INFORME Técnico" -ForegroundColor Yellow
Write-Host "5) Salir`n"

$choice = Read-Host "Ingresa tu opción (1-5)"

switch ($choice) {
    "1" {
        Write-Host "`nAbriendo Menú Principal..." -ForegroundColor Green
        & python -m streamlit run menu_principal.py
    }
    "2" {
        Write-Host "`nAbriendo Dashboard..." -ForegroundColor Green
        & python -m streamlit run dashboard.py
    }
    "3" {
        Write-Host "`nAbriendo Chatbot..." -ForegroundColor Green
        & python -m streamlit run app_agent.py
    }
    "4" {
        Write-Host "`nAbriendo Informe..." -ForegroundColor Green
        & python -m streamlit run informe.py
    }
    "5" {
        Write-Host "`nSaliendo..." -ForegroundColor Yellow
        exit
    }
    default {
        Write-Host "`nOpción inválida. Por favor intenta de nuevo." -ForegroundColor Red
        Read-Host "Presiona Enter para continuar"
    }
}
