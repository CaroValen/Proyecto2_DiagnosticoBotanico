import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from motores import diagnosticar_prolog


class PruebasProlog(unittest.TestCase):
    @patch("motores.subprocess.run")
    def test_envia_sintomas_por_nombre_y_no_por_orden_de_respuestas(self, ejecutar):
        ejecutar.return_value.returncode = 0
        ejecutar.return_value.stdout = "Diagnostico: plaga_cochinilla\n"
        ejecutar.return_value.stderr = ""
        self.assertIn("plaga_cochinilla", diagnosticar_prolog(["puntos_blancos"]))
        argumentos = ejecutar.call_args.args[0]
        self.assertIn("diagnosticar([puntos_blancos])", argumentos)
        self.assertNotIn("stdin", ejecutar.call_args.kwargs)

    @patch("motores.subprocess.run")
    def test_rechaza_sintoma_desconocido(self, ejecutar):
        with self.assertRaises(ValueError):
            diagnosticar_prolog(["sintoma_inventado"])
        ejecutar.assert_not_called()

    @patch("motores.subprocess.run")
    def test_error_de_prolog(self, ejecutar):
        ejecutar.return_value.returncode = 1
        ejecutar.return_value.stderr = "Error de prueba"
        with self.assertRaises(RuntimeError):
            diagnosticar_prolog(["puntos_blancos"])


if __name__ == "__main__":
    unittest.main()
