import flet as ft

BRAND_GREEN = "#339966"
DARK_BG = "#262626"
LIGHT_GRAY = "#F5F7FA"
FONT_FAMILY = "UD"

LANG_TEXTS = {
    "ja": {
        "title_main": "ホーム", "title_list": "リスト", "title_history": "履歴", "title_settings": "設定",
        "important_notice": "【重要】新機能が追加されました！", "submit_info": "ボイコット商品情報をお寄せください",
        "input_area": "にゅうりょくえりあ (TOP)", "lang_setting": "言語設定", "lang_desc": "つかう ことばを えらびます", "ready": "準備中"
    },
    "en": {
        "title_main": "TOP", "title_list": "List", "title_history": "History", "title_settings": "Settings",
        "important_notice": "[Notice] New features have been added!", "submit_info": "Please send us boycott product info",
        "input_area": "Input Area (TOP)", "lang_setting": "Language", "lang_desc": "Choose your language", "ready": "Under Construction"
    }
}

class RoundButton(ft.Container):
    def __init__(self, label="", text_text="", on_click=None):
        super().__init__()
        if text_text:
            self.content = ft.Column([
                ft.Text(label, size=20, color=ft.Colors.WHITE),
                ft.Text(text_text, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, font_family=FONT_FAMILY),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1)
            # ft.Padding(left, top, right, bottom)
            self.padding = ft.Padding(0, 12, 0, 12)
        else:
            self.content = ft.Text(label, size=24, color=ft.Colors.WHITE)
            self.padding = ft.Padding(0, 6, 0, 6)
        self.bgcolor = BRAND_GREEN
        self.shape = ft.BoxShape.CIRCLE
        self.width = 70
        self.height = 70
        self.on_click = on_click

class BottomMenuBar(ft.Container):
    def __init__(self, current_screen, on_change_screen, lang):
        super().__init__()
        if lang not in LANG_TEXTS:
            lang = "ja"

        t = LANG_TEXTS[lang]
        def make_nav_btn(label, text, target):
            is_active = current_screen == target
            return ft.GestureDetector(
                content=ft.Column([
                    ft.Text(label, size=20, color=ft.Colors.WHITE if is_active else "#999999"),
                    ft.Text(text, size=12, font_family=FONT_FAMILY, color=ft.Colors.WHITE if is_active else "#999999", weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                on_tap=lambda _: on_change_screen(target)
            )
        self.content = ft.Row([
            make_nav_btn("🏠", t["title_main"], "main"),
            make_nav_btn("📋", t["title_list"], "itemtype_widget"),
            RoundButton(label="📷", text_text="スキャン", on_click=lambda _: on_change_screen("scan_widget")),
            make_nav_btn("🕒", t["title_history"], "history_widget"),
            make_nav_btn("⚙️", t["title_settings"], "settings_widget"),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        self.bgcolor = DARK_BG
        self.border_radius = 25
        self.height = 65
        # ft.Margin(left, top, right, bottom)
        self.margin = ft.Margin(10, 0, 10, 15)
        # ft.Padding(left, top, right, bottom)
        self.padding = ft.Padding(10, 0, 10, 0)

def get_main_content(lang):
    if lang not in LANG_TEXTS:
        lang = "ja"

    t = LANG_TEXTS[lang]
    return ft.Stack([
        ft.Container(bgcolor=BRAND_GREEN, expand=True),
        ft.Container(padding=20, content=ft.Column([
            ft.Container(
                content=ft.Text(t["important_notice"], color="#333333", size=14, font_family=FONT_FAMILY), 
                bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), 
                border_radius=15, 
                padding=10, 
                height=80, 
                alignment="center_left"
            ),
            ft.ElevatedButton(
                content=ft.Text(t["submit_info"]),
                height=55, 
                width=float("inf"), 
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
            ),
            ft.Container(content=ft.Text(t["input_area"], font_family=FONT_FAMILY, color=ft.Colors.WHITE), height=200),
        ], spacing=15))
    ], expand=True)

def get_itemtype_content(lang):
    if lang not in LANG_TEXTS: lang = "ja"
    t = LANG_TEXTS[lang]
    return ft.Container(bgcolor=LIGHT_GRAY, alignment="center", content=ft.Text(f"{t['title_list']} ({t['ready']})", size=20, color="#262626", font_family=FONT_FAMILY))

def get_scan_content(lang):
    return ft.Container(bgcolor=ft.Colors.BLACK, alignment="center", content=ft.Text("Camera / Barcode Scan", size=20, color=ft.Colors.WHITE, font_family=FONT_FAMILY))

def get_history_content(lang):
    if lang not in LANG_TEXTS: lang = "ja"
    t = LANG_TEXTS[lang]
    return ft.Container(bgcolor=LIGHT_GRAY, alignment="center", content=ft.Text(f"{t['title_history']} ({t['ready']})", size=20, color="#262626", font_family=FONT_FAMILY))

def get_settings_content(lang, on_toggle_lang):
    if lang not in LANG_TEXTS: lang = "ja"
    t = LANG_TEXTS[lang]
    return ft.Container(bgcolor=LIGHT_GRAY, content=ft.Column([
        ft.Container(content=ft.Text(t["title_settings"], color=ft.Colors.WHITE, size=20, weight=ft.FontWeight.BOLD, font_family=FONT_FAMILY), bgcolor=BRAND_GREEN, height=65, alignment="center"),
        ft.Column([
            ft.Container(bgcolor=ft.Colors.WHITE, border_radius=15, padding=20, content=ft.Column([
                ft.Row([ft.Text("🏠", size=20), ft.Text(t["lang_setting"], size=17, weight=ft.FontWeight.BOLD, color="#262626", font_family=FONT_FAMILY)], spacing=10),
                ft.Text(t["lang_desc"], size=12, color="#888888", font_family=FONT_FAMILY),
                ft.Row([
                    ft.Text("日本語", size=16, font_family=FONT_FAMILY, weight=ft.FontWeight.BOLD if lang == "ja" else ft.FontWeight.NORMAL, color=BRAND_GREEN if lang == "ja" else "#999999"),
                    ft.Switch(value=(lang == "en"), active_track_color=BRAND_GREEN, on_change=lambda e: on_toggle_lang(e.control.value)),
                    ft.Text("English", size=16, font_family=FONT_FAMILY, weight=ft.FontWeight.BOLD if lang == "en" else ft.FontWeight.NORMAL, color=BRAND_GREEN if lang == "en" else "#999999"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
            ], spacing=10), height=150)
        ], expand=True, scroll=ft.ScrollMode.AUTO, padding=20)
    ], spacing=0), expand=True)

def main(page: ft.Page):
    page.title = "Boycott App"
    page.padding = 0
    page.window_width = 400
    page.window_height = 800

    saved_lang = "ja"
    state = {"current_screen": "main", "lang": saved_lang}

    main_content_area = ft.Container(expand=True)
    bottom_bar_container = ft.Container()
    app_layout = ft.Column([main_content_area, bottom_bar_container], spacing=0, expand=True)

    def refresh_ui():
        target = state["current_screen"]
        lang = state["lang"]
        if lang not in LANG_TEXTS:
            lang = "ja"

        if target == "main":
            main_content_area.content = get_main_content(lang)
        elif target == "itemtype_widget":
            main_content_area.content = get_itemtype_content(lang)
        elif target == "scan_widget":
            main_content_area.content = get_scan_content(lang)
        elif target == "history_widget":
            main_content_area.content = get_history_content(lang)
        elif target == "settings_widget":
            main_content_area.content = get_settings_content(lang, toggle_language)

        bottom_bar_container.content = BottomMenuBar(
            current_screen=target,
            on_change_screen=change_screen,
            lang=lang
        )
        page.update()

    def change_screen(target_name):
        state["current_screen"] = target_name
        refresh_ui()

    def toggle_language(is_english):
        new_lang = "en" if is_english else "ja"
        state["lang"] = new_lang
        page.client_storage.set("user_lang", new_lang)
        refresh_ui()

    page.add(app_layout)
    refresh_ui()

ft.run(main)
