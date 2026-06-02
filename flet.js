(function() {
    console.log("Flet Bootloader Initializing...");
    
    // ローディング画面の作成
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
            
            // ✨ 存在しない runtime モジュールを排除し、シンプルなダミー関数でラップして実行します
            pyodide.runPython(`
import sys
import flet_core

# flet としてインポートできるように偽装
sys.modules['flet'] = flet_core

# エラーの原因だったruntimeのダミーを安全に作成
from types import ModuleType
runtime_dummy = ModuleType("runtime")
flet_core.runtime = runtime_dummy
sys.modules['flet_core.runtime'] = runtime_dummy

# app関数の挙動をブラウザ環境用に上書き
def browser_app(target, *args, **kwargs):
    # Flet Web環境用の内部初期化処理
    from flet_core.page import Page
    import asyncio
    
    async def bootstrap():
        # 擬似的なページオブジェクトを生成してアプリのメインを走らせる
        p = Page(None, "kaeru-app")
        target(p)
        
    try:
        # 既にイベントループがある場合はそれを利用、なければ新規実行
        loop = asyncio.get_running_loop()
        loop.create_task(bootstrap())
    except RuntimeError:
        asyncio.run(bootstrap())

flet_core.app = browser_app
flet_core.app_async = browser_app
`);

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
