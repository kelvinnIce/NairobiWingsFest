(function () {
  // the ticket reads differently for each lane
  var COPY = {
    attendee: { admit: "One hungry guest", h: "Your ticket is your vote", btn: "Get my ticket first" },
    vendor: { admit: "One wing kitchen", h: "Hold your spot", btn: "Apply for a spot" },
    sponsor: { admit: "One founding partner", h: "Start the talk", btn: "Talk to us first" }
  };
  function sync() {
    var r = document.querySelector('input[name="role"]:checked');
    var c = COPY[r ? r.value : "attendee"] || COPY.attendee;
    var set = function (sel, t) { var e = document.querySelector(sel); if (e) e.textContent = t; };
    set("[data-admit]", c.admit); set("[data-stub-h]", c.h); set("[data-stub-btn]", c.btn);
  }
  document.querySelectorAll('input[name="role"]').forEach(function (i) { i.addEventListener("change", sync); });
  document.querySelectorAll("[data-role-link]").forEach(function (a) { a.addEventListener("click", function () { setTimeout(sync, 0); }); });
  sync();
})();
