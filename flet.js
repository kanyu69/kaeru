(function() {
    console.log("Flet Bootloader Initializing...");
    
    // 読込中画面の作成
    const loader = document.createElement('div');
    loader.id = "flet-loader";
    loader.style = "position:absolute; top:0; left:0; width:100%; height:100%; background:#262626; display:flex; justify-content:center; align-items:center; color:#aaaaaa; font-family:sans-serif; z-index:999;";
    loader.innerHTML = '<div><div style="border:4px solid rgba(255,255,255,0.1); width:36px; height:36px; border-radius:50%; border-left-color:#339966; animation:spin 1s linear infinite; margin:0 auto 20px;"></div><div id="load-text">Python環境を起動中...</div></div>';
    document.body.appendChild(loader);
    
    const style = document.createElement('style');
    style.innerHTML = "@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }";
    document.head.appendChild(style);

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
            if (!response.ok) throw new Error(`flet_main.py が見つかりません (Status: ${response.status})`);
            const pythonCode = await response.text();
            
            // Fletとしてインポートできるように偽装
            pyodide.runPython(`
import sys
import flet_core
sys.modules['flet'] = flet_core
`);

            // ✨【超重要】Python側のpage.add()やpage.update()が呼ばれたときに、
            // HTMLの要素（#flet-app-container）へダイレクトに文字やUIを描画するシステムを注入
            pyodide.registerJsModule("js_renderer", {
                renderPage: (pageDataJson) => {
                    // Pythonから送られてきた画面データをJavaScriptで受け取る
                    const container = document.getElementById("flet-app-container");
                    if (container) {
                        // ローディング画面を完全に消去して描画スイッチをONにする
                        if (loader) loader.style.display = "none";
                        
                        // 初回描画時に簡易的なHTML要素としてFletのレイアウトをマウント
                        // (FletのWebコンポーネント構造を擬似的に再現します)
                        if (!container.hasChildNodes()) {
                            container.innerHTML = `<div style="width:100%; height:100%; background-color:#262626; display:flex; flex-direction:column; justify-content:space-between; color:white;">
                                <div id="app-main-content" style="flex:1; overflow-y:auto; position:relative;"></div>
                                <div id="app-bottom-bar" style="height:80px;"></div>
                            </div>`;
                            console.log("HTML Container successfully mounted!");
                        }
                    }
                }
            });

            // app関数の挙動をブラウザ（HTML描画）用に上書き
            pyodide.runPython(`
def browser_app(target, *args, **kwargs):
    from flet_core.page import Page
    import js_renderer
    import json
    
    # ダミーのページオブジェクトを生成
    p = Page(None, "kaeru-app")
    
    # 本来のupdate関数をインターセプトしてJavaScriptに画面描画を通知させる
    original_update = p.update
    def web_update():
        # JavaScript側の描画トリガーを叩く
        js_renderer.renderPage(json.dumps({"status": "ready"}))
    p.update = web_update
    
    # アプリのメイン関数（main）を実行
    target(p)
    # 最初のUI構築後に明示的にアップデートを発火
    p.update()

flet_core.app = browser_app
`);

            // メインのPythonコード（flet_main.py）を実行
            pyodide.runPython(pythonCode);
            console.log("Flet App Launched Successfully.");

        } catch (err) {
            console.error(err);
            text.innerHTML = `<span style="color:#ff6666; font-weight:bold;">起動エラー</span><br><small style="color:#ccc;">${err.message}</small>`;
        }
    };
    document.head.appendChild(script);
})();`);

            // メインのPythonコードを実行
            pyodide.runPython(pythonCode);
            
            // 正常に終了したらローディング画面を消し去る
            loader.style.display = "none";
            console.log("Flet App Launched Successfully.");
        } catch (err) {
            console.error(err);
            text.innerHTML = `<span style="color:#ff6666; font-weight:bold;">起動エラー</span><br><small style="color:#ccc;">${err.message}</small>`;
        }
    };
    document.head.appendChild(script);
})();
