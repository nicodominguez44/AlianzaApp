import flet as ft
import mainInicio
import globals
import mainNovedadForm
import requests


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
        "pernocte_novedad": globals.selected_option_pernocte_nov,
        "fecha_novedad": globals.selected_date_nov,
        "novedad": globals.writed_novedad,
    }

    # Enviar el registro al backend
    send_data_to_backend(registro, page)
    print("Registro novedad generado con éxito.")

    registro_general = {
        "username": page.client_storage.get("username"),
        "nombre": page.client_storage.get("user_info")["nombre"],
        "legajo": page.client_storage.get("user_info")["legajo"],
        "pernocte_novedad": globals.selected_option_pernocte_nov,
        "fecha_novedad": globals.selected_date_nov,
        "novedad": globals.writed_novedad,
    }
    url_general = "https://nicolasdominguez.pythonanywhere.com/guardar_novedad_general" # Reemplaza con la URL de tu backend
    try:
        response_general = requests.post(url_general, json=registro_general)
        response_general.raise_for_status()
        print("Registro de novedad general guardado con éxito.")
    except requests.exceptions.RequestException as e:
        print(f"Error al guardar el registro de novedad general: {e}")
        page.update()



def limpiar_novedad():
     # Limpiar las variables globales
    
    globals.selected_option_pernocte_nov = "Sin seleccionar" 
    globals.selected_date_nov = "Sin seleccionar"
    globals.writed_novedad = ""


# Función principal de la página final
def mainNovedad_Final(page: ft.Page):
    page.clean()
    page.title= "Tu Novedad"

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
                              on_click=lambda e: mainNovedadForm.mainNovedad_Form(page))
    )

    page.add(app_bar)

       #Textfields de formulario
           # PERNOCTE TOMADO DE ENTRADA

    pernocte_title=ft.Text("Pernocte",color= ft.Colors.WHITE, style=ft.TextStyle(size=10))
    pernocte_value= globals.selected_option_pernocte_nov
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
                ft.Text(globals.selected_date_nov,
                            text_align=ft.TextAlign.CENTER,color= ft.Colors.CYAN_ACCENT),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Column([ ft.Text("NOVEDAD",color= ft.Colors.WHITE,
                                 style=ft.TextStyle(size=8,weight=ft.FontWeight.BOLD)),
                    ft.Text(globals.writed_novedad,color= ft.Colors.CYAN_ACCENT),],
                   alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=5),
        ], spacing=5,expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER))
    )



    row11= ft.Row(
        [
            ft.ElevatedButton(
            text="Registrar e ir al inicio",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD),color=ft.Colors.WHITE),
            expand=True,height=50, bgcolor=ft.Colors.GREEN_ACCENT_400,
            on_click=lambda e: (generar_registro_nov(page),mainInicio.main_Inicio(page,page.client_storage.get("username"), page.client_storage.get("user_info")),limpiar_novedad()))
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
