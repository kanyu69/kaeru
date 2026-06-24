import flet as ft

def main(page: ft.Page):
    page.title = "Test"
    page.add(ft.Text("Step 1: OK"))
    page.add(ft.Container(bgcolor="#262626", height=65, content=ft.Text("Step 2: Container OK", color=ft.Colors.WHITE)))

ft.run(main)
