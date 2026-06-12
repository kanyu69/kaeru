import asyncio
import sys
import types
import js_renderer

sys.path.insert(0, '/tmp')

_storage_dict = {}

class DummyClientStorage:
    def get(self, key):
        return _storage_dict.get(key, None)
    def set(self, key, value):
        _storage_dict[key] = value
    def remove(self, key):
        _storage_dict.pop(key, None)
    def contains_key(self, key):
        return key in _storage_dict

_session_dict = {}

class DummySession:
    def get(self, key):
        return _session_dict.get(key, None)
    def set(self, key, value):
        _session_dict[key] = value
    def remove(self, key):
        _session_dict.pop(key, None)
    def contains_key(self, key):
        return key in _session_dict

class MockPage:
    def __init__(self):
        self.title = ""
        self.padding = 0
        self.spacing = 0
        self.bgcolor = None
        self.theme_mode = None
        self.fonts = {}
        self.horizontal_alignment = None
        self.vertical_alignment = None
        self.scroll = None
        self.window_width = 400
        self.window_height = 800
        self.controls = []
        self.overlay = []
        self.views = []
        self.route = "/"
        self.snack_bar = None
        self.dialog = None
        self.bottom_sheet = None
        self.navigation_bar = None
        self.appbar = None
        self.floating_action_button = None
        self.on_route_change = None
        self.on_view_pop = None
        self.on_keyboard_event = None
        self.on_resize = None
        self.on_connect = None
        self.on_disconnect = None
        self.on_close = None
        self.theme = None
        self.dark_theme = None
        self.rtl = False
        self.width = 400
        self.height = 800
        self.client_storage = DummyClientStorage()
        self.session = DummySession()

    def update(self):
        try:
            js_renderer.renderPage()
        except Exception as ex:
            print("renderPage warning: " + str(ex))

    def add(self, *controls):
        for c in controls:
            self.controls.append(c)

    def remove(self, *controls):
        for c in controls:
            if c in self.controls:
                self.controls.remove(c)

    def go(self, route):
        self.route = route

    def get_upload_url(self, *a, **k):
        return ""

    def set_clipboard(self, value):
        pass

    def launch_url(self, url, *a, **k):
        pass

    def show_snack_bar(self, snack_bar):
        self.snack_bar = snack_bar

    def close_dialog(self):
        self.dialog = None

    def open_dialog(self, dialog):
        self.dialog = dialog

    def show_bottom_sheet(self, bottom_sheet):
        self.bottom_sheet = bottom_sheet

    def close_bottom_sheet(self):
        self.bottom_sheet = None

import importlib
app_module = importlib.import_module('flet_main_app')

p = MockPage()

if hasattr(app_module, 'main'):
    try:
        app_module.main(p)
        print("main() completed")
    except Exception as e:
        print("main() error: " + str(e))
        import traceback
        traceback.print_exc()
    p.update()
    print("Flet App launched.")
else:
    print("Error: main() not found")        self.on_route_change = None
        self.on_view_pop = None
        self.on_keyboard_event = None
        self.on_resize = None
        self.on_connect = None
        self.on_disconnect = None
        self.on_close = None
        self.theme = None
        self.dark_theme = None
        self.rtl = False
        self.width = 400
        self.height = 800
        self.client_storage = DummyClientStorage()
        self.session = DummySession()

    def update(self):
        try:
            js_renderer.renderPage()
        except Exception as ex:
            print("renderPage warning: " + str(ex))

    def add(self, *controls):
        for c in controls:
            self.controls.append(c)

    def remove(self, *controls):
        for c in controls:
            if c in self.controls:
                self.controls.remove(c)

    def go(self, route):
        self.route = route

    def get_upload_url(self, *a, **k):
        return ""

    def set_clipboard(self, value):
        pass

    def launch_url(self, url, *a, **k):
        pass

    def show_snack_bar(self, snack_bar):
        self.snack_bar = snack_bar

    def close_dialog(self):
        self.dialog = None

    def open_dialog(self, dialog):
        self.dialog = dialog

    def show_bottom_sheet(self, bottom_sheet):
        self.bottom_sheet = bottom_sheet

    def close_bottom_sheet(self):
        self.bottom_sheet = None

