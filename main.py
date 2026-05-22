from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

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


ESTADOS = ["NO ENFERMO", "ENFERMEDAD LEVE", "ENFERMEDAD AGUDA", "ENFERMEDAD CRÓNICA"]


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

    if sumatoria < 10:
        return ESTADOS[0] 
    elif sumatoria < 25:
        return ESTADOS[1] 
    elif sumatoria < 40:
        return ESTADOS[2] 
    else:
        return ESTADOS[3]  


@app.post(
    "/predecir",
    summary="Clasificar estado de salud",
    response_description="Estado de salud clasificado",
)
def predecir(datos: DatosPaciente):
    """
    Recibe los datos del paciente y retorna la clasificación de su estado de salud:

    - **NO ENFERMO**: sumatoria de síntomas < 10
    - **ENFERMEDAD LEVE**: sumatoria entre 10 y 24
    - **ENFERMEDAD AGUDA**: sumatoria entre 25 y 39
    - **ENFERMEDAD CRÓNICA**: sumatoria >= 40
    """
    resultado = clasificar(datos)
    return {"clasificacion": resultado}


@app.get("/")
def root():
    return {"mensaje": "API de clasificación de enfermedades. Usa POST /predecir"}
