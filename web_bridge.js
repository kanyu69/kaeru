// web_bridge.js

let html5QrCodeScanner = null;
let cameraStream = null;

/**
 * 1. カメラを起動してリアルタイムスキャンを開始する
 */
function startWebScanner(pythonCallback) {
    const videoContainer = document.getElementById('camera-container');
    videoContainer.style.display = 'block';

    if ('BarcodeDetector' in window) {
        const barcodeDetector = new BarcodeDetector({ formats: ['ean_8', 'ean_13'] });
        const video = document.getElementById('camera-video');
        video.style.display = 'block';

        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
            .then((stream) => {
                cameraStream = stream;
                window.current_stream = stream; // ライト制御用にwindowに保持
                video.srcObject = stream;
                video.play();

                function track() {
                    if (!cameraStream) return;
                    barcodeDetector.detect(video)
                        .then((barcodes) => {
                            if (barcodes.length > 0 && pythonCallback) {
                                pythonCallback(barcodes[0].rawValue);
                            }
                            requestAnimationFrame(track);
                        })
                        .catch(() => requestAnimationFrame(track));
                }
                video.onloadedmetadata = () => { track(); };
            })
            .catch((err) => console.error("Camera access denied:", err));
    } else {
        // フォールバック: html5-qrcode を使用
        html5QrCodeScanner = new Html5Qrcode("camera-container");
        html5QrCodeScanner.start(
            { facingMode: "environment" },
            { fps: 10, qrbox: { width: 250, height: 250 } },
            (decodedText) => { if(pythonCallback) pythonCallback(decodedText); },
            () => { /* パースエラー無視 */ }
        ).catch(err => console.error(err));
    }
}

/**
 * 2. カメラを停止する
 */
function stopWebScanner() {
    document.getElementById('camera-container').style.display = 'none';

    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
        window.current_stream = null;
        const video = document.getElementById('camera-video');
        video.srcObject = null;
        video.style.display = 'none';
    }
    if (html5QrCodeScanner) {
        html5QrCodeScanner.stop().then(() => { html5QrCodeScanner = null; }).catch(e => console.log(e));
    }
}

/**
 * 3. バイブレーション
 */
function vibrateWeb() {
    if ('vibrate' in navigator) {
        navigator.vibrate(200);
    }
}

/**
 * 4. 効果音の再生
 */
function playWebSystemSound(soundId) {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(1200, audioCtx.currentTime);
    gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);

    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    oscillator.start();
    oscillator.stop(audioCtx.currentTime + 0.1);
}

/**
 * 5. アルバムから画像を選択して解析
 */
function openWebPhotoLibrary(pythonCallback) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    
    input.onchange = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        if ('BarcodeDetector' in window) {
            const img = new Image();
            img.src = URL.createObjectURL(file);
            img.onload = () => {
                const barcodeDetector = new BarcodeDetector({ formats: ['ean_8', 'ean_13'] });
                barcodeDetector.detect(img)
                    .then((barcodes) => {
                        if (barcodes.length > 0 && pythonCallback) pythonCallback(barcodes[0].rawValue);
                    });
            };
        } else {
            const html5QrCode = new Html5Qrcode("camera-container");
            html5QrCode.scanFile(file, true)
                .then(decodedText => { if(pythonCallback) pythonCallback(decodedText); })
                .catch(err => console.log("No barcode found", err));
        }
    };
    input.click();
}

/**
 * 6. カメラの権限確認（デバッグ用固定値）
 */
function getCameraAuthStatus() {
    return 3; 
}