// Flet Web Standard Bootloader
(function() {
    console.log("Flet Bootloader Initializing...");
    const script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";
    script.onload = async () => {
        try {
            let pyodide = await loadPyodide();
            await pyodide.loadPackage("micropip");
            const micropip = pyodide.pyimport("micropip");
            // flet-coreはPure Pythonなので100%確実にブラウザにインストール可能
            await micropip.install("flet-core");
            
            // flet_main.py を読み込んで実行
            const response = await fetch('flet_main.py');
            if (!response.ok) throw new Error("flet_main.py が見つかりません");
            const pythonCode = await response.text();
            
            // flet_coreをfletとして偽装して実行
            pyodide.runPython(`
import sys
import flet_core
sys.modules['flet'] = flet_core
` + pythonCode);
            console.log("Flet App Started Successfully!");
        } catch (err) {
            console.error("Flet Initialization Error:", err);
            document.body.innerHTML = `<div style="color:white; padding:20px; font-family:sans-serif;"><h3>起動エラー</h3><p>${err.message}</p></div>`;
        }
    };
    document.head.appendChild(script);
})();
