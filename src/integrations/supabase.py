import json
from urllib.parse import urlencode

from fastapi import HTTPException
from js import AbortSignal, Object, fetch
from pyodide.ffi import to_js


async def consultar_tabla(env, tabla: str, parametros: dict):
    base_url = getattr(env, "SUPABASE_URL", None)
    secret_key = getattr(env, "SUPABASE_SECRET_KEY", None)

    if not base_url or not secret_key:
        raise HTTPException(
            status_code=503,
            detail="Falta configurar la conexion a Supabase.",
        )

    query = urlencode(parametros)
    url = f"{str(base_url).rstrip('/')}/rest/v1/{tabla}?{query}"

    options = to_js(
        {
            "method": "GET",
            "headers": {
                "apikey": str(secret_key),
                "Accept": "application/json",
            },
        },
        dict_converter=Object.fromEntries,
    )
    options.signal = AbortSignal.timeout(10000)

    try:
        response = await fetch(url, options)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="No se pudo contactar con Supabase.",
        ) from None

    if not response.ok:
        print(f"Consulta a Supabase: HTTP {response.status}")
        raise HTTPException(
            status_code=502,
            detail="Supabase no pudo completar la consulta.",
        )

    return json.loads(await response.text())