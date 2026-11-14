import config
import time
from langchain.chat_models import init_chat_model

groq = init_chat_model("groq:openai/gpt-oss-120b", temperature=0)
gemini = init_chat_model("google_genai:gemini-3.1-flash-lite", temperature=0)

if __name__ == '__main__':
    pregunta = "Explica en 3 lineas que es un agente de IA"
    for nombre, modelo in [("Groq",groq),("Gemini",gemini)]:
        t0 = time.time()
        r = modelo.invoke(pregunta)
        print(f"{nombre:{time.time() - t0}}")
        print ("Tokens:", r.usage_metadata)