"""Pequeña práctica con NumPy, pandas y Matplotlib."""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


DIRECTORIO_RESULTADOS = Path(__file__).resolve().parent / "resultados"


def preparar_datos():
    """Crea un conjunto pequeño de temperaturas y lo devuelve como DataFrame."""
    fechas = pd.date_range("2025-01-01", periods=7, freq="D")
    temperaturas = np.array([7.1, 7.3, 7.4, 8.1, 9.5, 8.7, 8.6])

    datos = pd.DataFrame(
        {
            "fecha": fechas,
            "temperatura_media": temperaturas,
        }
    )
    return datos


def guardar_resultados(datos):
    """Guarda los datos en CSV y crea una gráfica de líneas."""
    DIRECTORIO_RESULTADOS.mkdir(parents=True, exist_ok=True)

    ruta_csv = DIRECTORIO_RESULTADOS / "temperaturas_practica.csv"
    ruta_grafica = DIRECTORIO_RESULTADOS / "temperaturas_practica.png"

    datos.to_csv(ruta_csv, index=False, date_format="%Y-%m-%d")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(
        datos["fecha"],
        datos["temperatura_media"],
        color="tab:orange",
        marker="o",
    )
    ax.set_title("Temperaturas de la práctica de venv")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Temperatura media (°C)")
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(ruta_grafica, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return ruta_csv, ruta_grafica


def main():
    datos = preparar_datos()
    media = np.mean(datos["temperatura_media"])
    ruta_csv, ruta_grafica = guardar_resultados(datos)

    print(datos)
    print(f"\nTemperatura media: {media:.2f} °C")
    print("CSV guardado en:", ruta_csv)
    print("Gráfica guardada en:", ruta_grafica)


if __name__ == "__main__":
    main()