import importlib
app_module = importlib.import_module('flet_main_app')

p = MockPage()

if hasattr(app_module, 'main'):
    try:
        app_module.main(p)
        print("main() completed")
    except Exception as e:
        print("main() error: " + str(e))
        import traceback
        traceback.print_exc()
    p.update()
    print("Flet App launched.")
else:
    print("Error: main() not found")        self.on_route_change = None
        self.on_view_pop = None
        self.on_keyboard_event = None
        self.on_resize = None
        self.on_connect = None
        self.on_disconnect = None
        self.on_close = None
        self.theme = None
        self.dark_theme = None
        self.rtl = False
        self.width = 400
        self.height = 800
        self.client_storage = DummyClientStorage()
        self.session = DummySession()

    def update(self):
        try:
            js_renderer.renderPage()
        except Exception as ex:
            print("renderPage warning: " + str(ex))

    def add(self, *controls):
        for c in controls:
            self.controls.append(c)

    def remove(self, *controls):
        for c in controls:
            if c in self.controls:
                self.controls.remove(c)

    def go(self, route):
        self.route = route

    def get_upload_url(self, *a, **k):
        return ""

    def set_clipboard(self, value):
        pass

    def launch_url(self, url, *a, **k):
        pass

    def show_snack_bar(self, snack_bar):
        self.snack_bar = snack_bar

    def close_dialog(self):
        self.dialog = None

    def open_dialog(self, dialog):
        self.dialog = dialog

    def show_bottom_sheet(self, bottom_sheet):
        self.bottom_sheet = bottom_sheet

    def close_bottom_sheet(self):
        self.bottom_sheet = None

import importlib
app_module = importlib.import_module('flet_main_app')

p = MockPage()

if hasattr(app_module, 'main'):
    try:
        app_module.main(p)
        print("main() completed")
    except Exception as e:
        print("main() error: " + str(e))
        import traceback
        traceback.print_exc()
    p.update()
    print("Flet App launched.")
else:
    print("Error: main() not found")        self.on_keyboard_event = None
        self.on_resize = None
        self.on_connect = None
        self.on_disconnect = None
        self.on_close = None
        self.theme = None
        self.dark_theme = None
        self.rtl = False
        self.width = 400
        self.height = 800
        self.client_storage = DummyClientStorage()
        self.session = DummySession()

    def update(self):
        try:
            js_renderer.renderPage()
        except Exception as ex:
            print("renderPage warning: " + str(ex))

    def add(self, *controls):
        for c in controls:
            self.controls.append(c)

    def remove(self, *controls):
        for c in controls:
            if c in self.controls:
                self.controls.remove(c)

    def go(self, route):
        self.route = route

    def get_upload_url(self, *a, **k):
        return ""

    def set_clipboard(self, value):
        pass

    def launch_url(self, url, *a, **k):
        pass

    def show_snack_bar(self, snack_bar):
        self.snack_bar = snack_bar

    def close_dialog(self):
        self.dialog = None

    def open_dialog(self, dialog):
        self.dialog = dialog

    def show_bottom_sheet(self, bottom_sheet):
        self.bottom_sheet = bottom_sheet

    def close_bottom_sheet(self):
        self.bottom_sheet = None

p = MockPage()

if 'main' in globals():
    try:
        globals()['main'](p)
        print("main() completed")
    except Exception as e:
        print("main() error: " + str(e))
        import traceback
        traceback.print_exc()
    p.update()
    print("Flet App launched.")
else:
    print("Error: main() not found")        return '"null"'

    async def send_commands_async(self, session_id, commands):
        return DummyCommandResult()

# --- loop ---
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# --- Page 初期化 ---
conn = DummyConnection()

from flet_core.page import Page
p = Page(conn, "kaeru-session-001", loop)

