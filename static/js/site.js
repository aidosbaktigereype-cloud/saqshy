/* Saqshy — интерактив сайта: меню, модалка, формы заявок, метки рекламы, цели аналитики. */
(function () {
  "use strict";

  var SITE = window.SITE || { i18n: {} };
  var TRACK_KEY = "saqshy_track";
  var TRACK_FIELDS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid", "yclid"];

  /* --- Аналитика ------------------------------------------------------------ */
  function goal(name, params) {
    try {
      if (window.ym && SITE.metrika) window.ym(Number(SITE.metrika), "reachGoal", name, params || {});
      if (window.gtag) window.gtag("event", name, params || {});
    } catch (e) { /* аналитика не должна ломать сайт */ }
  }

  function leadConversion() {
    goal("lead");
    try {
      if (window.gtag) {
        window.gtag("event", "generate_lead", { currency: "KZT" });
        if (SITE.gads && SITE.gadsLabel) window.gtag("event", "conversion", { send_to: SITE.gads + "/" + SITE.gadsLabel });
      }
    } catch (e) { /* ignore */ }
  }

  document.addEventListener("click", function (event) {
    var link = event.target.closest("[data-goal]");
    if (link) goal(link.getAttribute("data-goal") + "_click");
  });

  /* --- Метки рекламы: сохраняем при входе на сайт, подставляем в формы ------ */
  function readTracking() {
    var stored = {};
    try { stored = JSON.parse(localStorage.getItem(TRACK_KEY) || "{}"); } catch (e) { stored = {}; }
    var params = new URLSearchParams(window.location.search);
    var fresh = {};
    TRACK_FIELDS.forEach(function (key) { if (params.get(key)) fresh[key] = params.get(key).slice(0, 250); });
    if (Object.keys(fresh).length) {
      stored = fresh;
      try { localStorage.setItem(TRACK_KEY, JSON.stringify(stored)); } catch (e) { /* приватный режим */ }
    }
    return stored;
  }

  var tracking = readTracking();

  function fillHidden(form) {
    TRACK_FIELDS.forEach(function (key) {
      if (form.elements[key] && tracking[key]) form.elements[key].value = tracking[key];
    });
    if (form.elements.page) form.elements.page.value = window.location.href.slice(0, 500);
    if (form.elements.ym_client_id && window.ym && SITE.metrika) {
      try { window.ym(Number(SITE.metrika), "getClientID", function (id) { form.elements.ym_client_id.value = id; }); } catch (e) { /* ignore */ }
    }
  }

  /* --- Меню ----------------------------------------------------------------- */
  var burger = document.querySelector("[data-burger]");
  if (burger) {
    burger.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  document.querySelectorAll("[data-dropdown]").forEach(function (button) {
    button.addEventListener("click", function () {
      var item = button.closest(".nav-item");
      var open = item.classList.toggle("is-open");
      button.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function (event) {
    if (!event.target.closest(".has-dropdown")) {
      document.querySelectorAll(".nav-item.is-open").forEach(function (item) {
        if (!document.body.classList.contains("nav-open")) item.classList.remove("is-open");
      });
    }
  });
  document.querySelectorAll(".main-nav a").forEach(function (link) {
    link.addEventListener("click", function () { document.body.classList.remove("nav-open"); });
  });

  /* --- Маска телефона: +7 777 123 45 67 ------------------------------------- */
  function formatPhone(value) {
    var digits = value.replace(/\D/g, "");
    if (!digits) return "";
    if (digits[0] === "8") digits = "7" + digits.slice(1);
    if (digits[0] !== "7") digits = "7" + digits;
    digits = digits.slice(0, 11);
    var parts = ["+7"];
    if (digits.length > 1) parts.push(digits.slice(1, 4));
    if (digits.length > 4) parts.push(digits.slice(4, 7));
    if (digits.length > 7) parts.push(digits.slice(7, 9));
    if (digits.length > 9) parts.push(digits.slice(9, 11));
    return parts.join(" ");
  }
  document.querySelectorAll("[data-phone]").forEach(function (input) {
    input.addEventListener("input", function () { input.value = formatPhone(input.value); });
    input.addEventListener("focus", function () { if (!input.value) input.value = "+7 "; });
    input.addEventListener("blur", function () { if (input.value.trim() === "+7") input.value = ""; });
  });

  /* --- Модальное окно заявки ------------------------------------------------ */
  var modal = document.querySelector("[data-modal]");
  function resetBox(box) {
    var form = box.querySelector("[data-lead-form]");
    var success = box.querySelector("[data-lead-success]");
    if (form && success && !success.hidden) {
      form.reset();
      form.hidden = false;
      success.hidden = true;
    }
  }
  document.querySelectorAll("[data-open-lead]").forEach(function (button) {
    button.addEventListener("click", function () {
      if (!modal) return;
      var form = modal.querySelector("[data-lead-form]");
      resetBox(modal);
      form.elements.source.value = button.getAttribute("data-source") || "callback";
      if (form.elements.service) form.elements.service.value = button.getAttribute("data-service") || "";
      form.elements.message.value = button.getAttribute("data-note") ? "Пакет: " + button.getAttribute("data-note") : "";
      document.body.classList.remove("nav-open");
      if (typeof modal.showModal === "function") modal.showModal(); else modal.setAttribute("open", "");
      goal("modal_open");
      var phone = form.querySelector("[data-phone]");
      if (phone) setTimeout(function () { phone.focus(); }, 50);
    });
  });
  if (modal) {
    modal.addEventListener("click", function (event) {
      if (event.target === modal || event.target.closest("[data-close-modal]")) modal.close();
    });
  }

  /* --- Отправка заявки ------------------------------------------------------ */
  function setError(form, name, text) {
    var holder = form.querySelector('[data-error="' + name + '"]');
    if (holder) holder.textContent = text || "";
    var field = form.elements[name] && form.elements[name].closest && form.elements[name].closest(".field");
    if (field) field.classList.toggle("has-error", Boolean(text));
  }

  document.querySelectorAll("[data-lead-form]").forEach(function (form) {
    fillHidden(form);
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var status = form.querySelector("[data-status]");
      var button = form.querySelector('button[type="submit"]');
      status.textContent = "";
      setError(form, "phone", "");
      setError(form, "consent", "");

      var digits = (form.elements.phone.value || "").replace(/\D/g, "");
      var ok = true;
      if (digits.length < 11) { setError(form, "phone", SITE.i18n.phone); ok = false; }
      if (!form.elements.consent.checked) { setError(form, "consent", SITE.i18n.consent); ok = false; }
      if (!ok) return;

      fillHidden(form);
      var data = {};
      new FormData(form).forEach(function (value, key) { data[key] = value; });
      var label = button.textContent;
      button.disabled = true;
      button.textContent = SITE.i18n.sending;

      fetch(SITE.leadUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json", "X-CSRFToken": data.csrfmiddlewaretoken },
        body: JSON.stringify(data),
        credentials: "same-origin"
      })
        .then(function (response) { return response.json().then(function (body) { return { status: response.status, body: body }; }); })
        .then(function (result) {
          if (result.body.ok) {
            var box = form.closest("[data-lead-box]") || form.parentElement;
            var success = box.querySelector("[data-lead-success]");
            form.hidden = true;
            if (success) success.hidden = false;
            leadConversion();
            return;
          }
          var errors = result.body.errors || {};
          if (errors.phone) setError(form, "phone", SITE.i18n.phone);
          if (errors.consent) setError(form, "consent", SITE.i18n.consent);
          if (errors.__all__) status.textContent = result.status === 429 ? SITE.i18n.tooMany : SITE.i18n.error;
        })
        .catch(function () { status.textContent = SITE.i18n.error; })
        .finally(function () { button.disabled = false; button.textContent = label; });
    });
  });
})();
