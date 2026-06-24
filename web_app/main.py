import flet as ft

def main(page: ft.Page):
    page.title = "Test"
    
    content_area = ft.Container(expand=True)
    layout = ft.Column([content_area], spacing=0, expand=True)
    
    def refresh():
        content_area.content = ft.Text("Step 3: refresh via closure OK", color=ft.Colors.WHITE)
        page.update()
    
    page.add(layout)
    refresh()

ft.run(main)
