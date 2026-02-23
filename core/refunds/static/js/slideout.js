const overlay = document.querySelector(".slideout-overlay");

let activePanel = null;

document.addEventListener("click", (e) => {
  // OPEN
  const openBtn = e.target.closest("[data-slideout-open]");
  if (openBtn) {
    const target = openBtn.dataset.target;
    const panel = document.querySelector(`[data-slideout-panel="${target}"]`);

    if (!panel) return;

    // close currently open panel
    if (activePanel) {
      activePanel.classList.add("translate-x-full");
    }

    panel.classList.remove("translate-x-full");
    overlay.classList.remove("d-none");
    activePanel = panel;
    return;
  }

  // CLOSE (button)
  if (e.target.closest("[data-slideout-close]")) {
    closePanel();
    return;
  }

  // CLOSE (overlay)
  if (e.target === overlay) {
    closePanel();
  }
});

function closePanel() {
  if (!activePanel) return;
  activePanel.classList.add("translate-x-full");
  overlay.classList.add("d-none");
  activePanel = null;
}
