(function () {
  // show the floating button once the hero is out of view
  var hero = document.getElementById("top");
  if (hero && "IntersectionObserver" in window) {
    new IntersectionObserver(function (e) {
      document.body.classList.toggle("past-hero", !e[0].isIntersecting);
    }, { threshold: 0.05 }).observe(hero);
  }
  // carousel buttons
  document.querySelectorAll("[data-scroll]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var rail = document.querySelector(btn.getAttribute("data-target"));
      if (!rail) return;
      var step = rail.clientWidth * 0.8 * (btn.getAttribute("data-scroll") === "next" ? 1 : -1);
      rail.scrollBy({ left: step, behavior: "smooth" });
    });
  });
})();
