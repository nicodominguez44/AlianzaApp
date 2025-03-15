import flet as ft
import mainlogin
import mainInicio


def main(page: ft.Page):
    page.title: "controlador"

    def show_mainlogin(e):
        page.clean()
        mainlogin.main_login(page)

    usuario_sesion = mainlogin.main_login(page)

    if usuario_sesion:
        mainInicio.main_Inicio(page,page.client_storage.get("username"), page.client_storage.get("user_info"))
    else:
        show_mainlogin(None)

ft.app(target=main)
