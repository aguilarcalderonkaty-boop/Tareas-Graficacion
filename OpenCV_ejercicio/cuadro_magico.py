# Algoritmo alternativo para generar un Sudoku 
# Usamos rotaciones de filas

# La primera fila con números del 1 al 9
fila_base = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Lista para almacenar el tablero
tablero = []

# Creamos las 9 filas aplicando rotaciones
for i in range(9):
    # Cada fila se obtiene rotando la base
    # El patrón de rotación asegura más o menos
    desplazamiento = (i * 3 + i // 3) % 9
    fila = fila_base[desplazamiento:] + fila_base[:desplazamiento]
    tablero.append(fila)

# Imprimir el tablero con formato de Sudoku
for i, fila in enumerate(tablero):
    for j, num in enumerate(fila):
        print(num, end=" ")
        if (j + 1) % 3 == 0 and j != 8:
            print("|", end=" ")
    print()
    if (i + 1) % 3 == 0 and i != 8:
        print("- " * 11)
