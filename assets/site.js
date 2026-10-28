(function () {
  var header = document.querySelector(".mast");
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  if (header && toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        header.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && header.classList.contains("is-open")) {
        header.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  var buttons = document.querySelectorAll("[data-copy-link]");
  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      var url = window.location.href;
      var status = button.nextElementSibling;

      function report(message) {
        if (status) status.textContent = message;
      }

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(
          function () {
            report("Copied.");
          },
          function () {
            report("Copy did not work. Use the address at the top of the browser.");
          }
        );
      } else {
        report("Copy did not work. Use the address at the top of the browser.");
      }
    });
  });
})();
