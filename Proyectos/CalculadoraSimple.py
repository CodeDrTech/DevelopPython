#Trae funcion para limpar consola
from os import system


def Sumar(F1, F2):    
    return F1+F2

def Restar(F1, F2):
    return F1-F2
    
def Multiplicar(F1, F2):
    return F1*F2
    
def Dividir(F1, F2):
    return F1/F2
    


#Elegir opcion a calcular
print("Que quieres hacer? \n" "Sumar= S \n" "Restar= R \n" "Multiplicar= M \n" "Dividir= D")
Respuesta=input()
Respuesta=Respuesta.upper()

if Respuesta=="S":
    print("Inserte el primer dato y presione enter")
    N1=float(input())
    print("Inserte el segundo dato y presione enter")
    N2=float(input())
    resultado=Sumar(N1,N2)
elif Respuesta=="R":
    print("Inserte el primer dato y presione enter")
    N1=float(input())
    print("Inserte el segundo dato y presione enter")
    N2=float(input())
    resultado=Restar(N1,N2)
elif Respuesta=="M":
    print("Inserte el primer dato y presione enter")
    N1=float(input())
    print("Inserte el segundo dato y presione enter")
    N2=float(input())
    resultado=Multiplicar(N1,N2)
elif Respuesta=="D":
    print("Inserte el primer dato y presione enter")
    N1=float(input())
    print("Inserte el segundo dato y presione enter")
    N2=float(input())
    resultado=Dividir(N1,N2)
else:print("No es una respuesta valida")

Sumar()

#Datos a insertar por parte de usuario
#print("Inserte el primer dato y presione enter")
#N1=float(input())
#print("Inserte el segundo dato y presione enter")
#N2=float(input())

#Imprime el resultado de la operacion
print(f'El resultado de la operacion es {resultado}')

print("Desea limpiar la consola? Sí= Y No= N")
Respuesta_limpiar_consola=input()
Respuesta_limpiar_consola=Respuesta_limpiar_consola.upper()

if Respuesta_limpiar_consola =="Y":
    system("cls")
    
else:print("Vuelva a ejecutar el programa para reiniciar")