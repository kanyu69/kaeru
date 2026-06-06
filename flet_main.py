def get_main_content(lang):
    if lang not in LANG_TEXTS:
        lang = "ja"
        
    t = LANG_TEXTS[lang]
    return ft.Stack([
        ft.Image(src="data/images/top.png", fit=ft.ImageFit.COVER, expand=True),
        ft.Padding(padding=20, content=ft.Column([  # 👈 ここが原因です！
            ft.Container(content=ft.Text(t["important_notice"], color="#333333", size=14, font_family=FONT_FAMILY), bgcolor=ft.colors.with_opacity(0.5, ft.colors.WHITE), border_radius=15, padding=10, height=80, alignment=ft.alignment.center_left),
            ft.ElevatedButton(text=t["submit_info"], height=55, width=float("inf"), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
            ft.Container(content=ft.Text(t["input_area"], font_family=FONT_FAMILY, color=ft.colors.WHITE), height=200),
        ], spacing=15))
    ], expand=True)
