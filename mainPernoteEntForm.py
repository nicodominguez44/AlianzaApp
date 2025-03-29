import flet as ft
import datetime
import locale
import accionBotonPern
import mainPernoteSal
import mainPernoteEnt
import globals
import json
import os
import requests

ARCHIVO_DATOS_ENTRADA = "datos_entrada.json"

def guardar_datos_entrada():
    print("Guardando datos de entrada...")
    datos = {
        "selected_option_pernocte": globals.selected_option_pernocte,
        "selected_date_ent": globals.selected_date_ent,
        "selected_time_ent": globals.selected_time_ent,
        "writed_name": globals.writed_name,
        "writed_legajo": globals.writed_legajo,
        "writed_train_ent": globals.writed_train_ent,
        "writed_obs_ent": globals.writed_obs_ent,
    }
    with open(ARCHIVO_DATOS_ENTRADA, "w") as f:
        json.dump(datos, f)


def cargar_datos_entrada():
    if os.path.exists(ARCHIVO_DATOS_ENTRADA):
        with open(ARCHIVO_DATOS_ENTRADA, "r") as f:
            datos = json.load(f)
            globals.selected_option_pernocte = datos.get("selected_option_pernocte", "")
            globals.selected_date_ent = datos.get("selected_date_ent", "")
            globals.selected_time_ent = datos.get("selected_time_ent", "")
            globals.writed_name = datos.get("writed_name", "")
            globals.writed_legajo = datos.get("writed_legajo", "")
            globals.writed_train_ent = datos.get("writed_train_ent", "")
            globals.writed_obs_ent = datos.get("writed_obs_ent", "")





try:
    locale.setlocale(locale.LC_TIME, 'es_ES')
except locale.Error:
    print("La localidad 'es_ES' no está soportada, usando la predeterminada.")
    locale.setlocale(locale.LC_TIME, 'C')



def validar_campos_ent(page):
    # Validación para el nombre y apellido
    if globals.writed_name == "":
        page.update()
        return False
    
    # Validación para el legajo
    if globals.writed_legajo == "":
        page.update()
        return False
    
    # Validación para pernocte (PopupMenu)
    if globals.selected_option_pernocte == "seleccionar pernocte":
        page.update()
        return False
    
    # Validación para la fecha (DatePicker)
    if globals.selected_date_ent == "Sin seleccionar":

        page.update()
        return False
    
    # Validación para la hora (TimePicker)
    if globals.selected_time_ent == "Sin seleccionar":
        page.update()
        return False
    
    # Validacion para tren entrada
    if globals.writed_train_ent == "":
        page.update()
        return False
    
    # Validacion para observaciones entrada
    if globals.writed_obs_ent == "":
        page.update()
        return False


    # Si todo está completo, retorna True
    return True


def registrar_entrada(page):
    if validar_campos_ent(page):  # Si todo está bien

        # Obtener los datos del formulario
        username = page.client_storage.get("username")
        nombre = globals.writed_name
        legajo = globals.writed_legajo
        lugar_pernocte = globals.selected_option_pernocte
        fecha_entrada = globals.selected_date_ent
        hora_entrada = globals.selected_time_ent
        tren_remis_entrada = globals.writed_train_ent
        observaciones_entrada = globals.writed_obs_ent

        # Crear el diccionario con los datos
        datos_entrada = {
            "username": username,
            "nombre": nombre,
            "legajo": legajo,
            "lugar_pernocte": lugar_pernocte,
            "fecha_entrada": fecha_entrada,
            "hora_entrada": hora_entrada,
            "tren_remis_entrada": tren_remis_entrada,
            "observaciones_entrada": observaciones_entrada,
        }

        # Enviar la solicitud POST al backend
        FLASK_URL_REGISTRAR_ENTRADA = "https://nicolasdominguez.pythonanywhere.com/registrar_entrada"
        try:
            response = requests.post(FLASK_URL_REGISTRAR_ENTRADA, json=datos_entrada)
            response.raise_for_status()
            print("Entrada registrada con éxito")
            mainPernoteSal.mainPernote_Sal(page)  # Navegar a la página de salida
            guardar_datos_entrada()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error al registrar la entrada: {e}")
            return False
    else:
        return False


