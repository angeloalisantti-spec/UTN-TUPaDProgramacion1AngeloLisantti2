"""Estadísticas sobre el dataset de países."""


def pais_mayor_poblacion(paises):
    if not paises:
        return None
    return max(paises, key=lambda p: p["poblacion"])


def pais_menor_poblacion(paises):
    if not paises:
        return None
    return min(paises, key=lambda p: p["poblacion"])


def pais_mayor_superficie(paises):
    if not paises:
        return None
    return max(paises, key=lambda p: p["superficie"])


def pais_menor_superficie(paises):
    if not paises:
        return None
    return min(paises, key=lambda p: p["superficie"])


def promedio_poblacion(paises):
    if not paises:
        return 0.0
    return sum(p["poblacion"] for p in paises) / len(paises)


def promedio_superficie(paises):
    if not paises:
        return 0.0
    return sum(p["superficie"] for p in paises) / len(paises)


def cantidad_por_continente(paises):
    """Devuelve un diccionario {continente: cantidad}."""
    resultado = {}
    for p in paises:
        cont = p["continente"]
        resultado[cont] = resultado.get(cont, 0) + 1
    return resultado


def mostrar_estadisticas(paises):
    if not paises:
        print("No hay datos para calcular estadísticas.")
        return
    mayor = pais_mayor_poblacion(paises)
    menor = pais_menor_poblacion(paises)
    mayor_sup = pais_mayor_superficie(paises)
    menor_sup = pais_menor_superficie(paises)
    print("\n--- Estadísticas ---")
    print(f"País con mayor población: {mayor['nombre']} ({mayor['poblacion']:,})")
    print(f"País con menor población: {menor['nombre']} ({menor['poblacion']:,})")
    print(f"País con mayor superficie: {mayor_sup['nombre']} ({mayor_sup['superficie']:,} km²)")
    print(f"País con menor superficie: {menor_sup['nombre']} ({menor_sup['superficie']:,} km²)")
    print(f"Promedio de población: {promedio_poblacion(paises):,.2f}")
    print(f"Promedio de superficie: {promedio_superficie(paises):,.2f} km²")
    print("Cantidad de países por continente:")
    for cont, cant in sorted(cantidad_por_continente(paises).items()):
        print(f"  - {cont}: {cant}")