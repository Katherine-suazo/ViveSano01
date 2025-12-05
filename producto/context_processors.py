from .models import CategoriaProducto


def categorias_existentes(request):
    """Context processor that indicates whether at least one CategoriaProducto exists.

    Returns:
        dict: {'has_categorias': True/False}
    """
    try:
        has = CategoriaProducto.objects.exists()
    except Exception:
        has = False
    return {'has_categorias': has}
