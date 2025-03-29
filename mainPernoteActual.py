import flet as ft
import mainInicio
import requests

def mainPernote_Actual(page: ft.Page):
    page.clean()
    page.title = "Pernoctes Actuales"

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
    page.padding= ft.padding.only(left=10, top=10, right=10, bottom=0)

    def eliminar_todas_entradas(e):
        def close_dlg(e):
            password_dialog.open = False
            page.update()

        def check_password(e):
            password = password_field.value
            FLASK_URL_ELIMINAR_TODAS = "https://nicolasdominguez.pythonanywhere.com/eliminar_todas_entradas"
            try:
                response = requests.delete(FLASK_URL_ELIMINAR_TODAS, json={'password': password})
                response.raise_for_status()
                print("Todas las entradas han sido eliminadas")
                
                password_dialog.open = False
                page.update()
                mainPernote_Actual(page)  # Recargar la página

            except requests.exceptions.RequestException as e:
                print(f"Error al eliminar todas las entradas: {e}")
                password_error.value = "Contraseña incorrecta"
                page.update()

        password_field = ft.TextField(password=True, can_reveal_password=True)
        password_error = ft.Text("", color=ft.Colors.RED)

        password_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Ingrese la contraseña admin", text_align=ft.TextAlign.CENTER),
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
       


    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        actions=[ft.PopupMenuButton(
            items=[ft.PopupMenuItem(text= "Vaciar",icon=ft.Icons.DELETE,on_click=lambda e: eliminar_todas_entradas(e))])],
        leading=ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click=lambda e: mainInicio.main_Inicio(page,page.client_storage.get("username"),
                                                                        page.client_storage.get("user_info"))),
        
        )
    page.add(app_bar)

    # Obtener los datos del backend
    FLASK_URL_OBTENER_ENTRADAS = "https://nicolasdominguez.pythonanywhere.com/obtener_entradas"
    try:
        response = requests.get(FLASK_URL_OBTENER_ENTRADAS)
        response.raise_for_status()
        entradas = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener las entradas: {e}")
        entradas = {}

    # Crear las secciones para cada lugar de pernocte
    secciones = {}
    for lugar in ["Dock Central", "Mercedes BAP", "Campana", "Junin"]:
        secciones[lugar] = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(lugar, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_ACCENT, text_align=ft.TextAlign.CENTER)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,expand=True,spacing=5),
            padding=10,
            border_radius=10,
            bgcolor=ft.Colors.BLUE_900,
            margin=5,expand=True)

    # Agregar las entradas a las secciones correspondientes
    for lugar, registros in entradas.items():
        if lugar in secciones:
            for registro in registros:
                detalles = f"{registro['legajo']}/{registro['nombre']}: {registro['fecha_entrada']}, {registro['hora_entrada']} - {registro['tren_remis_entrada']}{registro['observaciones_entrada']}"
                page.client_storage.set("id_registro_a_eliminar", registro['id'])
                print(f"ID almacenado: {page.client_storage.get('id_registro_a_eliminar')}")
                
                secciones[lugar].content.controls.append(
                    ft.Text(detalles, size=14, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER)
                )
                secciones[lugar].content.controls.append(ft.Divider(color=ft.Colors.WHITE24))

    

    # Crear la interfaz de usuario
    filas = [ft.Row(controls=[secciones[lugar]], expand=True) for lugar in secciones]
    
    page.add(
        ft.Column(
            controls=[*filas], scroll=ft.ScrollMode.AUTO,expand=True
        )
    )

#ft.app(mainPernote_Actual)
