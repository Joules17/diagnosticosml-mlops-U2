# Diagnóstico Oportuno de Enfermedades con MLOps

## Problema

Los sistemas de salud enfrentan el reto de diagnosticar enfermedades de forma oportuna,
especialmente cuando se trata de enfermedades huérfanas con datos escasos. La falta de
herramientas escalables y confiables dificulta la detección temprana y el tratamiento
adecuado de los pacientes.

## Propósito

Construir una solución de software que, apoyada en modelos de machine learning, permita
clasificar el estado de salud de un paciente a partir de sus síntomas, facilitando el
diagnóstico oportuno de manera escalable y reproducible.

## Solución planteada

Se desarrolla un aplicativo que expone un modelo de clasificación mediante una API,
capaz de determinar el nivel de riesgo de un paciente según los síntomas reportados. La
solución sigue prácticas de MLOps para garantizar la trazabilidad, el despliegue
automatizado y el monitoreo continuo del modelo en producción.

## Estructura del repositorio

| Rama | Contenido |
|------|-----------|
| `main` | Descripción general del proyecto |
| `solucion-inicial` | Implementación base: API, modelo y configuración de despliegue |