from langchain.tools import tool 
import json 
from config import supabase

@tool
def calcular_dosis(hectareas: float, litros_por_ha: float) -> str: 
    """Calcula los litros totales de un producto para una superficie.
    Usar cuando el usuario pregunte cuanto producto necesita."""
    return f"{hectareas * litros_por_ha:.2f} litros"

@tool 
def convertir_moneda(pesos: float, tipo_cambio: float = 18.5) -> str:
    """Convierte pesos mexicanos a dolares con el tipo de cambio especificado y regresa un JSON."""
    dolares = pesos / tipo_cambio
    resultado = {
        "pesos": pesos,
        "tipo de cambio": tipo_cambio,
        "resultado": f"{dolares:.2f} dolares"
    }
    return json.dumps(resultado, ensure_ascii=False, indent=2)

@tool 
def buscar_productos(texto: str = "", categoria: str = "", cultivo: str = "") -> str:
    """Busca productos del catalogo, filtros opcionales: texto (parte del nombre),
    categoria (fungicida, fertilizante, herramienta) y cultivo (aguacate, berries, general).
    Devuelve id, nombre, precio y existencia."""
    q = supabase.table("productos").select("id, nombre, categoria, cultivo, precio, existencia")
    if texto:
        q = q.ilike("nombre", f"%{texto}%")
    if categoria:
        q = q.ilike("categoria", f"%{categoria}%")
    if cultivo:
        q = q.ilike("cultivo", f"%{cultivo}%")
    datos = q.limit(10).execute().data
    if not datos:
        return "No existen registros con esos filtros"
    return json.dumps(datos, ensure_ascii=False)

@tool
def registrar_pedido(producto_id: int, cantidad: int, cliente: str) -> str:
    """Registra un pedido. Usar solamente despues de que el cliente confirme 
    producto, cantidad y su nombre."""
    res = supabase.table("productos").select("existencia, nombre").eq("id", producto_id).execute().data
    if not res: 
        return f"No existe el producto con ID='{producto_id}'"
    pro = res[0]
    if pro["existencia"] < cantidad:
        return f"No hay existencia suficiente, hay: {pro['existencia']} de {pro['nombre']}."

    supabase.table("pedidos").insert({"producto_id": producto_id, "cantidad": cantidad, "cliente": cliente}).execute()
    supabase.table("productos").update({"existencia": pro["existencia"] - cantidad}).eq("id", producto_id).execute()
    return f"Pedido registrado exitosamente: {cantidad} de {pro['nombre']} para {cliente}."