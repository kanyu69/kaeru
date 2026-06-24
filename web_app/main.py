import flet as ft

def main(page: ft.Page):
    page.title = "Test"
    page.add(ft.Text("Step 5: before image", color=ft.Colors.WHITE))
    page.add(ft.Image(src="data/images/icon/home.png", height=28))
    page.add(ft.Text("Step 5: after image", color=ft.Colors.WHITE))

ft.run(main)
