document.addEventListener("DOMContentLoaded",function(){const e=document.querySelectorAll(".data-table");e.forEach(e=>{autoResizeColumns(e),makeColumnsResizable(e)})});function autoResizeColumns(e){const n=e.querySelectorAll("th"),t=e.querySelectorAll("tbody tr");n.forEach((e,n)=>{let s=100;const o=measureTextWidth(e.textContent,e);s=Math.max(s,o),t.forEach(e=>{const t=e.cells[n];if(t){const e=measureTextWidth(t.textContent,t);s=Math.max(s,e)}}),s=Math.min(s,800),e.style.minWidth=s+"px",e.style.maxWidth=s+"px",t.forEach(e=>{const t=e.cells[n];t&&(t.style.minWidth=s+"px",t.style.maxWidth=s+"px")})})}function measureTextWidth(e,t){const s=document.createElement("canvas"),n=s.getContext("2d"),o=window.getComputedStyle(t);n.font=o.font;const i=n.measureText(e);return i.width+40}function makeColumnsResizable(e){const t=e.querySelectorAll("th");t.forEach((t,n)=>{const s=document.createElement("div");s.className="column-resizer",s.style.cssText=`
      position: absolute;
      top: 0;
      right: 0;
      width: 5px;
      height: 100%;
      cursor: col-resize;
      background: transparent;
      z-index: 1;
    `,t.style.position="relative",t.appendChild(s);let o,i;s.addEventListener("mousedown",e=>{e.preventDefault(),o=e.pageX,i=t.offsetWidth,document.addEventListener("mousemove",a),document.addEventListener("mouseup",r),s.style.background="var(--color-link)"});function a(s){const r=i+(s.pageX-o),a=Math.max(100,Math.min(r,800));t.style.minWidth=a+"px",t.style.maxWidth=a+"px";const c=e.querySelectorAll("tbody tr");c.forEach(e=>{const t=e.cells[n];t&&(t.style.minWidth=a+"px",t.style.maxWidth=a+"px")})}function r(){document.removeEventListener("mousemove",a),document.removeEventListener("mouseup",r),s.style.background="transparent"}})}