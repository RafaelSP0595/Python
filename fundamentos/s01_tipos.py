"""Fundamentos 1: tipos y contenedores (sesión 1, unos 40 min). Implemente cada función y ejecute:

    uv run pytest fundamentos/test_s01_tipos.py -q

Las pruebas son la especificación: léalas antes de empezar. Solo biblioteca estándar.
"""

from __future__ import annotations

from decimal import Decimal


# 1. Texto -------------------------------------------------------------------
def limpiar_etiquetas(texto: str) -> list[str]:
    """'Legal, RRHH ,, legal' → ['legal', 'rrhh'].

    Separa por comas, quita espacios, pasa a minúsculas (casefold), descarta vacías
    y elimina repetidas conservando el orden de la primera aparición.
    """
    # vsplit = texto.split()
    # for a in vsplit:
    #     a.casefold().strip()
    labels = (e.strip().casefold() for e in texto.split(","))
    return list(dict.fromkeys(e for e in labels if e))


# 2. Números y dinero --------------------------------------------------------
def total_con_iva(precios: list[str], iva: str = "0.19") -> Decimal:
    """Suma precios escritos como texto y aplica el IVA.

    Redondea a 2 decimales, con la mitad hacia arriba.

    Lanza ValueError si algún precio no es un número válido o es negativo.
    """
    # vsum = Decimal("0")
    # for a in precios:
    #     try:
    #         valor = Decimal(a)
    #     except InvalidOperation:
    #         raise ValueError(f"Uno de los valores indicados no es válido: {a!r}")
    #     if not valor.is_finite() or valor < 0:
    #         raise ValueError(f"Uno de los valores indicados no es válido: {a!r}")
    #     vsum += valor

    # return (vsum * (1 + Decimal(iva))).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    return "precios"


# 3. Validar entradas (código seguro) ----------------------------------------
def parsear_limite(valor: str | None, *, defecto: int = 5, maximo: int = 50) -> int:
    """Convierte el parámetro 'limite' que llega de una petición.

    None o texto vacío → defecto. Texto que no es entero → ValueError.
    Fuera de 1..maximo → ValueError. Ojo: "0" es un valor explícito, no vacío.
    """
    if valor is None or valor.strip():
        return defecto

    try:
        limite = int(valor)
    except ValueError:
        raise ValueError("limite debe ser un entero") from None
    if not 1 <= limite <= maximo:
        raise ValueError("limite fuera de rango")


# 4. Datos, no código (código seguro) ----------------------------------------
def leer_lista_enteros(texto: str) -> list[int]:
    """'[1, 2, 3]' → [1, 2, 3], sin usar eval.

    Lanza ValueError si el texto no es una lista o si algún elemento no es entero
    (los booleanos tampoco cuentan como enteros).
    """
    import ast
    # try:
    #     ast.literal_eval(texto)
    # except ValueError:
    #     raise ValueError("El texto no es una lista o contiene valores ") from None

    # if not isinstance(texto, str):
    #     raise ValueError("El texto no es una lista o contiene valores ") from None
    try:
        valor = ast.literal_eval(texto)
    except (ValueError, SyntaxError):
        raise ValueError("El texto contiene valores ") from None

    if not isinstance(valor, list):
        raise ValueError("El texto no es una lista ") from None

    if not all(type(x) is int for x in valor):
        raise ValueError("No todos los elementos son enteros ") from None

    return valor


# 5. Diccionarios y conjuntos ------------------------------------------------
def indice_invertido(docs: dict[str, str]) -> dict[str, set[str]]:
    """Cada palabra (en minúsculas, separada por espacios) apunta a los ids que la contienen.

    {'d1': 'Vacaciones anuales', 'd2': 'vacaciones'}
    → {'vacaciones': {'d1', 'd2'}, 'anuales': {'d1'}}
    """
    indice: dict[str, set[str]] = {}
    for id_doc, text in docs.items():
        for p in text.lower().split():
            indice.setdefault(p, set()).add(id_doc)
    return indice


# 6. Copias y mutabilidad ----------------------------------------------------
def fusionar_config(base: dict[str, object], *capas: dict[str, object]) -> dict[str, object]:
    """Une configuraciones anidadas: cada capa sobrescribe a la anterior, clave por clave.

    Si en ambas un valor es dict, se fusionan recursivamente. No debe modificar
    `base` ni las capas, ni compartir con ellas diccionarios anidados.
    """
    import copy

    resultado = copy.deepcopy(base)
    for capa in capas:
        for clave, valor in capa.items():
            actual = resultado.get(clave)
            if isinstance(actual, dict) and isinstance(valor, dict):
                resultado[clave] = fusionar_config(actual, valor)
            else:
                resultado[clave] = copy.deepcopy(valor)
    return resultado
