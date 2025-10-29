"""
Herramientas (Tools) para el agente inteligente de Pastelería 1000 Sabores
Cada herramienta es una acción específica que el agente puede ejecutar de forma autónoma
"""

from langchain.tools import BaseTool
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
import json
import pandas as pd
from datetime import datetime


# ==================== SCHEMA DE INPUTS PARA TOOLS ====================

class SearchProductsInput(BaseModel):
    """Input para búsqueda de productos"""
    query: str = Field(description="Consulta de búsqueda del producto (ej: 'torta vegana chocolate', 'productos sin azúcar')")
    category: Optional[str] = Field(default=None, description="Categoría específica para filtrar (opcional)")
    max_price: Optional[float] = Field(default=None, description="Precio máximo para filtrar (opcional)")


class CalculateDiscountInput(BaseModel):
    """Input para cálculo de descuentos"""
    product_code: str = Field(description="Código del producto (ej: 'TC001')")
    customer_age: Optional[int] = Field(default=None, description="Edad del cliente")
    promo_code: Optional[str] = Field(default=None, description="Código promocional (ej: 'FELICES50')")
    customer_email: Optional[str] = Field(default=None, description="Email del cliente para validar descuento DUOC")
    quantity: int = Field(default=1, description="Cantidad de productos")


class CheckInventoryInput(BaseModel):
    """Input para verificar disponibilidad"""
    product_code: str = Field(description="Código del producto a verificar")
    capacity_needed: Optional[int] = Field(default=None, description="Capacidad o porciones necesarias")


class CustomerHistoryInput(BaseModel):
    """Input para consultar historial del cliente"""
    customer_id: Optional[str] = Field(default=None, description="ID del cliente")
    customer_email: Optional[str] = Field(default=None, description="Email del cliente")


# ==================== TOOL 1: BÚSQUEDA DE PRODUCTOS ====================

class SearchProductsTool(BaseTool):
    """Herramienta para buscar productos en el catálogo de la pastelería"""
    
    name: str = "search_products"
    description: str = """
    Busca productos en el catálogo de Pastelería 1000 Sabores.
    Útil cuando el cliente pregunta por:
    - Tipos de tortas o productos específicos
    - Productos por categoría (veganos, sin azúcar, cuadradas, circulares)
    - Características específicas (personalizable, ingredientes)
    - Rangos de precio
    
    Input: query (texto de búsqueda), category (opcional), max_price (opcional)
    Output: Lista de productos encontrados con detalles
    """
    args_schema: Type[BaseModel] = SearchProductsInput
    data_loader: Any = Field(default=None)
    
    def _run(self, query: str, category: Optional[str] = None, max_price: Optional[float] = None) -> str:
        """Ejecuta la búsqueda de productos"""
        try:
            # Cargar todos los productos (obtener los diccionarios directamente)
            self.data_loader.cargar_productos()  # Esto carga self.productos
            productos = self.data_loader.productos  # Acceder a la lista de diccionarios
            
            # Convertir a formato estructurado
            query_lower = query.lower()
            resultados = []
            
            for producto in productos:
                if not isinstance(producto, dict):
                    continue
                    
                match = False
                
                # Filtrar por categoría si se especifica
                if category:
                    cat_producto = producto.get('categoria', '').lower()
                    if category.lower() not in cat_producto and cat_producto not in category.lower():
                        continue
                
                # Filtrar por precio máximo
                if max_price and producto.get('precio', 0) > max_price:
                    continue
                
                # Búsqueda por términos en nombre, descripción, categoría
                nombre = producto.get('nombre', '').lower()
                descripcion = producto.get('descripcion', '').lower()
                categoria = producto.get('categoria', '').lower()
                ingredientes = ' '.join(producto.get('ingredientes', [])).lower()
                
                # Buscar coincidencias
                texto_completo = f"{nombre} {descripcion} {categoria} {ingredientes}"
                
                for term in query_lower.split():
                    if term in texto_completo:
                        match = True
                        break
                
                if match:
                    resultados.append(producto)
            
            if not resultados:
                return f"No se encontraron productos que coincidan con '{query}'"
            
            # Formatear resultados
            if len(resultados) > 10:
                resultados = resultados[:10]  # Limitar a 10 resultados
            
            response = f"✅ Encontré {len(resultados)} producto(s) relacionado(s) con '{query}':\n\n"
            
            for idx, prod in enumerate(resultados, 1):
                response += f"{idx}. **{prod.get('nombre', 'N/A')}** (Código: {prod.get('codigo', 'N/A')})\n"
                response += f"   - Precio: ${prod.get('precio', 0):,} CLP\n"
                response += f"   - Categoría: {prod.get('categoria', 'N/A')}\n"
                response += f"   - Descripción: {prod.get('descripcion', 'N/A')}\n"
                response += f"   - Personalizable: {'Sí ✓' if prod.get('personalizable') else 'No'}\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error al buscar productos: {str(e)}"
    
    async def _arun(self, query: str, category: Optional[str] = None, max_price: Optional[float] = None) -> str:
        """Versión asíncrona (no implementada)"""
        return self._run(query, category, max_price)


