"""Funciones para consultar y analizar temperaturas de Open-Meteo."""


URL_ARCHIVO = "https://archive-api.open-meteo.com/v1/archive"


def obtener_datos(latitud, longitud, fecha_inicio, fecha_fin, timeout=30):
    """Obtiene de Open-Meteo las temperaturas diarias de un periodo."""
    import requests

    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "start_date": fecha_inicio,
        "end_date": fecha_fin,
        "daily": "temperature_2m_mean,temperature_2m_max,temperature_2m_min",
        "timezone": "Europe/Madrid",
    }

    respuesta = requests.get(URL_ARCHIVO, params=parametros, timeout=timeout)
    respuesta.raise_for_status()
    return respuesta.json()


def extraer_series(datos):
    """Extrae y valida las fechas y las tres series de temperaturas."""
    if not isinstance(datos, dict) or not isinstance(datos.get("daily"), dict):
        raise ValueError("La respuesta no contiene un diccionario 'daily'.")

    diarios = datos["daily"]
    claves = [
        "time",
        "temperature_2m_mean",
        "temperature_2m_max",
        "temperature_2m_min",
    ]

    claves_ausentes = [clave for clave in claves if clave not in diarios]
    if claves_ausentes:
        raise ValueError(f"Faltan las claves: {', '.join(claves_ausentes)}.")

    series = [diarios[clave] for clave in claves]
    if any(not isinstance(serie, list) for serie in series):
        raise TypeError("Las fechas y temperaturas deben estar en listas.")

    return tuple(series)


def calcular_media(valores):
    """Calcula la media; devuelve None cuando la colección está vacía."""
    if not valores:
        return None
    if any(valor is None for valor in valores):
        raise ValueError("No se puede calcular la media con valores ausentes.")
    return sum(valores) / len(valores)


def construir_registros(fechas, medias, maximas, minimas):
    """Relaciona cada fecha con sus temperaturas y amplitud térmica."""
    longitudes = {len(fechas), len(medias), len(maximas), len(minimas)}
    if len(longitudes) != 1:
        raise ValueError("Las cuatro listas deben tener la misma longitud.")

    if any(
        valor is None
        for serie in (fechas, medias, maximas, minimas)
        for valor in serie
    ):
        raise ValueError("Las listas no pueden contener valores ausentes.")

    return [
        {
            "fecha": fecha,
            "media": media,
            "maxima": maxima,
            "minima": minima,
            "amplitud_termica": round(maxima - minima, 1),
        }
        for fecha, media, maxima, minima in zip(
            fechas, medias, maximas, minimas
        )
    ]


def resumir_periodo(registros):
    """Construye un resumen estadístico a partir de los registros."""
    if not registros:
        return {
            "numero_dias": 0,
            "temperatura_media": None,
            "maxima_absoluta": None,
            "minima_absoluta": None,
            "amplitud_media": None,
        }

    return {
        "numero_dias": len(registros),
        "temperatura_media": round(
            calcular_media([registro["media"] for registro in registros]), 2
        ),
        "maxima_absoluta": max(registro["maxima"] for registro in registros),
        "minima_absoluta": min(registro["minima"] for registro in registros),
        "amplitud_media": round(
            calcular_media(
                [registro["amplitud_termica"] for registro in registros]
            ),
            2,
        ),
    }


def ejecutar_programa():
    """Coordina la consulta de Jaén y muestra el resumen del periodo."""
    datos = obtener_datos(
        latitud=37.7796,
        longitud=-3.7849,
        fecha_inicio="2025-01-01",
        fecha_fin="2025-01-31",
    )
    fechas, medias, maximas, minimas = extraer_series(datos)
    registros = construir_registros(fechas, medias, maximas, minimas)
    resumen = resumir_periodo(registros)

    print("Resumen meteorológico de Jaén — enero de 2025")
    for nombre, valor in resumen.items():
        print(f"{nombre}: {valor}")

    return registros, resumen


if __name__ == "__main__":
    ejecutar_programa()
