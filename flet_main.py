import flet as ft

# ==========================================
# 共通デザイン・スタイル定義
# ==========================================
BRAND_GREEN = "#339966"
DARK_BG = "#262626"
LIGHT_GRAY = "#F5F7FA"
FONT_FAMILY = "UD"

# 多言語テキスト定義辞書 (Kivyのロジックを移行)
LANG_TEXTS = {
    "ja": {
        "title_main": "ホーム",
        "title_list": "リスト",
        "title_history": "履歴",
        "title_settings": "設定",
        "important_notice": "【重要】新機能が追加されました！",
        "submit_info": "ボイコット商品情報をお寄せください",
        "input_area": "にゅうりょくえりあ (TOP)",
        "lang_setting": "言語設定",
        "lang_desc": "つかう ことばを えらびます",
        "ready": "準備中"
    },
    "en": {
        "title_main": "TOP",
        "title_list": "List",
        "title_history": "History",
        "title_settings": "Settings",
        "important_notice": "[Notice] New features have been added!",
        "submit_info": "Please send us boycott product info",
        "input_area": "Input Area (TOP)",
        "lang_setting": "Language",
        "lang_desc": "Choose your language",
        "ready": "Under Construction"
    }
}

# ==========================================
# カスタムコンポーネント (UIパーツ)
# ==========================================

class RoundButton(ft.Container):
    def __init__(self, icon_source, text_text="", on_click=None):
        super().__init__()
        if text_text:
            self.content = ft.Column(
                [
                    ft.Image(src=icon_source, height=28, fit=ft.ImageFit.CONTAIN),
                    ft.Text(text_text, size=12, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, font_family=FONT_FAMILY),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=1,
            )
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
        
        t = LANG_TEXTS[lang]
        
        def make_nav_btn(icon, text, target):
            is_active = current_screen == target
            return ft.GestureDetector(
                content=ft.Column(
                    [
                        ft.Image(src=icon, height=28, fit=ft.ImageFit.CONTAIN, opacity=1.0 if is_active else 0.5),
                        ft.Text(text, size=12, font_family=FONT_FAMILY, 
                                color=ft.colors.WHITE if is_active else "#999999",
                                weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),
                on_tap=lambda _: on_change_screen(target)
            )

        self.content = ft.Row(
            [
                make_nav_btn("data/images/icon/home.png", t["title_main"], "main"),
                make_nav_btn("data/images/icon/list.png", t["title_list"], "itemtype_widget"),
                RoundButton(
                    icon_source="data/images/icon/scan.png", 
                    text_text="スキャン", 
                    on_click=lambda _: on_change_screen("scan_widget")
                ),
                make_nav_btn("data/images/icon/history.png", t["title_history"], "history_widget"),
                make_nav_btn("data/images/icon/set.png", t["title_settings"], "settings_widget"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.bgcolor = DARK_BG
        self.border_radius = 25
        self.height = 65
        self.margin = ft.margin.only(left=10, right=10, bottom=15)
        self.padding = ft.padding.symmetric(horizontal=10)

# ==========================================
# 各画面のコンテンツ定義 (言語引数 lang を追加)
# ==========================================

def get_main_content(lang):
    t = LANG_TEXTS[lang]
    return ft.Stack(
        [
            ft.Image(src="data/images/top.png", fit=ft.ImageFit.COVER, expand=True),
            ft.Padding(
                padding=20,
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(t["important_notice"], color="#333333", size=14, font_family=FONT_FAMILY),
                            bgcolor=ft.colors.with_opacity(0.5, ft.colors.WHITE),
                            border_radius=15,
                            padding=10,
                            height=80,
                            alignment=ft.alignment.center_left,
                        ),
                        ft.ElevatedButton(
                            text=t["submit_info"],
                            height=55,
                            width=float("inf"),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        ),
                        ft.Container(
                            content=ft.Text(t["input_area"], font_family=FONT_FAMILY, color=ft.colors.WHITE),
                            height=200,
                        ),
                    ],
                    spacing=15,
                )
            )
        ],
        expand=True
    )

def get_itemtype_content(lang):
    t = LANG_TEXTS[lang]
    return ft.Container(
        bgcolor=LIGHT_GRAY,
        alignment=ft.alignment.center,
        content=ft.Text(f"{t['title_list']} ({t['ready']})", size=20, color="#262626", font_family=FONT_FAMILY)
    )

def get_scan_content(lang):
    return ft.Container(
        bgcolor=ft.colors.BLACK,
        alignment=ft.alignment.center,
        content=ft.Text("Camera / Barcode Scan", size=20, color=ft.colors.WHITE, font_family=FONT_FAMILY)
    )

def get_history_content(lang):
    t = LANG_TEXTS[lang]
    return ft.Container(
        bgcolor=LIGHT_GRAY,
        alignment=ft.alignment.center,
        content=ft.Text(f"{t['title_history']} ({t['ready']})", size=20, color="#262626", font_family=FONT_FAMILY)
    )

def get_settings_content(lang, on_toggle_lang):
    t = LANG_TEXTS[lang]
    return ft.Container(
        bgcolor=LIGHT_GRAY,
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(t["title_settings"], color=ft.colors.WHITE, size=20, weight=ft.FontWeight.BOLD, font_family=FONT_FAMILY),
                    bgcolor=BRAND_GREEN,
                    height=65,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    [
                        ft.Container(
                            bgcolor=ft.colors.WHITE,
                            border_radius=15,
                            padding=20,
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Image(src="data/images/icon/home.png", width=22, height=22),
                                            ft.Text(t["lang_setting"], size=17, weight=ft.FontWeight.BOLD, color="#262626", font_family=FONT_FAMILY)
                                        ],
                                        spacing=10,
                                    ),
                                    ft.Text(t["lang_desc"], size=12, color="#888888", font_family=FONT_FAMILY),
                                    ft.Row(
                                        [
                                            ft.Text("日本語", size=16, font_family=FONT_FAMILY, 
                                                    weight=ft.FontWeight.BOLD if lang == "ja" else ft.FontWeight.NORMAL, 
                                                    color=BRAND_GREEN if lang == "ja" else "#999999"),
                                            # 言語切り替えスイッチ (ONでEnglish, OFFで日本語)
                                            ft.Switch(
                                                value=(lang == "en"), 
                                                active_track_color=BRAND_GREEN,
                                                on_change=lambda e: on_toggle_lang(e.control.value)
                                            ),
                                            ft.Text("English", size=16, font_family=FONT_FAMILY, 
                                                    weight=ft.FontWeight.BOLD if lang == "en" else ft.FontWeight.NORMAL, 
                                                    color=BRAND_GREEN if lang == "en" else "#999999"),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=15,
                                    )
                                ],
                                spacing=10,
                            ),
                            height=150,
                        )
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    padding=20,
                ),
            ],
            spacing=0,
        ),
        expand=True
    )

