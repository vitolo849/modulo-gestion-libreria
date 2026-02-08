import flet as ft

def main (page: ft.Page):
    page.title= "Administracion de usuarios"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment= ft.CrossAxisAlignment.START
    
    btn_productos = ft.ElevatedButton("Productos", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), width=200, height=50)
    btn_membresias = ft.ElevatedButton("Membresías", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), width=200, height=50)
   
    
    
    page.add(btn_productos, margen, btn_membresias)
ft.run(main)   