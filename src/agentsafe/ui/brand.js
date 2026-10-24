"use strict";
const brandZh = document.documentElement.lang === "zh";
const brandCopy = {back:"← 返回检查",eyebrow:"01 已选定 · 三款设计对比",title:"小小图标，一眼认出。",intro:"已选定 01「A 字标」作为默认图标。其他两款仍可在当前标签页里预览对比。",adopted:"已采用",aTitle:"A 字标",aText:"用清晰的字母轮廓延续 AgentSafe 的品牌，缩到小图标时仍容易辨认。",frameLabel:"截图 / 遮盖",bTitle:"截图取景框",bText:"取景框与实心遮盖条，直接表达截图检查和手动打码的用途。",fileLabel:"文件 / 审阅",cTitle:"折角文件",cText:"文件折角加遮盖条，更偏向开发产物审阅；暖色背景在侧栏中更显眼。",try:"在标签页里预览",svg:"下载 SVG ↗",context:"浏览器中的样子",contextText:"同一个图标，标签页和侧栏两种展示。",footer:"原创矢量设计，附 SVG、PNG 和 ICO。应用已采用 01「A 字标」；这里的预览仅切换当前标签页的图标。"};
if (brandZh) {
  document.title="AgentSafe · 三款图标对比";
  for (const el of document.querySelectorAll("[data-brand]")) el.textContent=brandCopy[el.dataset.brand];
}
const names = brandZh ? {monogram:"01 · A 字标",frame:"02 · 截图取景框",document:"03 · 折角文件"} : {monogram:"01 · A monogram",frame:"02 · Review frame",document:"03 · Private artifact"};
function selectBrand(name) {
  for (const card of document.querySelectorAll("[data-variant]")) card.classList.toggle("selected",card.dataset.variant===name);
  for (const button of document.querySelectorAll("[data-select]")) button.setAttribute("aria-pressed",String(button.dataset.select===name));
  document.getElementById("favicon-svg").href=`/icons/${name}.svg`;
  document.getElementById("favicon-png").href=`/icons/${name}-32.png`;
  document.getElementById("favicon-ico").href=`/icons/${name}.ico`;
  document.getElementById("chosen-mark").src=`/icons/${name}.svg`;
  for (const image of document.querySelectorAll(".context-mark")) image.src=`/icons/${name}-32.png`;
  document.getElementById("selection-note").textContent=(brandZh?"正在预览：":"Previewing: ")+names[name];
}
for (const button of document.querySelectorAll("[data-select]")) {
  button.setAttribute("aria-label",(brandZh?"在标签页里预览：":"Try in this tab: ")+names[button.dataset.select]);
  button.onclick=()=>selectBrand(button.dataset.select);
}
selectBrand("monogram");