# ==========================================
# メインアプリケーション（全体の構造）
# ==========================================
def main(page: ft.Page):
    page.title = "Boycott App"
    page.width = 390
    page.height = 844
    page.padding = 0

    # 💾 設定の読込ロジック (Kivy版の JsonStore の代わり)
    # ブラウザのLocalStorage等に自動保存される仕組みです
    saved_lang = page.client_storage.get("user_lang")
    # 保存されていなければデフォルトは日本語("ja")
    if not saved_lang:
        saved_lang = "ja"
        page.client_storage.set("user_lang", "ja")

    # 現在の状態を保持する変数群
    state = {
        "current_screen": "main",
        "lang": saved_lang
    }

    main_content_area = ft.Container(expand=True)

    # 画面全体をリフレッシュする関数
    def refresh_ui():
        target = state["current_screen"]
        lang = state["lang"]

        # 1. 現在の画面に合わせて中身を生成
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
        
        # 2. メニューバーの文字も言語を反映して再生成
        page.controls[0].controls[1] = BottomMenuBar(
            current_screen=target, 
            on_change_screen=change_screen,
            lang=lang
        )
        page.update()

    # 画面切り替えイベント
    def change_screen(target_name):
        state["current_screen"] = target_name
        refresh_ui()

    # 🌐 言語切り替えイベント（ロジックの肝）
    def toggle_language(is_english):
        new_lang = "en" if is_english else "ja"
        state["lang"] = new_lang
        # ブラウザ/端末に設定を保存する
        page.client_storage.set("user_lang", new_lang)
        # 画面を再描画して文字を切り替える
        refresh_ui()

    # 初期描画
    refresh_ui()

    page.add(
        ft.Column(
            [
                main_content_area,
                BottomMenuBar(current_screen="main", on_change_screen=change_screen, lang=state["lang"])
            ],
            spacing=0,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)                # スキャンボタン（仮で押したらスキャン画面へ切り替え）
                RoundButton(
                    icon_source="data/images/icon/scan.png", 
                    text_text="スキャン", 
                    on_click=lambda _: on_change_screen("scan_widget")
                ),
                make_nav_btn("data/images/icon/history.png", "履歴", "history_widget"),
                make_nav_btn("data/images/icon/set.png", "設定", "settings_widget"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.bgcolor = DARK_BG
        self.border_radius = 25
        self.height = 65
        self.margin = ft.margin.only(left=10, right=10, bottom=15)
        self.padding = ft.padding.symmetric(horizontal=10)

# ==========================================
# 各画面のコンテンツ定義 (中身だけを返す関数)
# ==========================================

# 1. TOP画面の中身
def get_main_content():
    return ft.Stack(
        [
            ft.Image(src="data/images/top.png", fit=ft.ImageFit.COVER, expand=True),
            ft.Padding(
                padding=20,
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text("【重要】新機能が追加されました！", color="#333333", size=14, font_family=FONT_FAMILY),
                            bgcolor=ft.colors.with_opacity(0.5, ft.colors.WHITE),
                            border_radius=15,
                            padding=10,
                            height=80,
                            alignment=ft.alignment.center_left,
                        ),
                        ft.ElevatedButton(
                            text="ボイコット商品情報をお寄せください",
                            height=55,
                            width=float("inf"),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        ),
                        ft.Container(
                            content=ft.Text("にゅうりょくえりあ (TOP)", font_family=FONT_FAMILY, color=ft.colors.WHITE),
                            height=200,
                        ),
                    ],
                    spacing=15,
                )
            )
        ],
        expand=True
    )

