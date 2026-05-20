import os
import requests # 忘れずに追加
import threading # loading画面用
import random
import re
import webbrowser

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen, FadeTransition, SlideTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.animation import Animation
from kivy.graphics import Color, Ellipse, Rotate, PushMatrix, PopMatrix
from kivy.metrics import dp
from kivy.uix.recycleview import RecycleView
from kivy.uix.modalview import ModalView
from kivy.factory import Factory # kvで定義したクラスを呼ぶため
from kivy.uix.image import Image
from kivy.storage.jsonstore import JsonStore

from datetime import datetime

# Web環境(Pyodide / WebAssembly)かどうかの判定
# platform == 'web' または環境変数、あるいは環境によりモジュールが存在するかで判定
IS_WEB = (platform == 'web' or os.environ.get('KIVY_BUILD') == 'web')

# 【修正】Pyodide環境で動的にインポートが成功するように保護
if IS_WEB:
    try:
        from js import window, document
    except ImportError:
        pass

_ios_bridge = None

# 環境に応じた設定ファイルの保存先
if platform == 'ios':
    from os.path import expanduser
    # iOSアプリの書き込み可能ディレクトリを取得
    user_data_dir = expanduser('~/Documents')
    settings_path = os.path.join(user_data_dir, 'user_settings.json')
elif IS_WEB:
    # Webブラウザ環境用の擬似パス（IndexedDBなどのブラウザ内ストレージに永続化されます）
    settings_path = 'user_settings.json'
else:
    # PC環境などの場合はカレントディレクトリ
    settings_path = 'user_settings.json'

# 正しいパスでJsonStoreを初期化
store = JsonStore(settings_path)


class MyApp(App):
    lang = StringProperty('ja')
    flashlight_status = BooleanProperty(False)

    def build(self):
        self.title = "Kaeru App"

        # 必要なKVファイルをここで読み込む
        Builder.load_file('main.kv')
        Builder.load_file('camera.kv')

        # 言語をロード
        self.lang = 'ja'

        return Factory.MainRoot()

    def toggle_flashlight(self):
        print(f"DEBUG: Toggle Flashlight. Current status: {self.flashlight_status}")

        if platform == 'ios':
            try:
                # iOSの場合のみ関数内で動的にインポートすることで、Web環境でのクラッシュを防ぐ
                from pyobjus import autoclass

                # クラスとして取得するのは AVCaptureDevice のみ
                AVCaptureDevice = autoclass('AVCaptureDevice')

                # デフォルトのデバイスを "vide" (ビデオ) 指定で取得
                device = AVCaptureDevice.defaultDeviceWithMediaType_("vide")

                if device and device.hasTorch():
                    # 設定変更のロック
                    if device.lockForConfiguration_(None):
                        self.flashlight_status = not self.flashlight_status

                        # 1 は ON (AVCaptureTorchModeOn), 0 は OFF (AVCaptureTorchModeOff)
                        mode = 1 if self.flashlight_status else 0
                        device.setTorchMode_(mode)

                        device.unlockForConfiguration()
                        print(f"DEBUG: iOS Flashlight set to {mode}")
                else:
                    print("DEBUG: Device has no torch or camera not found")
            except Exception as e:
                print(f"DEBUG: iOS Flashlight Error: {e}")

        elif IS_WEB:
            # --- Web（ブラウザ）環境でのライト（Torch）制御 ---
            try:
                self.flashlight_status = not self.flashlight_status
                # 【修正】Pyodideでは eval_string ではなく js.eval や直接 window オブジェクトを操作できます。
                # 汎用的に動くようJavaScriptの関数を実行する形にします。
                import js

                js_code = f"""
                (function() {{
                    if (window.current_stream) {{
                        const track = window.current_stream.getVideoTracks()[0];
                        if (track) {{
                            const capabilities = track.getCapabilities();
                            if (capabilities.torch) {{
                                track.applyConstraints({{ advanced: [{{ torch: {str(self.flashlight_status).lower()} }}] }});
                            }} else {{
                                console.log("このブラウザ・デバイスはWebからのライト制御に対応していません");
                            }}
                        }}
                    }}
                }})();
                """
                js.eval(js_code)
                print(f"DEBUG: Web Flashlight set to {self.flashlight_status}")
            except Exception as e:
                print(f"DEBUG: Web Flashlight Error: {e}")

        else:
            # PCなどのデバッグ環境用
            self.flashlight_status = not self.flashlight_status
            print(f"DEBUG: Simulation Flashlight: {self.flashlight_status}")


if __name__ == '__main__':
    # フォントの登録
    # 【注意】ブラウザ環境でフォントファイルを読み込むには、
    # サーバー上の fonts/ フォルダの中に該当のTTFファイルが配置されている必要があります。
    try:
        LabelBase.register(name="UD", fn_regular="fonts/UDEVGothicHS-Regular.ttf")
    except Exception as e:
        print(f"Font Load Warning: {e}")

    MyApp().run()