import random

def recibir_ecuacion():
    a = float(input("Ingrese el coeficiente 'a': "))
    b = float(input("Ingrese el coeficiente 'b': "))
    c = float(input("Ingrese el coeficiente 'c': "))
    return a, b, c

def obtener_numero():
    numero = int(input("\nIngrese un número del 1 al 5: "))
    while numero < 1 or numero > 5:
        print("Número fuera del rango. Inténtelo de nuevo.")
        numero = int(input("Ingrese un número del 1 al 5: "))
    return 2 ** numero

def generar_binarios(cantidad):
    binarios = []
    for _ in range(cantidad):
        signo = random.choice(['0', '1'])
        numero = ''.join(random.choice('01') for _ in range(8))
        decimal = ''.join(random.choice(['0', '1']))  # Parte decimal de longitud 2
        binario = signo + numero + decimal
        decimal_value = binario_a_decimal(binario)
        evaluacion = evaluar_ecuacion(a, b, c, decimal_value)
        binarios.append((binario, decimal_value, evaluacion))
    return binarios

def binario_a_decimal(binario):
    signo = -1 if binario[0] == '1' else 1
    numero = int(binario[1:9], 2)
    decimal = 0.5 if binario[9] == '1' else 0
    return signo * (numero + decimal)

def evaluar_ecuacion(a, b, c, x):
    return a * x ** 2 + b * x + c

def mezclar_cromosomas(binarios_sorted):
    new_binaries = []
    option = random.choice(["mejor_con_mejor", "mejor_con_peor", "aleatorio"])
    print(f"\nOrden de mezcla de cromosomas: {option}")

    if option == "mejor_con_mejor":
        pairs = [(binarios_sorted[i], binarios_sorted[i + 1]) for i in range(0, len(binarios_sorted) - 1, 2)]
    elif option == "mejor_con_peor":
        pairs = [(binarios_sorted[i], binarios_sorted[-(i + 1)]) for i in range(len(binarios_sorted) // 2)]
    else:
        random.shuffle(binarios_sorted)
        pairs = [(binarios_sorted[i], binarios_sorted[i + 1]) for i in range(0, len(binarios_sorted) - 1, 2)]

    start_index = random.randint(0, 9)  # Random start index between 0 and 9
    print(f"Posición de inicio para XOR en todos los pares: {start_index}")

    for pair in pairs:
        bin1, bin2 = pair
        new_bin1 = bin1[0][:start_index]  # Extract the prefix from bin1
        new_bin2 = bin2[0][:start_index]  # Extract the prefix from bin2

        # Ensure bin1 and bin2 have the same length
        if len(bin1[0]) < 10:
            bin1 = (bin1[0][0] + '0' * (10 - len(bin1[0])), bin1[1], bin1[2])
        if len(bin2[0]) < 10:
            bin2 = (bin2[0][0] + '0' * (10 - len(bin2[0])), bin2[1], bin2[2])

        for i in range(start_index, 10):
            new_bin1 += str(int(bin1[0][i]) ^ int(bin2[0][i]))  # Apply XOR bit by bit
            new_bin2 += str(int(bin2[0][i]) ^ int(bin1[0][i]))  # Apply XOR bit by bit

        new_decimal1 = binario_a_decimal(new_bin1)
        new_decimal2 = binario_a_decimal(new_bin2)
        new_eval1 = evaluar_ecuacion(a, b, c, new_decimal1)
        new_eval2 = evaluar_ecuacion(a, b, c, new_decimal2)
        new_binaries.append((new_bin1, new_decimal1, new_eval1))
        new_binaries.append((new_bin2, new_decimal2, new_eval2))

    print("\nLos nuevos binarios después de mezclar son:")
    for binario in new_binaries:
        print(f"{binario[0]} ({binario[1]}): {binario[2]}")

    # Selección aleatoria de dos cromosomas para modificar
    chromosomes_to_modify = random.sample(range(len(new_binaries)), 2)
    positions_to_modify = [random.randint(0, 9) for _ in range(2)]
    print("\nSe han modificado los números en las siguientes posiciones:")
    for i in range(2):
        print(f"Cromosoma {chromosomes_to_modify[i] + 1}, posición {positions_to_modify[i] + 1}")

    # Modificar los números en las posiciones seleccionadas
    for i in range(2):
        chromosome_index = chromosomes_to_modify[i]
        position_index = positions_to_modify[i]
        old_bin = new_binaries[chromosome_index][0]
        new_bin = old_bin[:position_index] + str(1 - int(old_bin[position_index])) + old_bin[position_index + 1:]
        print(f"Cromosoma {chromosome_index + 1}: {old_bin} -> {new_bin}")

        new_decimal = binario_a_decimal(new_bin)
        new_eval = evaluar_ecuacion(a, b, c, new_decimal)
        new_binaries[chromosome_index] = (new_bin, new_decimal, new_eval)

    # Imprimir la matriz final
    print("\nLa matriz completa después de las modificaciones es:")
    for binario in new_binaries:
        print(f"{binario[0]} ({binario[1]}): {binario[2]}")

    return new_binaries

# Inicialización
matriz_inicial = None

# Solicitar número de generaciones
num_generaciones = int(input("Ingrese el número de generaciones a ciclar: "))

# Ciclo principal
for generacion in range(1, num_generaciones + 1):
    print(f"\n{'GENERACION ' + str(generacion):^40}")
    if matriz_inicial is None:
        a, b, c = recibir_ecuacion()
        print(f"\nLa ecuación de segundo grado ingresada es: {a}x² + {b}x + {c}")

        numero = obtener_numero()
        print(f"\t2 elevada a la {numero}")

        binarios = generar_binarios(numero)
    else:
        binarios = matriz_inicial

    binarios_sorted = sorted(binarios, key=lambda x: x[2], reverse=True)

    print("\nLos números binarios aleatorios generados son:")
    for binario in binarios_sorted:
        print(f"{binario[0]} ({binario[1]}): {binario[2]}")

    nuevos_binarios = mezclar_cromosomas(binarios_sorted)
    matriz_inicial = nuevos_binarios
