import flet as ft
import mainNovedad
import mainlogin
import accionBotonPern
import os
import requests
import asyncio

ARCHIVO_SESION = "sesion.txt"

def cerrar_sesion(page):
    if os.path.exists(ARCHIVO_SESION):
        os.remove(ARCHIVO_SESION)
    mainlogin.main_login(page)


#FUNCION PARA OBTENER URL DE BOTON "NOTICIAS"
async def obtener_url_noticias(page):
    try:
        page.splash = ft.ProgressBar() #Muestra el indicador de carga
        page.update()
        response = requests.get("http://nicolasdominguez.pythonanywhere.com/obtener_url_noticias")
        response.raise_for_status()
        data = response.json()
        page.splash = None #Oculta el indicador de carga
        page.update()
        return data["url"]
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la URL de noticias: {e}")
        page.splash = None #Oculta el indicador de carga
        page.update()
        return None

async def on_click_noticias(page):
    url = await obtener_url_noticias(page)
    if url:
        await page.launch_url(url)


#FUNCION PARA OBTENER URL DE BOTON "INFORMACION UTIL"
async def obtener_url_informacion_util(page):
    try:
        page.splash = ft.ProgressBar() #Muestra el indicador de carga
        page.update()
        response = requests.get("http://nicolasdominguez.pythonanywhere.com/obtener_url_informacion_util")
        response.raise_for_status()
        data = response.json()
        page.splash = None #Oculta el indicador de carga
        page.update()
        return data["url"]
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la URL de informacion util: {e}")
        page.splash = None #Oculta el indicador de carga
        page.update()
        return None

async def on_click_informacion_util(page):
    url = await obtener_url_informacion_util(page)
    if url:
        await page.launch_url(url)


def main_Inicio(page: ft.Page, username: str, user_info: dict):
    page.clean()
    page.title= "Menu Inicio"

    page.decoration = ft.BoxDecoration(
        gradient= ft.LinearGradient(
            colors=[ft.Colors.BLUE_600, ft.Colors.INDIGO_900],
            stops=[0,1],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        )
    )

    page.bgcolor= ft.Colors.TRANSPARENT
    page.window.width=360
    page.window.height=720
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.padding= ft.padding.only(left=30, top=20, right=30, bottom=30)

    page.client_storage.set("username", username)
    page.client_storage.set("user_info", user_info)

    app_bar = ft.AppBar(
        title=ft.Text(f"Hola {user_info['nombre']}",color=ft.Colors.CYAN_ACCENT, size=14),
        bgcolor= ft.Colors.TRANSPARENT,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(
                        text= "Cerrar Sesión",
                        icon=ft.icons.EXIT_TO_APP,
                        on_click=lambda e: cerrar_sesion(page),
                    )
                ],
                icon=ft.icons.MORE_VERT, icon_color= ft.Colors.BLUE_900
            ),
        ]
    )

    page.add(app_bar)


    logo = ft.Image(src= 'assets/logoFrateAlianza1.png',width=70,)
    titulo= ft.Text("Menu Inicio", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))


    row1= ft.Row(
        [
            ft.ElevatedButton(
            text="Pernoctes",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_900)
            ),
            expand=True, height=70, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLUE_900,
            on_click= lambda e: accionBotonPern.boton_pernocte_f(e, page))
        ]
    )

    row2= ft.Row(
        [
            ft.ElevatedButton(
            text="Libro de Novedades",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_900)
            ),
            expand=True,height=70,bgcolor=ft.Colors.WHITE,color=ft.Colors.BLUE_900,
            on_click= lambda e: mainNovedad.main_Novedad(page))
        ]
    )


    row3= ft.Row(
        [
            ft.ElevatedButton(
            text="Web Alianza",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_900)
            ),
            expand=True,height=70,bgcolor=ft.Colors.WHITE,color=ft.Colors.BLUE_900,
            on_click= lambda _: asyncio.run(on_click_noticias(page)))
        ]
    ) 

    #row4= ft.Row(
        #[
           # ft.ElevatedButton(
           # text="Información Útil",
            #style= ft.ButtonStyle(
                #text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_900)
            #),
            #expand=True, height=70, bgcolor=ft.Colors.WHITE,color=ft.Colors.BLUE_900,
            #on_click=  lambda _: asyncio.run(on_click_informacion_util(page)))
        #]
    #)

    columna1= ft.Column(
        controls=[logo,titulo],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10    
    )


    columna2= ft.Column(
        controls=[row1, row2, row3],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=25
    )

    columna3= ft.Column(
        controls=[columna1,columna2],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=50
    )
   
    page.add(columna3)

