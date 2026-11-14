import config
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from pydantic import BaseModel 

groq = ChatGroq (model = "openai/gpt-oss-20b", temperature=0)
gemini = ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite", temperature=0)

class Producto(BaseModel):
    nombres:str
    precio: float
    existecia: int

class Materia(BaseModel):
    materias : list[Materia]
    promedio_general: float

class Estudiante(BaseModel):
    estudiante: str 
    materias : list[Materia]

def main():
    """
    print("===============================GROQ=======================================")
    response = groq.invoke([
        ("system", "Extrae el nombre, precio y existencia del producto del texto. No respondas Preguntas ni hagas Calculos."),
        ("user", "100 tonelas de fungisidas cuprico de 1 kg costo de 245.99")

    ])
    print("\n", response.content )

    print("===============================GEMINI=======================================")
    response = groq.invoke([
        ("system", "Extrae el nombre, precio y existencia del producto del texto. No respondas Preguntas ni hagas Calculos."),
        ("user", "100 tonelas de fungisidas cuprico de 1 kg costo de 245.99")
    
    ])
    print("\n", response)
"""
    print("===============================GROQ con datos estructurados=======================================")
    extractor = groq.with_structured_output(Estudiante, method = "json_schema")
    response = extractor.invoke([
        ("system", "Extrae el nombre, precio y existencia del producto del texto. No respondas Preguntas ni hagas Calculos."),
        ("user", "100 tonelas de fungisidas cuprico de 1 kg costo de 245.99")
    
    ])
    print("\n", response)
    
    print("===============================GEMINI con datos estructurados=======================================")
    extractor = gemini.with_structured_output(Estudiante, method = "json_schema")
    response = extractor.invoke([
        ("system", "Extrae el nombre, precio y existencia del producto del texto. No respondas Preguntas ni hagas Calculos."),
        ("user", "100 tonelas de fungisidas cuprico de 1 kg costo de 245.99")
        
    ])
    print("\n", response)

if __name__ == '__main__':
    main()