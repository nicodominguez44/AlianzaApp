import flet as ft
import mainInicio
import requests

def mainNovedad_Historial_General(page: ft.Page):
    page.clean()
    page.title= "Novedades Historial General"

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
    page.padding= ft.padding.only(left=30, top=10, right=30, bottom=30)


    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        actions=[ft.PopupMenuButton(
            items=[ft.PopupMenuItem(text= "Vaciar",icon=ft.Icons.DELETE,on_click=lambda e: vaciar_historial_general_novedad())])],
        leading=ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click=lambda e: mainInicio.main_Inicio(page,page.client_storage.get("username"),
                                                                        page.client_storage.get("user_info"))),
        
        )

    page.add(app_bar)

    # FUNCION PARA VACIAR EL HISTORIAL GENERAL DE NOVEDADES
    def vaciar_historial_general_novedad():

        def close_dlg(e):
            password_dialog_gral.open = False
            page.update()

        def check_password(e):
            password = password_field.value
            FLASK_URL_VACIAR_NOV_GENERAL = "https://nicolasdominguez.pythonanywhere.com/vaciar_historial_general_novedades"
            try:
                response = requests.delete(FLASK_URL_VACIAR_NOV_GENERAL, json={'password': password})
                response.raise_for_status()
                print("Historial general NOVEDAD vaciado con éxito")
                rows.clear()
                container_novedad_general.controls.clear()
                page.update()
                password_dialog_gral.open = False
                page.update()
            except requests.exceptions.RequestException as e:
                print(f"Error al vaciar el historial general de novedades: {e}")
                password_error.value = "Contraseña incorrecta"
                page.update()

        password_field = ft.TextField(password=True, can_reveal_password=True)
        password_error = ft.Text("", color=ft.Colors.RED)

        password_dialog_gral = ft.AlertDialog(
            modal=True,
            title=ft.Text("Ingrese la contraseña admin",text_align=ft.TextAlign.CENTER),
            content=ft.Column([password_field, password_error],alignment=ft.MainAxisAlignment.CENTER,height=80),
            actions=[
                ft.ElevatedButton("Aceptar", on_click=check_password),
                ft.ElevatedButton("Cancelar", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            on_dismiss=lambda e: print("Dialog dismissed!"),
        )
        page.add (password_dialog_gral)
        password_dialog_gral.open = True
        page.update()


    # OBTENER HISTORIAL GENERAL DE NOVEDADES DESDE EL BACKEND
    FLASK_URL_NOV_GENERAL = "https://nicolasdominguez.pythonanywhere.com/novedades_general"
    try:
        username = page.client_storage.get("username")
        headers = {'X-Username': username}
        response = requests.get(FLASK_URL_NOV_GENERAL, headers=headers)
        response.raise_for_status()
        registros = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el historial general: {e}")
        registros = []

    registros.reverse()


    # Mostrar los registros en la página
    rows = []
    for registro in registros:
        row = ft.Row(
            [
                ft.Column([
                    ft.Text(f"{registro['pernocte_novedad']} - {registro['fecha_novedad']}", color=ft.Colors.CYAN_ACCENT,style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ft.Text(f"Nombre: {registro['nombre']} - Legajo: {registro['legajo']}", color=ft.Colors.WHITE,style=ft.TextStyle(size=12)),
                    ft.Text(f"Novedad: {registro['novedad']}", color=ft.Colors.WHITE, style=ft.TextStyle(size=12),expand=True)
                ], spacing=5, expand=True),
            ],
            alignment=ft.MainAxisAlignment.START,expand=True
        )
    
        
    # Contenedor para el registro con estilo
        container_novedad_general = ft.Container(
            content=row, # Ajustar el ancho al tamaño de la pantalla
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=10),
            border_radius=ft.border_radius.all(8),
            bgcolor=ft.Colors.BLUE_900,
            
        )

        rows.append(container_novedad_general)
    
    
    def on_column_scroll(e: ft.OnScrollEvent):
        print(
            f"Type: {e.event_type}, pixels: {e.pixels}, min_scroll_extent: {e.min_scroll_extent}, max_scroll_extent: {e.max_scroll_extent}"
        )


    container_novedad_general = ft.Column(
        controls=rows,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=10,
        height=500,
        scroll= ft.ScrollMode.AUTO,
        on_scroll= on_column_scroll
    )

    titulo= ft.Text("Historial General de Novedades", color= ft.Colors.WHITE, style=ft.TextStyle(size=18,weight=ft.FontWeight.BOLD))

    columna1= ft.Column(
        controls=[titulo,container_novedad_general],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )

    page.add(columna1)

#ft.app(target=mainNovedad_Historial_General)