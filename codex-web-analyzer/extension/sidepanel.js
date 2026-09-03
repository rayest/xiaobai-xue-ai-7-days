const $ = id => document.getElementById(id);
let controller;
let resultText = "";

async function loadSettings() { const saved = await chrome.storage.local.get(["token", "sessionId"]); $("token").value = saved.token || ""; return saved; }
async function extractCurrentPage() {
  const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
  if (!tab?.id) throw new Error("没有找到当前标签页");
  try { const response = await chrome.tabs.sendMessage(tab.id, { type: "extract-page" }); if (response?.ok) return response.page; } catch {}
  const [result] = await chrome.scripting.executeScript({ target: { tabId: tab.id }, func: () => {
    const selection = window.getSelection()?.toString().trim() || ""; const root = document.querySelector("article, main, [role='main']") || document.body; const clone = root.cloneNode(true);
    clone.querySelectorAll("script, style, nav, header, footer, aside, form, button, input, textarea, select").forEach(node => node.remove());
    const content = (selection || clone.innerText || "").replace(/[ \t]+/g, " ").replace(/\n{4,}/g, "\n\n\n").trim().slice(0, 120000); return { title: document.title, url: location.href, content, selection };
  }});
  if (!result?.result?.content) throw new Error("无法读取此页面。请刷新普通网页后重试；chrome://、扩展商店和部分 PDF 页面不支持读取。"); return result.result;
}

function setStatus(text, type = "idle") { const el = $("status"); el.className = `status status-${type}`; el.innerHTML = `<i></i>${text}`; }
function escapeHtml(value) { return value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
function renderMarkdown(source) {
  const lines = escapeHtml(source).split("\n"); let html = "", inList = false, inCode = false;
  for (const line of lines) {
    if (line.startsWith("``")) { if (inCode) { html += "</pre>"; inCode = false; } else { html += "<pre>"; inCode = true; } continue; }
    if (inCode) { html += `${line}\n`; continue; }
    if (/^### /.test(line)) html += `<h3>${line.slice(4)}</h3>`;
    else if (/^## /.test(line)) html += `<h2>${line.slice(3)}</h2>`;
    else if (/^# /.test(line)) html += `<h1>${line.slice(2)}</h1>`;
    else if (/^[-*] /.test(line)) { if (!inList) { html += "<ul>"; inList = true; } html += `<li>${line.slice(2)}</li>`; }
    else { if (inList) { html += "</ul>"; inList = false; } if (/^> /.test(line)) html += `<blockquote>${line.slice(2)}</blockquote>`; else if (line.trim()) html += `<p>${line}</p>`; }
  }
  if (inList) html += "</ul>"; if (inCode) html += "</pre>";
  return html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
}
function updateResult() { $("result-card").classList.toggle("is-hidden", !resultText); $("empty-state").classList.toggle("is-hidden", !!resultText); $("result-preview").innerHTML = renderMarkdown(resultText); $("modal-rendered").innerHTML = renderMarkdown(resultText); $("modal-raw").textContent = resultText; $("result-count").textContent = `${resultText.length.toLocaleString()} 字`; }
function append(text) { resultText += text; updateResult(); }
async function copyResult(button) {
  if (!resultText) return;
  try {
    if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(resultText);
    else { const helper = document.createElement("textarea"); helper.value = resultText; helper.style.position = "fixed"; helper.style.opacity = "0"; document.body.appendChild(helper); helper.select(); document.execCommand("copy"); helper.remove(); }
    button.textContent = "已复制 ✓"; button.classList.add("copied"); setTimeout(() => { button.textContent = "复制内容"; button.classList.remove("copied"); }, 1600);
  } catch { button.textContent = "复制失败"; }
}

async function analyze() {
  $("analyze").disabled = true; $("stop").disabled = false; resultText = ""; updateResult(); setStatus("读取网页…", "working"); controller = new AbortController();
  try {
    const page = await extractCurrentPage(); $("page-card").classList.remove("is-hidden"); $("page-title").textContent = page.title || "无标题"; let hostname = "当前网页"; try { hostname = new URL(page.url).hostname; } catch {} $("page-meta").textContent = `${page.content.length.toLocaleString()} 字符 · ${hostname}`;
    const instruction = $("instruction").value.trim() || $("preset").value; const settings = await chrome.storage.local.get(["sessionId"]); const token = $("token").value.trim(); await chrome.storage.local.set({ token });
    const response = await fetch("http://127.0.0.1:43127/analyze", { method: "POST", signal: controller.signal, headers: { "Content-Type": "application/json", "X-Bridge-Token": token }, body: JSON.stringify({ ...page, instruction, sessionId: settings.sessionId || "" }) });
    if (!response.ok) throw new Error((await response.text()) || `Bridge HTTP ${response.status}`); setStatus("Codex 分析中…", "working");
    const reader = response.body.getReader(); const decoder = new TextDecoder(); let buffer = "";
    while (true) { const { value, done } = await reader.read(); if (done) break; buffer += decoder.decode(value, { stream: true }); const events = buffer.split("\n\n"); buffer = events.pop();
      for (const event of events) { const data = event.split("\n").find(line => line.startsWith("data: "))?.slice(6); if (!data) continue; let payload = JSON.parse(data); if (typeof payload === "string") { try { payload = JSON.parse(payload); } catch {} }
        if (event.includes("event: error")) throw new Error(payload.message || "Codex 执行失败"); if (event.includes("event: done")) { setStatus("分析完成", "done"); continue; } if (payload.type === "thread.started" && payload.thread_id) await chrome.storage.local.set({ sessionId: payload.thread_id }); if (payload.type === "item.completed" && payload.item?.type === "agent_message") append(payload.item.text || ""); if (payload.type === "error") append(`\n提示：${payload.message}\n`);
      }
    }
    if (resultText) setStatus("分析完成", "done");
  } catch (error) { if (error.name !== "AbortError") { setStatus("分析失败", "error"); append(`\n**错误：** ${error.message}`); } } finally { $("analyze").disabled = false; $("stop").disabled = true; controller = null; }
}

$("analyze").addEventListener("click", analyze); $("stop").addEventListener("click", () => controller?.abort()); $("open-result").addEventListener("click", () => $("result-modal").classList.remove("is-hidden")); $("close-result").addEventListener("click", () => $("result-modal").classList.add("is-hidden")); $("modal-copy").addEventListener("click", e => copyResult(e.currentTarget)); $("copy-result").addEventListener("click", e => copyResult(e.currentTarget));
$("toggle-token").addEventListener("click", () => { const input = $("token"); input.type = input.type === "password" ? "text" : "password"; }); $("render-tab").addEventListener("click", () => { $("render-tab").classList.add("active"); $("raw-tab").classList.remove("active"); $("modal-rendered").classList.remove("is-hidden"); $("modal-raw").classList.add("is-hidden"); }); $("raw-tab").addEventListener("click", () => { $("raw-tab").classList.add("active"); $("render-tab").classList.remove("active"); $("modal-raw").classList.remove("is-hidden"); $("modal-rendered").classList.add("is-hidden"); }); $("result-modal").addEventListener("click", e => { if (e.target.id === "result-modal") $("result-modal").classList.add("is-hidden"); });
loadSettings();
