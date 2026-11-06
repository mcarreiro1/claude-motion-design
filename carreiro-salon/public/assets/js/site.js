(function () {
  var body = document.body;

  // Header hairline once the page scrolls
  var header = document.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  var toggle = document.querySelector('.menu-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    document.querySelectorAll('.nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        body.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Reserve: choose a location, then go to that location's online booking
  var panel = document.getElementById('reserve-panel');
  var lastFocus = null;
  function openReserve(e) {
    if (!panel) return;
    e.preventDefault();
    body.classList.remove('menu-open');
    lastFocus = document.activeElement;
    panel.hidden = false;
    body.style.overflow = 'hidden';
    var first = panel.querySelector('.reserve-option');
    if (first) first.focus();
  }
  function closeReserve() {
    if (!panel || panel.hidden) return;
    panel.hidden = true;
    body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }
  document.querySelectorAll('[data-reserve]').forEach(function (el) { el.addEventListener('click', openReserve); });
  if (panel) {
    panel.addEventListener('click', function (e) { if (e.target === panel) closeReserve(); });
    panel.querySelector('.reserve-close').addEventListener('click', closeReserve);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeReserve(); });
  }

  // Newsletter (Netlify Forms, submitted in place)
  document.querySelectorAll('form[data-signup]').forEach(function (form) {
    var status = form.querySelector('.form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = form.querySelector('input[type="email"]');
      if (!email.value || !email.checkValidity()) {
        status.textContent = 'Please enter a valid email address, like name@example.com.';
        email.focus();
        return;
      }
      status.textContent = 'Signing you up…';
      var data = new URLSearchParams(new FormData(form)).toString();
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: data })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset();
          status.textContent = 'Thank you! You’re on the list.';
        })
        .catch(function () {
          status.textContent = 'We couldn’t sign you up just now. Please try again, or follow us on Instagram @carreirothestudio.';
        });
    });
  });

  // Journal category filters
  var filterBar = document.querySelector('.filters');
  if (filterBar) {
    var items = document.querySelectorAll('[data-cats]');
    filterBar.addEventListener('click', function (e) {
      var btn = e.target.closest('button');
      if (!btn) return;
      filterBar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
      var cat = btn.getAttribute('data-filter');
      items.forEach(function (it) {
        it.hidden = !(cat === 'all' || it.getAttribute('data-cats').split('|').indexOf(cat) !== -1);
      });
    });
  }
})();
