




def view(content_area,ft):
    content_area.content = ft.Text("Agregar nuevo producto", size=25)
    content_area.content = txt_basico = ft.TextField(
        label="Nombre",
        hint_text="Nombre producto",
        width=300,
    )