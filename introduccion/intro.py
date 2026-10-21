"""Práctica de la introducción a Python.

Cada función tiene su firma, una docstring con lo que debe hacer y `raise NotImplementedError`.
Reemplace esa línea por la implementación y ejecute, desde la raíz del proyecto:

    uv run pytest introduccion -v          # todas
    uv run pytest introduccion -k saludo   # solo las de un ejercicio

Los ejercicios siguen el orden de la presentación "Python para quien ya programa".
"""

from __future__ import annotations

import functools  # noqa: F401  (lo necesita el ejercicio 12)
import math  # noqa: F401  (lo necesita el ejercicio 8)
from collections.abc import Callable, Iterator
from dataclasses import dataclass


# 1. Un programa es un archivo ----------------------------------------------------------
def saludo(nombre: str, formal: bool = False) -> str:
    """Saludo para `nombre`, sin los espacios que traiga a los lados.

    saludo("Ana") → "Hola, Ana"
    saludo("Ana", formal=True) → "Buenos días, Ana."
    Pista: f-strings y el método strip.
    """
    if formal:
        return f"Buenos días, {nombre.strip()}"
    else:
        return f"Hola, {nombre.strip()}"

# 2. Bloques y condiciones --------------------------------------------------------------
def clasificar_temperatura(t: float) -> str:
    """Clasifica la temperatura de un modelo de IA.

    Menor que 0.3 → "precisa"; de 0.3 a 1 (incluido) → "equilibrada"; mayor que 1 → "creativa".
    Si es negativa o mayor que 2: ValueError.
    """
    if t < 0 or t > 2:
        raise ValueError(f"Fuera de rango: {t}, verifique por favor") 
    elif t < 0.3:
        print ("Precisa")
    elif t >= 0.3 or t <= 1:
        print ("Equilibrada")
    else:
        print ("Creativa")

# 3. Recorrer y contar ------------------------------------------------------------------
def contar_vocales(texto: str) -> dict[str, int]:
    """Cuántas veces aparece cada vocal (a, e, i, o, u), sin importar mayúsculas.

    Siempre devuelve las cinco claves, aunque alguna valga 0. El texto viene sin tildes.
    contar_vocales("Hola Mundo") → {"a": 1, "e": 0, "i": 0, "o": 2, "u": 1}
    """
    #Por extensión
    vocales = {"a": 1, "e": 0, "i": 0, "o": 0, "u": 0}
    #Por comprensión
    conteo = {v: 0 for v in "aeiou"}
    for letra in texto.lower():
        if letra in conteo:
            conteo[letra] += 1 

    return conteo

# 4. Funciones que devuelven varios valores ---------------------------------------------
def resumen(numeros: list[float]) -> tuple[float, float, float]:
    """(mínimo, máximo, promedio) de la lista. Lista vacía: ValueError.
    min(), max(), len(), sum()
    resumen([4, 1, 7]) → (1, 7, 4.0)
    """
    if numeros == []:        
        raise ValueError(f"No existen datos") 
    return min(numeros), max(numeros), sum(numeros) / len(numeros)

# 5. Al llamar, se pasa el objeto -------------------------------------------------------
def agregar_etiqueta(etiquetas: list[str] | None, nueva: str) -> list[str]:
    """Una lista con las etiquetas y `nueva` al final, si no estaba ya.

    No modifica la lista que recibe: devuelve otra. Con None, empieza de una lista vacía.
    agregar_etiqueta(["rrhh"], "legal") → ["rrhh", "legal"]
    """
    #Opción 1
    base = [] if etiquetas is None else etiquetas.copy()
    #Opción 2
    # base = [] if etiquetas is None else list(etiquetas)    
    # #Opción 3
    # base = [] if etiquetas is None else etiquetas[:]
    if nueva not in base:
        base.append(nueva)
    return base

# 6. Comprensiones ----------------------------------------------------------------------
def largos(palabras: list[str]) -> dict[str, int]:
    """Diccionario palabra → largo, sin las palabras vacías o de solo espacios.

    Con una comprensión de diccionario. largos(["sol", "", "luna"]) → {"sol": 3, "luna": 4}
    """
    #return {p: len(p) for p in palabras if p.strip() }
    return {p: len(p) for p in palabras if len(p.strip()) > 0 }

