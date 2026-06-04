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
            
            // Fletとしてインポートできるように偽装
            pyodide.runPython("import sys\nimport flet_core\nsys.modules['flet'] = flet_core");

            // Python側の画面更新トリガーをJavaScriptでキャッチするモジュール
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

            // app関数の挙動をブラウザ環境用にオーバーライド（Connectionダミー完全版）
            pyodide.runPython(`
def browser_app(target, *args, **kwargs):
    from flet_core.page import Page
    import js_renderer
    import asyncio
    
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    # ✨ 'NoneType' エラーを防ぐため、Pageクラスが内部で要求する最低限のプロパティを持ったダミーオブジェクトを生成
    class DummyPubSubHub:
        def __init__(self):
            pass
            
    class DummyConnection:
        def __init__(self):
            self.pubsubhub = DummyPubSubHub()
            self.page_url = "http://localhost"
            
        def send_command(self, session_id, command):
            # コマンド送信をエミュレート（エラーを防ぐ）
            pass
            
    # 作成したダミーConnectionを第一引数に引き渡します
    conn = DummyConnection()
    p = Page(conn, "kaeru-session-001", loop)
    
    def web_update():
        js_renderer.renderPage()
    p.update = web_update
    
    target(p)
    p.update()

flet_core.app = browser_app
`);

            // メインのPythonコードを実行
            pyodide.runPython(pythonCode);
            console.log("Flet App Launched Successfully.");

        } catch (err) {
            console.error(err);
            text.innerHTML = '<span style="color:#ff6666; font-weight:bold;">起動エラー</span><br><small style="color:#ccc;">' + err.message + '</small>';
        }
    };
    document.head.appendChild(script);
})();
