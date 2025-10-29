"""
Tests básicos para el agente inteligente
Valida funcionalidad de herramientas, memoria y agente
"""

import pytest
import os
from unittest.mock import Mock, patch

# Importar componentes a testear
from src.agent import initialize_tools, create_agent
from src.memory import create_short_term_memory, create_long_term_memory
from src.data_loader import PasteleriaDataLoader
from src.discount_calculator import DiscountCalculator


# ==================== FIXTURES ====================

@pytest.fixture
def data_loader():
    """Fixture para data loader"""
    return PasteleriaDataLoader()


@pytest.fixture
def discount_calculator():
    """Fixture para calculadora de descuentos"""
    return DiscountCalculator()


@pytest.fixture
def tools(data_loader, discount_calculator):
    """Fixture para herramientas"""
    return initialize_tools(data_loader, discount_calculator)


@pytest.fixture
def short_term_memory():
    """Fixture para memoria de corto plazo"""
    return create_short_term_memory(memory_type="buffer")


# ==================== TESTS DE HERRAMIENTAS ====================

def test_search_products_tool_exists(tools):
    """Verifica que SearchProductsTool existe"""
    tool_names = [tool.name for tool in tools]
    assert "search_products" in tool_names


def test_calculate_discount_tool_exists(tools):
    """Verifica que CalculateDiscountTool existe"""
    tool_names = [tool.name for tool in tools]
    assert "calculate_discount" in tool_names


def test_check_inventory_tool_exists(tools):
    """Verifica que CheckInventoryTool existe"""
    tool_names = [tool.name for tool in tools]
    assert "check_inventory" in tool_names


def test_customer_history_tool_exists(tools):
    """Verifica que CustomerHistoryTool existe"""
    tool_names = [tool.name for tool in tools]
    assert "customer_history" in tool_names


def test_total_tools_count(tools):
    """Verifica que hay exactamente 4 herramientas"""
    assert len(tools) == 4


def test_search_products_tool_execution(tools):
    """Test de ejecución básica de SearchProductsTool"""
    search_tool = tools[0]
    result = search_tool._run(query="chocolate")
    
    # Verificar que retorna string
    assert isinstance(result, str)
    # Verificar que no está vacío
    assert len(result) > 0
    # Verificar que menciona productos
    assert "producto" in result.lower() or "torta" in result.lower()


def test_calculate_discount_tool_execution(tools):
    """Test de ejecución básica de CalculateDiscountTool"""
    discount_tool = tools[1]
    
    # Test con descuento por edad
    result = discount_tool._run(
        product_code="TC001",
        customer_age=55,
        quantity=1
    )
    
    # Verificar formato de respuesta
    assert isinstance(result, str)
    assert "precio" in result.lower() or "descuento" in result.lower()


def test_check_inventory_tool_execution(tools):
    """Test de ejecución básica de CheckInventoryTool"""
    inventory_tool = tools[2]
    
    result = inventory_tool._run(
        product_code="TC001",
        capacity_needed=15
    )
    
    # Verificar respuesta
    assert isinstance(result, str)
    assert len(result) > 0


def test_customer_history_tool_execution(tools):
    """Test de ejecución básica de CustomerHistoryTool"""
    history_tool = tools[3]
    
    result = history_tool._run(
        customer_email="test@example.com"
    )
    
    # Verificar respuesta
    assert isinstance(result, str)
    assert len(result) > 0


# ==================== TESTS DE MEMORIA ====================

def test_short_term_memory_initialization(short_term_memory):
    """Verifica inicialización de memoria de corto plazo"""
    assert short_term_memory is not None
    assert short_term_memory.memory_type == "buffer"


def test_short_term_memory_add_message(short_term_memory):
    """Test de agregar mensajes a memoria de corto plazo"""
    short_term_memory.add_message(
        user_message="Hola",
        agent_response="Hola, ¿en qué puedo ayudarte?"
    )
    
    # Verificar que se agregó
    assert short_term_memory.message_count == 1
    
    # Verificar que se puede recuperar
    messages = short_term_memory.get_messages()
    assert len(messages) >= 1


def test_short_term_memory_context(short_term_memory):
    """Test de recuperación de contexto"""
    short_term_memory.add_message(
        user_message="Test query",
        agent_response="Test response"
    )
    
    context = short_term_memory.get_context()
    
    # Verificar que retorna string
    assert isinstance(context, str)
    # Verificar que contiene información
    assert "test" in context.lower()


def test_short_term_memory_clear(short_term_memory):
    """Test de limpiar memoria"""
    short_term_memory.add_message("Test", "Response")
    assert short_term_memory.message_count > 0
    
    short_term_memory.clear()
    assert short_term_memory.message_count == 0


def test_short_term_memory_preferences(short_term_memory):
    """Test de extracción de preferencias"""
    short_term_memory.add_message(
        user_message="Quiero productos veganos",
        agent_response="Tenemos varias opciones veganas"
    )
    
    preferences = short_term_memory.extract_user_preferences()
    
    # Verificar estructura
    assert isinstance(preferences, dict)
    assert "categorias_interes" in preferences


