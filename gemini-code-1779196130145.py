from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

# Pyodide環境（Webブラウザ実行環境）のJS操作ライブラリをインポート
try:
    import js
    from pyodide.ffi import create_proxy
    IS_WEB = True
except ImportError:
    IS_WEB = False

class WebBridge:
    def __init__(self):
        self.last_barcode = None
        self._callback_proxy = None
        
        if IS_WEB:
            # JavaScript側にPythonのコールバックを登録するためのプロキシを作成
            self._callback_proxy = create_proxy(self.set_detected_barcode)

    def set_detected_barcode(self, code):
        """バーコードが検出された時にJS側から呼ばれるメソッド"""
        if code:
            # Pythonの文字列に変換して保持
            self.last_barcode = str(code)
            print(f"[DEBUG] Barcode Detected: {self.last_barcode}")

    def consume_last_barcode(self):
        """読み取ったバーコードを取得し、バッファをクリアする (元のconsumeLastBarcodeと同等)"""
        if not self.last_barcode:
            return None
        ret = self.last_barcode
        self.last_barcode = None
        return ret

    def start_jan_scanner(self):
        """カメラのJANコードスキャナーを起動する"""
        print("[DEBUG] startJanScanner")
        if IS_WEB:
            # JS側のスキャン開始関数を呼び出す
            js.startWebScanner(self._callback_proxy)
            self.make_kivy_transparent()
        else:
            print("Non-web environment: Cannot start camera.")

    def stop_jan_scanner(self):
        """スキャナーを停止する"""
        print("[DEBUG] stopJanScanner")
        if IS_WEB:
            js.stopWebScanner()

    def make_kivy_transparent(self):
        """Kivyの背景を透明にして背面のカメラ映像が見えるようにする"""
        print("[DEBUG] makeKivyTransparent")
        if IS_WEB:
            # HTML/CSS側のレイヤーを操作して透過させる
            js.makeKivyTransparent()

    def play_system_sound(self, sound_id):
        """指定されたIDの効果音を再生する (Webでは標準ビープ音等で代替)"""
        if IS_WEB:
            js.playWebSystemSound(int(sound_id))

    def vibrate(self):
        """端末をバイブレーション（振動）させる"""
        if IS_WEB:
            js.vibrateWeb()

    def open_url(self, url_string):
        """指定したURLをブラウザの別タブで開く"""
        if IS_WEB:
            js.window.open(url_string, '_blank')

    def open_photo_library(self):
        """フォトライブラリ（ファイル選択）を開き、選択された画像をVision(JS)で解析する"""
        if IS_WEB and self._callback_proxy:
            js.openWebPhotoLibrary(self._callback_proxy)

    def camera_auth_status(self):
        """カメラの権限状態を返す (Webでは簡易的に可否の擬似ステータスを返却)"""
        # 0: NotDetermined, 1: Restricted, 2: Denied, 3: Authorized
        if IS_WEB:
            return js.getCameraAuthStatus()
        return 0

    def bundle_id(self):
        """アプリの識別子を返す（Webではドメイン名を返却）"""
        if IS_WEB:
            return js.window.location.hostname
        return "com.example.kivyweb"


# --- Kivyアプリの動作確認用UIサンプルー ---
class BarcodeScannerApp(App):
    def build(self):
        self.bridge = WebBridge()

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.result_label = Label(text="Barcode: None", size_hint_y=0.2)
        layout.add_widget(self.result_label)

        btn_start = Button(text="Start Scanner")
        btn_start.bind(on_press=lambda x: self.bridge.start_jan_scanner())
        layout.add_widget(btn_start)

        btn_stop = Button(text="Stop Scanner")
        btn_stop.bind(on_press=lambda x: self.bridge.stop_jan_scanner())
        layout.add_widget(btn_stop)

        btn_album = Button(text="Open Photo Library")
        btn_album.bind(on_press=lambda x: self.bridge.open_photo_library())
        layout.add_widget(btn_album)

        # 定期的にバーコードの読み取りを監視（ポーリング）
        Clock.schedule_interval(self.check_barcode, 0.5)

        return layout

    def check_barcode(self, dt):
        code = self.bridge.consume_last_barcode()
        if code:
            self.result_label.text = f"Barcode: {code}"
            self.bridge.vibrate()
            self.bridge.play_system_sound(1000) # 任意のSoundID

if __name__ == '__main__':
    BarcodeScannerApp().run()