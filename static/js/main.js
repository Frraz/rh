(function () {
  "use strict";

  // Proteção contra duplo submit — usa flag no próprio form
  document.addEventListener("submit", function (e) {
    const form = e.target;

    // Confirmação em ações destrutivas
    const confirmMsg = form.getAttribute("data-confirm");
    if (confirmMsg && !confirm(confirmMsg)) {
      e.preventDefault();
      return;
    }

    // Bloqueia reenvio usando atributo no form
    if (form.hasAttribute("data-submitting")) {
      e.preventDefault();
      return;
    }
    form.setAttribute("data-submitting", "true");

    // Feedback visual no botão
    const btn = form.querySelector('[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.style.opacity = "0.65";
      btn.style.cursor = "not-allowed";
      btn.setAttribute("data-original", btn.innerHTML);
      btn.innerHTML = "Salvando...";
    }

    // Safety: remove bloqueio após 10s caso algo falhe
    setTimeout(function () {
      form.removeAttribute("data-submitting");
      if (btn) {
        btn.disabled = false;
        btn.style.opacity = "";
        btn.style.cursor = "";
        btn.innerHTML = btn.getAttribute("data-original") || btn.innerHTML;
      }
    }, 10000);
  }, true); // captura na fase capture para pegar antes do HTMX

  // Auto-fechar mensagens
  setTimeout(function () {
    document.querySelectorAll("[data-auto-close]").forEach(function (el) {
      el.style.transition = "opacity 0.5s";
      el.style.opacity = "0";
      setTimeout(function () { el.remove(); }, 500);
    });
  }, 5000);

  // Formatar CPF
  document.addEventListener("input", function (e) {
    if (e.target.name === "cpf") {
      var v = e.target.value.replace(/\D/g, "").slice(0, 11);
      v = v.replace(/(\d{3})(\d)/, "$1.$2");
      v = v.replace(/(\d{3})(\d)/, "$1.$2");
      v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
      e.target.value = v;
    }
    if (e.target.name === "cnpj") {
      var v = e.target.value.replace(/\D/g, "").slice(0, 14);
      v = v.replace(/^(\d{2})(\d)/, "$1.$2");
      v = v.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
      v = v.replace(/\.(\d{3})(\d)/, ".$1/$2");
      v = v.replace(/(\d{4})(\d)/, "$1-$2");
      e.target.value = v;
    }
  });

  // HTMX loading
  document.addEventListener("htmx:beforeRequest", function () {
    var el = document.getElementById("htmx-loading");
    if (el) el.classList.remove("hidden");
  });
  document.addEventListener("htmx:afterRequest", function () {
    var el = document.getElementById("htmx-loading");
    if (el) el.classList.add("hidden");
  });

}());