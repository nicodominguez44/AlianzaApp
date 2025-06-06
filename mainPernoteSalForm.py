import flet as ft
import datetime
import locale
import accionBotonPern
import mainPernoteSal
import mainPernoteFinal
import globals
import os
import requests
import asyncio



try:
    locale.setlocale(locale.LC_TIME, 'es_ES')
except locale.Error:
    print("La localidad 'es_ES' no está soportada, usando la predeterminada.")
    locale.setlocale(locale.LC_TIME, 'C')


def validar_campos_sal(page):
    
    
    # Validación para el tren de salida
    if globals.writed_train_sal == "":
        page.update()
        return False
    
    
    # Validación para la fecha (DatePicker)
    if globals.selected_date_sal == "Sin seleccionar":
        page.update()
        return False
    
    # Validación para la hora (TimePicker)
    if globals.selected_time_sal == "Sin seleccionar":
        page.update()
        return False
    
    # Validacion para las observaciones de salida
    if globals.writed_obs_sal == "":
        page.update()
        return False


    # Si todo está completo, retorna True
    return True

# Crea el ProgressRing
progress_ring = ft.ProgressRing(color=ft.Colors.WHITE)

# Crea el AlertDialog con el ProgressRing
dialog_carga = ft.AlertDialog(
    title=ft.Text("Registrando...",text_align=ft.TextAlign.CENTER,color=ft.Colors.WHITE),
    content=ft.Column([progress_ring], horizontal_alignment=ft.CrossAxisAlignment.CENTER,alignment=ft.MainAxisAlignment.CENTER,height=100),
    modal=True,bgcolor=ft.Colors.BLACK45
)

def dialog_open(page):
    page.add(dialog_carga)
    dialog_carga.open = True
    page.update()


def dialog_close(page):
    dialog_carga.open = False
    page.update()

async def registrar_salida(page):
    
    if validar_campos_sal(page):
        # Mostrar el ProgressRing
        dialog_open(page)

        # Obtener el ID del registro a eliminar
        id_registro = page.client_storage.get("id_registro_a_eliminar")
        print(f"ID del registro a eliminar: {id_registro}")  # Imprimir el ID

        # Enviar la solicitud DELETE al backend
        FLASK_URL_ELIMINAR_ENTRADA = f"https://nicolasdominguez.pythonanywhere.com/eliminar_entrada/{id_registro}"
        print(f"URL de eliminación: {FLASK_URL_ELIMINAR_ENTRADA}")  # Imprimir la URL

        try:
            response = requests.delete(FLASK_URL_ELIMINAR_ENTRADA)
            response.raise_for_status()
            print("Salida registrada y entrada eliminada con éxito")
            print(f"Respuesta del backend: {response.text}")

            # Generar el registro
            await generar_registro(page)

            #limpia los registros globales
            limpiar_registro()
            # Llamar a la siguiente pantalla después de completar la operación
            dialog_close(page)
            await mainPernoteFinal.mainPernote_Final_Inicio(page)
            
            
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error al eliminar la entrada: {e}")

            # Cerrar el ProgressRing (remover el AlertDialog)
            dialog_close(page)
            return False
        
    else:
        return False


#Función para generar y guardar el registro en el backend
async def generar_registro(page):
    username = page.client_storage.get("username")
    registro = {
        "username": page.client_storage.get("username"),
        "nombre": page.client_storage.get("user_info")["nombre"],
        "legajo": page.client_storage.get("user_info")["legajo"],
        "lugar_pernocte": globals.selected_option_pernocte,
        "fecha_entrada": globals.selected_date_ent,
        "hora_entrada": globals.selected_time_ent,
        "tren_remis_entrada": globals.writed_train_ent,
        "observaciones_entrada": globals.writed_obs_ent,
        "fecha_salida": globals.selected_date_sal,
        "hora_salida": globals.selected_time_sal,
        "tren_remis_salida": globals.writed_train_sal,
        "observaciones_salida": globals.writed_obs_sal,
    }
    
    #GUARDAR REGISTRO EN HISTORIAL INDIVIDUAL
    FLASK_URL = f"https://nicolasdominguez.pythonanywhere.com/guardar_registro/{username}"  # URL del backend
    try:
        response = requests.post(FLASK_URL,json=registro)
        response.raise_for_status() # Lanza una excepción para códigos de error HTTP
        print("Registro generado con éxito")
    except requests.exceptions.RequestException as e:
        print(f"Error al generar el registro: {e}")

    #GUARDAR REGISTRO EN HISTORIAL GENERAL
    FLASK_URL_GENERAL = "https://nicolasdominguez.pythonanywhere.com/guardar_registro_general"  # URL para el historial general
    try:
        response = requests.post(FLASK_URL_GENERAL, json=registro)
        response.raise_for_status()
        print("Registro general generado con éxito.")
    except requests.exceptions.RequestException as e:
        print(f"Error al generar el registro general: {e}")

