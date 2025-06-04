import flet as ft
import datetime
import locale
import accionBotonPern
import mainPernoteSal
import mainPernoteEnt
import requests
import asyncio


#servicio de fecha y hora
try:
    locale.setlocale(locale.LC_TIME, 'es_ES')
except locale.Error:
    print("La localidad 'es_ES' no está soportada, usando la predeterminada.")
    locale.setlocale(locale.LC_TIME, 'C')

# Crea el ProgressRing
progress_ring = ft.ProgressRing(color=ft.Colors.WHITE)

# Crea el AlertDialog con el ProgressRing
dialog_carga = ft.AlertDialog(
    title=ft.Text("Registrando...",text_align=ft.TextAlign.CENTER,color=ft.Colors.WHITE),
    content=ft.Column([progress_ring], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                      alignment=ft.MainAxisAlignment.CENTER,height=100),
    modal=True,bgcolor=ft.Colors.BLACK45
)

# Referencias a los controles que vamos a validar
popupMenu_ref = ft.Ref[ft.PopupMenuButton]()
selected_option_ref = ft.Ref[ft.Text]()
date_picker_button_ref = ft.Ref[ft.ElevatedButton]() # Referencia al botón de fecha
selected_date_ref = ft.Ref[ft.Text]()
time_picker_button_ref = ft.Ref[ft.ElevatedButton]() # Referencia al botón de hora
selected_time_ref = ft.Ref[ft.Text]()
tf_tren_remis_ref = ft.Ref[ft.TextField]()
tf_observaciones_ref = ft.Ref[ft.TextField]()  
    
def validar_campos_ent(page):
    es_valido = True

    lugar_pernocte= page.client_storage.get("lugar_pernocte")
    fecha_entrada= page.client_storage.get("fecha_entrada")
    hora_entrada= page.client_storage.get("hora_entrada")
    tren_remis_entrada= page.client_storage.get("tren_remis_entrada")
    observaciones_entrada= page.client_storage.get("observaciones_entrada")

    #Validación para pernocte
    if not lugar_pernocte or lugar_pernocte== "Seleccionar pernocte":
        popupMenu_ref.current.icon_color = ft.Colors.RED
        selected_option_ref.current.color = ft.Colors.RED
        es_valido = False
    else:
        popupMenu_ref.current.icon_color = ft.Colors.BLUE_GREY_900
        selected_option_ref.current.color = ft.Colors.BLUE_900

    #Validacion para fecha de entrada
    if not fecha_entrada or fecha_entrada== "Sin seleccionar":
        date_picker_button_ref.current.bgcolor = ft.Colors.RED
        date_picker_button_ref.current.color = ft.Colors.WHITE
        selected_date_ref.current.color = ft.Colors.RED
        es_valido = False
    else:
        date_picker_button_ref.current.bgcolor = ft.Colors.WHITE
        date_picker_button_ref.current.color = ft.Colors.BLUE_900
        selected_date_ref.current.color = ft.Colors.WHITE

    #Validación para hora entrada
    if not hora_entrada or hora_entrada == "Sin seleccionar":
        time_picker_button_ref.current.bgcolor = ft.Colors.RED
        time_picker_button_ref.current.color = ft.Colors.WHITE
        selected_time_ref.current.color = ft.Colors.RED
        es_valido = False
    else:
        time_picker_button_ref.current.bgcolor = ft.Colors.WHITE
        time_picker_button_ref.current.color = ft.Colors.BLUE_900
        selected_time_ref.current.color = ft.Colors.WHITE

    #Validacion para Tren Entrada   
    if not tren_remis_entrada or tren_remis_entrada== "":
        tf_tren_remis_ref.current.border_color = ft.Colors.RED
        tf_tren_remis_ref.current.error_text = "Campo obligatorio"
        es_valido = False
    else:
        tf_tren_remis_ref.current.border_color = ft.Colors.CYAN_ACCENT
        tf_tren_remis_ref.current.error_text = None

    #Validacion para observaciones de entrada
    if not observaciones_entrada or observaciones_entrada== "":
        tf_observaciones_ref.current.border_color = ft.Colors.RED
        tf_observaciones_ref.current.error_text = "Campo obligatorio"
        es_valido = False
    else:
        tf_observaciones_ref.current.border_color = ft.Colors.CYAN_ACCENT
        tf_observaciones_ref.current.error_text = None
    
    page.update()
    return es_valido

def dialog_open(page):
    page.add(dialog_carga)
    dialog_carga.open = True
    page.update()

def dialog_close(page):
    dialog_carga.open = False
    page.update()
    
