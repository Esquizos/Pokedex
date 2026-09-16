#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================
   POKÉDEX EN PYTHON - Generación I (151 Pokémon)
====================================================

Una Pokédex de consola con:
  - Búsqueda por nombre o número
  - Listado completo
  - Filtro por tipo
  - Comparación entre dos Pokémon
  - Estadísticas totales y "el más fuerte por stat"
  - Pokémon aleatorio ("Pokémon sorpresa")

Uso:
    python pokedex.py

No requiere librerías externas, solo Python 3 estándar.
"""

import random
import sys
import textwrap

from pokedex_data import POKEMON_DATA, POKEMON_BY_ID, POKEMON_BY_NAME

CAMPOS = ("id", "nombre", "tipo1", "tipo2", "hp", "atk", "def", "spa", "spd", "spe", "desc")

ANCHO = 60


# ----------------------------------------------------------------------
# Utilidades de presentación
# ----------------------------------------------------------------------

def linea(caracter="-"):
    print(caracter * ANCHO)


def titulo(texto):
    linea("=")
    print(texto.center(ANCHO))
    linea("=")


def total_stats(p):
    return p[4] + p[5] + p[6] + p[7] + p[8] + p[9]


def formatear_tipo(p):
    if p[3]:
        return f"{p[2]}/{p[3]}"
    return p[2]


def mostrar_ficha(p):
    """Imprime la ficha completa de un Pokémon."""
    _id, nombre, t1, t2, hp, atk, de, spa, spd, spe, desc = p
    linea("=")
    print(f"#{_id:03d}  {nombre}".center(ANCHO))
    print(f"Tipo: {formatear_tipo(p)}".center(ANCHO))
    linea("-")
    print(textwrap.fill(desc, width=ANCHO))
    linea("-")
    print(f"{'HP':<12}{hp:>4}")
    print(f"{'Ataque':<12}{atk:>4}")
    print(f"{'Defensa':<12}{de:>4}")
    print(f"{'At. Esp.':<12}{spa:>4}")
    print(f"{'Def. Esp.':<12}{spd:>4}")
    print(f"{'Velocidad':<12}{spe:>4}")
    linea("-")
    print(f"{'TOTAL':<12}{total_stats(p):>4}")
    linea("=")


def mostrar_fila_tabla(p):
    _id, nombre, t1, t2, hp, atk, de, spa, spd, spe, desc = p
    tipo = formatear_tipo(p)
    print(f"{_id:>3} {nombre:<14}{tipo:<16}{hp:>4}{atk:>5}{de:>5}{spa:>5}{spd:>5}{spe:>5}{total_stats(p):>7}")


def encabezado_tabla():
    print(f"{'#':>3} {'Nombre':<14}{'Tipo':<16}{'HP':>4}{'ATK':>5}{'DEF':>5}{'SPA':>5}{'SPD':>5}{'SPE':>5}{'TOTAL':>7}")
    linea()


# ----------------------------------------------------------------------
# Funciones principales
# ----------------------------------------------------------------------

def buscar():
    consulta = input("\nIngresa nombre o número de Pokédex: ").strip().lower()
    p = None
    if consulta.isdigit():
        p = POKEMON_BY_ID.get(int(consulta))
    else:
        p = POKEMON_BY_NAME.get(consulta)

    if p:
        mostrar_ficha(p)
    else:
        print(f"\nNo se encontró ningún Pokémon que coincida con '{consulta}'.")


def listar_todos():
    titulo("LISTADO COMPLETO (151 POKÉMON)")
    encabezado_tabla()
    for p in POKEMON_DATA:
        mostrar_fila_tabla(p)
    print(f"\nTotal: {len(POKEMON_DATA)} Pokémon.")


def filtrar_por_tipo():
    tipo = input("\n¿Qué tipo quieres filtrar (ej. Fuego, Agua, Planta...)? ").strip().lower()
    resultados = [p for p in POKEMON_DATA if p[2].lower() == tipo or (p[3] and p[3].lower() == tipo)]
    if not resultados:
        print(f"\nNo hay Pokémon del tipo '{tipo}'.")
        return
    titulo(f"POKÉMON DE TIPO {tipo.upper()}")
    encabezado_tabla()
    for p in resultados:
        mostrar_fila_tabla(p)
    print(f"\nSe encontraron {len(resultados)} Pokémon de tipo {tipo}.")


def comparar():
    print("\n--- Comparar dos Pokémon ---")
    a = input("Primer Pokémon (nombre o número): ").strip().lower()
    b = input("Segundo Pokémon (nombre o número): ").strip().lower()

    def resolver(consulta):
        if consulta.isdigit():
            return POKEMON_BY_ID.get(int(consulta))
        return POKEMON_BY_NAME.get(consulta)

    p1, p2 = resolver(a), resolver(b)
    if not p1 or not p2:
        print("\nNo se pudo encontrar uno o ambos Pokémon.")
        return

    titulo(f"{p1[1]} VS {p2[1]}")
    etiquetas = ["HP", "Ataque", "Defensa", "At. Esp.", "Def. Esp.", "Velocidad", "TOTAL"]
    stats1 = list(p1[4:10]) + [total_stats(p1)]
    stats2 = list(p2[4:10]) + [total_stats(p2)]

    print(f"{'Estadística':<12}{p1[1]:>15}{p2[1]:>15}")
    linea()
    for etiqueta, s1, s2 in zip(etiquetas, stats1, stats2):
        marca1 = " *" if s1 > s2 else "  "
        marca2 = " *" if s2 > s1 else "  "
        print(f"{etiqueta:<12}{s1:>13}{marca1}{s2:>13}{marca2}")
    linea()
    ganador = p1[1] if total_stats(p1) > total_stats(p2) else (p2[1] if total_stats(p2) > total_stats(p1) else "Empate")
    print(f"Mayor total de estadísticas: {ganador}")


def pokemon_aleatorio():
    p = random.choice(POKEMON_DATA)
    print("\n¡Pokémon sorpresa!")
    mostrar_ficha(p)


def rankings():
    titulo("RANKINGS DESTACADOS")
    campos = [
        ("HP", 4), ("Ataque", 5), ("Defensa", 6),
        ("At. Especial", 7), ("Def. Especial", 8), ("Velocidad", 9),
    ]
    for nombre_campo, idx in campos:
        mejor = max(POKEMON_DATA, key=lambda p: p[idx])
        print(f"Mayor {nombre_campo:<15}: {mejor[1]:<12} ({mejor[idx]})")

    mejor_total = max(POKEMON_DATA, key=total_stats)
    peor_total = min(POKEMON_DATA, key=total_stats)
    linea()
    print(f"Mayor TOTAL de stats : {mejor_total[1]} ({total_stats(mejor_total)})")
    print(f"Menor TOTAL de stats : {peor_total[1]} ({total_stats(peor_total)})")


def menu():
    titulo("POKÉDEX - GENERACIÓN I")
    print("""
 1) Buscar Pokémon por nombre o número
 2) Listar todos los Pokémon
 3) Filtrar por tipo
 4) Comparar dos Pokémon
 5) Pokémon aleatorio
 6) Ver rankings (mejores estadísticas)
 0) Salir
""")


def main():
    while True:
        menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            buscar()
        elif opcion == "2":
            listar_todos()
        elif opcion == "3":
            filtrar_por_tipo()
        elif opcion == "4":
            comparar()
        elif opcion == "5":
            pokemon_aleatorio()
        elif opcion == "6":
            rankings()
        elif opcion == "0":
            print("\n¡Hasta la próxima, Entrenador!")
            sys.exit(0)
        else:
            print("\nOpción no válida, intenta de nuevo.")

        input("\nPulsa ENTER para continuar...")


if __name__ == "__main__":
    main()
