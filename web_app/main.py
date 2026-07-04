import flet as ft
import json
import asyncio
import sys
from datetime import datetime

# ブラウザ環境(Pyodide)専用の通信モジュールを読み込む
if sys.platform == "emscripten":
    from pyodide.http import pyfetch
else:
    import urllib.request as urllib_req

# カラー定義
BRAND_GREEN = "#339966"
DARK_BG = "#262626"
LIGHT_GRAY = "#F5F7FA"

# 翻訳データの定義
ITEM_NAMES = {
    "ja": {
        "ITEM_LEMON": "レモン", "ITEM_ORANGE": "オレンジ", "ITEM_GRAPEFRUIT": "グレープフルーツ",
        "ITEM_ZAKURO": "ザクロ", "ITEM_RAIMU": "ライム", "ITEM_IS": "イスラエル"
    },
    "en": {
        "ITEM_LEMON": "Lemon", "ITEM_ORANGE": "Orange", "ITEM_GRAPEFRUIT": "Grapefruit",
        "ITEM_ZAKURO": "Pomegranate", "ITEM_RAIMU": "Lime", "ITEM_IS": "Israel"
    }
}

LANG_TEXTS = {
    "ja": {
        "title_main": "ホーム", "title_list": "リスト", "title_history": "履歴", "title_settings": "設定",
        "important_notice": "【重要】新機能が追加されました！", "submit_info": "ボイコット商品情報をお寄せください",
        "input_area": "バーコードを入力してスキャンをテストできます", "lang_setting": "言語設定",
        "lang_desc": "つかう ことばを えらびます", "ready": "準備中", "search_btn": "検索", "searching": "検索中...",
        "not_registered": "未登録のバーコードです", "area_label": "⚠️{}産 ", "item_usage_label": "{}{}使用！⚠️",
        "company": "会社名", "clear_history": "履歴をすべて削除", "no_history": "履歴はありません"
    },
    "en": {
        "title_main": "TOP", "title_list": "List", "title_history": "History", "title_settings": "Settings",
        "important_notice": "[Notice] New features have been added!", "submit_info": "Please send us boycott product info",
        "input_area": "Enter Barcode to simulate scanning", "lang_setting": "Language",
        "lang_desc": "Choose your language", "ready": "Under Construction", "search_btn": "Search", "searching": "Searching...",
        "not_registered": "Not Registered", "area_label": "⚠️Origin: {} ", "item_usage_label": "{}{} used!⚠️",
        "company": "Company", "clear_history": "Clear History", "no_history": "No history available"
    }
}

# Supabase 設定
SUPABASE_URL = "https://iktqvcqxrkabmbgjl.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_z2zAh-vbopc9_ZBGE_wozg_YPrOuQ_x"

# 非同期の通信関数
async def connect_sheet_async(jan_code: str):
    url = f"{SUPABASE_URL}/rest/v1/products?jan=eq.{jan_code}"
    headers = {"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {SUPABASE_ANON_KEY}"}
    
    try:
        if sys.platform == "emscripten":
            response = await pyfetch(url, method="GET", headers=headers)
            if response.status == 200:
                data = await response.json()
                return data[0] if data else None
        else:
            req = urllib_req.Request(url, headers=headers)
            with urllib_req.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode("utf-8"))
                return data[0] if data else None
    except Exception as e:
        print(f"Database Error: {e}")
    return None

async def connect_sheet_all_async():
    url = f"{SUPABASE_URL}/rest/v1/products"
    headers = {"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {SUPABASE_ANON_KEY}"}
    
    try:
        if sys.platform == "emscripten":
            response = await pyfetch(url, method="GET", headers=headers)
            if response.status == 200:
                return await response.json()
        else:
            req = urllib_req.Request(url, headers=headers)
            with urllib_req.urlopen(req, timeout=10) as r:
                return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"Database Error: {e}")
    return []

