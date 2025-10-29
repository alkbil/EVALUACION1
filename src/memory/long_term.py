"""
Sistema de Memoria de Largo Plazo
Almacena conversaciones previas usando ChromaDB y embeddings
"""

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os


class LongTermMemory:
    """
    Gestiona la memoria de largo plazo usando vector store
    Permite recuperar contexto de conversaciones pasadas
    """
    
    def __init__(
        self,
        persist_directory: str = "./data/chroma_db",
        collection_name: str = "pasteleria_conversations",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ):
        """
        Inicializa el sistema de memoria de largo plazo
        
        Args:
            persist_directory: Directorio para persistir la base de datos
            collection_name: Nombre de la colección
            embedding_model: Modelo de embeddings a usar
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Crear directorio si no existe
        os.makedirs(persist_directory, exist_ok=True)
        
        # Inicializar embeddings
        print("🔄 Cargando modelo de embeddings...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Inicializar o cargar vector store
        try:
            self.vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=persist_directory
            )
            print(f"✅ Memoria de largo plazo cargada desde {persist_directory}")
        except Exception as e:
            print(f"⚠️ Creando nueva base de datos de memoria: {e}")
            self.vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=persist_directory
            )
        
        self.conversation_count = 0
    
    def store_conversation(
        self,
        user_message: str,
        agent_response: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Almacena una conversación en la memoria de largo plazo
        
        Args:
            user_message: Mensaje del usuario
            agent_response: Respuesta del agente
            metadata: Metadata adicional (customer_id, preferences, etc.)
        """
        try:
            # Crear documento combinado
            conversation_text = f"Usuario: {user_message}\nAsistente: {agent_response}"
            
            # Preparar metadata (ChromaDB solo acepta str, int, float, bool)
            doc_metadata = {
                "timestamp": datetime.now().isoformat(),
                "conversation_id": self.conversation_count,
                "user_message": user_message,
                "agent_response": agent_response
            }
            
            if metadata:
                # Filtrar y convertir metadata compleja
                for key, value in metadata.items():
                    if value is None:
                        doc_metadata[key] = None
                    elif isinstance(value, (str, int, float, bool)):
                        doc_metadata[key] = value
                    elif isinstance(value, list):
                        # Convertir listas a string JSON
                        doc_metadata[key] = json.dumps(value) if value else ""
                    elif isinstance(value, dict):
                        # Convertir diccionarios a string JSON
                        doc_metadata[key] = json.dumps(value)
                    else:
                        # Convertir otros tipos a string
                        doc_metadata[key] = str(value)
            
            # Crear documento
            document = Document(
                page_content=conversation_text,
                metadata=doc_metadata
            )
            
            # Agregar a vector store
            self.vectorstore.add_documents([document])
            self.conversation_count += 1
            
            print(f"💾 Conversación #{self.conversation_count} almacenada en memoria de largo plazo")
            
        except Exception as e:
            print(f"⚠️ Error almacenando conversación: {e}")
    
    def retrieve_similar_conversations(
        self,
        query: str,
        k: int = 3,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Recupera conversaciones similares de la memoria
        
        Args:
            query: Consulta para buscar conversaciones similares
            k: Número de resultados a recuperar
            filter_metadata: Filtros adicionales (ej: customer_id)
        
        Returns:
            Lista de conversaciones relevantes
        """
        try:
            # Buscar documentos similares
            if filter_metadata:
                results = self.vectorstore.similarity_search(
                    query,
                    k=k,
                    filter=filter_metadata
                )
            else:
                results = self.vectorstore.similarity_search(query, k=k)
            
            # Formatear resultados
            conversations = []
            for doc in results:
                conversations.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "user_message": doc.metadata.get("user_message", ""),
                    "agent_response": doc.metadata.get("agent_response", ""),
                    "timestamp": doc.metadata.get("timestamp", "")
                })
            
            return conversations
            
        except Exception as e:
            print(f"⚠️ Error recuperando conversaciones: {e}")
            return []
    
    def get_customer_history(
        self,
        customer_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Obtiene el historial completo de un cliente
        
        Args:
            customer_id: ID del cliente
            limit: Límite de conversaciones a recuperar
        
        Returns:
            Lista de conversaciones del cliente
        """
        try:
            # Buscar por customer_id en metadata
            results = self.vectorstore.similarity_search(
                "",  # Query vacío para obtener todos
                k=limit,
                filter={"customer_id": customer_id}
            )
            
            conversations = []
            for doc in results:
                conversations.append({
                    "content": doc.page_content,
                    "timestamp": doc.metadata.get("timestamp", ""),
                    "user_message": doc.metadata.get("user_message", ""),
                    "agent_response": doc.metadata.get("agent_response", "")
                })
            
            # Ordenar por timestamp
            conversations.sort(
                key=lambda x: x.get("timestamp", ""),
                reverse=True
            )
            
            return conversations
            
        except Exception as e:
            print(f"⚠️ Error obteniendo historial del cliente: {e}")
            return []
    
    def extract_customer_preferences(
        self,
        customer_id: Optional[str] = None,
        recent_conversations: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Extrae preferencias del cliente de conversaciones previas
        
        Args:
            customer_id: ID del cliente
            recent_conversations: Conversaciones recientes alternativas
        
        Returns:
            Dict con preferencias identificadas
        """
        conversations = []
        
        if customer_id:
            conversations = self.get_customer_history(customer_id, limit=20)
        elif recent_conversations:
            conversations = recent_conversations
        
        if not conversations:
            return {
                "productos_favoritos": [],
                "categorias_preferidas": [],
                "restricciones_alimentarias": [],
                "rango_presupuesto": "No definido",
                "frecuencia_compra": "Primera vez"
            }
        
        # Analizar texto de todas las conversaciones
        all_text = " ".join([
            conv.get("content", "") + " " + 
            conv.get("user_message", "") + " " + 
            conv.get("agent_response", "")
            for conv in conversations
        ]).lower()
        
        preferences = {
            "productos_favoritos": [],
            "categorias_preferidas": [],
            "restricciones_alimentarias": [],
            "ocasiones_frecuentes": [],
            "rango_presupuesto": "No definido"
        }
        
        # Detectar productos favoritos
        productos_keywords = {
            "chocolate": "Tortas de chocolate",
            "vainilla": "Tortas de vainilla",
            "frutas": "Tortas de frutas",
            "manjar": "Tortas de manjar"
        }
        
        for keyword, producto in productos_keywords.items():
            if all_text.count(keyword) >= 2:  # Mencionado 2+ veces
                preferences["productos_favoritos"].append(producto)
        
        # Detectar categorías preferidas
        if "vegano" in all_text or "vegana" in all_text:
            preferences["categorias_preferidas"].append("Productos veganos")
        if "sin azúcar" in all_text:
            preferences["categorias_preferidas"].append("Productos sin azúcar")
        if "cuadrada" in all_text:
            preferences["categorias_preferidas"].append("Tortas cuadradas")
        
        # Detectar restricciones
        if "alérgico" in all_text or "alergia" in all_text:
            preferences["restricciones_alimentarias"].append("Alergias")
        if "vegetariano" in all_text:
            preferences["restricciones_alimentarias"].append("Vegetariano")
        if "celíaco" in all_text or "gluten" in all_text:
            preferences["restricciones_alimentarias"].append("Sin gluten")
        
        # Detectar ocasiones frecuentes
        if "cumpleaños" in all_text:
            preferences["ocasiones_frecuentes"].append("Cumpleaños")
        if "boda" in all_text:
            preferences["ocasiones_frecuentes"].append("Bodas")
        
        # Estimar presupuesto
        if "económico" in all_text or "barato" in all_text:
            preferences["rango_presupuesto"] = "Económico (< $30.000)"
        elif "premium" in all_text or any(str(p) in all_text for p in range(50000, 100000, 10000)):
            preferences["rango_presupuesto"] = "Premium (> $50.000)"
        else:
            preferences["rango_presupuesto"] = "Medio ($30.000 - $50.000)"
        
        return preferences
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la memoria de largo plazo
        
        Returns:
            Dict con estadísticas
        """
        try:
            # Obtener cantidad de documentos
            collection = self.vectorstore._collection
            count = collection.count()
            
            return {
                "total_conversations": count,
                "collection_name": self.collection_name,
                "persist_directory": self.persist_directory,
                "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
            }
        except Exception as e:
            return {
                "error": str(e),
                "total_conversations": 0
            }
    
    def clear_all(self):
        """PRECAUCIÓN: Elimina toda la memoria de largo plazo"""
        try:
            self.vectorstore.delete_collection()
            print("⚠️ Memoria de largo plazo eliminada")
            
            # Recrear vectorstore vacío
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            self.conversation_count = 0
        except Exception as e:
            print(f"❌ Error eliminando memoria: {e}")


# ==================== FUNCIÓN HELPER ====================

def create_long_term_memory(
    persist_directory: str = "./data/chroma_db",
    collection_name: str = "pasteleria_conversations"
) -> LongTermMemory:
    """
    Factory function para crear memoria de largo plazo
    
    Args:
        persist_directory: Directorio de persistencia
        collection_name: Nombre de la colección
    
    Returns:
        Instancia de LongTermMemory
    """
    return LongTermMemory(
        persist_directory=persist_directory,
        collection_name=collection_name
    )
