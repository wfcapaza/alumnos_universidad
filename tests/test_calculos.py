import unittest
from etl.calculos import (calcular_estado_academico, calcular_condicion_beca)

class TestCalculos(unittest.TestCase):

    def test_estado_academico_destacado(self):
        resultado = calcular_estado_academico(18)
        self.assertEqual(resultado, "Destacado")

    def test_estado_academico_regular(self):
        resultado = calcular_estado_academico(14)
        self.assertEqual(resultado, "Regular")

    def test_estado_academico_riesgo(self):
        resultado = calcular_estado_academico(9)
        self.assertEqual(resultado, "Riesgo Académico")

    def test_beca_completa(self):
        resultado = calcular_condicion_beca(18, 20)
        self.assertEqual(resultado, "Beca Completa")

    def test_media_beca(self):
        resultado = calcular_condicion_beca(16, 15)
        self.assertEqual(resultado, "Media Beca")

    def test_sin_beneficio(self):
        resultado = calcular_condicion_beca(12, 20)
        self.assertEqual(resultado, "Sin Beneficio")

    def test_estado_academico_limite_destacado(self):
        resultado = calcular_estado_academico(16.0)
        self.assertEqual(resultado, "Destacado")

    def test_estado_academico_limite_regular(self):
        resultado = calcular_estado_academico(10.5)
        self.assertEqual(resultado, "Regular")

    def test_beca_completa_limite(self):
        resultado = calcular_condicion_beca(17.0, 18)
        self.assertEqual(resultado, "Beca Completa")

    def test_no_beca_completa_por_creditos(self):
        resultado = calcular_condicion_beca(17.0, 17)
        self.assertEqual(resultado, "Media Beca")


if __name__ == "__main__":
    unittest.main()