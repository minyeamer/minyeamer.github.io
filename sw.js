const cacheName = self.location.pathname
const pages = [

  "/blog/hugo-blog-5/",
  "/",
  "/posts/",
  "/blog/hugo-blog-4/",
  "/blog/hugo-blog-3/",
  "/blog/hugo-blog-2/",
  "/blog/hugo-blog-1/",
  "/blog/openup-handson/",
  "/blog/uv-project/",
  "/blog/spark-study-8/",
  "/blog/kube-installtion/",
  "/blog/container-history/",
  "/blog/spark-study-7/",
  "/blog/spark-study-6/",
  "/blog/install-ubuntu-server/",
  "/blog/spark-study-5/",
  "/blog/programmers-sql-4-5/",
  "/blog/spark-study-4/",
  "/blog/spark-study-3/",
  "/blog/spark-study-2/",
  "/blog/spark-study-1/",
  "/blog/airflow-study-7/",
  "/blog/airflow-study-6/",
  "/blog/airflow-study-5/",
  "/blog/airflow-study-4/",
  "/blog/airflow-study-3/",
  "/blog/airflow-study-2/",
  "/blog/airflow-study-1/",
  "/blog/10000-recipe/",
  "/blog/smartstore-login-3/",
  "/blog/smartstore-login-2/",
  "/blog/smartstore-login-1/",
  "/blog/hugo-blog-old-3/",
  "/blog/hugo-blog-old-2/",
  "/blog/hugo-blog-old-1/",
  "/blog/jekyll-blog/",
  "/blog/dacon-shop-review/",
  "/blog/dacon-audio-mnist/",
  "/blog/dacon-consumption-prediction/",
  "/blog/big-o-list/",
  "/blog/baekjoon-1197-mst/",
  "/blog/algorithm-basics/",
  "/categories/",
  "/search/",
  "/tags/",
  "/main.min.78359fe1d15e2512e12b611be00b7eae5b99431f676240e1db8c04ffbf97a6ea.css",
  
];

self.addEventListener("install", function (event) {
  self.skipWaiting();

  caches.open(cacheName).then((cache) => {
    return cache.addAll(pages);
  });
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") {
    return;
  }

  /**
   * @param {Response} response
   * @returns {Promise<Response>}
   */
  function saveToCache(response) {
    if (cacheable(response)) {
      return caches
        .open(cacheName)
        .then((cache) => cache.put(request, response.clone()))
        .then(() => response);
    } else {
      return response;
    }
  }

  /**
   * @param {Error} error
   */
  function serveFromCache(error) {
    return caches.open(cacheName).then((cache) => cache.match(request.url));
  }

  /**
   * @param {Response} response
   * @returns {Boolean}
   */
  function cacheable(response) {
    return response.type === "basic" && response.ok && !response.headers.has("Content-Disposition")
  }

  event.respondWith(fetch(request).then(saveToCache).catch(serveFromCache));
});