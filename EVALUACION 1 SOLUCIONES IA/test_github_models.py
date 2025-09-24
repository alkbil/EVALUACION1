from openai import OpenAI
import os
from dotenv import load_dotenv

def test_github_models():
    """Prueba la conexión con GitHub Models"""
    load_dotenv()
    
    # Verificar variables de entorno
    token = os.getenv('GITHUB_TOKEN')
    base_url = os.getenv('GITHUB_BASE_URL')
    
    print("🧪 Test de GitHub Models")
    print("=" * 50)
    
    if not token or token == "tu_token_de_github_aqui":
        print("❌ GITHUB_TOKEN no configurado")
        print("💡 Obtén tu token en: https://github.com/settings/tokens")
        return False
    
    print(f"🔑 Token: {token[:15]}...")
    print(f"🌐 Base URL: {base_url}")
    
    try:
        client = OpenAI(
            base_url=base_url,
            api_key=token
        )
        
        # Probar con una consulta simple
        response = client.chat.completions.create(
            model="gpt-4",  # Ajusta según lo disponible
            messages=[{"role": "user", "content": "Responde solo con 'GitHub Models OK'"}],
            max_tokens=10,
            temperature=0.1
        )
        
        resultado = response.choices[0].message.content
        print("✅ Conexión exitosa con GitHub Models!")
        print("🤖 Respuesta:", resultado)
        return True
        
    except Exception as e:
        print("❌ Error de conexión:", str(e))
        print("💡 Posibles soluciones:")
        print("1. Verifica que el token tenga permisos suficientes")
        print("2. Revisa que la base URL sea correcta")
        print("3. Confirma que el servicio esté disponible")
        return False

if __name__ == "__main__":
    test_github_models()