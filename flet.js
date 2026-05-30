(function() {
    console.log("Flet Bootloader Initializing...");
    
    // 読込中画面の作成
    const loader = document.createElement('div');
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
            // ✨ 確実に同じフォルダから取得するために「./」を付与
            const response = await fetch('./flet_main.py');
            if (!response.ok) throw new Error(`flet_main.py が見つかりません (Status: ${response.status})`);
            const pythonCode = await response.text();
            
            // Fletの偽装と実行
            pyodide.runPython(`
import sys
import flet_core
sys.modules['flet'] = flet_core
` + pythonCode);
            
            // 成功したらローディングを消す
            loader.style.display = "none";
        } catch (err) {
            console.error(err);
            text.innerHTML = `<span style="color:#ff6666; font-weight:bold;">起動エラー</span><br><small style="color:#ccc;">${err.message}</small>`;
        }
    };
    document.head.appendChild(script);
})();
