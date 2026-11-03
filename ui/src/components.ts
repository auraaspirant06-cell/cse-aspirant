/**
 * CSE Aspirant - Web Dashboard UI Components
 */
export function updateMetricCard(elementId: string, value: string | number) {
  const el = document.getElementById(elementId);
  if (el) {
    el.textContent = String(value);
  }
}

export function renderKeyBadge(key: string): string {
  const escapedKey = key.replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "'": "&#39;",
    '"': "&quot;"
  }[character] || character));
  return `<span style="padding: 6px 12px; background: #1e293b; border-radius: 6px; border: 1px solid #334155;">🔑 ${escapedKey}</span>`;
}

