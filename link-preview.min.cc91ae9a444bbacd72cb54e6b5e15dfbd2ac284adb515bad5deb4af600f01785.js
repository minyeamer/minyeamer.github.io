async function generatePreview(e){const t=e.getAttribute("data-url");if(!t)return;try{const n=await getLinkPreview(t,{headers:{"User-Agent":"Mozilla/5.0 (compatible; HugoLinkPreview/1.0)"}});console.log("Fetched data:",n);const s=`
      <div class="link-card" style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden; max-width: 600px; margin: 10px 0; display: flex; text-decoration: none; color: inherit;">
        ${n.images&&n.images[0]?`<img src="${n.images[0]}" alt="${n.title}" style="width: 200px; height: 150px; object-fit: cover;">`:""}
        <div style="padding: 10px; flex: 1;">
          <h3 style="margin: 0; font-size: 18px;">${n.title||"No Title"}</h3>
          <p style="margin: 5px 0; color: #666;">${n.description||"No Description"}</p>
          <small style="color: #999;">${n.url}</small>
        </div>
      </div>
    `;e.innerHTML=s,console.log("Preview generated for:",t)}catch(n){console.error("미리보기 생성 실패:",n),e.innerHTML=`<a href="${t}" target="_blank">${t}</a>`}}document.addEventListener("DOMContentLoaded",()=>{console.log("DOMContentLoaded fired");const e=document.querySelectorAll(".link-preview");console.log("Found previews:",e.length),e.forEach(generatePreview)})