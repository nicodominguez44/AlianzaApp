import flet as ft
import mainInicio
import mainNovedadHistGral
import requests

def mainNovedad_Historial(page: ft.Page):
    page.clean()
    page.title= "Novedades Historial"

    page.decoration = ft.BoxDecoration(
        gradient= ft.LinearGradient(
            colors=['#0542fa', '#000740'],
            stops=[0,1],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        )
    )

    page.bgcolor= ft.Colors.TRANSPARENT
    page.window.width=360
    page.window.height=720
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.padding= ft.padding.only(left=30, top=10, right=30, bottom=30)


    logo = ft.Image(src= 'logoFrateAlianza1.png',width=70,)
    titulo= ft.Text("Historial Novedades", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))

    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text= "Vaciar", icon=ft.icons.DELETE,on_click=lambda e: vaciar_historial_novedad()),
                    ft.PopupMenuItem(text="Historial General (admin)",icon=ft.icons.MENU_BOOK_ROUNDED,on_click=lambda e:mainNovedadHistGral.mainNovedad_Historial_General(page))
                ],
                icon=ft.icons.MORE_VERT, icon_color= ft.Colors.BLUE_900
            ),
        ]
    )

    page.add(app_bar)

    # FUNCION PARA VACIAR EL HISTORIAL DE NOVEDADES INDIVIDUAL

    def vaciar_historial_novedad():

        def close_dlg(e):
            password_dialog.open = False
            page.update()

        def check_password(e):
            password = password_field.value
            username = page.client_storage.get("username")
            FLASK_URL_VERIFICAR = f"https://nicolasdominguez.pythonanywhere.com/verificar_historial_password/{username}"
            try:
                response = requests.post(FLASK_URL_VERIFICAR, json={'password': password})
                response.raise_for_status()
                result = response.json()['result']
                if result:
                    FLASK_URL_VACIAR_NOV = f"https://nicolasdominguez.pythonanywhere.com/vaciar_historial_novedad/{username}" 
                    response_vaciar = requests.delete(FLASK_URL_VACIAR_NOV, json={'password': password})
                    response_vaciar.raise_for_status()
                    print("Historial vaciado con éxito")
                    rows.clear()
                    container_novedad.controls.clear()
                    page.update()
                    password_dialog.open = False
                    page.update()
                else:
                    password_error.value = "Contraseña incorrecta"
                    page.update()
            except requests.exceptions.RequestException as e:
                print(f"Error al verificar la contraseña: {e}")

        password_field = ft.TextField(password=True, can_reveal_password=True)
        password_error = ft.Text("", color=ft.colors.RED)

        password_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Ingrese la contraseña", text_align=ft.TextAlign.CENTER),
            content=ft.Column([password_field, password_error], alignment=ft.MainAxisAlignment.CENTER, height=80),
            actions=[
                ft.ElevatedButton("Aceptar", on_click=check_password),
                ft.ElevatedButton("Cancelar", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            on_dismiss=lambda e: print("Dialog dismissed!"),

        )
        page.add(password_dialog)
        password_dialog.open = True
        page.update()

    # Leer los registros desde el archivo JSON
    url = f"https://nicolasdominguez.pythonanywhere.com/novedades/{page.client_storage.get('username')}" 
    try:
        response = requests.get(url)
        response.raise_for_status()
        registros = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener registros del backend: {e}")
        registros = []

    registros.reverse()

    # Mostrar los registros en la página
    rows = []
    for registro in registros:
        row = ft.Row(
            [
                ft.Column([ft.Text(f"{registro['pernocte_novedad']} - {registro['fecha_novedad']}", color=ft.Colors.CYAN_ACCENT, style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                           ft.Text(f"Novedad: {registro['novedad']}", color=ft.Colors.WHITE,style=ft.TextStyle(size=12),
                                   expand=True),
                           
                       ],spacing=5,expand=True),
            ],
            alignment=ft.MainAxisAlignment.START,expand=True
        )
    
        
    # Contenedor para el registro con estilo
        container_registro_nov = ft.Container(
            content=row, # Ajustar el ancho al tamaño de la pantalla
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=10),
            border_radius=ft.border_radius.all(8),
            bgcolor=ft.Colors.BLUE_900,
            
        )

        rows.append(container_registro_nov)
    
    
    def on_column_scroll(e: ft.OnScrollEvent):
        print(
            f"Type: {e.event_type}, pixels: {e.pixels}, min_scroll_extent: {e.min_scroll_extent}, max_scroll_extent: {e.max_scroll_extent}"
        )


    container_novedad = ft.Column(
        controls=rows,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=10,
        height=380,
        scroll= ft.ScrollMode.AUTO,
        on_scroll= on_column_scroll
    )

    



    row9= ft.Row(
        [
            ft.ElevatedButton(
            text="Ir al inicio",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD),color=ft.Colors.WHITE),
            expand=True,height=50, bgcolor=ft.Colors.BLUE_ACCENT,
            on_click=lambda e: mainInicio.main_Inicio(page,page.client_storage.get("username"), page.client_storage.get("user_info")))
        ]
    )

    columna1= ft.Column(
        controls=[logo,titulo,container_novedad],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10    
    )


    columna2= ft.Column(
        controls=[row9],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=35
    )

    columna3= ft.Column(
        controls=[columna1,columna2],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )
   
    page.add(columna3)

