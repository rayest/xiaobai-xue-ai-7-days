function extractPage() {
  const selection = window.getSelection()?.toString().trim() || "";
  const root = document.querySelector("article, main, [role='main']") || document.body;
  const clone = root.cloneNode(true);
  clone.querySelectorAll("script, style, nav, header, footer, aside, form, button, input, textarea, select").forEach(node => node.remove());
  const content = (selection || clone.innerText || "")
    .replace(/[ \t]+/g, " ")
    .replace(/\n{4,}/g, "\n\n\n")
    .trim()
    .slice(0, 120000);
  return { title: document.title, url: location.href, content, selection };
}

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message?.type === "extract-page") {
    try { sendResponse({ ok: true, page: extractPage() }); }
    catch (error) { sendResponse({ ok: false, error: error.message }); }
  }
  return true;
});