# ==================== TOOL 2: CÁLCULO DE DESCUENTOS ====================

class CalculateDiscountTool(BaseTool):
    """Herramienta para calcular descuentos aplicables a un producto"""
    
    name: str = "calculate_discount"
    description: str = """
    Calcula el precio final de un producto aplicando descuentos disponibles.
    Útil cuando el cliente pregunta por:
    - Precio con descuento
    - Descuentos aplicables según edad o promoción
    - Precio final para múltiples unidades
    
    Descuentos disponibles:
    - Mayores de 50 años: 50% descuento
    - Código FELICES50: 10% descuento
    - Estudiantes DUOC (email @duoc.cl) en cumpleaños: 100% gratis
    
    Input: product_code, customer_age (opcional), promo_code (opcional), customer_email (opcional), quantity
    Output: Desglose de precio con descuentos aplicados
    """
    args_schema: Type[BaseModel] = CalculateDiscountInput
    data_loader: Any = Field(default=None)
    discount_calculator: Any = Field(default=None)
    
    def _run(
        self, 
        product_code: str, 
        customer_age: Optional[int] = None,
        promo_code: Optional[str] = None,
        customer_email: Optional[str] = None,
        quantity: int = 1
    ) -> str:
        """Ejecuta el cálculo de descuentos"""
        try:
            # Buscar el producto
            productos = self.data_loader.cargar_productos()
            producto = None
            
            for p in productos:
                if isinstance(p, dict) and p.get('codigo') == product_code:
                    producto = p
                    break
            
            if not producto:
                return f"❌ No se encontró el producto con código '{product_code}'"
            
            precio_base = producto.get('precio', 0)
            precio_total = precio_base * quantity
            
            # Determinar tipo de cliente
            tipo_cliente = None
            descuento_porcentaje = 0
            descuento_descripcion = ""
            
            if customer_age and customer_age >= 50:
                tipo_cliente = "mayor_50"
                descuento_porcentaje = 50
                descuento_descripcion = "Descuento mayores de 50 años"
            elif promo_code and promo_code.upper() == "FELICES50":
                tipo_cliente = "felices50"
                descuento_porcentaje = 10
                descuento_descripcion = "Código promocional FELICES50"
            elif customer_email and "@duoc.cl" in customer_email.lower():
                tipo_cliente = "estudiante_duoc"
                descuento_porcentaje = 100
                descuento_descripcion = "Estudiante DUOC - Torta de cumpleaños GRATIS"
            
            # Calcular precio final
            if tipo_cliente:
                descuento_monto = precio_total * (descuento_porcentaje / 100)
                precio_final = precio_total - descuento_monto
            else:
                descuento_monto = 0
                precio_final = precio_total
            
            # Formatear respuesta
            response = f"💰 **CÁLCULO DE PRECIO - {producto.get('nombre')}**\n\n"
            response += f"📦 Cantidad: {quantity} unidad(es)\n"
            response += f"💵 Precio unitario: ${precio_base:,}\n"
            response += f"💵 Subtotal: ${precio_total:,}\n\n"
            
            if tipo_cliente:
                response += f"🎉 **DESCUENTO APLICADO: {descuento_descripcion}**\n"
                response += f"💸 Descuento: -{descuento_porcentaje}% (${descuento_monto:,})\n"
                response += f"✅ **PRECIO FINAL: ${precio_final:,}**\n\n"
            else:
                response += f"ℹ️ No se aplicaron descuentos\n"
                response += f"✅ **PRECIO FINAL: ${precio_final:,}**\n\n"
            
            response += "💡 **Descuentos disponibles:**\n"
            response += "- Mayores de 50 años: 50% descuento\n"
            response += "- Código FELICES50: 10% descuento\n"
            response += "- Estudiantes DUOC en cumpleaños: GRATIS\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error al calcular descuento: {str(e)}"
    
    async def _arun(
        self, 
        product_code: str, 
        customer_age: Optional[int] = None,
        promo_code: Optional[str] = None,
        customer_email: Optional[str] = None,
        quantity: int = 1
    ) -> str:
        """Versión asíncrona"""
        return self._run(product_code, customer_age, promo_code, customer_email, quantity)


