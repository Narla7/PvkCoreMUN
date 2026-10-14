/* PVKcoreMUN — the only script on the site.
   It reveals sections as the folio is read. Nothing else moves. */

(function () {
  "use strict";

  var targets = document.querySelectorAll(".reveal");
  if (!targets.length) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function showAll() {
    for (var i = 0; i < targets.length; i++) targets[i].classList.add("shown");
  }

  if (reduce || !("IntersectionObserver" in window)) {
    showAll();
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("shown");
      io.unobserve(entry.target);
    });
  }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });

  for (var j = 0; j < targets.length; j++) io.observe(targets[j]);

  // Safety net: nothing may stay invisible because an observer callback went
  // missing. Anything still hidden after a second comes in regardless.
  window.setTimeout(showAll, 1000);
})();