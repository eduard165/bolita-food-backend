from fastapi import APIRouter, Request

from integrations.supabase import consultar_tabla

router = APIRouter(prefix="/api", tags=["Catalogo"])


@router.get("/menu")
async def obtener_menu(request: Request):
    productos = await consultar_tabla(
        env=request.scope["env"],
        tabla="productos",
        parametros={
            "select": "id,nombre,descripcion",
            "activo": "eq.true",
            "order": "nombre.asc",
        },
    )

    return {
        "productos": productos,
        "cantidad": len(productos),
    }