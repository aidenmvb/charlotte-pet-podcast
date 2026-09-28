(function () {
  var buttons = document.querySelectorAll("[data-copy-link]");
  if (!buttons.length) return;

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
