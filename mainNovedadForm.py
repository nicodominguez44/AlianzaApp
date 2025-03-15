import flet as ft
import datetime
import locale
import mainNovedad
import mainNovedadFinal
import globals



try:
    locale.setlocale(locale.LC_TIME, 'es_ES')
except locale.Error:
    print("La localidad 'es_ES' no está soportada, usando la predeterminada.")
    locale.setlocale(locale.LC_TIME, 'C')

def validar_campos_nov(page):
        
    # Validación para pernocte para novedad (PopupMenu)
    if globals.selected_option_pernocte_nov == "Sin seleccionar":
        page.update()
        return False
    
    # Validación para la fecha de la novedad (DatePicker)
    if globals.selected_date_nov == "Sin seleccionar": 
        page.update()
        return False
    
    
    # Validacion para novedad
    if globals.writed_novedad == "":
        page.update()
        return False
    
    # Si todo está completo, retorna True
    return True

def registrar_novedad(page):
    if validar_campos_nov(page):  # Si todo está bien
        # Proceder con la acción de registrar la entrada
        mainNovedadFinal.mainNovedad_Final(page)


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

    selected_option_text= globals.selected_option_pernocte_nov if globals.selected_option_pernocte_nov != "Sin seleccionar" else "seleccionar pernocte"
    selected_option= ft.Text(selected_option_text, color= ft.Colors.BLUE_900, style=ft.TextStyle(size=18))

    def update_selected_pernocte(option):
        globals.selected_option_pernocte_nov = option  # Actualizamos el valor global con la opción seleccionada
        selected_option.value = option  # Actualizamos el valor en el widget Text
        page.update()

    popupMenu= ft.PopupMenuButton(
                icon_color= ft.Colors.BLUE_900,
                bgcolor= ft.Colors.BLACK87,
                icon= ft.Icons.ARROW_DROP_DOWN_CIRCLE, icon_size=35,
                
                items=[
                    ft.PopupMenuItem(text="Dock Central",on_click=lambda e: update_selected_pernocte("Dock Central")),
                    ft.PopupMenuItem(text="Mercedes BAP", on_click=lambda e: update_selected_pernocte("Mercedes BAP")),
                    ft.PopupMenuItem(text="Campana",on_click=lambda e: update_selected_pernocte("Campana")),
                    ft.PopupMenuItem(text="Junin",on_click=lambda e: update_selected_pernocte("Junin"))
                    ]
                )

            # NOVEDAD

    novedad=ft.Text("NOVEDAD", color= ft.Colors.WHITE, style=ft.TextStyle(size=10))

    def actualizar_nov(e):
        globals.writed_novedad = tf_novedad.value
        page.update()

    tf_novedad=ft.TextField(value=globals.writed_novedad,
                bgcolor=ft.Colors.WHITE, text_size=14,color=ft.Colors.BLACK, autofocus=True,
                border_radius=ft.border_radius.only(top_left=0,top_right=15,bottom_left=15,bottom_right=15),
                border_color=ft.Colors.CYAN_ACCENT, multiline=True, max_length=500, on_change= actualizar_nov,
                expand=True
                )
    
    novedad_columna= ft.Column([novedad,tf_novedad], expand= True,spacing=5)

            # FECHA DE LA NOVEDAD

    selected_date_text_value = globals.selected_date_nov if globals.selected_date_nov != "Sin seleccionar" else "Sin seleccionar"
    selected_date_text=ft.Text(selected_date_text_value,color= ft.Colors.WHITE,
                               style=ft.TextStyle(size=14,weight=ft.FontWeight.BOLD))

    def handle_change(e):
        # Actualizar el texto con la nueva fecha seleccionada
        date_selected = e.control.value.strftime('%d %B %Y')  # Formato "13 de febrero de 2025"
        selected_date_text.value = f"{date_selected}"  # Actualizar el texto
        globals.selected_date_nov = date_selected
        page.update()  # Actualizar la interfaz para reflejar el cambio

    def handle_dismissal(e):
        selected_date_text.value = "Sin seleccionar"
        globals.selected_date_nov = "Sin seleccionar"
        page.update()  # Actualizar la interfaz para reflejar el cambio

    RowFechaNov= ft.Row([
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
                                     on_click=lambda e: registrar_novedad(page) )
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