const cacheName = "calc-app-v1";
const resourcesToCache = [
    "/",
    "/manifest.json",
    "/static/icons/icon-192x192.png",
    "/static/icons/icon-512x512.png"
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(cacheName).then((cache) => cache.addAll(resourcesToCache))
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
