"use strict";
const copy = {
  en: {
    redactedHint:"Only your selected regions were covered. Other private content may remain; review the downloaded copy manually before sharing.",redacted:"PNG copy rechecked with the original scan settings. These results cover this one new image only; other selected files are not rechecked here and the original is unchanged.",
    terms:"Extra checks: sensitive words / phrases (optional)",termsHint:"Enter a customer name, internal project name or phrase you want kept private, one per line (2–128 characters, up to 100). Spaces and commas stay within a phrase; English matches ignore case and avoid larger words. No automatic judgment or spelling variants. Chinese terms work in text files; image OCR currently reads English.",termsDemo:"Customer / project names ↗",invalidTerm:"Enter one literal phrase per line, 2–128 characters each, up to 100; no control characters. Do not enter passwords or token values.",termsSynthetic:"Fictional business sample · checks Project Cedar, Acme Training and 华星演示客户 without any domain configuration. Chinese is demonstrated in the log, not image OCR.",termCount:"sensitive phrases",domainCount:"internal domains",cookieCount:"session cookie names",
    local:"On this device",stop:"End session",eyebrow:"A MOMENT BEFORE YOU SHARE",title:"A little context can travel too far.",intro:"Check screenshots and debugging logs locally. Locate what needs review, then decide what to share.",selectTitle:"Choose your files",formats:"PNG · JPEG · LOG · TXT",dropTitle:"Drop files here",dropHint:"or choose screenshots and logs from your device",choose:"Choose files",limits:"Up to 20 files · 24 MiB total · no folders",snapshot:"After editing an original, select the updated file again. The browser selection is a snapshot.",demoTitle:"NO FILES YET?",demoHint:"Try fictional samples. No real business data.",before:"Before review ↗",after:"After review ↗",miss:"Known OCR miss ↗",settingsTitle:"Add your context",settingsHint:"Email, authentication fields and cookies are checked automatically. Add names or domains you want kept private; both fields are optional.",domains:"Extra checks: internal domains (optional)",domainsHint:"For the original sample, enter northstar.test. For your files, enter an internal domain only, without https:// or a path, one per line or comma separated. Includes subdomains and emails on those domains.",advanced:"Optional: session cookie names",cookies:"Sensitive session cookies",cookiesHint:"Only enter cookie names, never their values. Other populated cookies generate a review warning.",scan:"Check selected files →",localHint:"File bytes go only to the process on this computer. Nothing is sent to a cloud service.",checkingHealth:"Checking image scanning…",reviewTitle:"Review before sharing",reselect:"Choose updated files ↗",clear:"Clear results",boundary:"Image markings only locate evidence. Use Cover image manually to choose opaque regions, check a new PNG and save it. Edit logs in your usual tools, then reselect and scan again.",emptyTitle:"Your review starts here.",emptyHint:"Choose files or try a sample. Results show image regions and clickable masked log excerpts.",footer:"Experimental Alpha · OCR currently reads English text. No automatic redaction or upload protection. A scan cannot certify privacy. AgentSafe keeps settings and results in this session only; PNG copies are saved only when you click Save.",noPolicy:"Both fields can be empty. General email/authentication/cookie rules still run; private names and internal domains are not inferred.",hasPolicy:"These extra checks apply only to this session. Changing them requires a new scan.",selected:"files selected",remove:"Remove file",preparing:"Reading your selected files…",running:"Checking locally",transfer:"Sending the selected snapshots to the process on this computer…",incomplete:"Some files were not fully checked",high:"Findings need your review",warn:"Review warnings before sharing",manual:"Image needs manual review",none:"No supported rule matched",resultHint:"This is a review aid, not a privacy certificate. Images are not redacted, and log excerpts may still contain private context; keep this page private.",synthetic:"Fictional sample · northstar.test and demo_session are used for this check. Reviewed copies are prepared in advance, not automatically redacted.",ownFiles:"Your selected snapshots · using the settings from this scan.",tooMany:"Select at most 20 files. No scan was started.",tooLarge:"Select at most 24 MiB in total. Images are limited to 10 MiB and text files to 5 MiB each.",invalidDomain:"Enter ASCII domains only, without URLs or paths; at most 100 domains.",invalidCookie:"Enter cookie names only; at most 100 names of 128 characters each.",network:"Connection interrupted. No completed result is available for this attempt. Open AgentSafe again if the session has ended.",expired:"Session expired. Open AgentSafe again to reconnect.",ended:"Session ended. AgentSafe has cleared its in-memory results. Close this tab, or open the launcher to start again.",readError:"The browser could not read a selected file. Select it again and retry.",failed:"The scan could not complete. No privacy decision was made; reselect files and try again.",clearAll:"Remove all",cancelled:"Selection cancelled; the previous selection is unchanged.",refresh:"Files are selected; start a new scan to update the results.",stale:"Settings or selection changed. The result below belongs to the previous scan; run a new check.",errorCount:"incomplete",manualCount:"images need manual review",checking:"Checking file",plainReady:"Text scanning is available.",ocrUnavailable:"Image scanning is unavailable. Install Tesseract with English data, then reopen AgentSafe. Text files can still be checked.",genericError:"The request was rejected; no new scan was started. Check the selection and settings, then retry."
  },
  zh: {
    redactedHint:"仅覆盖了你选择的区域，其他内容仍可能敏感；分享前请人工审阅下载的副本。",redacted:"PNG 副本已沿用原扫描设置重检。结果只对应这张新图片，未同时重检其他所选文件；原件未修改。",
    terms:"额外标记：敏感词／短语（可选）",termsHint:"填写不适合公开的客户名、内部项目名或短语，每行一项，2–128 个字符，最多 100 项。空格和逗号保留在短语内；英文不区分大小写，避免匹配到较长单词内部。不自动判断敏感性或识别拼写变体。中文可用于日志；图片 OCR 目前识别英文。",termsDemo:"客户／项目名 ↗",invalidTerm:"敏感词每行一项，每项 2–128 个字符，最多 100 项，不含控制字符。请勿填写密码或 Token 值。",termsSynthetic:"虚构业务样本 · 只配置 Project Cedar、Acme Training 和华星演示客户，没有配置域名。中文检测展示在日志中，不代表支持中文图片 OCR。",termCount:"项敏感词／短语",domainCount:"个内部域名",cookieCount:"个会话 Cookie 名称",
    local:"仅在本机",stop:"结束使用",eyebrow:"分享之前，留一步检查",title:"先看清楚，再分享。",intro:"在本机检查截图和调试日志，找到需要审阅的位置，再决定哪些内容适合分享。",selectTitle:"选择文件",formats:"PNG · JPEG · LOG · TXT",dropTitle:"把文件拖到这里",dropHint:"或从电脑中选择截图与日志",choose:"选择文件",limits:"最多 20 个文件 · 总计 24 MiB · 不支持文件夹",snapshot:"修改原件后，请重新选择更新后的文件。浏览器当前选中的是文件快照。",demoTitle:"手里没有文件？",demoHint:"试用虚构样本，无真实业务数据。",before:"修改前 ↗",after:"修改后 ↗",miss:"已知 OCR 漏检 ↗",settingsTitle:"告诉我们哪些信息敏感",settingsHint:"邮箱、认证字段和 Cookie 会自动检查。你也可以指定不适合公开的名称或域名，下面两个输入框都可留空。",domains:"额外标记：内部域名（可选）",domainsHint:"原始样本填 northstar.test。自己的文件填写内部域名，每行一个或逗号分隔，不含 https:// 或路径；同时检查其子域名及该域名的邮箱。",advanced:"可选：敏感会话 Cookie 名称",cookies:"敏感会话 Cookie",cookiesHint:"只填名称，不填 Cookie 的值。其他有值的 Cookie 会提示人工判断。",scan:"开始检查所选文件 →",localHint:"文件只传给这台电脑上的扫描进程，不发送到云端服务。",checkingHealth:"正在检查图片扫描环境…",reviewTitle:"审阅结果，再决定分享",reselect:"重新选择修改后的文件 ↗",clear:"清除结果",boundary:"标记框仅用于定位。点击手动打码，选择实心遮盖区域，检查新 PNG 后另存副本。日志请用熟悉的工具修改，再重新选择并检查。",emptyTitle:"从一次检查开始。",emptyHint:"选择文件或试用样本；这里将显示图片问题位置，以及可点击定位的脱敏日志片段。",footer:"实验性 Alpha · OCR 目前识别英文文字。未提供自动打码或上传拦截；扫描不能保证隐私安全。设置和结果仅在会话中临时保留；仅点击另存时下载 PNG 副本。",noPolicy:"两个输入框都可留空，仍会检查普通邮箱、认证字段和 Cookie；不会自动判断哪些名称或域名属于内部信息。",hasPolicy:"额外标记只用于本次会话；修改设置后，请重新检查。",selected:"个文件已选择",remove:"移除文件",preparing:"正在读取所选文件…",running:"正在本机检查",transfer:"正在把所选文件快照传给本机扫描进程…",incomplete:"部分文件未完成检查",high:"发现需要你审阅的内容",warn:"有提示需要人工判断",manual:"图片需要人工检查",none:"未命中已支持的规则",resultHint:"检测结果用于辅助审阅，不是隐私保证。图片没有打码，日志片段也可能保留未识别的私密信息，请勿直接分享此页面。",synthetic:"虚构样本 · 本次使用 northstar.test 和 demo_session 配置。修改后样本预先制作，并非自动打码。",ownFiles:"你选择的文件快照 · 使用本次检查时填写的设置。",tooMany:"最多选择 20 个文件，尚未开始扫描。",tooLarge:"文件总计最多 24 MiB；每张图片最多 10 MiB，每个文本文件最多 5 MiB。",invalidDomain:"只填写英文域名，不含网址或路径，最多 100 个。",invalidCookie:"只填写 Cookie 名称，最多 100 个，每个最多 128 个字符。",network:"连接中断，本次尚无完整结果。如果会话已结束，请重新打开 AgentSafe。",expired:"会话已过期，请重新打开 AgentSafe。",ended:"本次使用已结束，AgentSafe 已清除内存中的结果。可以关闭此标签页，或重新打开启动器。",readError:"浏览器无法读取某个所选文件，请重新选择后再试。",failed:"检查未能完成，未作出隐私判断。请重新选择文件后再试。",clearAll:"全部移除",cancelled:"已取消选择，保留原来的文件。",refresh:"已选择文件，开始新检查即可更新结果。",stale:"设置或文件选择已变化。下方结果属于上一次检查，请重新扫描。",errorCount:"个未完成",manualCount:"张图片需人工检查",checking:"正在检查第",plainReady:"文本扫描可用。",ocrUnavailable:"图片扫描暂不可用。请安装含英文语言数据的 Tesseract，然后重新打开 AgentSafe。仍可检查文本文件。",genericError:"请求未被接受，未开始新的检查。请检查文件选择与设置后重试。"
  }
};
const lang = document.documentElement.lang === "zh" ? "zh" : "en";
const t = key => copy[lang][key];
const $ = id => document.getElementById(id);
for (const el of document.querySelectorAll("[data-copy]")) el.textContent = t(el.dataset.copy);
document.title = lang === "zh" ? "AgentSafe · 本地隐私检查" : "AgentSafe · Local privacy check";
$("file-list").setAttribute("aria-label", lang === "zh" ? "所选文件" : "Selected files");
let token = location.hash.slice(1) || sessionStorage.getItem("agentsafe-session") || "";
if (location.hash) {sessionStorage.setItem("agentsafe-session", token); history.replaceState(null, "", "/");}
let selected = [], busy = false, ended = false, hasResult = false;
let policyTimer;
const bytes = n => `${(n / 1048576).toFixed(2)} MiB`;
function showError(message, connection = false) {
  const el = $(connection ? "connection-error" : "scan-error");
  el.textContent = message; el.hidden = false;
  if (!connection) {$("review").hidden = false; $("empty-state").hidden = true;}
}
function setBusy(value) {
  busy = value;
  for (const el of document.querySelectorAll("#choose, #reselect, #clear, [data-demo], .remove-file, #remove-all, [data-edit-image], #copy-download")) el.disabled = busy || ended;
  for (const id of ["domains", "cookies", "terms"]) $(id).disabled = busy || ended;
  $("scan").disabled = busy || ended || !selected.length;
  $("stop").disabled = ended;
  $("drop-zone").setAttribute("aria-disabled", String(busy || ended));
}
async function api(path, options = {}) {
  let response;
  try {response = await fetch(path, {...options, headers:{"X-AgentSafe-Session":token, ...(options.headers || {})}, cache:"no-store", credentials:"omit"});}
  catch {throw new Error(t("network"));}
  if (response.status === 401) throw new Error(t("expired"));
  if (!response.ok) throw new Error(t("genericError"));
  return response.json();
}
function markStale() {
  if (hasResult) {$("result-context").textContent = t("stale"); $("result-context").hidden = false;}
}
function updateSelection() {
  $("file-list").replaceChildren();
  selected.forEach((file, index) => {
    const li = document.createElement("li");
    const ext = document.createElement("span"); ext.className = "file-type"; ext.textContent = file.name.split(".").pop().slice(0,5).toUpperCase();
    const name = document.createElement("span"); name.className = "file-name"; name.textContent = file.name;
    const size = document.createElement("span"); size.className = "file-size"; size.textContent = bytes(file.size);
    const remove = document.createElement("button"); remove.className = "remove-file"; remove.textContent = "×"; remove.setAttribute("aria-label", `${t("remove")} ${file.name}`); remove.onclick = () => {selected.splice(index,1); updateSelection(); markStale();};
    li.append(ext, name, size, remove); $("file-list").append(li);
  });
  $("selection-summary").hidden = !selected.length;
  $("selection-summary").replaceChildren();
  if (selected.length) {
    const count = document.createElement("span"); count.textContent = `${selected.length} ${t("selected")} · ${bytes(selected.reduce((n,f) => n + f.size,0))}`;
    const clear = document.createElement("button"); clear.className = "text-button"; clear.id = "remove-all"; clear.textContent = t("clearAll"); clear.onclick = () => {selected = []; updateSelection(); markStale();};
    $("selection-summary").append(count, clear);
  }
  setBusy(busy);
}
function choose() {if (!busy && !ended) {$("file-picker").value = ""; $("file-picker").click();}}
$("choose").onclick = choose; $("reselect").onclick = choose;
$("file-picker").onchange = () => {
  if (!$("file-picker").files.length) return;
  selected = Array.from($("file-picker").files); updateSelection(); markStale();
};
for (const event of ["dragenter","dragover"]) $("drop-zone").addEventListener(event, e => {e.preventDefault(); if (!busy && !ended) $("drop-zone").classList.add("dragover");});
for (const event of ["dragleave","drop"]) $("drop-zone").addEventListener(event, e => {e.preventDefault(); $("drop-zone").classList.remove("dragover");});
$("drop-zone").addEventListener("drop", e => {if (!busy && !ended && e.dataTransfer.files.length) {selected = Array.from(e.dataTransfer.files); updateSelection(); markStale();}});
// Do not let drops outside the selection zone navigate away from a review.
document.addEventListener("dragover", e => e.preventDefault()); document.addEventListener("drop", e => e.preventDefault());
function values(id) {return Array.from(new Set($(id).value.split(/[\s,，]+/).filter(Boolean)));}
function policy() {
  const domains = values("domains"), cookies = values("cookies");
  const terms = Array.from(new Set($("terms").value.split(/\r?\n/).map(value => value.trim()).filter(Boolean)));
  const host = /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?$/i;
  if (domains.length > 100 || domains.some(d => d.length > 253 || !host.test(d))) throw new Error(t("invalidDomain"));
  if (cookies.length > 100 || cookies.some(c => !/^[!#$%&'*+.^_`|~0-9A-Za-z-]{1,128}$/.test(c))) throw new Error(t("invalidCookie"));
  if (terms.length > 100 || terms.some(value => {const size = Array.from(value.replace(/ +/g, " ")).length; return size < 2 || size > 128 || /[\p{C}\u2028\u2029]/u.test(value);})) throw new Error(t("invalidTerm"));
  return {sensitive_domains:domains, session_cookie_names:cookies, sensitive_terms:terms};
}
function updatePolicyHint() {$("policy-hint").textContent = t($("domains").value.trim() || $("cookies").value.trim() || $("terms").value.trim() ? "hasPolicy" : "noPolicy");}
for (const id of ["domains", "cookies", "terms"]) $(id).addEventListener("input", () => {updatePolicyHint(); clearTimeout(policyTimer); policyTimer = setTimeout(markStale, 150);});
updatePolicyHint();
function prepareReview() {
  $("review").hidden = false; $("empty-state").hidden = true; $("scan-error").hidden = true;
  $("progress").hidden = false; $("progress-text").textContent = t("preparing"); $("progress-detail").textContent = ""; $("progress-bar").style.width = "0%";
  $("result-summary").hidden = true; $("result-context").hidden = true; $("cards").replaceChildren(); $("review-boundary").hidden = true; hasResult = false;
  clearRedaction();setBusy(true);
  $("review").scrollIntoView({behavior:matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth",block:"start"});
}
async function runSelected() {
  if (busy || ended || !selected.length) return;
  let config;
  try {
    if (selected.length > 20) throw new Error(t("tooMany"));
    if (selected.reduce((n,f) => n + f.size,0) > 24 * 1048576) throw new Error(t("tooLarge"));
    config = policy();
  } catch (error) {showError(error.message); return;}
  prepareReview();
  try {
    const snapshots = [];
    for (const file of selected) {
      try {snapshots.push(await file.arrayBuffer());} catch {throw new Error(t("readError"));}
    }
    const metadata = new TextEncoder().encode(JSON.stringify({files:selected.map((f,i) => ({name:f.name,size:snapshots[i].byteLength})),policy:config,lang}));
    const size = new ArrayBuffer(4); new DataView(size).setUint32(0, metadata.byteLength);
    $("progress-text").textContent = t("running"); $("progress-detail").textContent = t("transfer");
    await api("/api/scan", {method:"POST",headers:{"Content-Type":"application/octet-stream"},body:new Blob([size,metadata,...snapshots])});
    await poll();
  } catch (error) {if (!ended) {$("progress").hidden = true; showError(error.message); setBusy(false);}}
}
$("scan").onclick = runSelected;
for (const el of document.querySelectorAll("[data-demo]")) el.onclick = async () => {
  if (busy || ended) return;
  prepareReview();
  try {await api(`/api/demo/${el.dataset.demo}`, {method:"POST"}); await poll();}
  catch (error) {if (!ended) {$("progress").hidden = true; showError(error.message); setBusy(false);}}
};
function renderResult(result) {
  $("progress").hidden = true; $("result-summary").hidden = false;
  const title = result.incomplete ? "incomplete" : result.high ? "high" : result.manual_review ? "manual" : result.warn ? "warn" : "none";
  $("result-summary").className = `result-summary${result.incomplete ? " has-limit" : result.high ? " needs-review" : result.manual_review || result.warn ? " has-limit" : ""}`;
  const heading = document.createElement("strong"); heading.textContent = t(title);
  const findingCount = document.createElement("span"); findingCount.textContent = `${result.high} HIGH · ${result.warn} WARN`;
  const coverage = document.createElement("span"); coverage.textContent = `${result.total} ${lang === "zh" ? "个文件" : "files"} · ${result.incomplete} ${t("errorCount")}`;
  $("result-summary").replaceChildren(heading,findingCount,coverage);
  if (result.manual_review) {const manual = document.createElement("span"); manual.textContent = `${result.manual_review} ${t("manualCount")}`; $("result-summary").append(manual);}
  const counts = result.policy_counts || {domains:0,cookies:0,terms:0};
  const context = result.redacted ? "redacted" : result.synthetic ? (counts.terms ? "termsSynthetic" : "synthetic") : "ownFiles";
  $("result-context").textContent = `${t(context)} ${counts.terms} ${t("termCount")} · ${counts.domains} ${t("domainCount")} · ${counts.cookies} ${t("cookieCount")}. ${t(result.redacted ? "redactedHint" : "resultHint")}`;
  $("result-context").hidden = false;
  // Only server-rendered, escaped findings and normalized visible PNG pixels.
  // Log finding-line excerpts are masked before rendering; no raw log/OCR transcript.
  $("cards").innerHTML = result.cards;
  bindReviewCards($("cards"));
  bindRedaction(result, runRedaction);showCopy(result);
  $("review-boundary").hidden = false; hasResult = true; setBusy(false);
}
async function runRedaction(metadata) {
  if (busy || ended) return;
  prepareReview();
  try {await api("/api/redact",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(metadata)});await poll();}
  catch(error){if(!ended){try{const state=await api("/api/status");if(state.state==="done")renderResult(state);}catch{}$("progress").hidden=true;showError(error.message);setBusy(false);}}
}
async function poll() {
  while (!ended) {
    const result = await api("/api/status");
    if (result.state === "done") {renderResult(result); return;}
    if (result.state === "error") {showCopy(result);$("progress").hidden = true; showError(t("failed")); setBusy(false); return;}
    if (result.state === "idle") {$("progress").hidden = true; setBusy(false); return;}
    $("progress-text").textContent = `${t("running")} · ${result.current} / ${result.total}`;
    $("progress-detail").textContent = result.name;
    $("progress-bar").style.width = `${Math.max(3, ((result.current - 1) / result.total) * 100)}%`;
    await new Promise(resolve => setTimeout(resolve,400));
  }
}
$("clear").onclick = async () => {
  if (busy || ended) return;
  try {
    await api("/api/clear", {method:"POST"});
    clearRedaction();$("cards").replaceChildren(); $("review").hidden = true; $("empty-state").hidden = false; hasResult = false;
  } catch (error) {showError(error.message);}
};
$("stop").onclick = async () => {
  if (ended) return;
  try {
    await api("/api/stop", {method:"POST"}); ended = true; selected = []; $("file-picker").value = ""; $("domains").value = ""; $("cookies").value = ""; $("terms").value = "";
    clearRedaction();token = ""; sessionStorage.removeItem("agentsafe-session"); $("cards").replaceChildren(); $("file-list").replaceChildren(); document.body.classList.add("session-ended"); showError(t("ended"),true); setBusy(false);
  } catch (error) {showError(error.message,true);}
};
async function init() {
  if (!token) {ended = true; setBusy(false); showError(t("expired"),true); return;}
  try {
    let info = await api("/api/info");
    // The health probe runs independently so the first page can render quickly.
    while (info.ocr.pending && !ended) {await new Promise(resolve => setTimeout(resolve,500)); info = await api("/api/info");}
    if (ended) return;
    $("health").textContent = info.ocr.ready ? `${t("plainReady")} ${info.ocr.message}` : t("ocrUnavailable");
    $("health").classList.toggle("unavailable", !info.ocr.ready);
    const state = await api("/api/status");
    if (!busy && state.state === "done") {$("review").hidden = false; $("empty-state").hidden = true; renderResult(state);}
    else if (!busy && state.state === "running") {prepareReview(); await poll();}
  } catch (error) {showError(error.message,true);}
}
init();
