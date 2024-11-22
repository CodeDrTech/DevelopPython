import random


#1-10
#11-29
#30-38
def generar_numeros():
    numeros_aleatorios = []

    # Generar los dos primeros números del 1 al 10 sin repetición
    numeros_aleatorios.extend(random.sample(range(1, 11), 2))

    # Generar los dos siguientes números del 11 al 29 sin repetición
    numeros_aleatorios.extend(random.sample(range(11, 30), 2))

    # Generar los dos últimos números del 30 al 38 permitiendo repetición
    numeros_aleatorios.extend(random.choices(range(30, 39), k=2))

    return numeros_aleatorios

if __name__ == "__main__":
    numeros = generar_numeros()

    # Ordenar la lista de números de menor a mayor
    numeros.sort()

    print("Números aleatorios ordenados:", numeros)

