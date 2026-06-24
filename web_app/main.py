import flet as ft

def main(page: ft.Page):
    page.title = "Test"

    state = {"count": 0}
    label = ft.Text("Step 4: 0", color=ft.Colors.WHITE)

    def on_tap(_):
        state["count"] += 1
        label.value = f"Step 4: {state['count']}"
        page.update()

    gd = ft.GestureDetector(content=ft.Container(bgcolor="#339966", width=100, height=50), on_tap=on_tap)

    def on_switch_change(e):
        label.value = f"Switch: {e.control.value}"
        page.update()

    sw = ft.Switch(value=False, on_change=on_switch_change)

    page.add(ft.Column([label, gd, sw], spacing=10))

ft.run(main)
