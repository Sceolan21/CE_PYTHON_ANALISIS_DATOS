"""Pruebas automáticas de las funciones del módulo meteorologia."""

import unittest

from meteorologia import (
    calcular_media,
    construir_registros,
    extraer_series,
    resumir_periodo,
)


class PruebasCalcularMedia(unittest.TestCase):
    def test_lista_conocida(self):
        self.assertEqual(calcular_media([4, 6, 8]), 6)

    def test_lista_vacia(self):
        self.assertIsNone(calcular_media([]))

    def test_unico_valor(self):
        self.assertEqual(calcular_media([7.5]), 7.5)

    def test_temperaturas_negativas(self):
        self.assertEqual(calcular_media([-6, -3, 0]), -3)

    def test_valor_ausente(self):
        with self.assertRaises(ValueError):
            calcular_media([5.0, None, 8.0])


class PruebasRegistros(unittest.TestCase):
    def test_construir_registros_con_datos_conocidos(self):
        registros = construir_registros(
            ["2025-01-01", "2025-01-02"],
            [7.1, 7.3],
            [12.8, 12.9],
            [2.4, 2.5],
        )

        self.assertEqual(len(registros), 2)
        self.assertEqual(registros[0]["fecha"], "2025-01-01")
        self.assertEqual(registros[0]["amplitud_termica"], 10.4)

    def test_listas_vacias(self):
        self.assertEqual(construir_registros([], [], [], []), [])

    def test_longitudes_distintas(self):
        with self.assertRaises(ValueError):
            construir_registros(["2025-01-01"], [7.1, 7.3], [12.8], [2.4])


class PruebasEstructuraYResumen(unittest.TestCase):
    def test_extraer_series(self):
        datos = {
            "daily": {
                "time": ["2025-01-01"],
                "temperature_2m_mean": [7.1],
                "temperature_2m_max": [12.8],
                "temperature_2m_min": [2.4],
            }
        }

        fechas, medias, maximas, minimas = extraer_series(datos)
        self.assertEqual(fechas, ["2025-01-01"])
        self.assertEqual(medias, [7.1])
        self.assertEqual(maximas, [12.8])
        self.assertEqual(minimas, [2.4])

    def test_daily_ausente(self):
        with self.assertRaises(ValueError):
            extraer_series({})

    def test_resumen_con_un_registro(self):
        registros = construir_registros(
            ["2025-01-01"], [7.1], [12.8], [2.4]
        )
        resumen = resumir_periodo(registros)

        self.assertEqual(resumen["numero_dias"], 1)
        self.assertEqual(resumen["temperatura_media"], 7.1)
        self.assertEqual(resumen["maxima_absoluta"], 12.8)
        self.assertEqual(resumen["minima_absoluta"], 2.4)
        self.assertEqual(resumen["amplitud_media"], 10.4)

    def test_resumen_vacio(self):
        resumen = resumir_periodo([])
        self.assertEqual(resumen["numero_dias"], 0)
        self.assertIsNone(resumen["temperatura_media"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
