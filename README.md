# Herramienta de diagnóstico oportuno - MLOps Entrega 1

# Implementación de la solución

El principal objetivo es construir un modelo capaz de clasificar a un paciente en una de cuatro categorías de salud a partir de los síntomas reportados. 

# Documentación técnica

API REST construida con **FastAPI** que clasifica el estado de salud de un paciente a partir de sus sintomas.
github: https://github.com/Joules17/mlops-entrega1

## Estados posibles

| Estado             | Descripcion                |
|--------------------|----------------------------|
| NO ENFERMO         | Sumatoria < 8              |
| ENFERMEDAD LEVE    | Sumatoria entre 8 y 22     |
| ENFERMEDAD AGUDA   | Sumatoria entre 23 y 37    |
| ENFERMEDAD CRONICA | Sumatoria entre 38 y 44    |
| ENFERMEDAD TERMINAL| Sumatoria >= 45            |

---

## Requisitos

- Docker instalado: https://www.docker.com/

---

## Instrucciones con Docker

### 1. Construir la imagen

    docker build -t clasificador-enfermedades .

### 2. Ejecutar el contenedor

    docker run -p 8000:8000 clasificador-enfermedades

La API quedara disponible en: http://localhost:8000

### 3. Detener el contenedor

    docker stop $(docker ps -q --filter ancestor=clasificador-enfermedades)

---

## Documentacion interactiva (Swagger)

Con el contenedor corriendo, abrir en el navegador:

    http://localhost:8000/docs

Para la version ReDoc:

    http://localhost:8000/redoc

---
## Uso del endpoint `/predecir`

- Metodo: POST
- URL: http://localhost:8000/predecir
- Content-Type: application/json

### Body de la peticion

| Campo      | Tipo   | Requerido | Descripcion               |
|------------|--------|-----------|---------------------------|
| age        | int    | Si        | Edad del paciente         |
| sex        | string | Si        | Sexo: M o F               |
| occupation | string | Si        | Ocupacion del paciente    |
| symptom_1  | float  | No        | Sintoma 1 en escala 0-10  |
| symptom_2  | float  | No        | Sintoma 2 en escala 0-10  |
| symptom_3  | float  | No        | Sintoma 3 en escala 0-10  |
| symptom_4  | float  | No        | Sintoma 4 en escala 0-10  |
| symptom_5  | float  | No        | Sintoma 5 en escala 0-10  |

### Ejemplo

    curl -X POST http://localhost:8000/predecir -H "Content-Type: application/json" -d "{\"age\": 45, \"sex\": \"M\", \"occupation\": \"Agricultor\", \"symptom_1\": 7.5, \"symptom_2\": 6.0, \"symptom_3\": 4.0}"

### Respuesta esperada

    { "clasificacion": "ENFERMEDAD AGUDA" }

---

## Ejecucion local (sin Docker)

    pip install -r requirements.txt
    uvicorn main:app --reload