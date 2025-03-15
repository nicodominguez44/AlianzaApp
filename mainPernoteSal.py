import flet as ft
import mainInicio
import mainPernoteSalForm
import globals
import mainPernoteEntForm
import mainPernoteHistorial

def mainPernote_Sal(page: ft.Page):
    page.clean()
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
    page.padding= ft.padding.only(left=25, top=0, right=25, bottom=0)

    mainPernoteEntForm.cargar_datos_entrada()

    app_bar = ft.AppBar(
        bgcolor= ft.Colors.TRANSPARENT,
        leading=ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_SHARP,
                              icon_size=40,icon_color=ft.Colors.BLUE_900,
                              on_click=lambda e: mainInicio.main_Inicio(page,page.client_storage.get("username"), page.client_storage.get("user_info")))
    )

    page.add(app_bar)


    logo = ft.Image(src= 'logoFrateAlianza1.png',width=70,)
    titulo= ft.Text("Pernoctes", color= ft.Colors.WHITE, style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD))


    registroentrada= ft.Text("Entrada Registrada!", color= ft.Colors.CYAN_ACCENT, 
                             style=ft.TextStyle(size=24,weight=ft.FontWeight.W_300))
    
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
                    ft.Text(globals.selected_date_ent,
                            text_align=ft.TextAlign.CENTER,color= ft.Colors.CYAN_ACCENT)],
                    alignment=ft.MainAxisAlignment.START),

            ft.Row([
                    ft.Text("HORA",text_align=ft.TextAlign.CENTER,
                            color= ft.Colors.WHITE, style=ft.TextStyle(size=10,weight=ft.FontWeight.BOLD)),
                    ft.Text(globals.selected_time_ent,
                            text_align=ft.TextAlign.CENTER,color= ft.Colors.CYAN_ACCENT)],
                   alignment=ft.MainAxisAlignment.START),

            ft.Row([
                    ft.Text("TREN",text_align=ft.TextAlign.CENTER,
                            color= ft.Colors.WHITE, style=ft.TextStyle(size=10,weight=ft.FontWeight.BOLD)),
                    ft.Text(globals.writed_train_ent, color= ft.Colors.CYAN_ACCENT)],
                   alignment=ft.MainAxisAlignment.START),
            ft.Row([
                    ft.Text("OBSERVACIONES",color= ft.Colors.WHITE, style=ft.TextStyle(size=8,weight=ft.FontWeight.BOLD)),
                    ft.Text(globals.writed_obs_ent, color= ft.Colors.CYAN_ACCENT)],
                   alignment=ft.MainAxisAlignment.START),
        ],))
    )
    
    row7= ft.Row(
        [
            ft.ElevatedButton(
            text="Registrar Salida",
            style= ft.ButtonStyle(
                text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD)
            ),
            expand=True,height=70,bgcolor=ft.Colors.WHITE, color=ft.Colors.BLUE_900,
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
            height=70, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLUE_900,
            on_click=lambda e: mainPernoteHistorial.mainPernote_Historial(page))
        ]
    )


    columna1= ft.Column(
        controls=[logo,titulo,registroentrada],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,

    )

    columna2= ft.Column(
        controls=[conteiner_reg1,row7,row8],
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




