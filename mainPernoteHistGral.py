import flet as ft
import mainInicio
import requests
import asyncio

def mainPernote_Historial_General(page: ft.Page):
    page.clean()
    page.title= "Pernoctes Historial General"

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


    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        actions=[ft.PopupMenuButton(
            items=[ft.PopupMenuItem(text= "Vaciar",icon=ft.Icons.DELETE,on_click=lambda e: asyncio.run(vaciar_historial_general_pernote(page)))])],
        leading=ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click=lambda e: mainInicio.main_Inicio(page,page.client_storage.get("username"),
                                                                        page.client_storage.get("user_info"))),
        
        )

    page.add(app_bar)

    # FUNCION PARA VACIAR EL HISTORIAL GENERAL
    async def vaciar_historial_general_pernote(page): #Agregamos page como argumento
        def close_dlg(e):
            password_dialog_gral.open = False
            page.update()

        async def check_password(e): #Hacemos check_password asincrona
            password = password_field.value
            FLASK_URL_VACIAR_GENERAL = "http://nicolasdominguez.pythonanywhere.com/vaciar_historial_general"
            try:
                response = requests.delete(FLASK_URL_VACIAR_GENERAL, json={'password': password})
                response.raise_for_status()
                print("Historial general vaciado con éxito")
                rows.clear()
                container_historial_general.controls.clear()
                page.update()
                password_dialog_gral.open = False
                page.update()
            except requests.exceptions.RequestException as e:
                print(f"Error al vaciar el historial general: {e}")
                password_error.value = "Contraseña incorrecta"
                page.update()

        password_field = ft.TextField(password=True, can_reveal_password=True)
        password_error = ft.Text("", color=ft.Colors.RED)

        password_dialog_gral = ft.AlertDialog(
            modal=True,
            title=ft.Text("Ingrese la contraseña admin", text_align=ft.TextAlign.CENTER),
            content=ft.Column([password_field, password_error], alignment=ft.MainAxisAlignment.CENTER, height=80),
            actions=[
                ft.ElevatedButton("Aceptar", on_click=lambda e: asyncio.run(check_password(e))), #Hacemos check_password asincrona
                ft.ElevatedButton("Cancelar", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            on_dismiss=lambda e: print("Dialog dismissed!"),
        )
        page.add(password_dialog_gral)
        password_dialog_gral.open = True
        page.update()


    # OBTENER HISTORIAL GENERAL DE REGISTROS DESDE EL BACKEND
    async def obtener_registros_general(page): #Hacemos obtener_registros asincrona
        FLASK_URL_GENERAL = "https://nicolasdominguez.pythonanywhere.com/historial_general_pernocte"
        try:
            username = page.client_storage.get("username")
            headers = {'X-Username': username}
            response = requests.get(FLASK_URL_GENERAL, headers=headers)
            response.raise_for_status()
            registros = response.json()
            return registros
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener el historial general: {e}")
            return []

    registros = asyncio.run(obtener_registros_general(page)) #Llamamos a obtener_registros de forma asincrona
    registros.reverse()


    # Mostrar los registros en la página
    rows = []
    for registro in registros:
        row = ft.Row(
            [
                ft.Column([ft.Text(f"{registro['fecha_entrada']} - {registro['lugar_pernocte']}", color=ft.Colors.CYAN_ACCENT, style=ft.TextStyle(weight=ft.FontWeight.BOLD),expand=True),
                           ft.Text(f"Nombre y Legajo: {registro['nombre']} - {registro['legajo']}", color=ft.Colors.WHITE,style=ft.TextStyle(size=11),expand=True),
                           ft.Text(f"Entrada: {registro['fecha_entrada']} - {registro['hora_entrada']}", color=ft.Colors.WHITE,style=ft.TextStyle(size=11),expand=True),
                           ft.Text(f"Salida: {registro['fecha_salida']} - {registro['hora_salida']}", color=ft.Colors.WHITE,style=ft.TextStyle(size=11),expand=True),
                           ft.Text(f"Tren llegada: {registro['tren_remis_entrada']} - Tren salida: {registro['tren_remis_salida']}", color=ft.Colors.WHITE,style=ft.TextStyle(size=11),expand=True),
                           ft.Text(f"Obs. llegada: {registro['observaciones_entrada']}", color=ft.Colors.WHITE,style=ft.TextStyle(size=11),expand=True),
                           ft.Text(f"Obs. salida: {registro['observaciones_salida']}", color=ft.Colors.WHITE,style=ft.TextStyle(size=11),expand=True)
                       ],spacing=4,expand=True),
            ],
            alignment=ft.MainAxisAlignment.START,expand=True
        )
    
        
    # Contenedor para el registro con estilo
        container_registro_general = ft.Container(
            content=row, # Ajustar el ancho al tamaño de la pantalla
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=10),
            border_radius=ft.border_radius.all(8),
            bgcolor='#000740',
            
        )

        rows.append(container_registro_general)
    
    
    def on_column_scroll(e: ft.OnScrollEvent):
        print(
            f"Type: {e.event_type}, pixels: {e.pixels}, min_scroll_extent: {e.min_scroll_extent}, max_scroll_extent: {e.max_scroll_extent}"
        )


    container_historial_general = ft.Column(
        controls=rows,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=10,
        height=500,
        scroll= ft.ScrollMode.AUTO,
        on_scroll= on_column_scroll
    )

    titulo= ft.Text("Historial General Pernoctes", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))

    columna1= ft.Column(
        controls=[titulo,container_historial_general],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )

    page.add(columna1)

#ft.app(target=mainPernote_Historial_General)
