"""Funciones para lectura y escritura de archivos CSV del dataset de países."""

import csv
import os


def leer_csv(ruta):
    """Lee un archivo CSV y devuelve una lista de diccionarios con los países.

    Cada diccionario tiene las claves: nombre, poblacion, superficie, continente.
    Valida formato y tipos de datos. Devuelve (lista, errores).
    """
    paises = []
    errores = []

    if not os.path.exists(ruta):
        return paises, [f"El archivo '{ruta}' no existe."]

    try:
        with open(ruta, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            if lector.fieldnames is None:
                return paises, ["El archivo CSV está vacío o no tiene encabezado."]

            campos_esperados = {"nombre", "poblacion", "superficie", "continente"}
            if not campos_esperados.issubset(set(lector.fieldnames)):
                return paises, [
                    "El CSV no contiene las columnas requeridas: "
                    "nombre, poblacion, superficie, continente."
                ]

            for numero, fila in enumerate(lector, start=2):
                try:
                    nombre = (fila.get("nombre") or "").strip()
                    poblacion_txt = (fila.get("poblacion") or "").strip()
                    superficie_txt = (fila.get("superficie") or "").strip()
                    continente = (fila.get("continente") or "").strip()

                    if not nombre or not poblacion_txt or not superficie_txt or not continente:
                        errores.append(f"Línea {numero}: campos vacíos, registro omitido.")
                        continue

                    poblacion = int(poblacion_txt)
                    superficie = int(superficie_txt)

                    if poblacion < 0 or superficie < 0:
                        errores.append(f"Línea {numero}: valores negativos, registro omitido.")
                        continue

                    paises.append({
                        "nombre": nombre,
                        "poblacion": poblacion,
                        "superficie": superficie,
                        "continente": continente,
                    })
                except ValueError:
                    errores.append(f"Línea {numero}: formato numérico inválido, registro omitido.")
                except Exception as e:  # pragma: no cover - defensivo
                    errores.append(f"Línea {numero}: error inesperado ({e}).")

    except OSError as e:
        return paises, [f"No se pudo leer el archivo: {e}"]

    return paises, errores


def leer_csv_texto(contenido):
    """Lee un CSV desde un string y devuelve (lista_paises, errores)."""
    import csv
    import io

    paises = []
    errores = []
    if not contenido or not contenido.strip():
        return paises, ["El contenido CSV está vacío."]

    try:
        lector = csv.DictReader(io.StringIO(contenido))
        if lector.fieldnames is None:
            return paises, ["El CSV está vacío o no tiene encabezado."]

        campos_esperados = {"nombre", "poblacion", "superficie", "continente"}
        if not campos_esperados.issubset(set(lector.fieldnames)):
            return paises, [
                "El CSV no contiene las columnas requeridas: "
                "nombre, poblacion, superficie, continente."
            ]

        for numero, fila in enumerate(lector, start=2):
            try:
                nombre = (fila.get("nombre") or "").strip()
                poblacion_txt = (fila.get("poblacion") or "").strip()
                superficie_txt = (fila.get("superficie") or "").strip()
                continente = (fila.get("continente") or "").strip()

                if not nombre or not poblacion_txt or not superficie_txt or not continente:
                    errores.append(f"Línea {numero}: campos vacíos, registro omitido.")
                    continue

                poblacion = int(poblacion_txt)
                superficie = int(superficie_txt)

                if poblacion < 0 or superficie < 0:
                    errores.append(f"Línea {numero}: valores negativos, registro omitido.")
                    continue

                paises.append({
                    "nombre": nombre,
                    "poblacion": poblacion,
                    "superficie": superficie,
                    "continente": continente,
                })
            except ValueError:
                errores.append(f"Línea {numero}: formato numérico inválido, registro omitido.")
            except Exception as e:  # pragma: no cover
                errores.append(f"Línea {numero}: error inesperado ({e}).")
    except Exception as e:
        return paises, [f"Error al procesar el CSV: {e}"]

    return paises, errores


def guardar_csv(ruta, paises):
    """Guarda la lista de países en un archivo CSV."""
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(
                archivo, fieldnames=["nombre", "poblacion", "superficie", "continente"]
            )
            escritor.writeheader()
            for pais in paises:
                escritor.writerow(pais)
        return True, "Datos guardados correctamente."
    except OSError as e:
        return False, f"No se pudo guardar el archivo: {e}"