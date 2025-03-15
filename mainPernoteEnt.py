import flet as ft
import mainPernoteEntForm
import mainInicio
import mainPernoteHistorial



def mainPernote_Ent(page: ft.Page):
    page.clean()
    page.title= "Pernoctes Entrada"

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
    page.padding= ft.padding.only(left=30, top=10, right=30, bottom=30)


    logo = ft.Image(src= 'logoFrateAlianza1.png',width=70,)
    titulo= ft.Text("Pernoctes", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))

    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        leading=ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,
                              icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click=lambda e: mainInicio.main_Inicio(page,page.client_storage.get("username"), page.client_storage.get("user_info")))
    )

    page.add(app_bar)

    row5= ft.Row(
        [
            ft.ElevatedButton(
            text="Registrar Entrada",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD,color=ft.Colors.BLACK)
            ),
            expand=True, height=70, bgcolor=ft.Colors.WHITE,color=ft.Colors.BLUE_900,
            on_click=lambda e: mainPernoteEntForm.mainPernote_EntForm(page))
        ]
    )

    row6= ft.Row(
        [
            ft.ElevatedButton(
            text="Historial entradas/salidas",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD,color=ft.Colors.BLACK)
            ),
            expand=True,
            height=70, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLUE_900,
            on_click=lambda e: mainPernoteHistorial.mainPernote_Historial(page))
        ]
    )

    columna1= ft.Column(
        controls=[logo,titulo],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10    
    )


    columna2= ft.Column(
        controls=[row5, row6],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=35
    )

    columna3= ft.Column(
        controls=[columna1,columna2],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=80
    )
   
    page.add(columna3)