# client_storage と session はプロパティ(setter なし)なので
# インスタンスの __dict__ に直接書き込んでプロパティを隠蔽する
dummy_storage = DummyClientStorage()
dummy_session = DummySession()
object.__setattr__(p, '_Page__client_storage', dummy_storage)
object.__setattr__(p, '_Page__session', dummy_session)

# __dict__ に直接差し込む（上記で届かない場合の保険）
try:
    p.__dict__['client_storage'] = dummy_storage
except Exception:
    pass
try:
    p.__dict__['session'] = dummy_session
except Exception:
    pass

# プロパティ自体をクラスレベルで差し替える（最終手段）
try:
    Page.client_storage = property(lambda self: dummy_storage)
    Page.session = property(lambda self: dummy_session)
    print("Page.client_storage / session: クラスレベルで差し替え成功")
except Exception as e:
    print(f"クラスレベル差し替え失敗: {e}")

# update と add を安全版に上書き
def _safe_update():
    try:
        js_renderer.renderPage()
    except Exception as ex:
        print(f"renderPage warning: {ex}")

p.update = _safe_update

_original_add = getattr(p, 'add', None)
def _safe_add(*args):
    try:
        if _original_add:
            _original_add(*args)
        else:
            for c in args:
                p.controls.append(c)
    except Exception as e:
        print(f"page.add warning: {e}")
        for c in args:
            try:
                p.controls.append(c)
            except Exception:
                pass
p.add = _safe_add

# --- main() 実行 ---
if 'main' in globals():
    try:
        globals()['main'](p)
        print("main() 実行完了")
    except Exception as e:
        print(f"main() 実行エラー: {e}")
        import traceback
        traceback.print_exc()
    p.update()
    print("Flet App launched.")
else:
    print("Error: main() が見つかりません")        return '"null"'

    async def send_commands_async(self, session_id, commands):
        return DummyCommandResult()

# --- loop ---
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# --- Page 初期化 ---
conn = DummyConnection()
page_ok = False

try:
    from flet_core.page import Page
    p = Page(conn, "kaeru-session-001", loop)
    page_ok = True
    print("flet_core.Page: 初期化成功")
except Exception as e:
    print(f"flet_core.Page 初期化失敗 -> SimpleNamespace で代替: {e}")

if not page_ok:
    p = types.SimpleNamespace()
    p.controls = []
    p.overlay = []
    p.views = []
    p.route = "/"
    p.title = ""
    p.padding = 0
    p.spacing = 0
    p.bgcolor = None
    p.theme_mode = None
    p.fonts = {}
    p.horizontal_alignment = None
    p.vertical_alignment = None
    p.scroll = None
    p.window_width = 400
    p.window_height = 800
    p.snack_bar = None
    p.dialog = None
    p.bottom_sheet = None
    p.navigation_bar = None
    p.appbar = None
    p.floating_action_button = None
    p.on_route_change = None
    p.on_view_pop = None
    p.go = lambda route: None

    def _page_add(*args):
        for c in args:
            p.controls.append(c)
    p.add = _page_add

# どちらのケースでも上書き
p.client_storage = DummyClientStorage()
p.session = DummySession()

def _safe_update():
    try:
        js_renderer.renderPage()
    except Exception as ex:
        print(f"renderPage warning: {ex}")

p.update = _safe_update

_original_add = getattr(p, 'add', None)
def _safe_add(*args):
    try:
        if _original_add:
            _original_add(*args)
        else:
            for c in args:
                p.controls.append(c)
    except Exception as e:
        print(f"page.add warning: {e}")
        for c in args:
            try:
                p.controls.append(c)
            except Exception:
                pass
p.add = _safe_add

# --- main() 実行 ---
if 'main' in globals():
    try:
        globals()['main'](p)
        print("main() 実行完了")
    except Exception as e:
        print(f"main() 実行エラー: {e}")
        import traceback
        traceback.print_exc()
    p.update()
    print("Flet App launched.")
else:
    print("Error: main() が見つかりません")
