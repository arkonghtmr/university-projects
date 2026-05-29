function setupPageNavigation() {
  const menuButton = document.querySelector("[data-menu-button]");
  const mobileMenu = document.querySelector("[data-mobile-menu]");

  function closeMenu() {
    if (!menuButton || !mobileMenu) return;
    document.body.classList.remove("menu-open");
    menuButton.classList.remove("is-open");
    mobileMenu.classList.remove("is-open");
  }

  if (menuButton && mobileMenu) {
    menuButton.addEventListener("click", () => {
      const isOpen = mobileMenu.classList.toggle("is-open");
      menuButton.classList.toggle("is-open", isOpen);
      document.body.classList.toggle("menu-open", isOpen);
    });
  }

  document.querySelectorAll("[data-scroll]").forEach((button) => {
    button.addEventListener("click", () => {
      const target = document.getElementById(button.dataset.scroll);
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
      closeMenu();
    });
  });
}

function setupGridToggles() {
  document.querySelectorAll("[data-grid-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const frame = document.getElementById(button.dataset.gridToggle);
      if (!frame) return;

      const isHidden = frame.classList.toggle("grid-off");
      button.textContent = isHidden ? "Показать сетку" : "Скрыть сетку";
    });
  });
}

function setupModals() {
  const modals = document.querySelectorAll("[data-modal]");

  function closeAll() {
    modals.forEach((modal) => {
      modal.hidden = true;
    });
    document.body.classList.remove("modal-open");
  }

  document.querySelectorAll("[data-open-modal]").forEach((button) => {
    button.addEventListener("click", () => {
      closeAll();
      const modal = document.querySelector(`[data-modal="${button.dataset.openModal}"]`);
      if (!modal) return;
      modal.hidden = false;
      document.body.classList.add("modal-open");
    });
  });

  document.querySelectorAll("[data-close-modal]").forEach((button) => {
    button.addEventListener("click", closeAll);
  });

  modals.forEach((modal) => {
    modal.addEventListener("click", (event) => {
      if (event.target === modal) closeAll();
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeAll();
  });
}

function setupAccordions() {
  document.querySelectorAll("[data-accordion-trigger]").forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const item = trigger.closest("[data-accordion-item]");
      const list = item.closest("[data-accordion-list]");
      const isOpen = item.classList.contains("is-open");

      if (list) {
        list.querySelectorAll("[data-accordion-item]").forEach((entry) => {
          entry.classList.remove("is-open");
        });
      }

      if (!isOpen) item.classList.add("is-open");
    });
  });
}

function setupWireMenu() {
  const button = document.querySelector("[data-wire-menu]");
  const panel = document.querySelector("[data-wire-menu-panel]");
  if (!button || !panel) return;

  button.addEventListener("click", () => {
    panel.classList.toggle("is-open");
  });
}

setupPageNavigation();
setupGridToggles();
setupModals();
setupAccordions();
setupWireMenu();
