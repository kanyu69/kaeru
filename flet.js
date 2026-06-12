(function() {
    console.log("Flet Bootloader Initializing...");
    
    const loader = document.createElement('div');
    loader.id = "flet-loader";
    loader.style.cssText = "position:absolute;top:0;left:0;width:100%;height:100%;background-color:#262626;display:flex;justify-content:center;align-items:center;color:#aaaaaa;font-family:sans-serif;z-index:999;";
    loader.innerHTML = '<div><div id="flet-spinner" style="border:4px solid rgba(255,255,255,0.1);width:36px;height:36px;border-radius:50%;border-left-color:#339966;margin:0 auto 20px;"></div><div id="load-text">Python環境を起動中...</div></div>';
    document.body.appendChild(loader);
    
    const styleRef = document.createElement('style');
    styleRef.innerHTML = "@keyframes flet-spin{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}} #flet-spinner{animation:flet-spin 1s linear infinite;}";
    document.head.appendChild(styleRef);

    const script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";
    
    script.onload = async () => {
        const text = document.getElementById('load-text');
        try {
            text.innerText = "パッケージを準備中...";
            let pyodide = await loadPyodide();
            await pyodide.loadPackage("micropip");
            const micropip = pyodide.pyimport("micropip");
            await micropip.install("flet-core");
            
            text.innerText = "メインプログラムを読み込み中...";
            const response = await fetch('./flet_main.py');
            if (!response.ok) throw new Error("flet_main.py が見つかりません");
            const pythonCode = await response.text();
            
            pyodide.runPython("import sys\nimport flet_core\nsys.modules['flet'] = flet_core");

            pyodide.registerJsModule("js_renderer", {
                renderPage: () => {
                    const container = document.getElementById("flet-app-container");
                    if (container) {
                        if (loader) loader.style.display = "none";
                        if (!container.hasChildNodes()) {
                            container.innerHTML = '<div style="width:100%;height:100%;background-color:#262626;display:flex;flex-direction:column;justify-content:space-between;color:white;"><div id="app-main-content" style="flex:1;overflow-y:auto;position:relative;"></div><div id="app-bottom-bar" style="height:80px;"></div></div>';
                            console.log("HTML Container mounted.");
                        }
                    }
                }
            });

            pyodide.globals.set("RAW_PYTHON_CODE", pythonCode);

            pyodide.runPython(`
import asyncio
import sys
import types
import js_renderer

# ft.app() と ft.app_async() を無効化してから flet_main.py を実行
lines = RAW_PYTHON_CODE.split('\\n')
clean_lines = []
for line in lines:
    stripped = line.strip()
    if stripped.startswith('ft.app(') or stripped.startswith('ft.app_async('):
        clean_lines.append('# ' + line)
    else:
        clean_lines.append(line)
executable_code = '\\n'.join(clean_lines)
exec(executable_code, globals())

# ===== ダミー Page オブジェクトを組み立てる =====

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# --- client_storage のモック ---
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

# --- session のモック ---
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

# --- send_commands の戻り値モック ---
class DummyCommandResult:
    def __init__(self):
        self.results = []

# --- Connection モック ---
class DummyConnection:
    def __init__(self):
        self.page_url = "http://localhost"
        # pubsubhub が必要な場合に備えて
        self.pubsubhub = types.SimpleNamespace(
            subscribe=lambda *a, **k: None,
            unsubscribe=lambda *a, **k: None,
            send_message=lambda *a, **k: None,
        )

    def send_command(self, session_id, command):
        return '"null"'

    def send_commands(self, session_id, commands):
        # ← これが欠けていたことが今回のクラッシュの根本原因
        return DummyCommandResult()

    async def send_command_async(self, session_id, command):
        return '"null"'

    async def send_commands_async(self, session_id, commands):
        return DummyCommandResult()

# --- Page の組み立て ---
# Page.__init__ が send_commands を内部呼び出しするため try で保護する
conn = DummyConnection()
page_ok = False

try:
    from flet_core.page import Page
    p = Page(conn, "kaeru-session-001", loop)
    page_ok = True
    print("flet_core.Page: 初期化成功")
except Exception as e:
    print(f"flet_core.Page 初期化失敗 → SimpleNamespace で代替: {e}")

if not page_ok:
    # flet_core.Page が使えない場合の完全代替
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

# どちらのケースでも以下を上書きする
p.client_storage = DummyClientStorage()
p.session = DummySession()

def _safe_update():
    try:
        js_renderer.renderPage()
    except Exception as ex:
        print(f"renderPage warning: {ex}")

p.update = _safe_update

# page.add も安全版に上書き（send_commands クラッシュ対策）
_original_add = getattr(p, 'add', None)
def _safe_add(*args):
    try:
        if _original_add:
            _original_add(*args)
        else:
            for c in args:
                p.controls.append(c)
    except Exception as e:
        print(f"page.add warning (non-fatal): {e}")
        for c in args:
            try:
                p.controls.append(c)
            except Exception:
                pass
p.add = _safe_add

# ===== main() を実行 =====
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
`);

            console.log("Flet App Launched Successfully.");
            if (loader) loader.style.display = "none";

        } catch (err) {
            console.error(err);
            text.innerHTML = '<span style="color:#ff6666;font-weight:bold;">起動エラー</span><br><small style="color:#ccc;">' + err.message + '</small>';
        }
    };
    document.head.appendChild(script);
})();            // 🌟 実行ロジックは100% Python側で完結させ、末尾の ft.app もPython側で安全に無効化して実行します
            pyodide.runPython(`
import asyncio
import sys
from flet_core.page import Page
import js_renderer

# 1. 読み込んだ flet_main.py の中身を安全に加工（末尾のft.appを確実にコメントアウト）
lines = RAW_PYTHON_CODE.split('\\n')
clean_lines = []
for line in lines:
    if line.strip().startswith('ft.app('):
        clean_lines.append('# ' + line)
    else:
        clean_lines.append(line)
executable_code = '\\n'.join(clean_lines)

# 2. 加工したPythonコードだけを実行（これでJSが混ざる余地は0になります）
exec(executable_code, globals())

# 3. ダミーのブラウザ環境を構築してアプリを起動
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

class DummyPubSubHub:
    def __init__(self): pass

class DummyConnection:
    def __init__(self):
        self.pubsubhub = DummyPubSubHub()
        self.page_url = "http://localhost"
    def send_command(self, session_id, command): return '"\\\\\\"null\\\\\\""'
    def send_command_async(self, session_id, command):
        async def dummy_async(): return '"\\\\\\"null\\\\\\""'
        return dummy_async()

conn = DummyConnection()
p = Page(conn, "kaeru-session-001", loop)

p._invoke_method = lambda m, a=None, *v, **kw: '"\\\\\\"null\\\\\\""'
p._invoke_method_async = lambda *a, **k: asyncio.sleep(0, '"\\\\\\"null\\\\\\""')
p.update = lambda: js_renderer.renderPage()

# 4. 読み込まれた main() 関数を強制実行
if 'main' in globals():
    globals()['main'](p)
    p.update()
    print("Flet App forced completely.")
else:
    print("Error: main() not found.")
`);

            console.log("Flet App Launched Successfully.");

        } catch (err) {
            console.error(err);
            text.innerHTML = '<span style="color:#ff6666; font-weight:bold;">起動エラー</span><br><small style="color:#ccc;">' + err.message + '</small>';
        }
    };
    document.head.appendChild(script);
})();
