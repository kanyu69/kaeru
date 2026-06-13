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
            const [mainRes, bootRes] = await Promise.all([fetch('./flet_main.py'), fetch('./boot.py')]);
            if (!mainRes.ok) throw new Error("flet_main.py が見つかりません");
            if (!bootRes.ok) throw new Error("boot.py が見つかりません");
            const pythonCode = await mainRes.text();
            const bootCode = await bootRes.text();
            pyodide.runPython("import sys, flet_core; sys.modules['flet'] = flet_core");
            pyodide.registerJsModule("js_renderer", {
                renderPage: () => {
                    const container = document.getElementById("flet-app-container");
                    if (container) {
                        loader.style.display = "none";
                        if (!container.hasChildNodes()) {
                            container.innerHTML = '<div style="width:100%;height:100%;background-color:#262626;display:flex;flex-direction:column;color:white;"><div id="app-main-content" style="flex:1;overflow-y:auto;"></div><div id="app-bottom-bar" style="height:80px;"></div></div>';
                        }
                    }
                }
            });
            pyodide.FS.writeFile("/tmp/flet_main_app.py", pythonCode);
            pyodide.FS.writeFile("/tmp/boot_runner.py", bootCode);
            pyodide.runPython("import runpy; runpy.run_path('/tmp/boot_runner.py', run_name='__main__')");
        } catch (err) {
            console.error(err);
            text.innerHTML = '<span style="color:#ff6666;font-weight:bold;">起動エラー</span><br><small>' + err.message + '</small>';
        }
    };
    document.head.appendChild(script);
})();    def show_snack_bar(self, s): self.snack_bar = s
    def close_dialog(self): self.dialog = None
    def open_dialog(self, d): self.dialog = d
    def show_bottom_sheet(self, b): self.bottom_sheet = b
    def close_bottom_sheet(self): self.bottom_sheet = None

import importlib
app_module = importlib.import_module("flet_main_app")
p = MockPage()
if hasattr(app_module, "main"):
    try:
        app_module.main(p)
        print("main() completed")
    except Exception as e:
        import traceback
        traceback.print_exc()
    p.update()
    print("Flet App launched.")
else:
    print("Error: main() not found")
    document.head.appendChild(script);
})();
