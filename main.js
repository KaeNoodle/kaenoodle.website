/* ============================================================
   KAENOODLE — shared behaviour
   Loaded by every page with <script src="js/main.js" defer>.
   `defer` means the browser parses the HTML first and runs this
   after, so the elements always exist by the time we query them.
   ============================================================ */

/* ---------- Mobile nav ------------------------------------- */
/* Below 860px the links collapse behind a Menu button. The
   button's aria-expanded is what tells a screen reader whether
   the menu is open, so it has to stay in sync with the class. */
const toggle = document.querySelector('.nav-toggle');
const links  = document.querySelector('.nav-links');

if (toggle && links) {
  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  // Close on Escape, and return focus to the button so keyboard
  // users don't get stranded inside a hidden menu.
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && links.classList.contains('open')) {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });
}

/* ---------- Gallery reveal --------------------------------- */
/* Only used on the long grids (fursuits, art, projects).
   IntersectionObserver is handled by the browser off the main
   thread, so it's much cheaper than a scroll listener that
   measures every element on every frame. */
const items = document.querySelectorAll('.reveal');

if (items.length) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('in');
      observer.unobserve(entry.target);   // reveal once, then stop watching
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

  items.forEach((el, i) => {
    el.style.transitionDelay = (i % 3) * 60 + 'ms';   // stagger across a row
    observer.observe(el);
  });
}

/* ---------- Footer year ------------------------------------ */
const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();
