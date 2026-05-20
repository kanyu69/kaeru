const CACHE_NAME = 'kaeru-app-cache-v1';
// キャッシュするファイルの一覧（環境に応じて追加・変更してください）
const urlsToCache = [
  './',
  './index.html',
  './manifest.json',
  './main.kv',
  './camera.kv',
  './fonts/UDEVGothicHS-Regular.ttf'
];

// インストール時にファイルをキャッシュ
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// リクエスト発生時にキャッシュから返す（オフライン対応・高速化）
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // キャッシュがあればそれを返し、なければ通常のネットワーク通信を行う
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});

// 古いキャッシュの削除
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});