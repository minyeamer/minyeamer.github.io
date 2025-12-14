document.addEventListener("DOMContentLoaded",function(){const n=new URLSearchParams(window.location.search),e=n.get("q")||"",s=parseInt(n.get("page"))||1,t=10;window.bookSearch.initIndex().then(()=>{o(),i()});function o(){const t=document.getElementById("search-query-display");e?t.innerHTML=`"${e}" 검색 결과 <em class="list-count" id="search-count">0</em>`:t.textContent="검색어를 입력해주세요."}function i(){const l=document.querySelector(".search-base"),o=document.querySelector(".search-results"),d=Array.from(l.querySelectorAll(".post-item"));if(!e){document.getElementById("search-no-results").classList.remove("hidden"),document.getElementById("search-pagination").style.display="none";return}const i=window.bookSearchIndex.search(e);if(i.length===0){document.getElementById("search-no-results").classList.remove("hidden"),document.getElementById("search-count").textContent="0",document.getElementById("search-pagination").style.display="none";return}const n=[];i.forEach(e=>{const s=e.item.href,t=d.find(e=>{const t=e.querySelector(".post-title a");return t&&t.getAttribute("href")===s});t&&n.push(t.cloneNode(!0))});const u=Math.ceil(n.length/t),r=(s-1)*t,h=Math.min(r+t,n.length),c=document.createDocumentFragment();for(let e=r;e<h;e++)c.appendChild(n[e]);o.innerHTML="",o.appendChild(c),document.getElementById("search-count").textContent=n.length,a(s,u,e)}function a(e,t,n){const i=document.getElementById("search-pagination");if(t<=1){i.style.display="none";return}i.style.display="block";const a=e=>`/search/?q=${encodeURIComponent(n)}${e>1?"&page="+e:""}#pagination-anchor`,d=Math.floor((e-1)/10),s=d*10+1;let o=s+9;o>t&&(o=t);const c=s-10,l=o+1,u=s>1?`<a href="${a(c>1?c:1)}" class="pagination-nav pagination-link">
          <i class="fa-solid fa-backward"></i> 이전
        </a>`:`<span class="pagination-nav disabled">
          <i class="fa-solid fa-backward"></i> 이전
        </span>`;let r="";for(let t=s;t<=o;t++)t===e?r+=`<span class="pagination-page current" id="current-page">${t}</span>`:r+=`<a href="${a(t)}" class="pagination-page pagination-link">${t}</a>`;const h=l<=t?`<a href="${a(l)}" class="pagination-nav pagination-link">
          다음 <i class="fa-solid fa-forward"></i>
        </a>`:`<span class="pagination-nav disabled">
          다음 <i class="fa-solid fa-forward"></i>
        </span>`;i.innerHTML=`
      <div id="pagination-anchor"></div>
      <nav class="pagination">
        ${u}
        <div class="pagination-pages">
          ${r}
        </div>
        ${h}
      </nav>`}})