# 2. リスト画面の中身 (新規追加)
def get_itemtype_content():
    return ft.Container(
        bgcolor=LIGHT_GRAY,
        alignment=ft.alignment.center,
        content=ft.Text("リスト画面（準備中）", size=20, color="#262626", font_family=FONT_FAMILY)
    )

# 3. スキャン画面の中身 (新規追加)
def get_scan_content():
    return ft.Container(
        bgcolor=ft.colors.BLACK,
        alignment=ft.alignment.center,
        content=ft.Text("カメラ・バーコードスキャン画面", size=20, color=ft.colors.WHITE, font_family=FONT_FAMILY)
    )

# 4. 履歴画面の中身 (新規追加)
def get_history_content():
    return ft.Container(
        bgcolor=LIGHT_GRAY,
        alignment=ft.alignment.center,
        content=ft.Text("履歴画面（準備中）", size=20, color="#262626", font_family=FONT_FAMILY)
    )

# 5. 設定画面の中身
def get_settings_content():
    return ft.Container(
        bgcolor=LIGHT_GRAY,
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("設定", color=ft.colors.WHITE, size=20, weight=ft.FontWeight.BOLD, font_family=FONT_FAMILY),
                    bgcolor=BRAND_GREEN,
                    height=65,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    [
                        ft.Container(
                            bgcolor=ft.colors.WHITE,
                            border_radius=15,
                            padding=20,
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Image(src="data/images/icon/home.png", width=22, height=22),
                                            ft.Text("言語設定", size=17, weight=ft.FontWeight.BOLD, color="#262626", font_family=FONT_FAMILY)
                                        ],
                                        spacing=10,
                                    ),
                                    ft.Text("つかう ことばを えらびます", size=12, color="#888888", font_family=FONT_FAMILY),
                                    ft.Row(
                                        [
                                            ft.Text("日本語", size=16, font_family=FONT_FAMILY, weight=ft.FontWeight.BOLD, color=BRAND_GREEN),
                                            ft.Switch(value=False, active_        self.page = page
        self.current_screen = current_screen
        
        # ナビゲーションボタンのヘルパー関数 (<NavButton> の再現)
        def make_nav_btn(icon, text, target):
            is_active = current_screen == target
            return ft.GestureDetector(
                content=ft.Column(
                    [
                        ft.Image(src=icon, height=28, fit=ft.ImageFit.CONTAIN, opacity=1.0 if is_active else 0.5),
                        ft.Text(text, size=12, font_family=FONT_FAMILY, 
                                color=ft.colors.WHITE if is_active else "#999999",
                                weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),
                on_tap=lambda _: print(f"Go to {target}") # 画面遷移ロジックをここに
            )

        self.content = ft.Row(
            [
                make_nav_btn("data/images/icon/home.png", "TOP", "main"),
                make_nav_btn("data/images/icon/list.png", "リスト", "itemtype_widget"),
                # スキャンボタン (浮かせるために少し大きめのRoundButton)
                RoundButton(icon_source="data/images/icon/scan.png", text_text="スキャン"),
                make_nav_btn("data/images/icon/history.png", "履歴", "history_widget"),
                make_nav_btn("data/images/icon/set.png", "設定", "settings_widget"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.bgcolor = DARK_BG
        self.border_radius = 25
        self.height = 65
        self.margin = ft.margin.only(left=10, right=10, bottom=15)
        self.padding = ft.padding.symmetric(horizontal=10)

# ==========================================
# 各画面 (Widgets) の再現
# ==========================================

# <MainWidget> (TOP画面)
def main_view(page):
    return ft.Stack(
        [
            ft.Image(src="data/images/top.png", fit=ft.ImageFit.COVER, expand=True),
            ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                # 1. お知らせコーナー
                                ft.Container(
                                    content=ft.Text("【重要】新機能が追加されました！", color="#333333", size=14, font_family=FONT_FAMILY),
                                    bgcolor=ft.colors.with_opacity(0.5, ft.colors.WHITE),
                                    border_radius=15,
                                    padding=10,
                                    height=80,
                                    alignment=ft.alignment.center_left,
                                ),
                                # 2. リンクボタン
                                ft.ElevatedButton(
                                    text="ボイコット商品情報をお寄せください",
                                    height=55,
                                    width=float("inf"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                ),
                                # 3. メイン入力エリア
                                ft.Container(
                                    content=ft.Text("にゅうりょくえりあ", font_family=FONT_FAMILY),
                                    height=200,
                                ),
                                # 下部メニューのためのスペーサー
                                ft.Container(height=80)
                            ],
                            spacing=15,
                        ),
                        expand=True,
                        padding=20,
                    ),
                    BottomMenuBar(page, current_screen="main")
                ]
            )
        ],
        expand=True
    )

# <SettingsWidget> (設定画面)
def settings_view(page):
    return ft.Container(
        bgcolor=LIGHT_GRAY,
        content=ft.Column(
            [
                # ヘッダー
                ft.Container(
                    content=ft.Text("設定", color=ft.colors.WHITE, size=20, weight=ft.FontWeight.BOLD, font_family=FONT_FAMILY),
                    bgcolor=BRAND_GREEN,
                    height=65,
                    alignment=ft.alignment.center,
                ),
                # コンテンツエリア (スクロール可能)
                ft.Column(
                    [
                        # 言語設定カード
                        ft.Container(
                            bgcolor=ft.colors.WHITE,
                            border_radius=15,
                            padding=20,
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Image(src="data/images/icon/home.png", width=22, height=22),
                                            ft.Text("言語設定", size=17, weight=ft.FontWeight.BOLD, color="#262626", font_family=FONT_FAMILY)
                                        ],
                                        spacing=10,
                                    ),
                                    ft.Text("つかう ことばを えらびます", size=12, color="#888888", font_family=FONT_FAMILY),
                                    # スイッチ操作エリア
                                    ft.Row(
                                        [
                                            ft.Text("日本語", size=16, font_family=FONT_FAMILY, weight=ft.FontWeight.BOLD, color=BRAND_GREEN),
                                            # Flet標準のSwitch（カスタム風にする場合は装飾が必要）
                                            ft.Switch(value=False, active_track_color=BRAND_GREEN),
                                            ft.Text("English", size=16, font_family=FONT_FAMILY, color="#999999"),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=15,
                                    )
                                ],
                                spacing=10,
                            ),
                            height=150,
                        )
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    padding=20,
                ),
                BottomMenuBar(page, current_screen="settings_widget")
            ],
            spacing=0,
        ),
        expand=True
    )

# ==========================================
# Flet アプリケーション起動エントリーポイント
# ==========================================
def main(page: ft.Page):
    page.title = "Boycott App"
    page.width = 390   # スマホを意識したサイズ設定
    page.height = 844
    page.padding = 0
    
    # フォントのインポート設定（必要に応じてパスを調整してください）
    # page.fonts = {"UD": "fonts/YourUDFont.ttf"}

    # テスト用：ここでは仮に設定画面を表示します。
    # 必要に応じて main_view(page) などに切り替えてください。
    page.add(settings_view(page))

if __name__ == "__main__":
    ft.app(target=main)