ARCHIVO_DATOS_ENTRADA = "datos_entrada.json"

def limpiar_registro():
    #limpiar las variables globales
    print("registros pernocte limpiados con exito")
    globals.writed_name = ""
    globals.writed_legajo = ""
    globals.selected_option_pernocte= "Sin seleccionar"
    globals.selected_date_ent= "Sin seleccionar"
    globals.selected_time_ent= "Sin seleccionar"
    globals.writed_train_ent= ""
    globals.writed_obs_ent= ""
    globals.selected_date_sal= "Sin seleccionar"
    globals.selected_time_sal= "Sin seleccionar"
    globals.writed_train_sal= ""
    globals.writed_obs_sal= ""

    if os.path.exists(ARCHIVO_DATOS_ENTRADA):
        os.remove(ARCHIVO_DATOS_ENTRADA)


#####################################################################################################
#PAGE1

def mainPernote_SalForm(page: ft.Page):
    page.clean()
    page.title= "Salida Form"

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
    titulo= ft.Text("Registrar Salida", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))

    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        leading=ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,
                              icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click=lambda e: mainPernoteSal.mainPernote_Sal(page))
    )

    page.add(app_bar)

    #Textfields de formulario
           # PERNOCTE TOMADO DE ENTRADA

    pernocte_title=ft.Text("Pernocte",color= ft.Colors.WHITE, style=ft.TextStyle(size=10))
    pernocte_value= globals.selected_option_pernocte
    pernocte= ft.Text(pernocte_value, color= ft.Colors.CYAN_ACCENT, style=ft.TextStyle(size=18))
    pernocte_columna= ft.Column([pernocte_title,pernocte],
                                spacing=3,horizontal_alignment=ft.CrossAxisAlignment.CENTER)


            # NOMBRE Y APELLIDO TOMADO DE ENTRADA
    
    nombreyapellido_title= ft.Text("Nombre y Legajo",color= ft.Colors.WHITE, style=ft.TextStyle(size=10))
    nombreyapellido=ft.Text(f"{globals.writed_name} - {globals.writed_legajo}", color= ft.Colors.CYAN_ACCENT, style=ft.TextStyle(size=15))
    nombreyapellido_columna= ft.Column([nombreyapellido_title,nombreyapellido],
                                      spacing=3,horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def actualizar_nombre_salida():
        nombreyapellido.value =globals.writed_name
        page.update()

        page.add(nombreyapellido)
        page.add(ft.ElevatedButton("Actualizar Nombre", on_click=actualizar_nombre_salida))
        
    
            # SE FUE EN TREN O REMIS

    tren_remis_salida=ft.Text("Tren/Remis", color= ft.Colors.WHITE, style=ft.TextStyle(size=10))

    def actualizar_tren(e):
        globals.writed_train_sal = tf_tren_remis_salida.value
        page.update()

    tf_tren_remis_salida=ft.TextField(value=globals.writed_train_sal,
                bgcolor=ft.Colors.WHITE, color= ft.Colors.BLACK,
                border_radius=ft.border_radius.only(top_left=0,top_right=15,bottom_left=15,bottom_right=15),
                border_color=ft.Colors.CYAN_ACCENT, on_change= actualizar_tren
                )
    
    columna_tren= ft.Column([tren_remis_salida,tf_tren_remis_salida], expand= True,spacing=5)

            # OBSERVACIONES AL IRSE

    observaciones_salida=ft.Text("Observaciones al retirarse", color= ft.Colors.WHITE, style=ft.TextStyle(size=10))

    def actualizar_obs(e):
        globals.writed_obs_sal = tf_observaciones_salida.value
        page.update()

    tf_observaciones_salida=ft.TextField( value=globals.writed_obs_sal,
                bgcolor=ft.Colors.WHITE, text_size=14, color=ft.Colors.BLACK,
                border_radius=ft.border_radius.only(top_left=0,top_right=15,bottom_left=15,bottom_right=15),
                border_color=ft.Colors.CYAN_ACCENT, multiline=True, max_length=70, on_change=actualizar_obs
                )
    
    observaciones_columna= ft.Column([observaciones_salida,tf_observaciones_salida], expand= True,spacing=5)

            # FECHA DE SALIDA

    selected_date_text_value = globals.selected_date_sal if globals.selected_date_sal != "Sin seleccionar" else "Sin seleecionar"
    selected_date_text=ft.Text(selected_date_text_value,color= ft.Colors.WHITE, style=ft.TextStyle(size=14,weight=ft.FontWeight.BOLD))

    def handle_change(e):
        # Actualizar el texto con la nueva fecha seleccionada
        date_selected = e.control.value.strftime('%d %B %Y')  # Formato "13 de febrero de 2025"
        selected_date_text.value = f"{date_selected}"  # Actualizar el texto
        globals.selected_date_sal = date_selected
        page.update()  # Actualizar la interfaz para reflejar el cambio

    def handle_dismissal(e):
        selected_date_text.value = "Sin seleccionar"
        page.update()  # Actualizar la interfaz para reflejar el cambio

    RowFechaEnt= ft.Row([
        ft.ElevatedButton(
                    "Fecha",color=ft.Colors.BLUE_900,
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

            # HORA SALIDA

    # Crear un texto para mostrar la hora seleccionada
    selected_time_text_value = globals.selected_time_sal if globals.selected_time_sal != "Sin seleccionar" else "Sin seleecionar"
    time_text = ft.Text(selected_time_text_value,color= ft.Colors.WHITE, style=ft.TextStyle(size=14,weight=ft.FontWeight.BOLD))

    def handle_change1(e):
        # Actualiza el texto con la hora seleccionada
        selected_time = e.control.value.strftime('%H:%M')
        time_text.value = f"{selected_time}"
        globals.selected_time_sal = selected_time
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
                    "Hora",color=ft.Colors.BLUE_900,
                    bgcolor=ft.Colors.WHITE,
                    icon=ft.Icons.TIME_TO_LEAVE, icon_color=ft.Colors.BLUE_900,
                    on_click=lambda _: page.open(time_picker),
                ), time_text
        ], alignment=ft.MainAxisAlignment.CENTER)


    #Distribucion de la informacion


    async def async_cambiar_pagina_final(e):
        mainPernote_Final(page)
            


    container= ft.Container(
        bgcolor=ft.Colors.BLUE_700,
        alignment=ft.alignment.center,
        border_radius= ft.border_radius.only(top_left=20, top_right=20,bottom_left=0, bottom_right=0),
        expand= True,
        height=600,
        padding=ft.padding.only(left=20,top=10,right=20,bottom=10),
        content= ft.Column(
            [
            ft.Row([nombreyapellido_columna],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([pernocte_columna], alignment=ft.MainAxisAlignment.CENTER),
            RowFechaEnt,RowhoraEnt, ft.Row([columna_tren]),
            ft.Column([observaciones_columna]),           
            ft.Row([ft.ElevatedButton(text="Ver Resumen",
                                      style= ft.ButtonStyle(
                                          text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD),color=ft.Colors.WHITE),
                                     expand=True,height=50,bgcolor=ft.Colors.BLUE_900, color= ft.Colors.WHITE,
                                     on_click=lambda e: asyncio.run(async_cambiar_pagina_final(e)) if validar_campos_sal(page) else None)
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


#####################################################################################################
#PAGE2

def mainPernote_Final(page: ft.Page):
    page.clean()
    page.title= "Tu entrada y salida"

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

    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        leading=ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,
                              icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click=lambda e: mainPernote_SalForm(page))
    )

    page.add(app_bar)


    logo = ft.Image(src= 'logoFrateAlianza1.png',width=70,)
    titulo= ft.Text("Pernoctes", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))

       #Textfields de formulario
           # PERNOCTE TOMADO DE ENTRADA

    pernocte_title=ft.Text("Pernocte",color= ft.Colors.WHITE, style=ft.TextStyle(size=10))
    pernocte_value= globals.selected_option_pernocte
    pernocte= ft.Text(pernocte_value, color= ft.Colors.CYAN_ACCENT, style=ft.TextStyle(size=18))
    pernocte_columna= ft.Column([pernocte_title,pernocte],
                                spacing=3,horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            # NOMBRE Y APELLIDO TOMADO DE ENTRADA
    
    nombreyapellido_title= ft.Text("Nombre y Apellido",color= ft.Colors.WHITE, style=ft.TextStyle(size=10))
    nombreyapellido=ft.Text(globals.writed_name, color= ft.Colors.CYAN_ACCENT, style=ft.TextStyle(size=18))
    nombreyapellido_columna= ft.Column([nombreyapellido_title,nombreyapellido],
                                      spacing=3,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
            # TEXTO ENTRADA SALIDA

    registro_entrada_salida= ft.Text("Tu entrada y salida",
                                      color= ft.Colors.CYAN_ACCENT, style=ft.TextStyle(size=24,weight=ft.FontWeight.W_300),
                                      expand=True, text_align=ft.TextAlign.CENTER,)
    row_registro_entr_sal= ft.Row([registro_entrada_salida])

            # CONTEINER DEL REGISTRO
    
    conteiner_reg= ft.Container(
        bgcolor=ft.Colors.BLUE_700,
        alignment=ft.alignment.center,
        border_radius= ft.border_radius.only(top_left=20, top_right=20,bottom_left=20, bottom_right=20),
        expand= True,
        height=300,
        padding=ft.padding.only(left=10,top=10,right=10,bottom=10),
        content=(ft.Column([
            ft.Row([pernocte_columna], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([nombreyapellido_columna],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text("ENTRADA",text_align=ft.TextAlign.CENTER,
                            color= ft.Colors.WHITE, style=ft.TextStyle(size=18,weight=ft.FontWeight.BOLD)),
                    ft.Text("________",color=ft.Colors.TRANSPARENT),
                    ft.Text("SALIDA",text_align=ft.TextAlign.CENTER,
                            color= ft.Colors.WHITE, style=ft.TextStyle(size=18,weight=ft.FontWeight.BOLD))],
                   alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text(globals.selected_date_ent,
                            text_align=ft.TextAlign.CENTER,color= ft.Colors.CYAN_ACCENT),
                    ft.Text("FECHA",text_align=ft.TextAlign.CENTER,
                            color= ft.Colors.WHITE, style=ft.TextStyle(size=10,weight=ft.FontWeight.BOLD)),
                    ft.Text(globals.selected_date_sal,text_align=ft.TextAlign.CENTER,color= ft.Colors.CYAN_ACCENT)],
                    alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text(globals.selected_time_ent,
                            text_align=ft.TextAlign.CENTER,color= ft.Colors.CYAN_ACCENT),
                    ft.Text("HORA",text_align=ft.TextAlign.CENTER,
                            color= ft.Colors.WHITE, style=ft.TextStyle(size=10,weight=ft.FontWeight.BOLD)),
                    ft.Text(globals.selected_time_sal,
                            text_align=ft.TextAlign.CENTER,color= ft.Colors.CYAN_ACCENT)],
                   alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text(globals.writed_train_ent, color= ft.Colors.CYAN_ACCENT),
                    ft.Text("TREN",text_align=ft.TextAlign.CENTER,
                            color= ft.Colors.WHITE, style=ft.TextStyle(size=10,weight=ft.FontWeight.BOLD)),
                    ft.Text(globals.writed_train_sal, color= ft.Colors.CYAN_ACCENT)],
                   alignment=ft.MainAxisAlignment.CENTER),
            ft.Column([ ft.Text("OBSERVACIONES",color= ft.Colors.WHITE,
                                 style=ft.TextStyle(size=8,weight=ft.FontWeight.BOLD)),
                    ft.Text(globals.writed_obs_ent,color= ft.Colors.CYAN_ACCENT),
                    ft.Text(globals.writed_obs_sal, color= ft.Colors.CYAN_ACCENT)],
                   alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=5),
        ], spacing=5,expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER))
    )

    async def async_registrar_salida_y_cambiar_f1(e, page):
        if await registrar_salida(page):
            accionBotonPern.cambiar_a_f1(page)

    row11= ft.Row(
        [
            ft.ElevatedButton(
            text="Registrar e Ir al inicio",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD),color=ft.Colors.WHITE),
            expand=True,height=60, bgcolor=ft.Colors.GREEN_ACCENT_400,
            on_click=lambda e: asyncio.run(async_registrar_salida_y_cambiar_f1(e, page)) if validar_campos_sal(page) else None)
        ]
    )

    columna1= ft.Column(
        controls=[logo,titulo,row_registro_entr_sal],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=7    
    )

    columna2= ft.Column(
        controls=[conteiner_reg,row11],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    columna3= ft.Column(
        controls=[columna1,columna2],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )
   
    page.add(columna3)

#ft.app(target=mainPernote_SalForm)
