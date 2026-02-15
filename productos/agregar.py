def view(content_area, ft):
    
    content_area.content = ft.Column([
        ft.Text("Agregar nuevo producto", size=25),
        ft.TextField(
            label="Nombre",
            hint_text="Nombre producto",
            width=300,
        ),
        ft.TextField(
            label="ISBN",
            hint_text="ISBN",
            width=300,
        ),
        ft.TextField(
            label="Precio",
            hint_text="Precio",
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER,
        ),
        ft.TextField(
            label="Stock mínimo",
            hint_text="Stock mínimo",
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER,
        ),
        ft.ElevatedButton("Guardar", on_click=lambda e: guardar_producto()),
    ], spacing=10)



def guardar_producto():
    #fdfdkfldkf
    print("sds")