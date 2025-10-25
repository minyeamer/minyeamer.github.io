async function generatePreview(e){try{const t=await getLinkPreview(e);console.log(t);const n=`
      <div class="link-preview">
        <img src="${t.images[0]}" alt="${t.title}" style="width: 200px;">
        <h3>${t.title}</h3>
        <p>${t.description}</p>
        <a href="${t.url}">${t.url}</a>
      </div>
    `;document.getElementById("preview-container").innerHTML=n}catch(e){console.error("미리보기 생성 실패:",e)}}document.getElementById("link-input").addEventListener("keypress",e=>{if(e.key==="Enter"){const t=e.target.value;generatePreview(t)}})