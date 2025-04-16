import flet as ft
import datetime
import locale
import mainNovedad
import mainNovedadFinal
import requests
import asyncio



try:
    locale.setlocale(locale.LC_TIME, 'es_ES')
except locale.Error:
    print("La localidad 'es_ES' no está soportada, usando la predeterminada.")
    locale.setlocale(locale.LC_TIME, 'C')

# Referencias a los controles que vamos a validar
ref_popupMenu = ft.Ref[ft.PopupMenuButton]()
ref_selected_option = ft.Ref[ft.Text]()
ref_date_picker_button = ft.Ref[ft.ElevatedButton]() # Referencia al botón de fecha
ref_selected_date = ft.Ref[ft.Text]()
ref_novedad_text = ft.Ref[ft.TextField]() 

def validar_campos_nov(page):
    valido= True

    lugar_pernote_novedad= page.client_storage.get("lugar_pernocte_novedad")
    novedad_escrita= page.client_storage.get("novedad_escrita")
    fecha_novedad= page.client_storage.get("fecha_novedad")
        
    # Validación para pernocte para novedad (PopupMenu)
    if not lugar_pernote_novedad or lugar_pernote_novedad == "Sin seleccionar":
        ref_popupMenu.current.icon_color = ft.Colors.RED
        ref_selected_option.current.color = ft.Colors.RED
        valido = False
    else:
        ref_popupMenu.current.icon_color = ft.Colors.BLUE_GREY_900
        ref_selected_option.current.color = ft.Colors.BLUE_900

    # Validación para la novedad
    if not novedad_escrita or novedad_escrita == "":
        ref_novedad_text.current.border_color = ft.Colors.RED
        ref_novedad_text.current.error_text = "Campo obligatorio"
        valido = False
    else:
        ref_novedad_text.current.border_color = ft.Colors.CYAN_ACCENT
        ref_novedad_text.current.error_text = None

    
    
    # Validacion para fecha novedad
    if not fecha_novedad or fecha_novedad == "Sin seleccionar":
        ref_selected_date.current.color = ft.Colors.RED
        ref_date_picker_button.current.bgcolor = ft.Colors.RED
        ref_date_picker_button.current.color = ft.Colors.WHITE
        valido = False
    else:
        ref_selected_date.current.color = ft.Colors.WHITE
        ref_date_picker_button.current.bgcolor = ft.Colors.WHITE
        ref_date_picker_button.current.color = ft.Colors.BLUE_900
    
    page.update()
    return valido

def ver_resumen_novedad(page):
    if validar_campos_nov(page):  
        mainNovedad_Final(page)

######################################################
#Page1

