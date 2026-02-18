"""Funciones auxiliares."""
from pathlib import Path
def check_dir(path: str | Path) -> Path:
    """
    Verifica que el directorio exista.
    Si no existe, lo crea.

    Returns:
        Path object del directorio validado.
    """
    path = Path(path)

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    return path