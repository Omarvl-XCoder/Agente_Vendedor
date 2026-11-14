from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from modelos import groq,gemini
from herramientas import calcular_dosis, convertir_moneda

PROMPT=("Eres un vendedor de una tienda agricola. Busca en el catalogo antes de dar precio." 
        "Nunca inventes productos. antes de registrar un pedido, resume producto, cantidad,total,"
        "y nombre del cliente , y pide confirmacion explicita")

#crear  el agente 

vendedor = create_agent(
    modelo = groq,
    tools=[calcular_dosis,convertir_moneda],
    system_prompt = PROMPT,
    checkpointer= InMemorySaver(),
)

def chat():
    cfg = {"configurable" : {"thread_id": "mostrador-1"}} #
    print ("Vendedor disponible. 'exit' o 'salir' para terminar")
    while True:
        texto = input("Client: ").strip()
        if texto.upper() in ('SALIR', 'EXIT'):
            break
        if not texto:
            continue
        try:
            response= vendedor.invoke({"messages": [{"role": "user","conten": texto}]},cfg)
            print(f"Vendedor: {response["messages"][-1].content}\n")
        except Exception as e: 
            print (f"ocurrio un error: {e}")

if __name__ == '__main__':
    chat()


"""tarea para la herramienta del tipo de cambio 
{
"pesos": 100
"tipo de cambio": 18.5,
"resultado": "54.05 dolares",
}

que regrese un json en ese formato 
"""

