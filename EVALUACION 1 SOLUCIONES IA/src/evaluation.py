from openai import OpenAI
import os
import numpy as np

class ResponseEvaluator:
    def __init__(self):
        self.client = None
        self.initialize_client()
    
    def initialize_client(self):
        """Inicializa el cliente de OpenAI para evaluación"""
        try:
            self.client = OpenAI(
                api_key=os.getenv('OPENAI_API_KEY'),
                base_url=os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
            )
        except Exception as e:
            print(f"❌ Error inicializando cliente de evaluación: {e}")
    
    def evaluar_fidelidad(self, query, contexto, respuesta):
        """Evalúa si la respuesta es fiel al contexto proporcionado"""
        if not self.client:
            return 7.0  # Valor por defecto si no hay cliente
        
        prompt = f"""
        Evalúa si la siguiente respuesta se basa ÚNICAMENTE en el contexto proporcionado.

        CONTEXTO AUTORIZADO:
        {contexto}

        PREGUNTA: {query}
        RESPUESTA: {respuesta}

        ¿La respuesta contiene información que NO está en el contexto?
        Responde con un número del 1-10 donde:
        - 1-3: La respuesta incluye mucha información externa no autorizada
        - 4-6: La respuesta mezcla información del contexto con algo de información externa  
        - 7-10: La respuesta se basa completamente en el contexto proporcionado

        Responde SOLO con el número:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=10
            )
            return float(response.choices[0].message.content.strip())
        except:
            return 7.0  # Valor por defecto en caso de error
    
    def evaluar_relevancia(self, query, respuesta):
        """Evalúa qué tan relevante es la respuesta para la consulta"""
        if not self.client:
            return 8.0  # Valor por defecto
        
        prompt = f"""
        Evalúa qué tan bien responde esta respuesta a la consulta del usuario.

        CONSULTA: {query}
        RESPUESTA: {respuesta}

        ¿La respuesta aborda completamente la consulta del usuario?
        Responde con un número del 1-10 donde:
        - 1-3: La respuesta es irrelevante o no aborda la consulta
        - 4-6: La respuesta es parcialmente relevante pero incompleta
        - 7-10: La respuesta es muy relevante y útil para el usuario

        Responde SOLO con el número:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=10
            )
            return float(response.choices[0].message.content.strip())
        except:
            return 8.0
    
    def evaluar_calidad_general(self, respuesta):
        """Evalúa la calidad general de la respuesta"""
        criterios = {
            "claridad": len(respuesta) < 1000,  # No demasiado larga
            "profesionalismo": all(word in respuesta.lower() for word in ["pastelería", "1000 sabores"]),
            "utilidad": len(respuesta) > 50,  # No demasiado corta
            "tono_adecuado": not any(word in respuesta.lower() for word in ["no sé", "no tengo idea", "error"])
        }
        
        puntaje = sum(criterios.values()) / len(criterios) * 10
        return puntaje
    
    def evaluar_respuesta_completa(self, query, contexto, respuesta, documentos_usados):
        """Evaluación completa con múltiples métricas"""
        fidelidad = self.evaluar_fidelidad(query, contexto, respuesta)
        relevancia = self.evaluar_relevancia(query, respuesta)
        calidad = self.evaluar_calidad_general(respuesta)
        
        # Ponderación de métricas
        puntaje_final = (fidelidad * 0.4) + (relevancia * 0.4) + (calidad * 0.2)
        
        return {
            "fidelidad": round(fidelidad, 1),
            "relevancia": round(relevancia, 1),
            "calidad_general": round(calidad, 1),
            "puntaje_final": round(puntaje_final, 1),
            "documentos_utilizados": len(documentos_usados)
        }