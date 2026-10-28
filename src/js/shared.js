(function () {
  // ---- Edit these as the project firms up ----
  var NWF = (window.NWF = {
    // Set once the date is locked, e.g. "2027-04-17T10:00:00+03:00". The countdown appears automatically.
    EVENT_DATE: null,
    // Where early-list signups are sent (Formspree, Airtable webhook, etc). Empty means the form only shows its confirmation.
    FORM_ENDPOINT: "",
    TOTAL_SPOTS: 20,
    // Add vendors as they confirm: [{ name: "Spot name" }]. Open spots fill in around them.
    CONFIRMED_VENDORS: []
  });

  function pad(n) { return String(n).padStart(2, "0"); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]; }); }

  document.querySelectorAll("[data-countdown]").forEach(function (el) {
    if (!NWF.EVENT_DATE) { el.textContent = el.getAttribute("data-fallback") || ""; return; }
    var target = new Date(NWF.EVENT_DATE).getTime();
    function tick() {
      var ms = target - Date.now();
      if (ms <= 0) { el.textContent = "Today is the day."; return; }
      var d = Math.floor(ms / 864e5), h = Math.floor((ms % 864e5) / 36e5), m = Math.floor((ms % 36e5) / 6e4);
      el.textContent = d + " days, " + h + " hours, " + m + " minutes to go";
    }
    tick(); setInterval(tick, 30000);
  });

  document.querySelectorAll("[data-slots]").forEach(function (ul) {
    for (var i = 0; i < NWF.TOTAL_SPOTS; i++) {
      var v = NWF.CONFIRMED_VENDORS[i];
      var li = document.createElement("li");
      li.className = "slot " + (v ? "is-taken" : "is-open");
      li.innerHTML = '<span class="slot-n">' + pad(i + 1) + '</span><span class="slot-name">' + (v ? esc(v.name) : "Open") + "</span>";
      ul.appendChild(li);
    }
  });

  var MESSAGES = {
    attendee: "You are on the list. We email you first when the date and venue lock.",
    vendor: "Got it. We will be in touch about your spot.",
    sponsor: "Got it. We will send the founding partner details."
  };

  document.querySelectorAll("form[data-signup]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      var msg = form.querySelector("[data-signup-msg]");
      var btn = form.querySelector("button[type=submit]");
      if (btn) btn.disabled = true;
      var send = NWF.FORM_ENDPOINT
        ? fetch(NWF.FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) })
        : Promise.resolve();
      send.then(function () {
        var scope = form.closest("[data-signup-scope]") || form;
        scope.classList.add("is-done");
        if (msg) msg.textContent = MESSAGES[data.role || "attendee"] || MESSAGES.attendee;
      }).catch(function () {
        if (msg) msg.textContent = "That did not send. Check your connection and try again.";
        if (btn) btn.disabled = false;
      });
    });
  });

  document.querySelectorAll("[data-role-link]").forEach(function (a) {
    a.addEventListener("click", function () {
      var r = document.querySelector('input[name="role"][value="' + a.getAttribute("data-role-link") + '"]');
      if (r) r.checked = true;
    });
  });
})();
