(function() {
    console.log("Flet Bootloader Initializing...");
    
    // 1. ローディング画面の作成
    const loader = document.createElement('div');
    loader.id = "flet-loader";
    loader.style.position = "absolute";
    loader.style.top = "0";
    loader.style.left = "0";
    loader.style.width = "100%";
    loader.style.height = "100%";
    loader.style.backgroundColor = "#262626";
    loader.style.display = "flex";
    loader.style.justifyContent = "center";
    loader.style.alignItems = "center";
    loader.style.color = "#aaaaaa";
    loader.style.fontFamily = "sans-serif";
    loader.style.zIndex = "999";
    loader.innerHTML = '<div><div id="flet-spinner" style="border:4px solid rgba(255,255,255,0.1); width:36px; height:36px; border-radius:50%; border-left-color:#339966; margin:0 auto 20px;"></div><div id="load-text">Python環境を起動中...</div></div>';
    document.body.appendChild(loader);
    
    // アニメーション用スタイルの追加
    const styleRef = document.createElement('style');
    styleRef.type = 'text/css';
    styleRef.innerHTML = "@keyframes flet-spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } } #flet-spinner { animation: flet-spin 1s linear infinite; }";
    document.head.appendChild(styleRef);

    // 2. Pyodideスクリプトの動的読み込み
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
            
            // Flet環境のモジュール偽装
            pyodide.runPython("import sys\nimport flet_core\nsys.modules['flet'] = flet_core");

            // Python側からの描画を受け取るJSモジュール
            pyodide.registerJsModule("js_renderer", {
                renderPage: () => {
                    const container = document.getElementById("flet-app-container");
                    if (container) {
                        if (loader) loader.style.display = "none";
                        if (!container.hasChildNodes()) {
                            container.innerHTML = '<div style="width:100%; height:100%; background-color:#262626; display:flex; flex-direction:column; justify-content:space-between; color:white;"><div id="app-main-content" style="flex:1; overflow-y:auto; position:relative;"></div><div id="app-bottom-bar" style="height:80px;"></div></div>';
                            console.log("HTML Container mounted.");
                        }
                    }
                }
            });

            // 🌟 事故を防ぐため、fetchしたコードをグローバル変数に「ただの文字列」として安全に格納します
            pyodide.globals.set("RAW_PYTHON_CODE", pythonCode);

            // 🌟 実行ロジックは100% Python側で完結させ、末尾の ft.app もPython側で安全に無効化して実行します
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
