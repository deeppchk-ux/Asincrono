import random
import aiohttp
import asyncio

# Lista de proxies funcionales
PROXIES = [
    "p.webshare.io:80:ytaeqbbo-rotate:xcjd9s05jqa2",
    "p.webshare.io:80:bglqtdcj-rotate:c92z8ep885ls",
    "p.webshare.io:80:gzxegjwb-rotate:tfdw4lqywa84",
    "p.webshare.io:80:rcnrlzqv-rotate:kk5694q21xfe"
]

def get_random_proxy():
    """
    Selecciona un proxy aleatorio de la lista y lo formatea para aiohttp.
    Retorna un diccionario compatible con aiohttp y None en caso de error.
    """
    if not PROXIES:
        print("DEBUG: Lista de proxies vacía")
        return None, None
    proxy = random.choice(PROXIES)
    try:
        ip, port, username, password = proxy.split(':')
        proxy_url = f"http://{username}:{password}@{ip}:{port}"
        print(f"DEBUG: Proxy HTTP seleccionado: {proxy_url}")
        return proxy_url, None  # aiohttp usa proxy_url directamente como string
    except ValueError as e:
        print(f"DEBUG: Formato de proxy inválido: {proxy}, Error: {e}")
        return None, None

async def fetch_url(url, proxy_url=None):
    """
    Realiza una solicitud HTTP asíncrona a una URL usando aiohttp con un proxy opcional.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxy_url) as response:
                if response.status == 200:
                    content = await response.text()
                    print(f"DEBUG: Solicitud exitosa a {url} con proxy {proxy_url}")
                    return content
                else:
                    print(f"DEBUG: Error en solicitud a {url}, status: {response.status}")
                    return None
    except Exception as e:
        print(f"DEBUG: Error en solicitud a {url}, Error: {e}")
        return None

async def main():
    """
    Función principal asíncrona para probar la selección de proxy y solicitud HTTP.
    """
    url_to_fetch = "https://api.ipify.org"  # Ejemplo: URL para obtener la IP
    proxy_url, error = get_random_proxy()
    
    if proxy_url:
        result = await fetch_url(url_to_fetch, proxy_url)
        if result:
            print(f"Resultado: {result}")
        else:
            print("No se pudo obtener el contenido.")
    else:
        print("No se pudo obtener un proxy válido.")

# Ejecutar el código asíncrono
if __name__ == "__main__":
    asyncio.run(main())