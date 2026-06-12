import asyncio
import sys
import types
import js_renderer

# ft.app() を無効化して flet_main.py を実行
lines = RAW_PYTHON_CODE.split('\n')
clean_lines = []
for line in lines:
    stripped = line.strip()
    if stripped.startswith('ft.app(') or stripped.startswith('ft.app_async('):
        clean_lines.append('# ' + line)
    else:
        clean_lines.append(line)
executable_code = '\n'.join(clean_lines)
exec(executable_code, globals())

# --- client_storage モック ---
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

# --- session モック ---
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

# --- send_commands 戻り値モック ---
class DummyCommandResult:
    def __init__(self):
        self.results = []

# --- Connection モック ---
class DummyConnection:
    def __init__(self):
        self.page_url = "http://localhost"
        self.pubsubhub = types.SimpleNamespace(
            subscribe=lambda *a, **k: None,
            unsubscribe=lambda *a, **k: None,
            send_message=lambda *a, **k: None,
        )

    def send_command(self, session_id, command):
        return '"null"'

    def send_commands(self, session_id, commands):
        return DummyCommandResult()

    async def send_command_async(self, session_id, command):
        return '"null"'

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
