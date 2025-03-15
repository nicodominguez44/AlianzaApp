import flet as ft
import mainPernoteEnt
import mainPernoteSal
import os

ARCHIVO_ESTADO = "estado.txt"

def cargar_estado():
    if os.path.exists(ARCHIVO_ESTADO):
        with open(ARCHIVO_ESTADO, "r") as f:
            return [int(f.read())]
    else:
        return [1]  # Valor predeterminado

def guardar_estado(valor):
    with open(ARCHIVO_ESTADO, "w") as f:
        f.write(str(valor[0]))

accion_actual = cargar_estado()


def funcion_1(e, page):
    mainPernoteEnt.mainPernote_Ent(page)
    print("Función 1 ejecutada")


def funcion_2(e, page):
    mainPernoteSal.mainPernote_Sal(page)
    print("Función 2 ejecutada")



def cambiar_a_f1(e):     
    accion_actual[0] = 1
    print("cambiado a funcion1")
    guardar_estado(accion_actual)
    

def cambiar_a_f2(e):
    accion_actual[0] = 2
    print("cambiado a funcion2")
    guardar_estado(accion_actual)

    
def boton_pernocte_f(e, page):   
    if accion_actual[0] == 1:
        funcion_1(e, page)
    else:
        funcion_2(e, page)


def obtener_cambiar_f1():
    return cambiar_a_f1

def obtener_cambiar_f2():
    return cambiar_a_f2
