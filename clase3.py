class Persona:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

    def __repr__(self) -> str:  # cómo se muestra
        return f"Persona({self.nombre!r})"

    def __eq__(self, otro: object) -> bool:  # qué significa "igual"
        return isinstance(otro, Persona) and otro.nombreempl == self.nombre


class Empleado:
    def __init__(self, nombreempl: str, identificacion: str) -> None:
        super().__init__(nombreempl)
        self.identificacion = identificacion


p = Empleado("Ramon", "1050")
p.p == Persona("Ramon")
p


from dataclasses import dataclass, field


@dataclass
class Persona:
    nombre: str
    apellido: str
    salario: int = 0
    etiquetas: list[str] = field(default_factory=list)


f = Persona("hola")
f == Persona("hola", "Ramon", " Castillo, con un salario de: ", 450, [])
f.salario, f.etiquetas
