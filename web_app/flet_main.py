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
    def __init__(self, icon_source, text_text="", on_click=None):
        super().__init__()
        if text_text:
            self.content = ft.Column([
                ft.Image(src=icon_source, height=28, fit=ft.ImageFit.CONTAIN),
                ft.Text(text_text, size=12, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, font_family=FONT_FAMILY),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1)
            self.padding = ft.padding.only(top=12, bottom=12)
        else:
            self.content = ft.Image(src=icon_source, fit=ft.ImageFit.CONTAIN)
            self.padding = ft.padding.only(top=6, bottom=6)
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
        def make_nav_btn(icon, text, target):
            is_active = current_screen == target
            return ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src=icon, height=28, fit=ft.ImageFit.CONTAIN, opacity=1.0 if is_active else 0.5),
                    ft.Text(text, size=12, font_family=FONT_FAMILY, color=ft.colors.WHITE if is_active else "#999999", weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                on_tap=lambda _: on_change_screen(target)
            )
        self.content = ft.Row([
            make_nav_btn("data/images/icon/home.png", t["title_main"], "main"),
            make_nav_btn("data/images/icon/list.png", t["title_list"], "itemtype_widget"),
            RoundButton(icon_source="data/images/icon/scan.png", text_text="スキャン", on_click=lambda _: on_change_screen("scan_widget")),
            make_nav_btn("data/images/icon/history.png", t["title_history"], "history_widget"),
            make_nav_btn("data/images/icon/set.png", t["title_settings"], "settings_widget"),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        self.bgcolor = DARK_BG
        self.border_radius = 25
        self.height = 65
        self.margin = ft.margin.only(left=10, right=10, bottom=15)

