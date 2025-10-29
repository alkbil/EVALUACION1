from openai import OpenAI
import os
from dotenv import load_dotenv

def discover_models():
    """Descubre qué modelos están disponibles en GitHub Models"""
    load_dotenv()
    
    token = os.getenv('GITHUB_TOKEN')
    base_url = os.getenv('GITHUB_BASE_URL')
    
    print("🔍 Descubriendo modelos disponibles en GitHub Models...")
    print("=" * 60)
    
    client = OpenAI(base_url=base_url, api_key=token)
    
    # Probar modelos comunes en GitHub/Copilot
    modelos_a_probar = [
        "gpt-3.5-turbo",
        "gpt-35-turbo",  # Versión Azure
        "claude-3-sonnet",  # Anthropic via GitHub
        "claude-3-haiku",
        "mistral-7b",
        "codellama-34b",
        "llama-2-70b",
        "starcoder2-15b"
    ]
    
    for modelo in modelos_a_probar:
        try:
            print(f"🔄 Probando modelo: {modelo}...", end=" ")
            
            response = client.chat.completions.create(
                model=modelo,
                messages=[{"role": "user", "content": "Responde con 'OK'"}],
                max_tokens=5,
                temperature=0.1
            )
            
            resultado = response.choices[0].message.content
            print(f"✅ FUNCIONA - Respuesta: {resultado}")
            
        except Exception as e:
            error_msg = str(e)
            if 'unknown_model' in error_msg:
                print("❌ No disponible")
            elif 'rate_limit' in error_msg:
                print("⏰ Límite de tasa")
            else:
                print(f"⚠️ Error: {error_msg[:50]}...")

if __name__ == "__main__":
    discover_models()