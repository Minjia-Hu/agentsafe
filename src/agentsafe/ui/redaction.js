"use strict";
const rcZh = document.documentElement.lang === "zh";
const rcStrings = {
  en:{title:"Cover what you choose.",cancel:"Cancel",intro:"Choose a detected region, or drag on the image to cover anything else. Solid blocks replace pixels in a new copy; the original is unchanged.",previewNote:"Cover preview only. Create and check the PNG copy before saving.",detected:"Detected regions",coordinates:"Or enter a rectangle in pixels",add:"Add rectangle +",undo:"Undo last",reset:"Clear covers",limit:"Check the whole image: detectors can miss content. Detected boxes include a 4 px margin; you can add more coverage yourself.",policy:"Recheck uses the original scan settings, including a sample's settings. No upload or privacy guarantee.",check:"Create & check PNG copy →",edit:"Cover image manually",entry:"Choose your own cover regions, then check and save a new PNG.",noBoxes:"No mapped regions. Drag on the image or enter coordinates to cover content yourself.",invalid:"Enter whole-pixel coordinates within the image; up to 100 rectangles.",count:"cover regions selected",copyTitle:"A new PNG copy",copyHint:"This download contains the exact pixels just checked. Review it manually before sharing; the original is unchanged.",save:"Save PNG copy ↗",image:"Manual image cover preview"},
  zh:{title:"遮盖你选择的内容。",cancel:"取消",intro:"勾选检测区域，或在图片上拖动框选其他内容。实心色块会替换新副本中的像素，原件保持不变。",previewNote:"这里是遮盖预览；生成并检查 PNG 副本后，再另存。",detected:"选择检测区域",coordinates:"也可以填写像素坐标",add:"添加遮盖区域 +",undo:"撤销上一块",reset:"清空遮盖",limit:"请审阅整张图片，检测可能漏掉内容。检测框默认向外扩展 4 像素；你也可以自行补充遮盖。",policy:"副本沿用原扫描的敏感性设置，样本也沿用样本设置。不上传，不保证隐私安全。",check:"生成并检查 PNG 副本 →",edit:"手动打码",entry:"自行选择遮盖区域，然后检查并另存新的 PNG 副本。",noBoxes:"没有可映射的检测框；可在图片上拖动框选，或填写坐标，自行遮盖内容。",invalid:"请填写图片范围内的整数像素坐标，最多选择 100 块区域。",count:"块遮盖区域已选择",copyTitle:"新的 PNG 副本",copyHint:"下载文件包含刚才重检的同一份像素。分享前仍需人工审阅；原件未修改。",save:"另存 PNG 副本 ↗",image:"手动打码预览"}
};
const rc = key => rcStrings[rcZh ? "zh" : "en"][key];
for (const el of document.querySelectorAll("[data-redaction]")) el.textContent=rc(el.dataset.redaction);
const rcDialog=document.getElementById("redaction-dialog"), rcStage=document.getElementById("redaction-stage");
rcStage.setAttribute("aria-label",rc("image"));
let rcState=null, rcDrag=null;
function rcError() {const el=document.getElementById("redaction-error");el.textContent=rc("invalid");el.hidden=false;}
function rcRectangle(region, cls) {
  const el=document.createElementNS("http://www.w3.org/2000/svg","rect");
  for (const key of ["x","y"]) el.setAttribute(key,region[key]);
  el.setAttribute("width",region.w);el.setAttribute("height",region.h);el.setAttribute("class",cls);return el;
}
function rcRender() {
  for (const rect of rcStage.querySelectorAll("rect")) rect.remove();
  if (!rcState) return;
  for (const r of rcState.regions) rcStage.append(rcRectangle(r,"cover-region"));
  for (const el of document.querySelectorAll("[data-cover-key]")) el.checked=rcState.regions.some(r=>r.key===el.dataset.coverKey);
  document.getElementById("cover-count").textContent=`${rcState.regions.length} ${rc("count")}`;
  document.getElementById("cover-check").disabled=!rcState.regions.length;
  document.getElementById("cover-undo").disabled=!rcState.regions.length;
  document.getElementById("cover-reset").disabled=!rcState.regions.length;
}
function rcAdd(region) {
  if (!rcState || rcState.regions.length>=100 || ![region.x,region.y,region.w,region.h].every(Number.isInteger) || region.x<0 || region.y<0 || region.w<1 || region.h<1 || region.x+region.w>rcState.w || region.y+region.h>rcState.h) {rcError();return false;}
  rcState.regions.push(region);document.getElementById("redaction-error").hidden=true;rcRender();return true;
}
function rcPoint(event) {
  // Invert the SVG transform so resizing/letterboxing never moves a cover
  // away from its source pixels, including narrow or tall screenshots.
  const point=new DOMPoint(event.clientX,event.clientY).matrixTransform(rcStage.getScreenCTM().inverse());
  return {x:Math.max(0,Math.min(rcState.w,Math.round(point.x))),y:Math.max(0,Math.min(rcState.h,Math.round(point.y)))};
}
function rcBetween(a,b) {return {x:Math.min(a.x,b.x),y:Math.min(a.y,b.y),w:Math.abs(a.x-b.x),h:Math.abs(a.y-b.y)};}
rcStage.onpointerdown=e=>{if (!rcState || e.button!==0) return;e.preventDefault();rcDrag={id:e.pointerId,start:rcPoint(e)};rcStage.setPointerCapture(e.pointerId);};
rcStage.onpointermove=e=>{if (!rcDrag || e.pointerId!==rcDrag.id) return;rcRender();rcStage.append(rcRectangle(rcBetween(rcDrag.start,rcPoint(e)),"draft-region"));};
rcStage.onpointerup=e=>{if (!rcDrag || e.pointerId!==rcDrag.id) return;const r=rcBetween(rcDrag.start,rcPoint(e));rcDrag=null;rcStage.releasePointerCapture(e.pointerId);if(r.w>=2&&r.h>=2) rcAdd(r);else rcRender();};
rcStage.onpointercancel=()=>{rcDrag=null;rcRender();};
document.getElementById("redaction-cancel").onclick=()=>rcDialog.close();
rcDialog.addEventListener("close",()=>{rcState=null;rcDrag=null;rcStage.replaceChildren();document.getElementById("redaction-regions").replaceChildren();});
document.getElementById("cover-undo").onclick=()=>{rcState.regions.pop();rcRender();};
document.getElementById("cover-reset").onclick=()=>{rcState.regions=[];rcRender();};
document.getElementById("cover-add").onclick=()=>rcAdd({x:Number(document.getElementById("cover-x").value),y:Number(document.getElementById("cover-y").value),w:Number(document.getElementById("cover-w").value),h:Number(document.getElementById("cover-h").value)});
document.getElementById("cover-check").onclick=async()=>{
  if (!rcState || !rcState.regions.length) return;
  const state=rcState, metadata={review_id:state.reviewId,image_index:state.index,regions:state.regions.map(({x,y,w,h})=>({x,y,w,h}))};
  rcDialog.close();await state.onCheck(metadata);
};
function rcOpen(card,index,result,onCheck) {
  const source=card.querySelector(".image-stage"), image=source.querySelector("image"), view=source.viewBox.baseVal;
  rcState={index,reviewId:result.review_id,w:view.width,h:view.height,regions:[],onCheck};
  rcStage.setAttribute("viewBox",`0 0 ${view.width} ${view.height}`);rcStage.replaceChildren(image.cloneNode(true));
  document.getElementById("redaction-name").textContent=card.querySelector("h2").textContent;
  document.getElementById("redaction-error").hidden=true;
  for (const [id,n] of [["cover-x",0],["cover-y",0],["cover-w",Math.min(100,view.width)],["cover-h",Math.min(30,view.height)]]) document.getElementById(id).value=n;
  const choices=document.getElementById("redaction-regions");choices.replaceChildren();
  const boxes=source.querySelectorAll(".region");
  for (const [i,rect] of Array.from(boxes).entries()) {
    const x=Math.max(0,Number(rect.getAttribute("x"))-4),y=Math.max(0,Number(rect.getAttribute("y"))-4);
    const right=Math.min(view.width,Number(rect.getAttribute("x"))+Number(rect.getAttribute("width"))+4),bottom=Math.min(view.height,Number(rect.getAttribute("y"))+Number(rect.getAttribute("height"))+4);
    const region={x,y,w:right-x,h:bottom-y,key:`box-${i}`},label=document.createElement("label"),checkbox=document.createElement("input"),name=document.createElement("span");
    label.className="redaction-option";checkbox.type="checkbox";checkbox.dataset.coverKey=region.key;name.textContent=rect.querySelector("title").textContent;
    checkbox.onchange=()=>{if(checkbox.checked){if(!rcAdd(region))checkbox.checked=false;}else{rcState.regions=rcState.regions.filter(r=>r.key!==region.key);rcRender();}};
    label.append(checkbox,name);choices.append(label);
  }
  if(!boxes.length){const hint=document.createElement("p");hint.textContent=rc("noBoxes");choices.append(hint);}
  rcRender();rcDialog.showModal();
}
function bindRedaction(result,onCheck) {
  if (!result.review_id) return;
  for (const [index,card] of Array.from(document.querySelectorAll("#cards .file-card")).entries()) {
    if (!card.querySelector(".image-stage")) continue;
    const entry=document.createElement("div"),hint=document.createElement("p"),button=document.createElement("button");
    entry.className="redaction-entry";hint.textContent=rc("entry");button.type="button";button.className="button secondary";button.textContent=rc("edit");button.dataset.editImage=String(index);
    button.onclick=()=>rcOpen(card,index,result,onCheck);entry.append(hint,button);card.append(entry);
  }
}
function showCopy(result) {
  const output=document.getElementById("copy-output"),anchor=document.getElementById("copy-download");
  output.hidden=!result.export;
  if(result.export){document.getElementById("copy-name").textContent=result.export.name;anchor.href=result.export.url;anchor.download=result.export.name;}
  else {anchor.removeAttribute("href");anchor.removeAttribute("download");document.getElementById("copy-name").textContent="";}
}
function clearRedaction() {if(rcDialog.open)rcDialog.close();showCopy({});}
