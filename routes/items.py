from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from pathlib import Path
import json
import threading

from models.items import Item, ItemCreate

router = APIRouter()
_lock = threading.Lock()
_DATA_FILE = Path(__file__).resolve().parents[1] / "db" / "data.json"

def _read_items() -> List[dict]:
    if not _DATA_FILE.exists():
        return []
    with _DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def _write_items(items: List[dict]) -> None:
    _DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with _DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

@router.get("/", response_model=List[Item], summary="Listar items")
def list_items():
    return _read_items()

@router.get("/id/{item_id}", response_model=Item, summary="Obtener item por id")
def get_item(item_id: int):
    items = _read_items()
    for it in items:
        if it["id"] == item_id:
            return it
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED, summary="Crear item")
def create_item(item: ItemCreate):
    with _lock:
        items = _read_items()
        next_id = (max((i["id"] for i in items), default=0) + 1) if items else 1
        new = item.dict()
        new["id"] = next_id
        items.append(new)
        _write_items(items)
    return new

@router.put("/{item_id}", response_model=Item, summary="Actualizar item (reemplazo)")
def update_item(item_id: int, item: ItemCreate):
    with _lock:
        items = _read_items()
        for idx, it in enumerate(items):
            if it["id"] == item_id:
                updated = item.dict()
                updated["id"] = item_id
                items[idx] = updated
                _write_items(items)
                return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar item")
def delete_item(item_id: int):
    with _lock:
        items = _read_items()
        for idx, it in enumerate(items):
            if it["id"] == item_id:
                items.pop(idx)
                _write_items(items)
                return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")


@router.get("/paged", response_model=List[Item], summary="Listar items paginados con limit/offset")
def list_items_paginated(
    limit: int = Query("10", description="Número máximo de items a retornar (entero)"),
    offset: int = Query("0", description="Desplazamiento inicial (entero)")
):
    """
    Convierte limit y offset (vienen como strings) a enteros y valida.
    Retorna error 400 si no son enteros o si están fuera de rango.
    Ejemplo: GET /items/paged?limit=20&offset=40
    """
    # conversión y validación de tipo
    try:
        limit_i = int(limit)
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El parámetro 'limit' debe ser un entero")

    try:
        offset_i = int(offset)
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El parámetro 'offset' debe ser un entero")

    # validaciones de rango
    if limit_i < 1 or limit_i > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro 'limit' debe estar entre 1 y 100"
        )
    if offset_i < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro 'offset' debe ser mayor o igual a 0"
        )

    items = _read_items()
    start = offset_i
    end = offset_i + limit_i
    return items[start:end]