#Libraries
import math
import time
import os
 
#Funciones
def espacio(x):
    if x >= 1:
        print("")
        x = x-1
 
wait = time.sleep
blank = os.system('cls')
 
#Bucle
while True:
    #Seleccion de operaciones
    print("""Selecciona la operacion deseada:
1.Suma
2.Resta
3.Multiplicacion
4.Division
5.Division exacta
6.Potencia
7.Apagar calculadora""")
    espacio(1)
 
    #Switch_01
    c=int(input())
 
    #Apagar calculadora
    if c == 7:
        print ("Gracias por usar esta calculadora")
        wait(2)
        quit()
 
    #Seleccion de numeros
    else:
        print("Escribe el primer numero")
        a=int(input())
        print("Escribe el segundo numero")
        b=int(input())
        espacio(2)
        print("El resultado de esta operacion és:")
 
        #Suma
        if c == 1:
            print(a+b)
            print("")
        #Resta
        if c == 2:
            print(a-b)
            print("")
        #Multiplicacion
        if c == 3:
            print(a*b)
            print("")
        #Division
        if c == 4:
            print(a/b)
            print("")
        #Division exacta
        if c == 5:
            print(a//b)
            print("")
#Final de programa