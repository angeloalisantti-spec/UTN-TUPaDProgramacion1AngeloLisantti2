"""Gestión de países: altas, actualizaciones, búsquedas y filtros."""

import unicodedata

from archivos import guardar_csv


def _normalizar(texto):
    """Quita acentos y pasa a minúsculas para comparaciones robustas."""
    if texto is None:
        return ""
    texto = str(texto).strip().lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def agregar_pais(paises, nombre, poblacion, superficie, continente):
    """Agrega un país nuevo. Devuelve (ok, mensaje)."""
    nombre = nombre.strip()
    continente = continente.strip()

    if not nombre or not continente:
        return False, "El nombre y el continente no pueden estar vacíos."
    if poblacion is None or superficie is None:
        return False, "Población y superficie son obligatorias."
    if poblacion < 0 or superficie < 0:
        return False, "Población y superficie no pueden ser negativas."

    # Evitar duplicados exactos por nombre (ignorando mayúsculas y acentos)
    for pais in paises:
        if _normalizar(pais["nombre"]) == _normalizar(nombre):
            return False, f"El país '{nombre}' ya existe."

    paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    })
    return True, f"País '{nombre}' agregado correctamente."


def actualizar_pais(paises, nombre, poblacion=None, superficie=None):
    """Actualiza población y/o superficie de un país. Devuelve (ok, mensaje)."""
    for pais in paises:
        if _normalizar(pais["nombre"]) == _normalizar(nombre):
            if poblacion is not None:
                if poblacion < 0:
                    return False, "La población no puede ser negativa."
                pais["poblacion"] = poblacion
            if superficie is not None:
                if superficie < 0:
                    return False, "La superficie no puede ser negativa."
                pais["superficie"] = superficie
            return True, f"País '{pais['nombre']}' actualizado correctamente."
    return False, f"No se encontró el país '{nombre}'."


def buscar_por_nombre(paises, texto):
    """Busca países cuyo nombre contenga el texto (coincidencia parcial, insensible a mayúsculas y acentos)."""
    texto_norm = _normalizar(texto)
    if not texto_norm:
        return []
    return [p for p in paises if texto_norm in _normalizar(p["nombre"])]


def filtrar_por_continente(paises, continente):
    """Filtra países por continente (coincidencia insensible a mayúsculas y acentos)."""
    continente_norm = _normalizar(continente)
    if not continente_norm:
        return []
    return [p for p in paises if _normalizar(p["continente"]) == continente_norm]


def filtrar_por_poblacion(paises, minimo, maximo):
    """Filtra países cuya población esté dentro del rango [minimo, maximo]."""
    return [p for p in paises if minimo <= p["poblacion"] <= maximo]


def filtrar_por_superficie(paises, minimo, maximo):
    """Filtra países cuya superficie esté dentro del rango [minimo, maximo]."""
    return [p for p in paises if minimo <= p["superficie"] <= maximo]


def ordenar_paises(paises, clave, ascendente=True):
    """Ordena una copia de la lista de países por la clave indicada.

    clave: 'nombre', 'poblacion' o 'superficie'.
    """
    if clave not in ("nombre", "poblacion", "superficie"):
        raise ValueError("Clave de ordenamiento no válida.")

    copia = list(paises)
    if clave == "nombre":
        copia.sort(key=lambda p: p["nombre"].lower(), reverse=not ascendente)
    else:
        copia.sort(key=lambda p: p[clave], reverse=not ascendente)
    return copia


def mostrar_paises(paises):
    """Imprime en consola la lista de países de forma tabular."""
    if not paises:
        print("No hay países para mostrar.")
        return
    print(f"{'Nombre':<22}{'Población':>15}{'Superficie (km²)':>20}{'Continente':>15}")
    print("-" * 72)
    for p in paises:
        print(f"{p['nombre']:<22}{p['poblacion']:>15}{p['superficie']:>20}{p['continente']:>15}")
    print(f"\nTotal: {len(paises)} país(es).")