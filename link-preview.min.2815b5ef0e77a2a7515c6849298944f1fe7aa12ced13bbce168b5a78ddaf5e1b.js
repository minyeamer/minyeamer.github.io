async function generatePreview(e){const t=e.getAttribute("data-url");if(console.log("Processing URL:",t),!t)return;try{if(typeof getLinkPreview=="undefined"){console.error("getLinkPreview is not defined. Library may not be loaded correctly."),e.innerHTML=`<a href="${t}" target="_blank">${t}</a>`;return}const n=await getLinkPreview(t,{headers:{"User-Agent":"Mozilla/5.0 (compatible; HugoLinkPreview/1.0)"}});console.log("Fetched data:",n);const s=`
      <div class="link-preview-card">
        ${n.images&&n.images[0]?`
          <div class="link-preview-image">
            <img src="${n.images[0]}" alt="${n.title||"Preview image"}">
          </div>
        `:""}
        <div class="link-preview-content">
          <h3 class="link-preview-title">${n.title||"No Title"}</h3>
          <p class="link-preview-description">${n.description||"No Description"}</p>
          <small class="link-preview-url">${n.url}</small>
        </div>
      </div>
    `;e.innerHTML=s,console.log("Preview generated for:",t)}catch(n){console.error("미리보기 생성 실패:",n),e.innerHTML=`<a href="${t}" target="_blank">${t}</a>`}}document.addEventListener("DOMContentLoaded",()=>{console.log("DOMContentLoaded fired");const e=document.querySelectorAll(".link-preview");console.log("Found previews:",e.length),e.forEach(generatePreview)})