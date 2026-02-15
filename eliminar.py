def view (content_area, ft):
    content_area.content = ft.Column([
        ft.Text("Eliminar producto", size=25),
    
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
        ft.ElevatedButton("Eliminar", on_click=lambda e: eliminar_producto()),
    ], spacing=10)



def eliminar_producto():
    #fdfdkfldkf
    print("Producto eliminado")