def mainPernote_EntForm(page: ft.Page):
    page.clean()
    page.title= "Entrada Form"

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
    page.padding= ft.padding.only(left=0, top=10, right=0, bottom=0)



    logo= ft.Image(src= 'logoFrateAlianza1.png',width=70,)
    titulo= ft.Text("Registrar Entrada", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))

    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        leading=ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,
                              icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click=lambda e: mainPernoteEnt.mainPernote_Ent(page))
    )

    page.add(app_bar)

    #Textfields de formulario
           # SELECCION DE PERNOCTE

    selected_option_text= "seleccionar pernocte"
    selected_option= ft.Text(selected_option_text, color= ft.Colors.BLUE_900, style=ft.TextStyle(size=18))

    def update_selected_pernocte(option):
        globals.selected_option_pernocte = option  # Actualizamos el valor global con la opción seleccionada
        selected_option.value = option  # Actualizamos el valor en el widget Text
        page.update()

    popupMenu= ft.PopupMenuButton(
                icon_color= ft.Colors.BLUE_GREY_900,
                bgcolor= ft.Colors.BLACK87,
                icon= ft.Icons.ARROW_DROP_DOWN_CIRCLE, icon_size=35,
                
                items=[
                    ft.PopupMenuItem(text="Dock Central",on_click=lambda e: update_selected_pernocte("Dock Central")),
                    ft.PopupMenuItem(text="Mercedes BAP", on_click=lambda e: update_selected_pernocte("Mercedes BAP")),
                    ft.PopupMenuItem(text="Campana",on_click=lambda e: update_selected_pernocte("Campana")),
                    ft.PopupMenuItem(text="Junin",on_click=lambda e: update_selected_pernocte("Junin")),
                
                    ]
                
                )
    
            # OBTENER NOMBRE, APELLIDO Y LEGAJO DE USUARIO

    username = page.client_storage.get("username")
    FLASK_URL_DATOS_USUARIO = f"https://nicolasdominguez.pythonanywhere.com/datos_usuario/{username}"
    try:
        response = requests.get(FLASK_URL_DATOS_USUARIO)
        response.raise_for_status()
        datos_usuario = response.json()
        globals.writed_name = datos_usuario['nombre']
        globals.writed_legajo = datos_usuario['legajo']
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos del usuario: {e}")
        globals.writed_name = "Error al cargar"
        globals.writed_legajo = "Error al cargar"

    # Mostrar los datos del usuario en la interfaz
    nombre_legajo = ft.Text(f"{globals.writed_name} - {globals.writed_legajo}", color=ft.colors.CYAN_ACCENT,style=ft.TextStyle(size=15),text_align= ft.TextAlign.CENTER)
    #legajo_usuario = ft.Text(f"{globals.writed_legajo}", color=ft.colors.CYAN_ACCENT,style=ft.TextStyle(size=15),text_align= ft.TextAlign.CENTER)
    
            # NOMBRE
    nombreylegajo=ft.Text("Nombre y Legajo", color= ft.Colors.WHITE, style=ft.TextStyle(size=10),text_align= ft.TextAlign.CENTER)
    nombre_columna= ft.Column([nombreylegajo,nombre_legajo],spacing=5,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    
            # LLEGÓ EN TREN O REMIS

    tren_remis=ft.Text("Tren/Remis", color= ft.Colors.WHITE, style=ft.TextStyle(size=10))

    def actualizar_tren(e):
        globals.writed_train_ent = tf_tren_remis.value
        page.update()

    tf_tren_remis=ft.TextField(
                bgcolor=ft.Colors.WHITE, text_size=14,color=ft.Colors.BLACK, autofocus=False,
                border_radius=ft.border_radius.only(top_left=0,top_right=15,bottom_left=15,bottom_right=15),
                border_color=ft.Colors.CYAN_ACCENT, on_change= actualizar_tren
                )
    
    tren_columna= ft.Column([tren_remis,tf_tren_remis], expand= True,spacing=5)

            # OBSERVACIONES AL ENTRAR

    observaciones=ft.Text("Observaciones al llegar", color= ft.Colors.WHITE, style=ft.TextStyle(size=10))

    def actualizar_obs(e):
        globals.writed_obs_ent = tf_observaciones.value
        page.update()

    tf_observaciones=ft.TextField(
                bgcolor=ft.Colors.WHITE, text_size=14,color=ft.Colors.BLACK, autofocus=False,
                border_radius=ft.border_radius.only(top_left=0,top_right=15,bottom_left=15,bottom_right=15),
                border_color=ft.Colors.CYAN_ACCENT, multiline=True, max_length=70, on_change= actualizar_obs
                )
    
    observaciones_columna= ft.Column([observaciones,tf_observaciones], expand= True,spacing=5)

            # FECHA DE ENTRADA

    selected_date_text=ft.Text("Sin seleccionar",color= ft.Colors.WHITE,
                               style=ft.TextStyle(size=14,weight=ft.FontWeight.BOLD))

    def handle_change(e):
        # Actualizar el texto con la nueva fecha seleccionada
        date_selected = e.control.value.strftime('%d %B %Y')  # Formato "13 de febrero de 2025"
        selected_date_text.value = f"{date_selected}"  # Actualizar el texto
        globals.selected_date_ent = date_selected
        page.update()  # Actualizar la interfaz para reflejar el cambio

    def handle_dismissal(e):
        selected_date_text.value = "Sin seleccionar"
        page.update()  # Actualizar la interfaz para reflejar el cambio

    RowFechaEnt= ft.Row([
        ft.ElevatedButton(
                    "Fecha", color=ft.Colors.BLUE_900,
                    bgcolor=ft.Colors.WHITE,
                    icon=ft.Icons.CALENDAR_MONTH, icon_color=ft.Colors.BLUE_900,
                    on_click=lambda e: page.open(
                        ft.DatePicker(
                            first_date=datetime.datetime(year=2023, month=10, day=1),
                            last_date=datetime.datetime(year=2033, month=10, day=1),
                            on_change=handle_change,
                            on_dismiss=handle_dismissal,
                        )
                    ),
                ),
                selected_date_text  # Añadir el control de texto para la fecha seleccionada], expand=True)
        ], alignment=ft.MainAxisAlignment.CENTER)

            # HORA ENTRADA

    # Crear un texto para mostrar la hora seleccionada
    time_text = ft.Text("Sin seleccionar",color= ft.Colors.WHITE, style=ft.TextStyle(size=14,weight=ft.FontWeight.BOLD))

    def handle_change1(e):
        # Actualiza el texto con la hora seleccionada
        selected_time = e.control.value.strftime('%H:%M')
        time_text.value = f"{selected_time}"
        globals.selected_time_ent = selected_time
        page.update()

    def handle_dismissal1(e):
        # Actualiza el texto con la hora seleccionada cuando se cierre el TimePicker
        time_text.value = f"Sin seleccionar"
        page.update()

    def handle_entry_mode_change(e):
        # Actualiza el texto con el modo de entrada cuando cambia
        time_text.value = f"Entry mode changed to {e.entry_mode}"
        page.update()

    time_picker = ft.TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        on_change=handle_change1,
        on_dismiss=handle_dismissal1,
        on_entry_mode_change=handle_entry_mode_change,
    )

    RowhoraEnt=ft.Row([
        ft.ElevatedButton(
                    "Hora", color=ft.Colors.BLUE_900,
                    bgcolor=ft.Colors.WHITE,
                    icon=ft.Icons.TIME_TO_LEAVE,icon_color=ft.Colors.BLUE_900,
                    on_click=lambda _: page.open(time_picker),
                ), time_text
        ], alignment=ft.MainAxisAlignment.CENTER)

            # DISTRIBUCION DE LA INFORMACION

    cambiar_f2= accionBotonPern.obtener_cambiar_f2()

    container= ft.Container(
        bgcolor=ft.Colors.BLUE_700,
        alignment=ft.alignment.center,
        border_radius= ft.border_radius.only(top_left=20, top_right=20,bottom_left=0, bottom_right=0),
        expand= True,
        height=600,
        padding=ft.padding.only(left=20,top=20,right=20,bottom=10),

        content= ft.Column(
            [
            ft.Row([nombre_columna],spacing=10,alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(bgcolor=ft.Colors.WHITE,
                         alignment=ft.alignment.center,
                         border_radius= ft.border_radius.only(top_left=20, top_right=20,bottom_left=20, bottom_right=20),
                         height=50,
                         content=ft.Row([popupMenu,selected_option],
                                alignment=ft.MainAxisAlignment.START,expand=True)
                        ),
            RowFechaEnt,RowhoraEnt,
            ft.Row([tren_columna]),
            ft.Row([observaciones_columna]),
            ft.Row([ft.ElevatedButton(text="Registrar Entrada",
                                      style= ft.ButtonStyle(
                                          text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE)),
                                     expand=True,height=60,bgcolor=ft.Colors.GREEN_ACCENT_400, color=ft.Colors.WHITE,
                                     on_click=lambda e:(cambiar_f2(e) if registrar_entrada(page) else None))
                    ]) 
            ], spacing=15
        )
    )  

    columna1= ft.Column(
        controls=[logo,titulo],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10    
    )

    columna2= ft.Column(
        controls=[container],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )


    columna3= ft.Column(
        controls=[columna1,
                  ft.Container(padding=ft.padding.only(left=25,top=0,right=25,bottom=0),
                               expand=True,
                               content= columna2)],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll= ft.ScrollMode.AUTO, expand=True,
    )

    page.add(columna3)


    
            
