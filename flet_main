import flet as ft

# ==========================================
# 共通デザイン・スタイル定義
# ==========================================
BRAND_GREEN = "#339966"  # 0.2, 0.6, 0.4
DARK_BG = "#262626"     # 0.15, 0.15, 0.15
LIGHT_GRAY = "#F5F7FA"   # 0.96, 0.97, 0.98

# Kivyの <Label> <Button> font_name: "UD" の代わり
FONT_FAMILY = "UD"

# ==========================================
# カスタムコンポーネント (Kivyのカスタムクラス)
# ==========================================

# <IconTextButton> の再現
class IconTextButton(ft.Container):
    def __init__(self, text, icon_source, on_click=None):
        super().__init__()
        self.content = ft.Row(
            [
                ft.Image(src=icon_source, width=20, height=20, fit=ft.ImageFit.CONTAIN),
                ft.Text(text, size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, font_family=FONT_FAMILY),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
        self.bgcolor = BRAND_GREEN
        self.border_radius = 22.5
        self.width = 200
        self.height = 45
        self.alignment = ft.alignment.center
        self.on_click = on_click

# <RoundButton> の再現
class RoundButton(ft.Container):
    def __init__(self, icon_source, text_text="", on_click=None):
        super().__init__()
        # テキストがあるかないかでレイアウトを切り替え
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

# <BottomMenuBar> の再現
class BottomMenuBar(ft.Container):
    def __init__(self, page, current_screen=""):
        super().__init__()
        self.page = page
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
