import flet as ft
import mainlogin
import mainInicio

def main(page: ft.Page):
    page.title = "Controlador"

    def show_mainlogin(e):
        page.clean()
        mainlogin.main_login(page)

    # Verificar si el usuario tiene una sesión iniciada
    username = page.client_storage.get("username")
    user_info = page.client_storage.get("user_info")

    if username and user_info:  # Si hay username y user_info en client_storage, se asume sesión iniciada
        mainInicio.main_Inicio(page, username, user_info)
    else:
        show_mainlogin(None)

ft.app(target=main)