async def registrar_entrada(page):
    if validar_campos_ent(page):
        dialog_open(page)

        # Crear el diccionario con los datos
        datos_entrada = {
            "username": page.client_storage.get("username"),
            "nombre": page.client_storage.get("user_info")["nombre"],
            "legajo": page.client_storage.get("user_info")["legajo"],
            "lugar_pernocte": page.client_storage.get("lugar_pernocte"),
            "fecha_entrada": page.client_storage.get("fecha_entrada"),
            "hora_entrada": page.client_storage.get("hora_entrada"),
            "tren_remis_entrada": page.client_storage.get("tren_remis_entrada"),
            "observaciones_entrada": page.client_storage.get("observaciones_entrada"),
        }

        # Enviar la solicitud POST al backend
        FLASK_URL_REGISTRAR_ENTRADA = "https://nicolasdominguez.pythonanywhere.com/registrar_entrada"
        try:
            response = requests.post(FLASK_URL_REGISTRAR_ENTRADA, json=datos_entrada)
            response.raise_for_status()
            print("Entrada registrada con éxito")
            
            result = response.json() # Parsear la respuesta JSON del backend
            registro_entrada_id = result.get('id') # Obtener el valor de la clave 'id'

            if registro_entrada_id is not None:
                print(f"Entrada registrada con éxito. ID del registro: {registro_entrada_id}")

                # **AQUÍ ES DONDE GUARDAMOS EL ID EN page.client_storage**
                page.client_storage.set("registro_entrada_id", str(registro_entrada_id))
                page.update() # Guardar los datos de forma asíncrona
                dialog_close(page)
                mainPernoteSal.mainPernote_Sal(page) # Pasar el ID
                page.update()
                
                return True
            else:
                print("Error: El backend no devolvió el ID del registro.")
                dialog_close(page)
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error al registrar la entrada: {e}")
            dialog_carga.open = False
            page.update()
            return False

    else:
        return False


