import flet as ft
import mainInicio
import requests


FLASK_URL = "https://nicolasdominguez.pythonanywhere.com/login"

def main_login(page: ft.Page):
    page.clean()
    page.title= "Menu Iniciar sesion"

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
    page.padding= ft.padding.only(left=30, top=50, right=30, bottom=30)


    logo = ft.Image(src= 'logoFrateAlianza1.png',width=70,)
    titulo= ft.Text("Iniciar Sesión", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))

    

    # Componentes da interface do usuário
    name_input = ft.TextField(
        autofocus=True, hint_text='Usuario',bgcolor=ft.Colors.WHITE, text_size=14,color=ft.Colors.BLACK,
                border_radius=ft.border_radius.only(top_left=0,top_right=15,bottom_left=15,bottom_right=15),
                border_color=ft.Colors.CYAN_ACCENT,keyboard_type=ft.KeyboardType.NUMBER)
    pass_input = ft.TextField( hint_text='Contraseña',
        password=True, can_reveal_password=True,bgcolor=ft.Colors.WHITE, text_size=14,color=ft.Colors.BLACK,
                border_radius=ft.border_radius.only(top_left=0,top_right=15,bottom_left=15,bottom_right=15),
                border_color=ft.Colors.CYAN_ACCENT,)
    
    error_message = ft.Text("", color="red", size=14, text_align=ft.TextAlign.CENTER)


    def on_login_click(e, name_input, pass_input, error_message, page):
        username = name_input.value
        password = pass_input.value

        # Realizamos la solicitud POST al backend Flask para verificar las credenciales
        response = requests.post(FLASK_URL, json={'username': username, 'password': password})
        
        
        if response.status_code == 200:
            try:
                result = response.json()
                error_message.value = result.get('message', 'Login exitoso')
                mainInicio.main_Inicio(page, result.get('username'), result.get('user_info')) #Modificacion aqui
            except requests.exceptions.JSONDecodeError:
                error_message.value = "Respuesta del servidor inválida."
        else:
            error_message.value = f"Error: {response.status_code} - {response.text}"
        page.update()

# Limpiar los campos después de intentarlo
    name_input.value = ""
    pass_input.value = ""
    page.update()
    
    
    submit_btn = ft.Row([ft.ElevatedButton(
        text='Iniciar Sesion',
        style= ft.ButtonStyle(text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE)),
         expand=True,height=70,on_click= lambda e: on_login_click(e, name_input, pass_input, error_message, page),
         bgcolor=ft.Colors.WHITE,color=ft.Colors.BLUE_900)],)


    columna1= ft.Column(
        controls=[logo,titulo],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10    
    )

    columna2= ft.Column(
        controls=[name_input, pass_input, submit_btn, error_message],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30
    )

    columna3= ft.Column(
        controls=[columna1,columna2],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=50
    )


    page.update()
    page.add(columna3)
