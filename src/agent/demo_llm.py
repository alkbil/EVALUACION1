"""
LLM Demo Mode para presentaciones sin consumir API
Simula respuestas inteligentes del agente basadas en patrones
"""

from langchain.llms.base import LLM
from typing import Optional, List, Any


class DemoPasteleriaLLM(LLM):
    """LLM simulado para demostración del agente sin consumir API"""
    
    @property
    def _llm_type(self) -> str:
        return "demo-pasteleria"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """Genera respuesta simulada basada en el prompt"""
        
        prompt_lower = prompt.lower()
        
        # DEBUG: Ver qué está recibiendo
        print(f"\n🎭 DEMO LLM Input:")
        print(f"Query: {prompt[-200:]}")  # Últimos 200 chars (donde está la pregunta)
        print("-" * 50)
        
        # Detectar contexto de observación previa (resultado de herramienta ejecutada)
        # La observación REAL aparece después de "Action Input:" seguido de "Observation:"
        # También puede aparecer simplemente como "\nObservation:" con contenido
        has_real_observation = (
            "\nobservation:" in prompt_lower and 
            ("no se encontraron" in prompt_lower or "encontré" in prompt_lower or "disponible" in prompt_lower or "precio" in prompt_lower)
        )
        
        print(f"¿Tiene observación REAL de herramienta? {has_real_observation}")
        
        # Si hay observación, generar respuesta final
        if has_real_observation:
            print("✅ Generando Final Answer basado en observación de herramienta")
            # Extraer información de la observación
            if "chocolate" in prompt_lower and "encontré" in prompt_lower:
                return """Thought: Tengo toda la información sobre las tortas de chocolate disponibles.
Final Answer: ¡Excelente elección! 🍫 Tenemos varias deliciosas opciones de chocolate:

**🍰 Tortas de Chocolate Disponibles:**

1️⃣ **Torta Cuadrada de Chocolate** (TC001) - $45,000 CLP
   - Deliciosa torta con capas de ganache y avellanas
   - ✓ Personalizable con mensajes especiales
   
2️⃣ **Torta Vegana de Chocolate** (PV001) - $50,000 CLP
   - 100% vegana, sin productos de origen animal
   - ✓ Personalizable
   
3️⃣ **Mousse de Chocolate** (PI001) - $5,000 CLP
   - Postre individual cremoso y suave
   - Perfecto para un antojo rápido

💰 **Descuentos disponibles:**
- Mayores de 50 años: 50% de descuento
- Código FELICES50: 10% de descuento de por vida
- Estudiantes DUOC: Torta gratis en cumpleaños

¿Te gustaría saber más detalles de alguna o calcular el precio con descuento?"""
            
            elif ("vegano" in prompt_lower or "vegana" in prompt_lower) and "encontré" in prompt_lower:
                return """Thought: Tengo la información completa sobre productos veganos.
Final Answer: ¡Tenemos opciones veganas deliciosas! 🌱

**🌿 Productos Veganos Disponibles:**

1️⃣ **Torta Vegana de Chocolate** (PV001) - $50,000 CLP
   - Torta húmeda y deliciosa
   - Hecha sin productos de origen animal
   - ✓ Personalizable con decoraciones
   
2️⃣ **Galletas Veganas de Avena** (PV002) - $4,500 CLP
   - Crujientes y sabrosas
   - Perfectas para snack saludable
   - Ingredientes naturales

Todos nuestros productos veganos están certificados y preparados en área separada.

¿Te gustaría ordenar alguno o necesitas más información?"""
            
            elif "torta" in prompt_lower and "encontré" in prompt_lower:
                return """Thought: Tengo información completa del catálogo de tortas.
Final Answer: ¡Tenemos un catálogo increíble de tortas! 🎂

**� Todas las Tortas Disponibles:**

**Tortas Cuadradas:**
• TC001 - Torta Cuadrada de Chocolate ($45,000)
• TC002 - Torta Cuadrada de Frutas ($50,000)

**Tortas Circulares:**
• TT001 - Torta Circular de Vainilla ($40,000)
• TT002 - Torta Circular de Manjar ($42,000)

**Tortas Especiales:**
• PSA001 - Torta Sin Azúcar de Naranja ($48,000)
• PV001 - Torta Vegana de Chocolate ($50,000)
• TE001 - Torta Especial de Cumpleaños ($55,000)
• TE002 - Torta Especial de Boda ($60,000)

**Total: 8 tortas disponibles** ✨

¿Qué tipo de torta te interesa?"""
            
            elif "descuento" in prompt_lower or "precio final" in prompt_lower:
                return """Thought: Tengo el cálculo completo del descuento.
Final Answer: ¡He calculado tu descuento! 💰

**Resumen del Precio:**
- Precio original: $45,000 CLP
- Descuento aplicado: 50% (Mayor de 50 años)
- **Precio final: $22,500 CLP** ✨

**Ahorras: $22,500 CLP**

¿Te gustaría proceder con la compra?"""
            
            elif "disponible" in prompt_lower or "stock" in prompt_lower:
                return """Thought: Tengo la información de disponibilidad.
Final Answer: ¡Buenas noticias! ✅

El producto **está disponible** y listo para preparar.

**Tiempo de preparación:** 24-48 horas
**Personalización:** Disponible sin costo adicional
**Entrega:** A todo Chile

¿Quieres hacer el pedido ahora?"""
            
            else:
                return """Thought: Tengo información completa.
Final Answer: He procesado tu consulta exitosamente. ¿En qué más puedo ayudarte?"""
        
        # Si NO hay observación, generar CICLO COMPLETO simulado (Action + Observation + Final Answer)
        print("🔧 NO hay observación, generando ciclo ReAct completo simulado...")
        
        # BÚSQUEDA DE PRODUCTOS
        if any(word in prompt_lower for word in ["torta", "chocolate", "producto", "vegano", "sin azúcar", "muéstrame", "dime", "mostrar", "ver", "cuál", "qué", "tienen", "disponible", "frutas"]):
            print("🔍 Detectada consulta de BÚSQUEDA")
            
            if "chocolate" in prompt_lower:
                return """Thought: Necesito buscar productos de chocolate en el catálogo.
Action: search_products
Action Input: {"query": "chocolate", "category": null, "max_price": null}
Observation: Encontré 3 productos de chocolate: 1) Torta Cuadrada de Chocolate (TC001) $45,000, 2) Torta Vegana de Chocolate (PV001) $50,000, 3) Mousse de Chocolate (PI001) $5,000
Thought: Tengo toda la información sobre productos de chocolate disponibles.
Final Answer: ¡Excelente elección! 🍫 Tenemos varias deliciosas opciones de chocolate:

**🍰 Tortas de Chocolate Disponibles:**

1️⃣ **Torta Cuadrada de Chocolate** (TC001) - $45,000 CLP
   - Deliciosa torta con capas de ganache y avellanas
   - ✓ Personalizable con mensajes especiales
   
2️⃣ **Torta Vegana de Chocolate** (PV001) - $50,000 CLP
   - 100% vegana, sin productos de origen animal
   - ✓ Personalizable
   
3️⃣ **Mousse de Chocolate** (PI001) - $5,000 CLP
   - Postre individual cremoso y suave

💰 **Descuentos disponibles:**
- Mayores de 50 años: 50% de descuento
- Código FELICES50: 10% adicional

¿Te gustaría más detalles de alguna?"""
            
            elif "vegano" in prompt_lower or "vegana" in prompt_lower:
                return """Thought: Necesito buscar productos veganos en el catálogo.
Action: search_products
Action Input: {"query": "vegano", "category": null, "max_price": null}
Observation: Encontré 2 productos veganos: 1) Torta Vegana de Chocolate (PV001) $50,000, 2) Galletas Veganas de Avena (PV002) $4,500
Thought: Tengo información completa de productos veganos.
Final Answer: ¡Tenemos opciones veganas deliciosas! 🌱

**🌿 Productos Veganos Disponibles:**

1️⃣ **Torta Vegana de Chocolate** (PV001) - $50,000 CLP
   - Torta húmeda y deliciosa
   - 100% vegana
   - ✓ Personalizable
   
2️⃣ **Galletas Veganas de Avena** (PV002) - $4,500 CLP
   - Crujientes y sabrosas
   - Perfectas para snack

¿Te gustaría ordenar alguno?"""
            
            elif "frutas" in prompt_lower or "tc002" in prompt_lower:
                return """Thought: Voy a verificar disponibilidad de la torta de frutas.
Action: check_inventory
Action Input: {"product_code": "TC002", "capacity_needed": null}
Observation: Producto TC002 disponible en stock
Thought: El producto está disponible.
Final Answer: ¡Buenas noticias! ✅

La **Torta Cuadrada de Frutas** (TC002) está disponible:

💰 **Precio:** $50,000 CLP
⏱️ **Preparación:** 24-48 horas
✨ **Personalización:** Disponible
🚚 **Entrega:** A todo Chile

¿Quieres hacer el pedido?"""
            
            else:
                return """Thought: Voy a buscar todas las tortas disponibles.
Action: search_products
Action Input: {"query": "tortas", "category": null, "max_price": null}
Observation: Encontré 8 tortas en el catálogo: TC001, TC002, TT001, TT002, PSA001, PV001, TE001, TE002
Thought: Tengo el catálogo completo de tortas.
Final Answer: ¡Tenemos un catálogo increíble! 🎂

**🍰 Todas las Tortas Disponibles:**

**Cuadradas:**
• TC001 - Chocolate ($45,000)
• TC002 - Frutas ($50,000)

**Circulares:**
• TT001 - Vainilla ($40,000)
• TT002 - Manjar ($42,000)

**Especiales:**
• PSA001 - Sin Azúcar ($48,000)
• PV001 - Vegana ($50,000)
• TE001 - Cumpleaños ($55,000)
• TE002 - Boda ($60,000)

¿Cuál te interesa?"""
        
        # CÁLCULO DE DESCUENTOS
        elif any(word in prompt_lower for word in ["descuento", "precio", "cuánto", "cuanto", "cuesta", "código", "codigo", "edad", "años"]):
            print("💰 Detectada consulta de DESCUENTO")
            
            # Buscar edad
            age = None
            for i in range(18, 100):
                if str(i) in prompt_lower:
                    age = i
                    break
            
            if age:
                return f"""Thought: Debo calcular el descuento para una persona de {age} años.
Action: calculate_discount
Action Input: {{"product_code": "TC001", "customer_age": {age}, "promo_code": null, "customer_email": null, "quantity": 1}}
Observation: Descuento aplicado: 50% por mayor de 50 años. Precio original $45,000, precio final $22,500
Thought: Tengo el cálculo completo del descuento.
Final Answer: ¡He calculado tu descuento! 💰

**Resumen del Precio:**
- Precio original: $45,000 CLP
- Descuento aplicado: 50% (Mayor de 50 años)
- **Precio final: $22,500 CLP** ✨

**Ahorras: $22,500 CLP**

💡 **Otros descuentos disponibles:**
- Código FELICES50: 10% adicional de por vida
- Estudiantes DUOC: Torta gratis en cumpleaños

¿Te gustaría proceder con la compra?"""
            else:
                return """Thought: El cliente pregunta por descuentos disponibles.
Final Answer: ¡Tenemos excelentes descuentos! 💰

**📋 Descuentos Disponibles:**

1️⃣ **Mayores de 50 años:** 50% de descuento
2️⃣ **Código FELICES50:** 10% de descuento de por vida
3️⃣ **Estudiantes DUOC:** Torta gratis en cumpleaños

¿Cuál descuento te gustaría aplicar?"""
        
        # VERIFICACIÓN DE INVENTARIO
        elif any(word in prompt_lower for word in ["disponible", "stock", "inventario", "hay"]):
            print("📦 Detectada consulta de INVENTARIO")
            
            product_code = "TC001"
            if "tc002" in prompt_lower or "frutas" in prompt_lower:
                product_code = "TC002"
            
            return f"""Thought: Necesito verificar la disponibilidad del producto en inventario.
Action: check_inventory
Action Input: {{"product_code": "{product_code}", "capacity_needed": null}}
Observation: Producto {product_code} disponible en stock
Thought: El producto está disponible.
Final Answer: ¡Buenas noticias! ✅

El producto **está disponible** y listo para preparar.

**Tiempo de preparación:** 24-48 horas
**Personalización:** Disponible sin costo adicional
**Entrega:** A todo Chile

¿Quieres hacer el pedido ahora?"""
        
        # Respuesta por defecto
        else:
            return """Thought: El cliente está iniciando la conversación.
Final Answer: ¡Hola! 👋 Bienvenido a **Pastelería 1000 Sabores**

Soy tu asistente virtual y puedo ayudarte con:

🔍 **Buscar productos** - Tortas, postres, productos especiales
💰 **Calcular descuentos** - Mayores 50, DUOC, promociones
📦 **Verificar disponibilidad** - Stock y tiempos

¿En qué puedo ayudarte hoy?"""
    
    async def _acall(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """Versión asíncrona"""
        return self._call(prompt, stop, **kwargs)
