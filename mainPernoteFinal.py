import flet as ft
import mainInicio
import accionBotonPern
import globals
import os

ARCHIVO_DATOS_ENTRADA = "datos_entrada.json"


def limpiar_registro():
     # Limpiar las variables globales
    globals.writed_name = ""
    globals.writed_legajo = ""
    globals.selected_option_pernocte = ""
    globals.selected_date_ent = "Sin seleccionar"
    globals.selected_time_ent = "Sin seleccionar"
    globals.writed_train_ent = ""
    globals.writed_obs_ent = ""
    globals.selected_date_sal = "Sin seleccionar"
    globals.selected_time_sal = "Sin seleccionar"
    globals.writed_train_sal = ""
    globals.writed_obs_sal = ""

    if os.path.exists(ARCHIVO_DATOS_ENTRADA):
        os.remove(ARCHIVO_DATOS_ENTRADA)




# Función principal de la página final
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
    page.padding= ft.padding.only(left=30, top=25, right=30, bottom=30)


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

    registro_entrada_salida= ft.Text("Tu entrada y salida se registraron correctamente",
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

    cambiar_f1= accionBotonPern.obtener_cambiar_f1()

    row11= ft.Row(
        [
            ft.ElevatedButton(
            text="Ir al inicio",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD),color=ft.Colors.WHITE),
            expand=True,height=50, bgcolor=ft.Colors.BLUE_ACCENT,
            on_click=lambda e: (cambiar_f1(e),mainInicio.main_Inicio(page,page.client_storage.get("username"), page.client_storage.get("user_info")),limpiar_registro()))
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
