import json
import pandas as pd

class PasteleriaDataLoader:
    def __init__(self):
        self.productos = []
        self.politicas = []
        self.faqs = []
    
    def cargar_productos(self):
        """Carga el catálogo completo de productos de la pastelería"""
        productos = [
            {
                "codigo": "TC001", "categoria": "Tortas Cuadradas", "nombre": "Torta Cuadrada de Chocolate",
                "precio": 45000, "personalizable": True,
                "descripcion": "Deliciosa torta de chocolate con capas de ganache y un toque de avellanas. Personalizable con mensajes especiales.",
                "ingredientes": ["chocolate", "ganache", "avellanas"]
            },
            {
                "codigo": "TC002", "categoria": "Tortas Cuadradas", "nombre": "Torta Cuadrada de Frutas", 
                "precio": 50000, "personalizable": True,
                "descripcion": "Una mezcla de frutas frescas y crema chantilly sobre un suave bizcocho de vainilla, ideal para celebraciones.",
                "ingredientes": ["frutas frescas", "crema chantilly", "vainilla"]
            },
            {
                "codigo": "TT001", "categoria": "Tortas Circulares", "nombre": "Torta Circular de Vainilla",
                "precio": 40000, "personalizable": True,
                "descripcion": "Bizcocho de vainilla clásico relleno con crema pastelera y cubierto con un glaseado dulce.",
                "ingredientes": ["vainilla", "crema pastelera", "glaseado"]
            },
            {
                "codigo": "TT002", "categoria": "Tortas Circulares", "nombre": "Torta Circular de Manjar",
                "precio": 42000, "personalizable": True, 
                "descripcion": "Torta tradicional chilena con manjar y nueces, un deleite para los amantes de los sabores dulces y clásicos.",
                "ingredientes": ["manjar", "nueces", "bizcocho"]
            },
            {
                "codigo": "PI001", "categoria": "Postres Individuales", "nombre": "Mousse de Chocolate",
                "precio": 5000, "personalizable": False,
                "descripcion": "Postre individual cremoso y suave, hecho con chocolate de alta calidad, ideal para los amantes del chocolate.",
                "ingredientes": ["chocolate", "crema", "azúcar"]
            },
            {
                "codigo": "PSA001", "categoria": "Productos Sin Azúcar", "nombre": "Torta Sin Azúcar de Naranja",
                "precio": 48000, "personalizable": True,
                "descripcion": "Torta ligera y deliciosa, endulzada naturalmente, ideal para quienes buscan opciones más saludables.",
                "ingredientes": ["naranja", "endulzante natural", "harina integral"]
            },
            {
                "codigo": "PV001", "categoria": "Productos Veganos", "nombre": "Torta Vegana de Chocolate",
                "precio": 50000, "personalizable": True,
                "descripcion": "Torta de chocolate húmeda y deliciosa, hecha sin productos de origen animal, perfecta para veganos.",
                "ingredientes": ["chocolate vegano", "leche vegetal", "harina"]
            }
        ]
        self.productos = productos
        return [f"PRODUCTO: {p['nombre']} - ${p['precio']} - {p['descripcion']} - Personalizable: {p['personalizable']}" for p in productos]
    
    def cargar_politicas(self):
        """Carga las políticas de descuentos y promociones"""
        politicas = [
            "DESCUENTO MAYORES 50 AÑOS: Usuarios mayores de 50 años reciben 50% de descuento en todos los productos al registrarse",
            "PROMOCIÓN FELICES50: Código FELICES50 da 10% de descuento de por vida al registrarse en la página web",
            "ESTUDIANTES DUOC: Estudiantes con correo institucional @duoc.cl reciben torta gratis en su cumpleaños, deben registrarse con su correo",
            "ENVÍOS: Realizamos envíos a todo Chile con seguimiento en tiempo real y selección de fechas de entrega preferidas",
            "PERSONALIZACIÓN: Todas las tortas pueden personalizarse con mensajes especiales, imágenes o decoraciones específicas",
            "GARANTÍA: Satisfacción garantizada o devolución del dinero en un plazo de 24 horas",
            "HISTORIA: Pastelería con 50 años de tradición y participación en Récord Guinness 1995 por la torta más grande del mundo",
            "MISIÓN: Ofrecer una experiencia dulce y memorable a nuestros clientes con productos de repostería de alta calidad",
            "VISIÓN: Convertirnos en la tienda online líder de productos de repostería en Chile"
        ]
        self.politicas = politicas
        return politicas
    
    def cargar_faqs(self):
        """Carga preguntas frecuentes de clientes"""
        faqs = [
            "¿Cómo me registro para obtener descuentos? - Debes registrarte en nuestra página web con tus datos personales y verificar tu edad o correo institucional",
            "¿Qué métodos de pago aceptan? - Aceptamos tarjetas de crédito/débito, transferencia bancaria y PayPal",
            "¿Hacen envíos a todo Chile? - Sí, entregamos en todo el país con costos de envío variables según la ubicación",
            "¿Puedo personalizar mi torta? - Sí, todas las tortas son personalizables con mensajes, fotos o decoraciones especiales",
            "¿Tienen productos para dietas especiales? - Sí, ofrecemos productos sin azúcar, sin gluten y opciones veganas",
            "¿Cuánto tiempo de anticipación debo pedir? - Recomendamos 48 horas de anticipación para tortas personalizadas",
            "¿Ofrecen muestras de productos? - Sí, puedes agendar una cita para degustación en nuestra pastelería",
            "¿Qué hago si mi producto llega dañado? - Contáctanos dentro de las 24 horas para reemplazo o devolución"
        ]
        self.faqs = faqs
        return faqs
    
    def obtener_categorias(self):
        """Retorna lista de categorías disponibles"""
        categorias = list(set([p['categoria'] for p in self.productos]))
        return categorias