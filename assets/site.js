(function () {
  var header = document.querySelector(".mast");
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  if (header && document.querySelector(".hero") && "ResizeObserver" in window) {
    new ResizeObserver(function () {
      document.documentElement.style.setProperty("--mast-height", header.offsetHeight + "px");
    }).observe(header);
  }

  if (header && toggle && nav) {
    document.documentElement.classList.add("nav-ready");
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

})();
