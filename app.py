"""Servidor web: API REST en Python + interfaz HTML (fuente de verdad: Python)."""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from archivos import leer_csv
from paises import (
    agregar_pais,
    actualizar_pais,
    buscar_por_nombre,
    filtrar_por_continente,
    filtrar_por_poblacion,
    filtrar_por_superficie,
    ordenar_paises,
)
from estadisticas import (
    pais_mayor_poblacion,
    pais_menor_poblacion,
    pais_mayor_superficie,
    pais_menor_superficie,
    promedio_poblacion,
    promedio_superficie,
    cantidad_por_continente,
)

ARCHIVO_CSV = os.path.join(BASE_DIR, "paises.csv")
HOST = "127.0.0.1"
PORT = 8000

# Estado en memoria (fuente de verdad en runtime)
paises, errores_carga = leer_csv(ARCHIVO_CSV)


def to_dict(pais):
    return {
        "nombre": pais["nombre"],
        "poblacion": pais["poblacion"],
        "superficie": pais["superficie"],
        "continente": pais["continente"],
    }


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path, content_type):
        try:
            with open(path, "rb") as f:
                data = f.read()
        except OSError:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self._send_file(os.path.join(BASE_DIR, "index.html"), "text/html; charset=utf-8")
            return

        if path == "/api/paises":
            self._send_json([to_dict(p) for p in paises])
            return

        if path == "/api/buscar":
            texto = (qs.get("q", [""])[0]).strip()
            resultados = buscar_por_nombre(paises, texto) if texto else paises
            self._send_json([to_dict(p) for p in resultados])
            return

        if path == "/api/filtrar":
            continente = (qs.get("continente", [""])[0]).strip()
            pob_min = qs.get("pob_min", [None])[0]
            pob_max = qs.get("pob_max", [None])[0]
            sup_min = qs.get("sup_min", [None])[0]
            sup_max = qs.get("sup_max", [None])[0]

            resultados = list(paises)
            if continente:
                resultados = filtrar_por_continente(resultados, continente)
            if pob_min is not None and pob_max is not None:
                try:
                    resultados = filtrar_por_poblacion(resultados, int(pob_min), int(pob_max))
                except ValueError:
                    self._send_json({"error": "Rango de población inválido."}, 400)
                    return
            if sup_min is not None and sup_max is not None:
                try:
                    resultados = filtrar_por_superficie(resultados, int(sup_min), int(sup_max))
                except ValueError:
                    self._send_json({"error": "Rango de superficie inválido."}, 400)
                    return
            self._send_json([to_dict(p) for p in resultados])
            return

        if path == "/api/ordenar":
            clave = qs.get("clave", ["nombre"])[0]
            asc = qs.get("asc", ["true"])[0].lower() != "false"
            if clave not in ("nombre", "poblacion", "superficie"):
                self._send_json({"error": "Clave inválida."}, 400)
                return
            ordenados = ordenar_paises(paises, clave, asc)
            self._send_json([to_dict(p) for p in ordenados])
            return

        if path == "/api/estadisticas":
            if not paises:
                self._send_json({"error": "Sin datos."}, 400)
                return
            mayor = pais_mayor_poblacion(paises)
            menor = pais_menor_poblacion(paises)
            mayor_sup = pais_mayor_superficie(paises)
            menor_sup = pais_menor_superficie(paises)
            data = {
                "mayor_poblacion": to_dict(mayor),
                "menor_poblacion": to_dict(menor),
                "mayor_superficie": to_dict(mayor_sup),
                "menor_superficie": to_dict(menor_sup),
                "promedio_poblacion": promedio_poblacion(paises),
                "promedio_superficie": promedio_superficie(paises),
                "cantidad_por_continente": cantidad_por_continente(paises),
                "total": len(paises),
            }
            self._send_json(data)
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        global paises
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/agregar":
            body = self._read_body()
            nombre = str(body.get("nombre", "")).strip()
            continente = str(body.get("continente", "")).strip()
            try:
                poblacion = int(body.get("poblacion"))
                superficie = int(body.get("superficie"))
            except (TypeError, ValueError):
                self._send_json({"ok": False, "mensaje": "Población y superficie deben ser enteros."}, 400)
                return
            ok, msg = agregar_pais(paises, nombre, poblacion, superficie, continente)
            self._send_json({"ok": ok, "mensaje": msg})
            return

        if path == "/api/actualizar":
            body = self._read_body()
            nombre = str(body.get("nombre", "")).strip()
            poblacion = body.get("poblacion", None)
            superficie = body.get("superficie", None)
            try:
                if poblacion not in (None, ""):
                    poblacion = int(poblacion)
                else:
                    poblacion = None
                if superficie not in (None, ""):
                    superficie = int(superficie)
                else:
                    superficie = None
            except (TypeError, ValueError):
                self._send_json({"ok": False, "mensaje": "Valores numéricos inválidos."}, 400)
                return
            ok, msg = actualizar_pais(paises, nombre, poblacion, superficie)
            self._send_json({"ok": ok, "mensaje": msg})
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        pass


def main():
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Servidor iniciado en http://{HOST}:{PORT}")
    print("Presione Ctrl+C para detener.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()