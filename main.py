"""Aplicación principal para gestionar información de países."""

import os
import sys
from archivos import leer_csv, guardar_csv

# Mejorar visualización de caracteres acentuados en Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from paises import (
    agregar_pais,
    actualizar_pais,
    buscar_por_nombre,
    filtrar_por_continente,
    filtrar_por_poblacion,
    filtrar_por_superficie,
    ordenar_paises,
    mostrar_paises,
)
from estadisticas import mostrar_estadisticas

ARCHIVO_CSV = "paises.csv"


def pedir_entero(mensaje, minimo=None):
    """Pide un entero al usuario con validación. Devuelve None si cancela."""
    while True:
        valor = input(mensaje).strip()
        if valor.lower() in ("", "cancelar", "c"):
            return None
        try:
            numero = int(valor)
            if minimo is not None and numero < minimo:
                print(f"El valor debe ser mayor o igual a {minimo}.")
                continue
            return numero
        except ValueError:
            print("Ingrese un número entero válido (o 'cancelar').")


def pedir_texto(mensaje, obligatorio=True):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        if not obligatorio:
            return ""
        print("El campo no puede estar vacío.")


def mostrar_menu():
    print("\n===== GESTIÓN DE PAÍSES =====")
    print("1.  Agregar país")
    print("2.  Actualizar población/superficie")
    print("3.  Buscar país por nombre")
    print("4.  Filtrar por continente")
    print("5.  Filtrar por rango de población")
    print("6.  Filtrar por rango de superficie")
    print("7.  Ordenar países")
    print("8.  Mostrar estadísticas")
    print("9.  Listar todos los países")
    print("10. Guardar cambios en CSV")
    print("0.  Salir")
    return input("Seleccione una opción: ").strip()


def main():
    paises, errores = leer_csv(ARCHIVO_CSV)
    for e in errores:
        print(f"[Advertencia] {e}")
    print(f"Se cargaron {len(paises)} países desde '{ARCHIVO_CSV}'.")

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            print("\n--- Agregar país ---")
            nombre = pedir_texto("Nombre: ")
            poblacion = pedir_entero("Población: ", minimo=0)
            if poblacion is None:
                print("Operación cancelada.")
                continue
            superficie = pedir_entero("Superficie (km²): ", minimo=0)
            if superficie is None:
                print("Operación cancelada.")
                continue
            continente = pedir_texto("Continente: ")
            ok, msg = agregar_pais(paises, nombre, poblacion, superficie, continente)
            print(msg if ok else f"Error: {msg}")

        elif opcion == "2":
            print("\n--- Actualizar país ---")
            nombre = pedir_texto("Nombre del país: ")
            print("Deje vacío para no modificar.")
            pob_txt = input("Nueva población: ").strip()
            sup_txt = input("Nueva superficie: ").strip()
            try:
                poblacion = int(pob_txt) if pob_txt else None
                superficie = int(sup_txt) if sup_txt else None
            except ValueError:
                print("Error: valores numéricos inválidos.")
                continue
            if poblacion is not None or superficie is not None:
                ok, msg = actualizar_pais(paises, nombre, poblacion, superficie)
                print(msg if ok else f"Error: {msg}")
            else:
                print("No se ingresaron cambios.")

        elif opcion == "3":
            print("\n--- Buscar país ---")
            texto = pedir_texto("Texto a buscar: ")
            resultados = buscar_por_nombre(paises, texto)
            if resultados:
                mostrar_paises(resultados)
            else:
                print("No se encontraron países con ese nombre.")

        elif opcion == "4":
            print("\n--- Filtrar por continente ---")
            continente = pedir_texto("Continente: ")
            resultados = filtrar_por_continente(paises, continente)
            if resultados:
                mostrar_paises(resultados)
            else:
                print("No se encontraron países en ese continente.")

        elif opcion == "5":
            print("\n--- Filtrar por rango de población ---")
            minimo = pedir_entero("Población mínima: ", minimo=0)
            if minimo is None:
                print("Operación cancelada.")
                continue
            maximo = pedir_entero("Población máxima: ", minimo=minimo)
            if maximo is None:
                print("Operación cancelada.")
                continue
            resultados = filtrar_por_poblacion(paises, minimo, maximo)
            if resultados:
                mostrar_paises(resultados)
            else:
                print("No se encontraron países en ese rango.")

        elif opcion == "6":
            print("\n--- Filtrar por rango de superficie ---")
            minimo = pedir_entero("Superficie mínima (km²): ", minimo=0)
            if minimo is None:
                print("Operación cancelada.")
                continue
            maximo = pedir_entero("Superficie máxima (km²): ", minimo=minimo)
            if maximo is None:
                print("Operación cancelada.")
                continue
            resultados = filtrar_por_superficie(paises, minimo, maximo)
            if resultados:
                mostrar_paises(resultados)
            else:
                print("No se encontraron países en ese rango.")

        elif opcion == "7":
            print("\n--- Ordenar países ---")
            print("Claves: 1=Nombre, 2=Población, 3=Superficie")
            clave_op = input("Clave: ").strip()
            clave_map = {"1": "nombre", "2": "poblacion", "3": "superficie"}
            if clave_op not in clave_map:
                print("Opción inválida.")
                continue
            orden = input("Orden (a=ascendente, d=descendente): ").strip().lower()
            ascendente = orden != "d"
            ordenados = ordenar_paises(paises, clave_map[clave_op], ascendente)
            mostrar_paises(ordenados)

        elif opcion == "8":
            mostrar_estadisticas(paises)

        elif opcion == "9":
            mostrar_paises(paises)

        elif opcion == "10":
            ok, msg = guardar_csv(ARCHIVO_CSV, paises)
            print(msg if ok else f"Error: {msg}")

        elif opcion == "0":
            print("Saliendo del programa. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()