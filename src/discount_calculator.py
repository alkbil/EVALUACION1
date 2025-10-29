class DiscountCalculator:
    def __init__(self):
        self.descuentos = {
            "mayor_50": 0.50,  # 50% descuento
            "felices50": 0.10,  # 10% descuento
            "estudiante_duoc": 1.00  # 100% descuento (gratis) en cumpleaños
        }
    
    def calcular_descuento(self, precio_base, tipo_cliente, es_cumpleanos=False):
        """Calcula descuentos según el tipo de cliente"""
        if tipo_cliente == "estudiante_duoc" and es_cumpleanos:
            return 0  # Gratis
        elif tipo_cliente == "mayor_50":
            return precio_base * self.descuentos["mayor_50"]
        elif tipo_cliente == "felices50":
            return precio_base * self.descuentos["felices50"]
        else:
            return precio_base  # Precio original
    
    def obtener_precio_final(self, precio_base, tipo_cliente=None, es_cumpleanos=False):
        """Calcula el precio final después de descuentos"""
        if not tipo_cliente:
            return precio_base
        
        descuento = self.calcular_descuento(precio_base, tipo_cliente, es_cumpleanos)
        
        if tipo_cliente == "estudiante_duoc" and es_cumpleanos:
            return 0  # Gratis
        else:
            return precio_base - descuento
    
    def explicar_descuentos(self):
        """Genera explicación completa de los descuentos disponibles"""
        return """
        🎉 **PROMOCIONES ESPECIALES DE PASTELERÍA 1000 SABORES** 🎉

        🔹 **MAYORES DE 50 AÑOS**: 50% de descuento en todos los productos (registrándose en nuestra web)
        🔹 **CÓDIGO FELICES50**: 10% de descuento de por vida al registrarse con el código
        🔹 **ESTUDIANTES DUOC**: Torta de cumpleaños GRATIS al registrarse con correo @duoc.cl

        💡 *Para activar los descuentos, regístrate en nuestra página web y verifica tu información*
        """
    
    def validar_tipo_cliente(self, edad, correo="", codigo_promocional=""):
        """Determina el tipo de cliente basado en los datos proporcionados"""
        if edad >= 50:
            return "mayor_50"
        elif codigo_promocional.upper() == "FELICES50":
            return "felices50"
        elif "@duoc.cl" in correo.lower():
            return "estudiante_duoc"
        else:
            return "regular"