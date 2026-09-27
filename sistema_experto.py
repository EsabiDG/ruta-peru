"""
sistema_experto.py
Motor de recomendación de destinos turísticos del Perú.
"""

from dataclasses import dataclass
from typing import Callable, List, Set, Dict


@dataclass
class Regla:
    nombre: str
    condicion: Callable[[Set[str]], bool]
    conclusion: str
    certeza: float
    explicacion: str


# Base de hechos: 11 destinos × 10 características = 110 hechos
base_hechos: Dict[str, List[str]] = {

    "Cusco": [
        "historia", "arqueologia", "montaña", "cultura", "patrimonio",
        "trekking", "tradiciones", "fotografia", "gastronomia", "aventura"
    ],

    "Machu Picchu": [
        "historia", "arqueologia", "montaña", "patrimonio", "naturaleza",
        "trekking", "cultura", "fotografia", "aventura", "paisaje"
    ],

    "Arequipa": [
        "historia", "cultura", "arquitectura", "patrimonio", "gastronomia",
        "montaña", "naturaleza", "fotografia", "aventura", "paisaje"
    ],

    "Puno": [
        "historia", "cultura", "tradiciones", "montaña", "lago",
        "naturaleza", "fotografia", "gastronomia", "patrimonio", "aventura"
    ],

    "Paracas": [
        "costa", "playa", "naturaleza", "mar", "fotografia",
        "aventura", "ecoturismo", "desierto", "fauna", "paisaje"
    ],

    "Ica": [
        "desierto", "aventura", "naturaleza", "cultura", "gastronomia",
        "fotografia", "paisaje", "oasis", "costa", "ecoturismo"
    ],

    "Huaraz": [
        "montaña", "trekking", "naturaleza", "aventura", "fotografia",
        "paisaje", "ecoturismo", "lagunas", "cultura", "andino"
    ],

    "Trujillo": [
        "historia", "arqueologia", "cultura", "patrimonio", "gastronomia",
        "costa", "playa", "fotografia", "tradiciones", "arquitectura"
    ],

    "Chiclayo": [
        "historia", "arqueologia", "cultura", "patrimonio", "gastronomia",
        "tradiciones", "fotografia", "arquitectura", "museos", "aventura"
    ],

    "Tarapoto": [
        "selva", "naturaleza", "aventura", "ecoturismo", "cascadas",
        "fotografia", "fauna", "gastronomia", "paisaje", "cultura"
    ],

    "Iquitos": [
        "selva", "naturaleza", "ecoturismo", "fauna", "aventura",
        "fotografia", "gastronomia", "paisaje", "cultura", "amazonia"
    ]
}


# Convertir los hechos a un conjunto
hechos_conocimiento: Set[str] = set()
for destino, caracteristicas in base_hechos.items():
    destino_id = destino.lower().replace(" ", "_")
    for c in caracteristicas:
        hechos_conocimiento.add(f"{destino_id}_{c}")

CANTIDAD_HECHOS = len(hechos_conocimiento)


def verificar_base_hechos() -> None:
    print("Cantidad de hechos:", CANTIDAD_HECHOS)
    if CANTIDAD_HECHOS >= 100:
        print("La base de conocimientos cumple el requisito.")
        print(f"Total de hechos: {CANTIDAD_HECHOS}")
    else:
        raise ValueError(f"Faltan hechos: {CANTIDAD_HECHOS}")


# Nombres legibles de los destinos
nombres_destinos: Dict[str, str] = {
    "recomendar_cusco": "Cusco",
    "recomendar_machu_picchu": "Machu Picchu",
    "recomendar_arequipa": "Arequipa",
    "recomendar_puno": "Puno",
    "recomendar_paracas": "Paracas",
    "recomendar_ica": "Ica",
    "recomendar_huaraz": "Huaraz",
    "recomendar_trujillo": "Trujillo",
    "recomendar_chiclayo": "Chiclayo",
    "recomendar_tarapoto": "Tarapoto",
    "recomendar_iquitos": "Iquitos"
}


