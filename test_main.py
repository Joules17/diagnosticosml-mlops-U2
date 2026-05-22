import pytest
from fastapi.testclient import TestClient
import main
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def archivo_temporal(monkeypatch, tmp_path):
    monkeypatch.setattr(main, "ARCHIVO_PREDICCIONES", tmp_path / "predicciones.txt")


def _paciente(**sintomas):
    return {"age": 30, "sex": "M", "occupation": "Ingeniero", **sintomas}


def test_todas_las_categorias():
    """Verifica que las 5 categorías de enfermedades sean obtenidas con distintos parámetros."""
    casos = [
        (_paciente(symptom_1=3.0), "NO ENFERMO"),
        (_paciente(symptom_1=9.0, symptom_2=5.0), "ENFERMEDAD LEVE"),
        (_paciente(symptom_1=8.0, symptom_2=8.0, symptom_3=8.0), "ENFERMEDAD AGUDA"),
        (_paciente(symptom_1=10.0, symptom_2=10.0, symptom_3=10.0, symptom_4=9.0), "ENFERMEDAD CRÓNICA"),
        (_paciente(symptom_1=10.0, symptom_2=10.0, symptom_3=10.0, symptom_4=10.0, symptom_5=5.0), "ENFERMEDAD TERMINAL"),
    ]
    for datos, esperado in casos:
        response = client.post("/predecir", json=datos)
        assert response.status_code == 200
        assert response.json()["clasificacion"] == esperado, f"Esperado {esperado} para {datos}"


def test_reporte_vacio_luego_prediccion():
    """Verifica que el reporte esté vacío antes de predecir y que registre correctamente después."""
    response = client.get("/reporte")
    assert response.status_code == 200
    data = response.json()
    assert data["total_por_categoria"] == {}
    assert data["ultimas_5"] == []
    assert data["fecha_ultima"] is None

    client.post("/predecir", json=_paciente(symptom_1=9.0, symptom_2=5.0))

    response = client.get("/reporte")
    assert response.status_code == 200
    data = response.json()
    assert data["total_por_categoria"].get("ENFERMEDAD LEVE") == 1
    assert len(data["ultimas_5"]) == 1
    assert data["fecha_ultima"] is not None