# 7. Errores ----------------------------------------------------------------------------
def a_entero(texto: str, defecto: int = 0) -> int:
    """El entero que representa el texto, o `defecto` si no es un entero válido.

    a_entero(" 7 ") → 7     a_entero("4.2") → 0     a_entero("x", defecto=-1) → -1
    Pista: try / except ValueError.
    """
    try:
        return int(texto)
    except ValueError:
        return "defecto"


# 8. Módulos de la biblioteca estándar --------------------------------------------------
def hipotenusa(a: float, b: float) -> float:
    """La hipotenusa de un triángulo rectángulo, redondeada a 2 decimales.

    Use math.sqrt (el import ya está arriba). hipotenusa(1, 1) → 1.41
    """
    # c = a**2 + b**2
    # return round(math.sqrt(c),2)

    return round(math.sqrt(a**2+b**2),2)

# 9. Clases -----------------------------------------------------------------------------
class Contador:
    """Contador que solo sube.

    Contador() empieza en 0; Contador(10), en 10. `valor` se lee como atributo (una property)
    y no se puede asignar. incrementar(paso=1) suma; con paso <= 0, ValueError. reiniciar()
    vuelve a 0. repr(c) → "Contador(6)".
    """

    def __init__(self, inicio: int = 0) -> None:
        self._valor = inicio

    @property
    def valor(self) -> int:
        return self._valor

    def incrementar(self, paso: int = 1) -> None:
        if paso <= 0:
            raise ValueError(f"El paso debe ser mayor a 0.")
        self._valor += paso

    def reiniciar(self) -> None:
        self._valor = 0

    def __repr__(self) -> str:
        return f"Contador({self._valor})"

# 10. dataclass -------------------------------------------------------------------------
@dataclass(frozen=True)
class Producto:
    """Producto inmutable. Precio negativo: ValueError al crearlo.

    `precio_con_iva` es una property: el precio por 1.19, redondeado a 2 decimales.
    """

    nombre: str
    precio: float
    etiquetas: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo")

    @property
    def precio_con_iva(self) -> float:
        return round (self.precio * 1.19,2)


# 11. Generadores -----------------------------------------------------------------------
def lineas_numeradas(texto: str) -> Iterator[str]:
    """Genera "1: texto", "2: texto"… por cada línea no vacía, sin espacios a los lados.

    Las líneas vacías no se cuentan. Debe ser un generador (yield), no devolver una lista.
    list(lineas_numeradas("a\\n\\n b ")) → ["1: a", "2: b"]
    """

    numero = 0
    for linea in texto.splitlines():
        if linea.strip():
            numero += 1
            yield f"{numero}: {linea.strip()}"    

def main() -> None:
    print(saludo("Rafael", False))
    clasificar_temperatura(1.1)
    print(contar_vocales("Hola ChamKito"))
    print(resumen([4,1,7]))    
    print(a_entero(" 54875 "))
    print(hipotenusa(5,6))
    c = Contador()
    print(c)
    c.incrementar(paso = 10)
    print(c)
    c.reiniciar()
    print(c)

    p = Producto("Prueba",145.4)
    print(p.precio_con_iva)
    # p2 = Producto("Prueba2",-15)
    # print(p2.precio_con_iva)

    gen = lineas_numeradas("primera\n\n  segunda  \n")
    print(list(gen))
    #print(next(gen))

    print(textos("prueba de todo en minuscula"))

# 12. Decoradores -----------------------------------------------------------------------
def en_mayusculas(funcion: Callable[..., str]) -> Callable[..., str]:
    """Decorador: la función decorada devuelve su resultado en mayúsculas.

    Debe aceptar cualquier argumento (*args, **kwargs) y conservar el nombre y la docstring
    de la original con functools.wraps (el import ya está arriba).
    """

    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        p = funcion(*args, **kwargs)
        return p.upper()    
    return envoltura

@en_mayusculas
def textos(txt: str):
    return txt

if __name__ == "__main__":
    main()
