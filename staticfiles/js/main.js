// Configuração HTMX
document.addEventListener("DOMContentLoaded", function () {
  // Indicador global de loading para requisições HTMX
  htmx.on("htmx:beforeRequest", function () {
    document.getElementById("global-loading")?.classList.remove("hidden");
  });

  htmx.on("htmx:afterRequest", function () {
    document.getElementById("global-loading")?.classList.add("hidden");
  });

  // Auto-fechar mensagens de alerta após 5 segundos
  setTimeout(function () {
    document.querySelectorAll("[data-auto-close]").forEach(function (el) {
      el.style.transition = "opacity 0.5s";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 500);
    });
  }, 5000);

  // Confirmar ações perigosas (forms com data-confirm)
  document.addEventListener("submit", function (e) {
    const form = e.target;
    const msg = form.getAttribute("data-confirm");
    if (msg && !confirm(msg)) {
      e.preventDefault();
    }
  });
});

// Formata CPF enquanto o usuário digita
function formatCPF(input) {
  let v = input.value.replace(/\D/g, "");
  if (v.length <= 11) {
    v = v.replace(/(\d{3})(\d)/, "$1.$2");
    v = v.replace(/(\d{3})(\d)/, "$1.$2");
    v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
  }
  input.value = v;
}