import flet as ft
import mainInicio
import asyncio


# Función principal de la página final
async def mainPernote_Final_Inicio(page: ft.Page):
    page.clean()
    page.title= "Registro Exitoso"

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


    logo = ft.Image(src= 'logoFrateAlianza1.png',width=70,)
    titulo= ft.Text("Pernoctes", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))

       #MENSAJE DE EXITO

    registro_entrada_salida= ft.Text("Tu entrada y salida se registraron correctamente",
                                      color= ft.Colors.GREEN_ACCENT_400, style=ft.TextStyle(size=22,weight=ft.FontWeight.W_400),
                                      expand=True, text_align=ft.TextAlign.CENTER,)
    Icon_check= ft.Icon(name=ft.Icons.CHECK_CIRCLE_ROUNDED,color=ft.Colors.GREEN_ACCENT_400,size=30)

    column_registro_entr_sal= ft.Column([Icon_check,registro_entrada_salida],
                                        alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER)


    columna1= ft.Column(
        controls=[logo,titulo],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=7    
    )

    columna2= ft.Column(
        controls=[column_registro_entr_sal],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    columna3= ft.Column(
        controls=[columna1,columna2],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=50
    )
   
    page.add(columna3)

    await asyncio.sleep(3)

    mainInicio.main_Inicio(page,page.client_storage.get("username"), page.client_storage.get("user_info"))
    page.update()

