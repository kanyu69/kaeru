(function() {
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
            const mainRes = await fetch('./flet_main.py');
            if (!mainRes.ok) throw new Error("flet_main.py が見つかりません");
            const pythonCode = await mainRes.text();
            pyodide.runPython("import sys, flet_core; sys.modules['flet'] = flet_core");
            pyodide.registerJsModule("js_renderer", {
                renderPage: () => {
                    const container = document.getElementById("flet-app-container");
                    if (container) {
                        loader.style.display = "none";
                    }
                }
            });
            pyodide.FS.writeFile("/tmp/flet_main_app.py", pythonCode);
            pyodide.runPython([
                "import sys, js_renderer",
                "sys.path.insert(0, '/tmp')",
                "_sd = {}",
                "class CS:",
                "    def get(self, k): return _sd.get(k)",
                "    def set(self, k, v): _sd.__setitem__(k, v)",
                "    def remove(self, k): _sd.pop(k, None)",
                "    def contains_key(self, k): return k in
