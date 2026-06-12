import asyncio
import sys
import types
import js_renderer

sys.path.insert(0, "/tmp")

_storage_dict = {}

class DummyClientStorage:
    def get(self, key): return _storage_dict.get(key, None)
    def set(self, key, value): _storage_dict[key] = value
    def remove(self, key): _storage_dict.pop(key, None)
    def contains_key(self, key): return key in _storage_dict

_session_dict = {}

class DummySession:
    def get(self, key): return _session_dict.get(key, None)
    def set(self, key, value): _session_dict[key] = value
    def remove(self, key): _session_dict.pop(key, None)
    def contains_key(self, key): return key in _session_dict

class MockPage:
    def __init__(self):
        self.title = ""
        self.padding = 0
        self.spacing = 0
        self.bgcolor = None
        self.theme_mode = None
        self.fonts = {}
        self.horizontal_alignment = None
        self.vertical_alignment = None
        self.scroll = None
        self.window_width = 400
        self.window_height = 800
        self.controls = []
        self.overlay = []
        self.views = []
        self.route = "/"
        self.snack_bar = None
        self.dialog = None
        self.bottom_sheet = None
        self.navigation_bar = None
        self.appbar = None
        self.floating_action_button = None
        self.theme = None
        self.dark_theme = None
        self.rtl = False
        self.width = 400
        self.height = 800
        self.client_storage = DummyClientStorage()
        self.session = DummySession()
    def update(self):
        try: js_renderer.renderPage()
        except Exception as ex: print("renderPage warning: " + str(ex))
    def add(self, *controls):
        for c in controls: self.controls.append(c)
    def remove(self, *controls):
        for c in controls:
            if c in self.controls: self.controls.remove(c)
    def go(self, route): self.route = route
    def get_upload_url(self, *a, **k): return ""
    def set_clipboard(self, value): pass
    def launch_url(self, url, *a, **k): pass
    def show_snack_bar(self, s): self.snack_bar = s
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