def get_translated_name(lang, item_id):
    if lang not in ITEM_NAMES:
        lang = "ja"
    return ITEM_NAMES[lang].get(item_id, item_id)

class RoundButton(ft.Container):
    def __init__(self, label="", text_text="", on_click=None):
        super().__init__()
        if text_text:
            self.content = ft.Column([
                ft.Text(label, size=20, color=ft.Colors.WHITE),
                ft.Text(text_text, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1)
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
            is_active = current_screen == target or (target == "itemtype_widget" and current_screen == "list_widget")
            return ft.GestureDetector(
                content=ft.Column([
                    ft.Text(label, size=20, color=ft.Colors.WHITE if is_active else "#999999"),
                    ft.Text(text, size=12, color=ft.Colors.WHITE if is_active else "#999999", weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL),
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
        self.margin = ft.Margin(10, 0, 10, 15)
        self.padding = ft.Padding(10, 0, 10, 0)

def get_main_content(lang):
    t = LANG_TEXTS[lang]
    return ft.Stack([
        ft.Container(bgcolor=BRAND_GREEN, expand=True),
        ft.Container(padding=20, content=ft.Column([
            ft.Container(content=ft.Text(t["important_notice"], color="#333333", size=14), bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), border_radius=15, padding=10, height=80, alignment="center_left"),
            ft.Button(content=ft.Text(t["submit_info"]), height=55, width=float("inf"), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
        ], spacing=15))
    ], expand=True)

def get_itemtype_content(lang, on_select_category):
    categories = [
        {"id": "ITEM_LEMON", "icon": "🍋"},
        {"id": "ITEM_ORANGE", "icon": "🍊"},
        {"id": "ITEM_GRAPEFRUIT", "icon": "🍊"},
        {"id": "ITEM_ZAKURO", "icon": "🍎"}
    ]
    
    list_items = []
    for cat in categories:
        list_items.append(
            ft.ListTile(
                leading=ft.Text(cat["icon"], size=24),
                title=ft.Text(get_translated_name(lang, cat["id"]), size=18, color="#262626", weight=ft.FontWeight.BOLD),
                on_click=lambda e, cid=cat["id"]: on_select_category(cid)
            )
        )

    return ft.Container(
        bgcolor=LIGHT_GRAY,
        padding=10,
        content=ft.Column([
            ft.Text(LANG_TEXTS[lang]["title_list"], size=22, weight=ft.FontWeight.BOLD, color="#262626"),
            ft.Card(content=ft.Container(content=ft.Column(list_items), padding=10))
        ])
    )

def get_list_widget_content(lang, category_id, products):
    t = LANG_TEXTS[lang]
    cards = []
    for row in products:
        if row.get("item") == category_id:
            display_area = get_translated_name(lang, row.get("area", ""))
            display_item = get_translated_name(lang, row.get("item", ""))
            area_text = t["area_label"].format(display_area) if display_area else ""
            msg = t["item_usage_label"].format(area_text, display_item)
            img_path = row.get("image_path") or "https://via.placeholder.com/150"

            cards.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Row([
                            ft.Image(src=img_path, width=60, height=60, fit=ft.ImageFit.CONTAIN),
                            ft.Column([
                                ft.Text(row.get("product_name", ""), size=16, weight=ft.FontWeight.BOLD, color="#262626"),
                                ft.Text(f"{t['company']}: {row.get('company_name', '')}", size=12, color="#555555"),
                                ft.Text(msg, size=12, color=ft.Colors.RED_600, weight=ft.FontWeight.BOLD),
                            ], expand=True)
                        ])
                    )
                )
            )
            
    if not cards:
        cards.append(ft.Text("No items found.", color="#262626"))

    return ft.Container(
        bgcolor=LIGHT_GRAY,
        padding=10,
        content=ft.Column([
            ft.Text(f"{get_translated_name(lang, category_id)} {t['title_list']}", size=20, weight=ft.FontWeight.BOLD, color="#262626"),
            ft.Column(cards, scroll=ft.ScrollMode.AUTO, expand=True)
        ], expand=True)
    )

def get_scan_content(lang, on_search):
    t = LANG_TEXTS[lang]
    jan_input = ft.TextField(label="JAN Code", hint_text="e.g. 4901234567890", keyboard_type=ft.KeyboardType.NUMBER)
    
    return ft.Container(
        bgcolor=ft.Colors.BLACK,
        padding=20,
        content=ft.Column([
            ft.Text("Scan Simulator", size=22, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            ft.Text(t["input_area"], color=ft.Colors.WHITE, size=14),
            jan_input,
            ft.Button(
                content=ft.Text(t["search_btn"], color=ft.Colors.WHITE),
                on_click=lambda _: on_search(jan_input.value),
                width=float("inf"),
                style=ft.ButtonStyle(bgcolor=BRAND_GREEN)
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    )

def get_history_content(lang, history_list, on_clear):
    t = LANG_TEXTS[lang]
    
    cards = []
    for item in history_list:
        cards.append(
            ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Row([
                        ft.Image(src=item['image_path'], width=50, height=50, fit=ft.ImageFit.CONTAIN),
                        ft.Column([
                            ft.Text(item['product_name'], size=14, weight=ft.FontWeight.BOLD, color="#262626"),
                            ft.Text(item['item_usage'], size=12, color=ft.Colors.RED_600),
                            ft.Text(item['scan_time'], size=10, color="#888888")
                        ], expand=True)
                    ])
                )
            )
        )
        
    if not cards:
        cards.append(ft.Container(content=ft.Text(t["no_history"], color="#262626"), alignment="center", padding=20))

    return ft.Container(
        bgcolor=LIGHT_GRAY,
        padding=10,
        content=ft.Column([
            ft.Row([
                ft.Text(t["title_history"], size=22, weight=ft.FontWeight.BOLD, color="#262626"),
                ft.TextButton(content=ft.Text(t["clear_history"], color=ft.Colors.RED), on_click=on_clear)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Column(cards, scroll=ft.ScrollMode.AUTO, expand=True)
        ], expand=True)
    )

def get_settings_content(lang, on_toggle_lang):
    t = LANG_TEXTS[lang]
    return ft.Container(
        bgcolor=LIGHT_GRAY,
        content=ft.Column([
            ft.Container(content=ft.Text(t["title_settings"], color=ft.Colors.WHITE, size=20, weight=ft.FontWeight.BOLD), bgcolor=BRAND_GREEN, height=65, alignment="center"),
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Container(
                        bgcolor=ft.Colors.WHITE,
                        border_radius=15,
                        padding=20,
                        content=ft.Column([
                            ft.Row([ft.Text("🏠", size=20), ft.Text(t["lang_setting"], size=17, weight=ft.FontWeight.BOLD, color="#262626")], spacing=10),
                            ft.Text(t["lang_desc"], size=12, color="#888888"),
                            ft.Row([
                                ft.Text("日本語", size=16, weight=ft.FontWeight.BOLD if lang == "ja" else ft.FontWeight.NORMAL, color=BRAND_GREEN if lang == "ja" else "#999999"),
                                ft.Switch(value=(lang == "en"), active_track_color=BRAND_GREEN, on_change=lambda e: on_toggle_lang(e.control.value)),
                                ft.Text("English", size=16, weight=ft.FontWeight.BOLD if lang == "en" else ft.FontWeight.NORMAL, color=BRAND_GREEN if lang == "en" else "#999999"),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
                        ], spacing=10)
                    )
                ])
            )
        ], spacing=0), expand=True
    )

async def main(page: ft.Page):
    page.title = "Boycott App"
    page.padding = 0
    page.window_width = 400
    page.window_height = 800

    state = {
        "current_screen": "main",
        "lang": "ja",
        "selected_category": None,
        "history": [],
        "all_products_cache": []  # リスト表示高速化＆タスク破棄防止用のキャッシュ
    }

    main_content_area = ft.Container(expand=True)
    bottom_bar_container = ft.Container()
    app_layout = ft.Column([main_content_area, bottom_bar_container], spacing=0, expand=True)

    async def handle_barcode_search_async(jan_code):
        if not jan_code:
            return
        t = LANG_TEXTS[state["lang"]]
        
        loading_dialog = ft.AlertDialog(title=ft.Text(t["searching"]), open=True)
        page.overlay.append(loading_dialog)
        page.update()

        result = await connect_sheet_async(jan_code)
        
        loading_dialog.open = False
        page.update()

        if not result:
            page.overlay.append(ft.AlertDialog(title=ft.Text(t["not_registered"]), content=ft.Text(f"JAN: {jan_code}"), open=True))
        else:
            display_area = get_translated_name(state["lang"], result.get("area", ""))
            display_item = get_translated_name(state["lang"], result.get("item", ""))
            area_text = t["area_label"].format(display_area) if display_area else ""
            msg = t["item_usage_label"].format(area_text, display_item)
            img_path = result.get("image_path") or "https://via.placeholder.com/150"

            now = datetime.now().strftime('%Y/%m/%d %H:%M')
            new_entry = {
                'product_name': str(result.get("product_name")),
                'item_usage': msg,
                'image_path': img_path,
                'scan_time': now
            }
            state["history"].insert(0, new_entry)

            page.overlay.append(ft.AlertDialog(
                title=ft.Text(result.get("product_name")),
                content=ft.Column([
                    ft.Image(src=img_path, width=100, height=100),
                    ft.Text(f"{t['company']}: {result.get('company_name')}"),
                    ft.Text(msg, color=ft.Colors.RED_600, weight=ft.FontWeight.BOLD)
                ], compact=True, height=200),
                open=True
            ))
        await refresh_ui_async()

    async def handle_category_select_async(category_id):
        state["selected_category"] = category_id
        state["current_screen"] = "list_widget"
        # リスト画面へ切り替えるタイミングで非同期のDB一括取得を行う
        state["all_products_cache"] = await connect_sheet_all_async()
        await refresh_ui_async()

    async def handle_clear_history_async(e):
        state["history"] = []
        await refresh_ui_async()

    async def refresh_ui_async():
        target = state["current_screen"]
        lang = state["lang"]

        if target == "main":
            main_content_area.content = get_main_content(lang)
        elif target == "itemtype_widget":
            main_content_area.content = get_itemtype_content(lang, lambda cid: page.run_task(handle_category_select_async, cid))
        elif target == "list_widget":
            # タスク中断を避けるため、描画関数自体は同期関数にし、データは事前にキャッシュされたものを渡す
            main_content_area.content = get_list_widget_content(lang, state["selected_category"], state["all_products_cache"])
        elif target == "scan_widget":
            main_content_area.content = get_scan_content(lang, lambda jan: page.run_task(handle_barcode_search_async, jan))
        elif target == "history_widget":
            main_content_area.content = get_history_content(lang, state["history"], lambda e: page.run_task(handle_clear_history_async, e))
        elif target == "settings_widget":
            main_content_area.content = get_settings_content(lang, lambda val: page.run_task(toggle_language_async, val))

        bottom_bar_container.content = BottomMenuBar(
            current_screen=target,
            on_change_screen=lambda tgt: page.run_task(change_screen_async, tgt),
            lang=lang
        )
        page.update()

    async def change_screen_async(target_name):
        state["current_screen"] = target_name
        await refresh_ui_async()

    async def toggle_language_async(is_english):
        state["lang"] = "en" if is_english else "ja"
        await refresh_ui_async()

    page.add(app_layout)
    await refresh_ui_async()

ft.run(main)