# ==================== TESTS DE DATA LOADER ====================

def test_data_loader_initialization(data_loader):
    """Verifica inicialización del data loader"""
    assert data_loader is not None


def test_data_loader_cargar_productos(data_loader):
    """Test de carga de productos"""
    productos = data_loader.cargar_productos()
    
    # Verificar que retorna lista
    assert isinstance(productos, list)
    # Verificar que tiene productos
    assert len(productos) > 0


def test_data_loader_categorias(data_loader):
    """Test de obtención de categorías"""
    categorias = data_loader.obtener_categorias()
    
    # Verificar que retorna lista
    assert isinstance(categorias, list)
    # Verificar que tiene categorías esperadas
    assert any("torta" in cat.lower() for cat in categorias)


# ==================== TESTS DE DISCOUNT CALCULATOR ====================

def test_discount_calculator_initialization(discount_calculator):
    """Verifica inicialización del calculador"""
    assert discount_calculator is not None


def test_discount_calculator_mayor_50(discount_calculator):
    """Test de descuento para mayores de 50"""
    precio_base = 10000
    tipo_cliente = "mayor_50"
    
    precio_final = discount_calculator.obtener_precio_final(
        precio_base=precio_base,
        tipo_cliente=tipo_cliente
    )
    
    # Debe ser 50% del precio base
    assert precio_final == precio_base * 0.5


def test_discount_calculator_felices50(discount_calculator):
    """Test de descuento código FELICES50"""
    precio_base = 10000
    tipo_cliente = "felices50"
    
    precio_final = discount_calculator.obtener_precio_final(
        precio_base=precio_base,
        tipo_cliente=tipo_cliente
    )
    
    # Debe ser 90% del precio base (10% descuento)
    assert precio_final == precio_base * 0.9


def test_discount_calculator_estudiante_duoc(discount_calculator):
    """Test de descuento estudiante DUOC"""
    precio_base = 10000
    tipo_cliente = "estudiante_duoc"
    
    precio_final = discount_calculator.obtener_precio_final(
        precio_base=precio_base,
        tipo_cliente=tipo_cliente,
        es_cumpleanos=True
    )
    
    # Debe ser gratis
    assert precio_final == 0


# ==================== TESTS DE INTEGRACIÓN ====================

@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="Requiere OPENAI_API_KEY"
)
def test_agent_creation():
    """Test de creación del agente (requiere API key)"""
    data_loader = PasteleriaDataLoader()
    calculator = DiscountCalculator()
    api_key = os.getenv("OPENAI_API_KEY")
    
    agent = create_agent(
        data_loader=data_loader,
        discount_calculator=calculator,
        openai_api_key=api_key,
        max_iterations=5,
        verbose=False
    )
    
    assert agent is not None
    assert len(agent.tools) == 4


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="Requiere OPENAI_API_KEY"
)
def test_agent_simple_query():
    """Test de consulta simple al agente (requiere API key)"""
    data_loader = PasteleriaDataLoader()
    calculator = DiscountCalculator()
    api_key = os.getenv("OPENAI_API_KEY")
    
    agent = create_agent(
        data_loader=data_loader,
        discount_calculator=calculator,
        openai_api_key=api_key,
        max_iterations=5,
        verbose=False
    )
    
    # Consulta simple
    result = agent.execute("¿Qué tortas de chocolate tienen?")
    
    # Verificar estructura de respuesta
    assert "success" in result
    assert "answer" in result
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0


# ==================== TESTS DE VALIDACIÓN ====================

def test_tools_have_descriptions(tools):
    """Verifica que todas las tools tienen descripción"""
    for tool in tools:
        assert hasattr(tool, "description")
        assert len(tool.description) > 0


def test_tools_have_names(tools):
    """Verifica que todas las tools tienen nombre"""
    for tool in tools:
        assert hasattr(tool, "name")
        assert len(tool.name) > 0


def test_tools_are_unique(tools):
    """Verifica que los nombres de tools son únicos"""
    names = [tool.name for tool in tools]
    assert len(names) == len(set(names))


# ==================== TESTS DE RENDIMIENTO ====================

def test_search_tool_performance(tools):
    """Test de rendimiento de búsqueda"""
    import time
    
    search_tool = tools[0]
    
    start = time.time()
    result = search_tool._run(query="chocolate")
    elapsed = time.time() - start
    
    # Debe completarse en menos de 2 segundos
    assert elapsed < 2.0


def test_discount_tool_performance(tools):
    """Test de rendimiento de cálculo"""
    import time
    
    discount_tool = tools[1]
    
    start = time.time()
    result = discount_tool._run(
        product_code="TC001",
        customer_age=55
    )
    elapsed = time.time() - start
    
    # Debe completarse en menos de 1 segundo
    assert elapsed < 1.0


# ==================== MAIN ====================

if __name__ == "__main__":
    # Ejecutar tests
    pytest.main([__file__, "-v", "--tb=short"])