# Reglas de producción R1–R11
base_de_conocimiento: List[Regla] = [
    Regla("R1",  lambda h: "interes_historia" in h and "interes_arqueologia" in h,
          "recomendar_cusco", 0.95,
          "Buscas historia y arqueología, dos elementos que definen a Cusco."),

    Regla("R2",  lambda h: "interes_arqueologia" in h and "interes_montaña" in h,
          "recomendar_machu_picchu", 0.98,
          "Arqueología y montaña se unen en Machu Picchu, la ciudadela Inca."),

    Regla("R3",  lambda h: "interes_cultura" in h and "interes_gastronomia" in h,
          "recomendar_arequipa", 0.91,
          "Cultura y gastronomía son el sello de Arequipa, la Ciudad Blanca."),

    Regla("R4",  lambda h: "interes_cultura" in h and "interes_tradiciones" in h,
          "recomendar_puno", 0.88,
          "Cultura y tradiciones se viven en Puno, capital folclórica del Perú."),

    Regla("R5",  lambda h: "interes_costa" in h and "interes_naturaleza" in h,
          "recomendar_paracas", 0.93,
          "Costa y naturaleza se encuentran en Paracas, reserva marina única."),

    Regla("R6",  lambda h: "interes_desierto" in h and "interes_aventura" in h,
          "recomendar_ica", 0.90,
          "Desierto y aventura son el alma de Ica, con sus dunas y el oasis de Huacachina."),

    Regla("R7",  lambda h: "interes_montaña" in h and "interes_trekking" in h,
          "recomendar_huaraz", 0.96,
          "Montaña y trekking son la esencia de Huaraz, puerta de la Cordillera Blanca."),

    Regla("R8",  lambda h: "interes_historia" in h and "interes_costa" in h,
          "recomendar_trujillo", 0.92,
          "Historia y costa se combinan en Trujillo, con sus huacas y su litoral."),

    Regla("R9",  lambda h: "interes_arqueologia" in h and "interes_gastronomia" in h,
          "recomendar_chiclayo", 0.89,
          "Arqueología y gastronomía destacan en Chiclayo, con el Señor de Sipán."),

    Regla("R10", lambda h: "interes_selva" in h and "interes_aventura" in h,
          "recomendar_tarapoto", 0.94,
          "Selva y aventura son el sello de Tarapoto, con sus cascadas y cataratas."),

    Regla("R11", lambda h: "interes_selva" in h and "interes_fauna" in h,
          "recomendar_iquitos", 0.97,
          "Selva y fauna son protagonistas en Iquitos, puerta de la Amazonía."),
]


class MotorDeReglas:

    def __init__(self, base_de_conocimiento: List[Regla]):
        self.base_de_conocimiento = base_de_conocimiento

    def inferir(self, hechos_iniciales: Set[str]):
        hechos = set(hechos_iniciales)
        reglas_activadas: List[Regla] = []

        cambios = True
        while cambios:
            cambios = False
            for regla in self.base_de_conocimiento:
                if regla.condicion(hechos):
                    if regla.conclusion not in hechos:
                        hechos.add(regla.conclusion)
                        reglas_activadas.append(regla)
                        cambios = True

        return hechos, reglas_activadas


