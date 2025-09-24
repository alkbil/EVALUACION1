import os
from openai import OpenAI
from dotenv import load_dotenv

def test_openai_connection():
    # Cargar variables del archivo .env
    load_dotenv()
    
    # Verificar si la API Key está configurada
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == "sk-tu-key-real-aqui":
        print("❌ ERROR: API Key no configurada")
        print("💡 Sigue estos pasos:")
        print("1. Ve a: https://platform.openai.com/api-keys")
        print("2. Crea una nueva API Key")
        print("3. Pégala en el archivo .env")
        print("4. Reemplaza: sk-tu-key-real-aqui")
        return False
    
    try:
        print("🔑 API Key encontrada:", api_key[:20] + "..." + api_key[-4:])
        
        client = OpenAI(api_key=api_key)
        
        print("🔄 Probando conexión con OpenAI...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Usar modelo económico para prueba
            messages=[{"role": "user", "content": "Responde solo con 'Conexión exitosa'"}],
            max_tokens=10,
            temperature=0.1
        )
        
        resultado = response.choices[0].message.content
        print("✅ Conexión exitosa con OpenAI!")
        print("🤖 Respuesta:", resultado)
        return True
        
    except Exception as e:
        print("❌ Error de conexión:", str(e))
        return False

if __name__ == "__main__":
    print("🧪 Test de conexión OpenAI")
    print("=" * 40)
    test_openai_connection()