##################################################################################################
#PAGE1

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

    #CAMPOS de formulario entrada

    # SELECCION DE PERNOCTE
    selected_pernocte_value= page.client_storage.get("lugar_pernocte") or "Seleccionar pernocte"
    selected_option= ft.Text(selected_pernocte_value, ref=selected_option_ref, color= ft.Colors.BLUE_900, style=ft.TextStyle(size=18))

    def update_selected_pernocte(option):
        page.client_storage.set("lugar_pernocte", option)
        selected_option.value = option
        page.update()

    popupMenu= ft.PopupMenuButton(
            ref=popupMenu_ref,
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
        nombre_usuario_local = datos_usuario['nombre']
        legajo_usuario_local = datos_usuario['legajo']
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos del usuario: {e}")
        nombre_usuario_local = "Error al cargar"
        legajo_usuario_local = "Error al cargar"

    # Mostrar los datos del usuario en la interfaz
    nombre_legajo = ft.Text(f"{nombre_usuario_local} - {legajo_usuario_local}", color=ft.colors.CYAN_ACCENT, style=ft.TextStyle(size=15), text_align=ft.TextAlign.CENTER)
    nombreylegajo_title = ft.Text("Nombre y Legajo", color=ft.Colors.WHITE, style=ft.TextStyle(size=10), text_align=ft.TextAlign.CENTER)
    nombre_columna = ft.Column([nombreylegajo_title, nombre_legajo], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    # LLEGÓ EN TREN O REMIS
    tren_remis=ft.Text("Tren/Remis", color= ft.Colors.WHITE, style=ft.TextStyle(size=10))

    def actualizar_tren(e):
        page.client_storage.set("tren_remis_entrada", e.control.value)
        page.update()

    tren_remis_entrada_value= page.client_storage.get("tren_remis_entrada") or ""
    tf_tren_remis=ft.TextField(ref=tf_tren_remis_ref, value=tren_remis_entrada_value,
                bgcolor=ft.Colors.WHITE, text_size=14,color=ft.Colors.BLACK, autofocus=False,
                border_radius=ft.border_radius.only(top_left=0,top_right=15,bottom_left=15,bottom_right=15),
                border_color=ft.Colors.CYAN_ACCENT, on_change= actualizar_tren
                )
    
    tren_columna= ft.Column([tren_remis,tf_tren_remis], expand= True,spacing=5)

    # OBSERVACIONES AL ENTRAR
    observaciones=ft.Text("Observaciones al llegar al pernocte", color= ft.Colors.WHITE, style=ft.TextStyle(size=10))

    def actualizar_obs(e):
        page.client_storage.set("observaciones_entrada", e.control.value)
        page.update()

    observaciones_entrada_value= page.client_storage.get("observaciones_entrada") or ""
    tf_observaciones=ft.TextField(ref=tf_observaciones_ref,value= observaciones_entrada_value,
                bgcolor=ft.Colors.WHITE, text_size=14,color=ft.Colors.BLACK, autofocus=False,
                border_radius=ft.border_radius.only(top_left=0,top_right=15,bottom_left=15,bottom_right=15),
                border_color=ft.Colors.CYAN_ACCENT, multiline=True, max_length=70, on_change= actualizar_obs
                )
    
    observaciones_columna= ft.Column([observaciones,tf_observaciones], expand= True,spacing=5)

    # FECHA DE ENTRADA
    selected_date_ent_value= page.client_storage.get("fecha_entrada") or "Sin seleccionar"
    selected_date_text = ft.Text(selected_date_ent_value,ref=selected_date_ref,
                                 color=ft.Colors.WHITE, style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD))

    def handle_change(e):
        date_selected = e.control.value.strftime('%d %B %Y')
        selected_date_text.value = f"{date_selected}"
        page.client_storage.set("fecha_entrada", date_selected)
        # Restablecer el color del botón de fecha al seleccionar una fecha válida
        date_picker_button_ref.current.bgcolor = ft.Colors.WHITE
        date_picker_button_ref.current.color = ft.Colors.BLUE_900
        selected_date_text.color = ft.Colors.WHITE
        page.update()

    def handle_dismissal(e):
        selected_date_text.value = "Sin seleccionar"
        page.client_storage.set("fecha_entrada", "Sin seleccionar")
        page.update()

    RowFechaEnt= ft.Row([
        ft.ElevatedButton("Fecha",
                    ref=date_picker_button_ref,
                    color=ft.Colors.BLUE_900,
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
                selected_date_text
        ], alignment=ft.MainAxisAlignment.CENTER)


    # HORA ENTRADA
    selected_time_ent_value= page.client_storage.get("hora_entrada") or "Sin seleccionar"
    time_text = ft.Text(selected_time_ent_value, ref=selected_time_ref,
                         color=ft.Colors.WHITE, style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD))

    def handle_change1(e):
        selected_time = e.control.value.strftime('%H:%M')
        time_text.value = f"{selected_time}"
        page.client_storage.set("hora_entrada", selected_time)
        # Restablecer el color del botón de hora al seleccionar una hora válida
        time_picker_button_ref.current.bgcolor = ft.Colors.WHITE
        time_picker_button_ref.current.color = ft.Colors.BLUE_900
        time_text.color = ft.Colors.WHITE
        page.update()

    def handle_dismissal1(e):
        time_text.value = "Sin seleccionar"
        page.client_storage.set("hora_entrada", "Sin seleccionar")
        page.update()

    def handle_entry_mode_change(e):
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
        ft.ElevatedButton("Hora",
                    ref=time_picker_button_ref,
                    color=ft.Colors.BLUE_900,
                    bgcolor=ft.Colors.WHITE,
                    icon=ft.Icons.TIME_TO_LEAVE,icon_color=ft.Colors.BLUE_900,
                    on_click=lambda _: page.open(time_picker),
                ), time_text
        ], alignment=ft.MainAxisAlignment.CENTER)

            # DISTRIBUCION DE LA INFORMACION

    #funcion para cambiar a la Page2
    async def async_cambiar_pagina_entfinal(e):
        mainPernote_EntFinal(page)
        

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
            ft.Row([ft.ElevatedButton(text="Ver Resumen",
                                      style= ft.ButtonStyle(
                                          text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE)),
                                     expand=True,height=50,bgcolor=ft.Colors.BLUE_900, color=ft.Colors.WHITE,
                                     on_click=lambda e:asyncio.run(async_cambiar_pagina_entfinal(e)) if validar_campos_ent(page) else None)
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


##################################################################################################
#PAGE2

def mainPernote_EntFinal(page: ft.Page):
    page.clean()
    page.update()
    page.title= "Tu entrada resumen"

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
    page.padding= ft.padding.only(left=30, top=10, right=30, bottom=0)



    logo= ft.Image(src= 'logoFrateAlianza1.png',width=70,)
    titulo= ft.Text("Registrar Entrada", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))


    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        toolbar_height=60,
        leading= ft.Column([ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,
                              icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click= lambda e: mainPernote_EntForm(page)),
                            ft.Text("editar",color= ft.Colors.WHITE, style=ft.TextStyle(size=10))],
                            spacing=-10, horizontal_alignment=ft.CrossAxisAlignment.CENTER,alignment=ft.MainAxisAlignment.CENTER
        )
    )

    page.add(app_bar)

    # Obtener datos desde client_storage
    pernocte_value = page.client_storage.get("lugar_pernocte") or "Seleccionar pernocte"
    fecha_ent_value = page.client_storage.get("fecha_entrada") or "Sin seleccionar"
    hora_ent_value = page.client_storage.get("hora_entrada") or "Sin seleccionar"
    tren_ent_value = page.client_storage.get("tren_remis_entrada") or ""
    obs_ent_value = page.client_storage.get("observaciones_entrada") or ""
    nombre_usuario = page.client_storage.get("user_info")["nombre"]
    legajo_usuario = page.client_storage.get("user_info")["legajo"]

    # PERNOCTE TOMADO DE ENTRADA

    pernocte_title=ft.Text("Pernocte",color= ft.Colors.WHITE, style=ft.TextStyle(size=10))
    pernocte= ft.Text(pernocte_value, color= ft.Colors.CYAN_ACCENT, style=ft.TextStyle(size=18))
    pernocte_columna= ft.Column([pernocte_title,pernocte],
                                spacing=3,horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            # NOMBRE Y APELLIDO TOMADO DE ENTRADA
    
    nombreyapellido_title= ft.Text("Nombre y Legajo",color= ft.Colors.WHITE, style=ft.TextStyle(size=10))
    nombreyapellido=ft.Text(f"{nombre_usuario} - {legajo_usuario}", color= ft.Colors.CYAN_ACCENT, style=ft.TextStyle(size=15))
    nombreyapellido_columna= ft.Column([nombreyapellido_title,nombreyapellido],
                                      spacing=3,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    registro_entrada= ft.Text("Tu registro de entrada", color= ft.Colors.CYAN_ACCENT, 
                             style=ft.TextStyle(size=24,weight=ft.FontWeight.W_300))
    
    # CONTAINER REGISTRO 1
    conteiner_reg1= ft.Container(
        bgcolor=ft.Colors.BLUE_700,
        alignment=ft.alignment.center,
        border_radius= ft.border_radius.only(top_left=20, top_right=20,bottom_left=20, bottom_right=20),
        expand= True,
        height=250,
        padding=ft.padding.only(left=20,top=10,right=20,bottom=10),
        content=(ft.Column([
            ft.Row([nombreyapellido_columna],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([pernocte_columna], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                    ft.Text("FECHA",text_align=ft.TextAlign.CENTER,
                            color= ft.Colors.WHITE, style=ft.TextStyle(size=10,weight=ft.FontWeight.BOLD)),
                    ft.Text(fecha_ent_value,
                            text_align=ft.TextAlign.CENTER,color= ft.Colors.CYAN_ACCENT)],
                    alignment=ft.MainAxisAlignment.START),

            ft.Row([
                    ft.Text("HORA",text_align=ft.TextAlign.CENTER,
                            color= ft.Colors.WHITE, style=ft.TextStyle(size=10,weight=ft.FontWeight.BOLD)),
                    ft.Text(hora_ent_value,
                            text_align=ft.TextAlign.CENTER,color= ft.Colors.CYAN_ACCENT)],
                   alignment=ft.MainAxisAlignment.START),

            ft.Row([
                    ft.Text("TREN",text_align=ft.TextAlign.CENTER,
                            color= ft.Colors.WHITE, style=ft.TextStyle(size=10,weight=ft.FontWeight.BOLD)),
                    ft.Text(tren_ent_value, color= ft.Colors.CYAN_ACCENT)],
                   alignment=ft.MainAxisAlignment.START),
            ft.Row([
                    ft.Text("OBSERVACIONES",color= ft.Colors.WHITE, style=ft.TextStyle(size=8,weight=ft.FontWeight.BOLD)),
                    ft.Text(obs_ent_value, color= ft.Colors.CYAN_ACCENT)],
                   alignment=ft.MainAxisAlignment.START),
        ],))
    )

    async def async_registrar_entrada_cambiar_f2(e, page):
        if await registrar_entrada(page):
            accionBotonPern.cambiar_a_f2(page)

    row7= ft.Row(
        [
            ft.ElevatedButton(
            text="Registrar Entrada",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD)),
            expand=True,height=60,bgcolor=ft.Colors.GREEN_ACCENT_400, color=ft.Colors.WHITE,
            on_click=lambda e: asyncio.run(async_registrar_entrada_cambiar_f2(e, page))if validar_campos_ent(page) else None)
        ]
    )

    columna1= ft.Column(
        controls=[logo,titulo,registro_entrada],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    columna2= ft.Column(
        controls=[conteiner_reg1,row7],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )

    columna3= ft.Column(
        controls=[columna1, columna2],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20    
    )
   
    page.add(columna3)