def recomendar(intereses_usuario: Set[str]) -> Dict:
    intereses = set(intereses_usuario)
    intereses.discard("ninguno")

    if "montana" in intereses:
        intereses.discard("montana")
        intereses.add("montaña")

    nombres_bonitos = {
        "historia": "Historia",
        "arqueologia": "Arqueología",
        "montaña": "Montaña",
        "cultura": "Cultura",
        "gastronomia": "Gastronomía",
        "tradiciones": "Tradiciones",
        "costa": "Costa",
        "desierto": "Desierto",
        "selva": "Selva",
        "trekking": "Trekking",
        "aventura": "Aventura",
        "naturaleza": "Naturaleza",
        "fauna": "Fauna",
    }

    if not intereses:
        return {
            "encontrado": False,
            "recomendacion": None,
            "certeza": 0.0,
            "regla": None,
            "explicacion": "No seleccionaste ningún interés.",
            "condiciones_cumplidas": [],
            "coincidencias": 0,
            "total_intereses": 0,
        }

    hechos_usuario = {f"interes_{i}" for i in intereses}
    hechos_totales = hechos_conocimiento.union(hechos_usuario)
    motor = MotorDeReglas(base_de_conocimiento)
    _, reglas_activadas = motor.inferir(hechos_totales)

    puntajes = {}
    for destino, caracteristicas in base_hechos.items():
        puntajes[destino] = sum(1 for i in intereses if i in caracteristicas)

    mejor_destino = max(puntajes, key=puntajes.get)
    mejor_coincidencias = puntajes[mejor_destino]

    intereses_bonitos = sorted([nombres_bonitos.get(i, i) for i in intereses])

    if reglas_activadas:
        regla_ganadora = max(reglas_activadas, key=lambda r: r.certeza)
        destino_final = nombres_destinos[regla_ganadora.conclusion]
        certeza_final = regla_ganadora.certeza
        regla_nombre = regla_ganadora.nombre
        explicacion = regla_ganadora.explicacion
    else:
        destino_final = mejor_destino
        regla_nombre = None
        proporcion = mejor_coincidencias / len(intereses)
        certeza_final = round(0.60 + (proporcion * 0.30), 2)
        explicacion = (
            f"Con tus {len(intereses)} intereses, {destino_final} coincide en "
            f"{mejor_coincidencias} de ellos. Es el destino que mejor encaja "
            f"con tu perfil de viaje."
        )

    return {
        "encontrado": True,
        "recomendacion": destino_final,
        "certeza": certeza_final,
        "regla": regla_nombre,
        "explicacion": explicacion,
        "condiciones_cumplidas": intereses_bonitos,
        "coincidencias": mejor_coincidencias,
        "total_intereses": len(intereses),
    }


def obtener_imagen_destino(destino: str) -> str:
    mapa = {
        "Cusco": "cusco.jpg", "Machu Picchu": "machu_picchu.jpg",
        "Arequipa": "arequipa.jpg", "Puno": "puno.jpg",
        "Paracas": "paracas.jpg", "Ica": "ica.jpg", "Huaraz": "huaraz.jpg",
        "Trujillo": "trujillo.jpg", "Chiclayo": "chiclayo.jpg",
        "Tarapoto": "tarapoto.jpg", "Iquitos": "iquitos.jpg",
    }
    return mapa.get(destino, "")


def obtener_descripcion_destino(destino: str) -> str:
    descripciones = {
        "Cusco": "Antigua capital del Imperio Inca, mezcla de historia, arquitectura y cultura viva.",
        "Machu Picchu": "Ciudadela Inca declarada Patrimonio de la Humanidad, rodeada de montañas.",
        "Arequipa": "La Ciudad Blanca, famosa por su arquitectura colonial y su exquisita gastronomía.",
        "Puno": "Capital folclórica del Perú, a orillas del lago Titicaca, cuna de tradiciones andinas.",
        "Paracas": "Reserva marina con playas, fauna y paisajes costeros únicos en el Pacífico.",
        "Ica": "Tierra del sol, las dunas y el oasis de Huacachina, ideal para la aventura.",
        "Huaraz": "Puerta de la Cordillera Blanca, paraíso del trekking y las lagunas de altura.",
        "Trujillo": "Ciudad de la eterna primavera, con huacas prehispánicas y costas norteñas.",
        "Chiclayo": "Capital de la amistad, con museos arqueológicos y una gastronomía reconocida.",
        "Tarapoto": "Puerta de la Amazonía, con cascadas, selva y aventura en la selva alta.",
        "Iquitos": "Ciudad amazónica, ideal para el ecoturismo, la fauna y la selva tropical.",
    }
    return descripciones.get(destino, "")


if __name__ == "__main__":
    verificar_base_hechos()
    print("Cantidad de reglas:", len(base_de_conocimiento))