import flet as ft
import mainPernoteEnt
import mainPernoteSal



def funcion_1(e, page):
    mainPernoteEnt.mainPernote_Ent(page)
    print("Función 1 ejecutada")


def funcion_2(e, page):
    mainPernoteSal.mainPernote_Sal(page)
    print("Función 2 ejecutada")



def cambiar_a_f1(page):     
    page.client_storage.set("estado_boton_pernocte", 1)
    print("Estado del botón cambiado a función 1 (entrada)")
    

def cambiar_a_f2(page):
    page.client_storage.set("estado_boton_pernocte", 2)
    print("Estado del botón cambiado a función 2 (salida)")

    
def boton_pernocte_f(e, page):   
    estado = page.client_storage.get("estado_boton_pernocte")
    if estado == 2:
        funcion_2(e, page)
    else:
        funcion_1(e, page)


def obtener_cambiar_f1():
    return cambiar_a_f1

def obtener_cambiar_f2():
    return cambiar_a_f2
