from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from pathlib import Path
from collections import Counter

app = FastAPI(
    title="Clasificador de Enfermedades",
    description=(
        "API para clasificar el estado de salud de un paciente a partir de sus síntomas. "
        "Retorna uno de los siguientes estados: "
        "**NO ENFERMO**, **ENFERMEDAD LEVE**, **ENFERMEDAD AGUDA** o **ENFERMEDAD CRÓNICA**."
    ),
    version="1.0.0",
)


class DatosPaciente(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Edad del paciente en años", example=45)
    sex: str = Field(..., pattern="^[MF]$", description="Sexo del paciente: 'M' o 'F'", example="M")
    occupation: str = Field(..., description="Ocupación del paciente", example="Agricultor")
    symptom_1: Optional[float] = Field(None, ge=0, le=10, description="Síntoma 1 (escala 0-10)", example=7.5)
    symptom_2: Optional[float] = Field(None, ge=0, le=10, description="Síntoma 2 (escala 0-10)", example=6.0)
    symptom_3: Optional[float] = Field(None, ge=0, le=10, description="Síntoma 3 (escala 0-10)", example=4.0)
    symptom_4: Optional[float] = Field(None, ge=0, le=10, description="Síntoma 4 (escala 0-10)", example=None)
    symptom_5: Optional[float] = Field(None, ge=0, le=10, description="Síntoma 5 (escala 0-10)", example=None)

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 45,
                "sex": "M",
                "occupation": "Agricultor",
                "symptom_1": 7.5,
                "symptom_2": 6.0,
                "symptom_3": 4.0,
                "symptom_4": None,
                "symptom_5": None,
            }
        }
    }


ESTADOS = ["NO ENFERMO", "ENFERMEDAD LEVE", "ENFERMEDAD AGUDA", "ENFERMEDAD CRÓNICA", "ENFERMEDAD TERMINAL"]

ARCHIVO_PREDICCIONES = Path("/app/data/predicciones.txt")


def registrar_prediccion(clasificacion: str):
    ARCHIVO_PREDICCIONES.parent.mkdir(parents=True, exist_ok=True)
    with open(ARCHIVO_PREDICCIONES, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {clasificacion}\n")


def clasificar(datos: DatosPaciente) -> str:
    sintomas = [
        datos.symptom_1,
        datos.symptom_2,
        datos.symptom_3,
        datos.symptom_4,
        datos.symptom_5,
    ]
    presentes = [s for s in sintomas if s is not None]

    if not presentes:
        return ESTADOS[0]  

    sumatoria = sum(presentes)

    if sumatoria < 8:
        return ESTADOS[0]
    elif sumatoria < 23:
        return ESTADOS[1]
    elif sumatoria < 38:
        return ESTADOS[2]
    elif sumatoria < 45:
        return ESTADOS[3]
    else:
        return ESTADOS[4]


@app.post(
    "/predecir",
    summary="Clasificar estado de salud",
    response_description="Estado de salud clasificado",
)
def predecir(datos: DatosPaciente):
    """
    Recibe los datos del paciente y retorna la clasificación de su estado de salud:

    - **NO ENFERMO**: sumatoria de síntomas < 8
    - **ENFERMEDAD LEVE**: sumatoria entre 8 y 22
    - **ENFERMEDAD AGUDA**: sumatoria entre 23 y 37
    - **ENFERMEDAD CRÓNICA**: sumatoria entre 38 y 44
    - **ENFERMEDAD TERMINAL**: sumatoria >= 45
    """
    resultado = clasificar(datos)
    registrar_prediccion(resultado)
    return {"clasificacion": resultado}


@app.get(
    "/reporte",
    summary="Reporte de predicciones",
    response_description="Estadísticas de predicciones realizadas",
)
def reporte():
    """
    Retorna estadísticas de todas las predicciones realizadas:

    - **total_por_categoria**: conteo de predicciones por cada categoría
    - **ultimas_5**: las últimas 5 predicciones con fecha y clasificación
    - **fecha_ultima**: fecha y hora de la última predicción
    """
    if not ARCHIVO_PREDICCIONES.exists():
        return {"total_por_categoria": {}, "ultimas_5": [], "fecha_ultima": None}

    lineas = ARCHIVO_PREDICCIONES.read_text(encoding="utf-8").splitlines()
    lineas = [l for l in lineas if l.strip()]

    if not lineas:
        return {"total_por_categoria": {}, "ultimas_5": [], "fecha_ultima": None}

    registros = [{"fecha": l.split(" | ")[0], "clasificacion": l.split(" | ")[1]} for l in lineas]

    return {
        "total_por_categoria": dict(Counter(r["clasificacion"] for r in registros)),
        "ultimas_5": registros[-5:],
        "fecha_ultima": registros[-1]["fecha"],
    }


@app.get("/")
def root():
    return {"mensaje": "API de clasificación de enfermedades. Usa POST /predecir"}
