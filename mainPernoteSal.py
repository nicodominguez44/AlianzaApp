import flet as ft
import mainInicio
import mainPernoteSalForm
import mainPernoteHistorial
import requests


# URL del backend
FLASK_URL_BASE = "https://nicolasdominguez.pythonanywhere.com"
FLASK_URL_OBTENER_ENTRADA = f"{FLASK_URL_BASE}/obtener_entrada/"


def mainPernote_Sal(page: ft.Page):
    page.clean()
    page.update()
    page.title= "Pernoctes Salida"

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
    page.padding= ft.padding.only(left=25, top=10, right=25, bottom=0)


    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        leading=ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,
                              icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click=lambda e: mainInicio.main_Inicio(page,page.client_storage.get("username"), page.client_storage.get("user_info")))
    )

    page.add(app_bar)


    logo = ft.Image(src= 'logoFrateAlianza1.png',width=70,)
    titulo= ft.Text("Pernoctes", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))


    registroentrada= ft.Row([ft.Text("Entrada Registrada", color= ft.Colors.GREEN_ACCENT_400,
                                style=ft.TextStyle(size=22,weight=ft.FontWeight.W_500)),
                             ft.Icon(name=ft.Icons.CHECK_CIRCLE_ROUNDED,color=ft.Colors.GREEN_ACCENT_400,size=27)
                             ],alignment=ft.MainAxisAlignment.CENTER)
    
    
    # Función para obtener los detalles de la entrada del backend
    def obtener_detalles_entrada(registro_id):
        url = f"{FLASK_URL_OBTENER_ENTRADA}{registro_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener detalles de la entrada: {e}")
            return None

     # **OBTENEMOS EL ID DESDE page.client_storage**
    registro_entrada_id_str = page.client_storage.get("registro_entrada_id")
    detalles_entrada = None

    if registro_entrada_id_str:
        try:
            registro_entrada_id = int(registro_entrada_id_str)
            detalles_entrada = obtener_detalles_entrada(registro_entrada_id)
        except ValueError:
            print("Error: El ID de entrada guardado no es un número válido.")
            detalles_entrada = ft.Text("Error: ID de entrada inválido.", color=ft.colors.RED_ACCENT_700)
        except Exception as e:
            print(f"Ocurrió un error al procesar el ID: {e}")
            detalles_entrada = ft.Text("Error al procesar el ID.", color=ft.colors.RED_ACCENT_700)
    else:
        detalles_entrada = ft.Text("No se encontró el ID de la entrada.", color=ft.colors.YELLOW_ACCENT_700)

    conteiner_reg1_content = None  # Inicializar la variable aquí

    if isinstance(detalles_entrada, dict): # Verificamos si obtuvimos un diccionario del backend
        pernocte_value = detalles_entrada.get('lugar_pernocte')
        fecha_ent_value = detalles_entrada.get('fecha_entrada')
        hora_ent_value = detalles_entrada.get('hora_entrada')
        tren_ent_value = detalles_entrada.get('tren_remis_entrada')
        obs_ent_value = detalles_entrada.get('observaciones_entrada')
        nombre_usuario = detalles_entrada.get('nombre')
        legajo_usuario = detalles_entrada.get('legajo')
        

        # PERNOCTE TOMADO DEL BACKEND
        pernocte_title=ft.Text("Pernocte",color= ft.Colors.WHITE, style=ft.TextStyle(size=10))
        pernocte= ft.Text(pernocte_value, color= ft.Colors.CYAN_ACCENT, style=ft.TextStyle(size=18))
        pernocte_columna= ft.Column([pernocte_title,pernocte],
                                     spacing=3,horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # NOMBRE Y APELLIDO TOMADO DEL BACKEND
        nombreyapellido_title= ft.Text("Nombre y Legajo",color= ft.Colors.WHITE, style=ft.TextStyle(size=10))
        nombreyapellido=ft.Text(f"{nombre_usuario} - {legajo_usuario}", color= ft.Colors.CYAN_ACCENT, style=ft.TextStyle(size=15))
        nombreyapellido_columna= ft.Column([nombreyapellido_title,nombreyapellido],
                                             spacing=3,horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # CONTAINER REGISTRO 1
        conteiner_reg1_content = (ft.Column([
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
        ]))
    else:
        # Define un contenido alternativo para el contenedor si no hay detalles
        conteiner_reg1_content = ft.Text("No se encontraron detalles de la entrada.", color=ft.colors.YELLOW_ACCENT_700)

    # CONTAINER REGISTRO 1 (se crea siempre, pero el contenido cambia)
    conteiner_reg1= ft.Container(
        bgcolor=ft.Colors.BLUE_700,
        alignment=ft.alignment.center,
        border_radius= ft.border_radius.only(top_left=20, top_right=20,bottom_left=20, bottom_right=20),
        expand= True,
        height=250,
        padding=ft.padding.only(left=20,top=10,right=20,bottom=10),
        content=conteiner_reg1_content
    )
    
    row7= ft.Row(
        [
            ft.ElevatedButton(
            text="Registrar Salida",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD)
            ),
            expand=True,height=60,bgcolor=ft.Colors.WHITE, color=ft.Colors.BLUE_900,
            on_click=lambda e: mainPernoteSalForm.mainPernote_SalForm(page))
        ]
    )

    row8= ft.Row(
        [
            ft.ElevatedButton(
            text="Historial entradas/salidas",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD,color=ft.Colors.BLACK)
            ),
            expand=True,
            height=60, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLUE_900,
            on_click=lambda e: mainPernoteHistorial.mainPernote_Historial(page))
        ]
    )


    columna1= ft.Column(
        controls=[logo,titulo,registroentrada],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=7,

    )

    columna2= ft.Column(
        controls=[conteiner_reg1,row7,row8],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=17
    )


    columna3= ft.Column(
        controls=[columna1, columna2],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=22   
    )
   
    page.add(columna3)
    