def mainNovedad_Form(page: ft.Page):
    page.clean()
    page.title= "Novedades Form"

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
    titulo= ft.Text("Registrar Novedad", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))

    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        leading=ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,
                              icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click=lambda e: mainNovedad.main_Novedad(page))
    )

    page.add(app_bar)

    # FORMULARIO
    # SELECCION DE PERNOCTE
    selected_option_text= page.client_storage.get("lugar_pernocte_novedad") or "seleccionar pernocte"
    selected_option= ft.Text(selected_option_text, ref=ref_selected_option, color= ft.Colors.BLUE_900, style=ft.TextStyle(size=18))

    def update_selected_pernocte(option):
        page.client_storage.set("lugar_pernocte_novedad", option)  
        selected_option.value = option  
        page.update()

    popupMenu= ft.PopupMenuButton(
                ref=ref_popupMenu,
                icon_color= ft.Colors.BLUE_900,
                bgcolor= ft.Colors.BLACK87,
                icon= ft.Icons.ARROW_DROP_DOWN_CIRCLE, icon_size=35,
                
                items=[
                    ft.PopupMenuItem(text="Dock Central",on_click=lambda e: update_selected_pernocte("Dock Central")),
                    ft.PopupMenuItem(text="Mercedes BAP", on_click=lambda e: update_selected_pernocte("Mercedes BAP")),
                    ft.PopupMenuItem(text="Campana",on_click=lambda e: update_selected_pernocte("Campana")),
                    ft.PopupMenuItem(text="Junin",on_click=lambda e: update_selected_pernocte("Junin"))
                    ])

    # NOVEDAD
    novedad=ft.Text("NOVEDAD", color= ft.Colors.WHITE, style=ft.TextStyle(size=10))

    def actualizar_nov(e):
        page.client_storage.set("novedad_escrita", e.control.value)
        page.update()

    novedad_guardada = page.client_storage.get("novedad_escrita") or ""
    tf_novedad=ft.TextField(ref=ref_novedad_text,value=novedad_guardada,
                bgcolor=ft.Colors.WHITE, text_size=14,color=ft.Colors.BLACK, autofocus=True,
                border_radius=ft.border_radius.only(top_left=0,top_right=15,bottom_left=15,bottom_right=15),
                border_color=ft.Colors.CYAN_ACCENT, multiline=True, max_length=500, 
                on_change= actualizar_nov,expand=True)
    novedad_columna= ft.Column([novedad,tf_novedad], expand= True,spacing=5)

    # FECHA DE LA NOVEDAD
    selected_date_text_value = page.client_storage.get("fecha_novedad") or "Sin seleccionar"
    selected_date_text=ft.Text(selected_date_text_value,ref=ref_selected_date,
                               color= ft.Colors.WHITE,style=ft.TextStyle(size=14,weight=ft.FontWeight.BOLD))

    def handle_change(e):
        date_selected = e.control.value.strftime('%d %B %Y')  
        selected_date_text.value = f"{date_selected}"  
        page.client_storage.set("fecha_novedad", date_selected)
        ref_date_picker_button.current.bgcolor = ft.Colors.WHITE
        ref_date_picker_button.current.color = ft.Colors.BLUE_900
        page.update()  

    def handle_dismissal(e):
        selected_date_text.value = "Sin seleccionar"
        page.client_storage.set("fecha_novedad", "Sin seleccionar")
        page.update() 

    RowFechaNov= ft.Row([
        ft.ElevatedButton(
                    "Fecha", ref= ref_date_picker_button,
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


    # DISTRIBUCION DE LA INFORMACION
    container= ft.Container(
        bgcolor=ft.Colors.BLUE_700,
        alignment=ft.alignment.center,
        border_radius= ft.border_radius.only(top_left=20, top_right=20,bottom_left=0, bottom_right=0),
        expand= True,
        height=600,
        padding=ft.padding.only(left=20,top=30,right=20,bottom=10),

        content= ft.Column(
            [
            ft.Container(bgcolor=ft.Colors.WHITE,
                         alignment=ft.alignment.center,
                         border_radius= ft.border_radius.only(top_left=20, top_right=20,bottom_left=20, bottom_right=20),
                         height=50,
                         content=ft.Row([popupMenu,selected_option],
                                alignment=ft.MainAxisAlignment.CENTER)
                        ),
            RowFechaNov,
            ft.Row([novedad_columna]),
            ft.Row([ft.ElevatedButton(text="Ver resumen",
                                      style= ft.ButtonStyle(
                                          text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD),color=ft.Colors.WHITE),
                                     expand=True,height=60,bgcolor=ft.Colors.BLUE_900,color=ft.Colors.WHITE,
                                     on_click=lambda e: ver_resumen_novedad(page) )
                    ]) 
            ], spacing=25
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
        controls=[columna1,ft.Container(padding=ft.padding.only(left=25,top=0,right=25,bottom=0),
                               expand=True,
                               content= columna2)],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll= ft.ScrollMode.AUTO, expand=True,
    )
    

    page.add(columna3)

######################################################
#Page2

# Función para enviar datos al backend
def send_data_to_backend(data, page):
    url = f"https://nicolasdominguez.pythonanywhere.com/guardar_novedad/{page.client_storage.get('username')}" 
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        print("Datos enviados al backend con éxito.")
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar datos al backend: {e}")
        page.update()

# Función para generar y guardar el registro en el backend
def generar_registro_nov(page: ft.Page): #añadimos page como parametro
    # Datos que quieres guardar en el registro
    registro = {
        "pernocte_novedad": page.client_storage.get("lugar_pernocte_novedad"),
        "fecha_novedad": page.client_storage.get("fecha_novedad"),
        "novedad": page.client_storage.get("novedad_escrita"),
    }

    # Enviar el registro al backend
    send_data_to_backend(registro, page)
    print("Registro novedad generado con éxito.")

    registro_general = {
        "username": page.client_storage.get("username"),
        "nombre": page.client_storage.get("user_info")["nombre"],
        "legajo": page.client_storage.get("user_info")["legajo"],
        "pernocte_novedad": page.client_storage.get("lugar_pernocte_novedad"),
        "fecha_novedad": page.client_storage.get("fecha_novedad"),
        "novedad": page.client_storage.get("novedad_escrita"),
    }
    url_general = "https://nicolasdominguez.pythonanywhere.com/guardar_novedad_general" # Reemplaza con la URL de tu backend
    try:
        response_general = requests.post(url_general, json=registro_general)
        response_general.raise_for_status()
        print("Registro de novedad general guardado con éxito.")
    except requests.exceptions.RequestException as e:
        print(f"Error al guardar el registro de novedad general: {e}")
        page.update()


def limpiar_novedad(page):
    page.client_storage.remove("lugar_pernocte_novedad")
    page.client_storage.remove("fecha_novedad")
    page.client_storage.remove("novedad_escrita")


# Crea el ProgressRing
progress_ring = ft.ProgressRing(color=ft.Colors.WHITE)

# Crea el AlertDialog con el ProgressRing
dialog_carga = ft.AlertDialog(
    title=ft.Text("Registrando...",text_align=ft.TextAlign.CENTER,color=ft.Colors.WHITE),
    content=ft.Column([progress_ring], horizontal_alignment=ft.CrossAxisAlignment.CENTER,alignment=ft.MainAxisAlignment.CENTER,height=100),
    modal=True,bgcolor=ft.Colors.BLACK45
)

async def generar_registro_novedad(page):
    if validar_campos_nov(page):
        page.add(dialog_carga)
        dialog_carga.open = True
        page.update()

        generar_registro_nov(page)
        limpiar_novedad(page)

        dialog_carga.open = False
        page.update()
        await mainNovedadFinal.main_Novedad_Final(page)
        page.update()
    else:
        dialog_carga.open = False
        page.update()
        return False



# Función principal de la página final
def mainNovedad_Final(page: ft.Page):
    page.clean()
    page.update()
    page.title= "Resumen tu novedad"

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
    page.padding= ft.padding.only(left=30, top=25, right=30, bottom=30)


    logo = ft.Image(src= 'logoFrateAlianza1.png',width=70,)
    titulo= ft.Text("Novedades", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))

    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        leading=ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,
                              icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click=lambda e: mainNovedad_Form(page))
    )

    page.add(app_bar)

    #Textfields de formulario
    # PERNOCTE TOMADO DE ENTRADA
    pernocte_title=ft.Text("Pernocte",color= ft.Colors.WHITE, style=ft.TextStyle(size=10))
    pernocte_value= page.client_storage.get("lugar_pernocte_novedad")
    pernocte= ft.Text(pernocte_value, color= ft.Colors.CYAN_ACCENT, style=ft.TextStyle(size=18))
    pernocte_columna= ft.Column([pernocte_title,pernocte],
                                spacing=3,horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    
    # TEXTO ENTRADA SALIDA
    registro_tu_novedad= ft.Text("Tu Novedad",
                                      color= ft.Colors.CYAN_ACCENT, style=ft.TextStyle(size=24,weight=ft.FontWeight.W_300),
                                      expand=True, text_align=ft.TextAlign.CENTER,)
    row_registro_tu_novedad= ft.Row([registro_tu_novedad])

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

            ft.Row([
                ft.Text("FECHA",text_align=ft.TextAlign.CENTER,
                            color= ft.Colors.WHITE, style=ft.TextStyle(size=10,weight=ft.FontWeight.BOLD)),
                ft.Text(page.client_storage.get("fecha_novedad"),
                            text_align=ft.TextAlign.CENTER,color= ft.Colors.CYAN_ACCENT)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Column([ ft.Text("NOVEDAD",color= ft.Colors.WHITE,
                                 style=ft.TextStyle(size=8,weight=ft.FontWeight.BOLD)),
                    ft.Text(page.client_storage.get("novedad_escrita"),color= ft.Colors.CYAN_ACCENT),],
                   alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=5),
        ], spacing=5,expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER))
    )



    row11= ft.Row(
        [
            ft.ElevatedButton(
            text="Registrar e ir al inicio",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD),color=ft.Colors.WHITE),
            expand=True,height=60, bgcolor=ft.Colors.GREEN_ACCENT_400,
            on_click=lambda e: asyncio.run(generar_registro_novedad(page)))
        ]
    )

    columna1= ft.Column(
        controls=[logo,titulo,row_registro_tu_novedad],
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

