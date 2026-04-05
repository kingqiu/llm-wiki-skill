/**
 * LLM Wiki — Bilingual Toggle
 * Shows/hides Chinese translations (.zh-trans elements) on each page.
 * State is persisted in localStorage and survives SPA navigation.
 */

const STORAGE_KEY = "llm-wiki-bilingual"

function getBilingualState(): boolean {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored !== null) return stored === "true"
  return false
}

function setBilingualState(enabled: boolean) {
  localStorage.setItem(STORAGE_KEY, String(enabled))
}

function applyBilingualState(enabled: boolean) {
  document.querySelectorAll<HTMLElement>(".zh-trans").forEach((el) => {
    el.style.display = enabled ? "block" : "none"
  })
  const btn = document.getElementById("bilingual-toggle")
  if (btn) {
    btn.setAttribute("aria-pressed", String(enabled))
    btn.title = enabled ? "Hide Chinese translation" : "Show Chinese translation"
    btn.classList.toggle("active", enabled)
  }
}

document.addEventListener("nav", () => {
  const btn = document.getElementById("bilingual-toggle")
  if (btn) {
    btn.addEventListener("click", () => {
      const next = !getBilingualState()
      setBilingualState(next)
      applyBilingualState(next)
    })
  }
  applyBilingualState(getBilingualState())
})