# ==================== TOOL 3: VERIFICACIÓN DE INVENTARIO ====================

class CheckInventoryTool(BaseTool):
    """Herramienta para verificar disponibilidad y capacidad de productos"""
    
    name: str = "check_inventory"
    description: str = """
    Verifica disponibilidad de productos y capacidad de porciones.
    Útil cuando el cliente pregunta por:
    - Disponibilidad inmediata de un producto
    - Si una torta sirve para cierto número de personas
    - Stock de productos específicos
    
    Input: product_code, capacity_needed (opcional, para número de personas)
    Output: Estado de disponibilidad y recomendaciones
    """
    args_schema: Type[BaseModel] = CheckInventoryInput
    data_loader: Any = Field(default=None)
    
    def _run(self, product_code: str, capacity_needed: Optional[int] = None) -> str:
        """Verifica inventario y capacidad"""
        try:
            # Buscar el producto
            productos = self.data_loader.cargar_productos()
            producto = None
            
            for p in productos:
                if isinstance(p, dict) and p.get('codigo') == product_code:
                    producto = p
                    break
            
            if not producto:
                return f"❌ No se encontró el producto con código '{product_code}'"
            
            # Información de disponibilidad
            response = f"📦 **INFORMACIÓN DE DISPONIBILIDAD**\n\n"
            response += f"🍰 **Producto:** {producto.get('nombre')}\n"
            response += f"📋 **Código:** {product_code}\n"
            response += f"✅ **Estado:** Disponible\n"
            response += f"⏱️ **Tiempo de preparación:** 24-48 horas\n\n"
            
            # Capacidad estimada según categoría
            categoria = producto.get('categoria', '').lower()
            
            if capacity_needed:
                capacidad_recomendada = self._estimar_capacidad(producto, categoria)
                
                if capacity_needed <= capacidad_recomendada:
                    response += f"👥 **Capacidad:** Este producto sirve para {capacidad_recomendada} personas\n"
                    response += f"✅ Es adecuado para tu evento de {capacity_needed} personas\n\n"
                else:
                    cantidad_necesaria = (capacity_needed // capacidad_recomendada) + 1
                    response += f"👥 **Capacidad:** Este producto sirve para {capacidad_recomendada} personas\n"
                    response += f"⚠️ Para {capacity_needed} personas, recomendamos:\n"
                    response += f"   - Opción 1: {cantidad_necesaria} unidades de este producto\n"
                    response += f"   - Opción 2: Una torta de mayor tamaño (consultar opciones XL)\n\n"
            else:
                capacidad_recomendada = self._estimar_capacidad(producto, categoria)
                response += f"👥 **Capacidad estimada:** {capacidad_recomendada} personas\n\n"
            
            response += "💡 **Información adicional:**\n"
            if producto.get('personalizable'):
                response += "- ✅ Este producto es personalizable\n"
            response += "- 📞 Para pedidos especiales, contáctanos con 48h de anticipación\n"
            response += "- 🚚 Consulta disponibilidad de envío según tu zona\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error al verificar inventario: {str(e)}"
    
    def _estimar_capacidad(self, producto: dict, categoria: str) -> int:
        """Estima capacidad de porciones según tipo de producto"""
        if 'xl' in producto.get('nombre', '').lower():
            return 20
        elif 'grande' in producto.get('nombre', '').lower():
            return 15
        elif 'individual' in categoria or 'postre individual' in categoria:
            return 1
        elif 'cuadrada' in categoria:
            return 12
        elif 'circular' in categoria:
            return 10
        else:
            return 8
    
    async def _arun(self, product_code: str, capacity_needed: Optional[int] = None) -> str:
        """Versión asíncrona"""
        return self._run(product_code, capacity_needed)


# ==================== TOOL 4: HISTORIAL DEL CLIENTE ====================

class CustomerHistoryTool(BaseTool):
    """Herramienta para consultar historial de compras y preferencias del cliente"""
    
    name: str = "customer_history"
    description: str = """
    Consulta el historial de compras y preferencias de un cliente.
    Útil cuando:
    - El cliente menciona compras previas
    - Necesitas hacer recomendaciones personalizadas
    - Quieres conocer preferencias pasadas del cliente
    
    Input: customer_id o customer_email
    Output: Historial de compras, preferencias y recomendaciones
    """
    args_schema: Type[BaseModel] = CustomerHistoryInput
    data_loader: Any = Field(default=None)
    
    def _run(self, customer_id: Optional[str] = None, customer_email: Optional[str] = None) -> str:
        """Consulta historial del cliente"""
        try:
            # Intentar cargar historial de clientes
            try:
                clientes = self.data_loader.cargar_clientes_ejemplo()
                historial = self.data_loader.cargar_ejemplos_pedidos()
            except:
                return "ℹ️ Sistema de historial no disponible actualmente. Por favor proporciona tus preferencias."
            
            # Buscar cliente
            cliente_info = None
            
            if customer_email:
                for info in clientes if isinstance(clientes, list) else []:
                    if isinstance(info, dict) and info.get('email') == customer_email:
                        cliente_info = info
                        break
                    elif isinstance(info, str) and customer_email.lower() in info.lower():
                        cliente_info = info
                        break
            
            if not cliente_info:
                response = "ℹ️ No encontré historial previo para este cliente.\n\n"
                response += "💡 **¿Primera vez con nosotros?** ¡Bienvenido!\n"
                response += "Te invito a explorar nuestro catálogo y con gusto te ayudaré a encontrar el producto perfecto.\n\n"
                response += "🎁 **Promociones para nuevos clientes:**\n"
                response += "- Código FELICES50: 10% de descuento de por vida\n"
                response += "- Mayores de 50 años: 50% descuento\n"
                response += "- Estudiantes DUOC: Torta de cumpleaños gratis\n"
                return response
            
            # Formatear historial encontrado
            response = "📊 **HISTORIAL DEL CLIENTE**\n\n"
            
            if isinstance(cliente_info, dict):
                response += f"👤 **Cliente:** {cliente_info.get('nombre', 'N/A')}\n"
                response += f"📧 **Email:** {cliente_info.get('email', 'N/A')}\n"
                response += f"🎂 **Edad:** {cliente_info.get('edad', 'N/A')}\n\n"
                
                # Preferencias
                if cliente_info.get('preferencias'):
                    response += "⭐ **Preferencias conocidas:**\n"
                    for pref in cliente_info.get('preferencias', []):
                        response += f"- {pref}\n"
                    response += "\n"
                
                # Compras previas
                if cliente_info.get('compras_previas'):
                    response += "🛍️ **Compras anteriores:**\n"
                    for compra in cliente_info.get('compras_previas', [])[:3]:
                        response += f"- {compra}\n"
                    response += "\n"
            else:
                response += str(cliente_info) + "\n\n"
            
            response += "💡 **Recomendación:** Basándome en tu historial, puedo sugerirte productos similares o novedades que podrían interesarte.\n"
            
            return response
            
        except Exception as e:
            return f"ℹ️ No se pudo acceder al historial: {str(e)}\nPero con gusto te ayudo a encontrar lo que buscas."
    
    async def _arun(self, customer_id: Optional[str] = None, customer_email: Optional[str] = None) -> str:
        """Versión asíncrona"""
        return self._run(customer_id, customer_email)


# ==================== FUNCIÓN HELPER PARA INICIALIZAR TOOLS ====================

def initialize_tools(data_loader, discount_calculator) -> List[BaseTool]:
    """
    Inicializa todas las herramientas con las dependencias necesarias
    
    Args:
        data_loader: Instancia de PasteleriaDataLoader
        discount_calculator: Instancia de DiscountCalculator
    
    Returns:
        Lista de herramientas listas para usar con el agente
    """
    tools = [
        SearchProductsTool(data_loader=data_loader),
        CalculateDiscountTool(data_loader=data_loader, discount_calculator=discount_calculator),
        CheckInventoryTool(data_loader=data_loader),
        CustomerHistoryTool(data_loader=data_loader)
    ]
    
    return tools
