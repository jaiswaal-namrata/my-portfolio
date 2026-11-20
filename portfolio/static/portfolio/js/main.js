(function () {
  'use strict';

  var revealItems = document.querySelectorAll('[data-reveal]');
  var prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (revealItems.length && 'IntersectionObserver' in window && !prefersReducedMotion) {
    var revealObserver = new IntersectionObserver(function (entries, observer) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -36px 0px' });

    document.documentElement.classList.add('has-scroll-reveal');
    revealItems.forEach(function (item) {
      revealObserver.observe(item);
    });
  }

  var menuButton = document.querySelector('.menu-toggle');
  var menu = document.querySelector('.nav-links');

  function closeMenu() {
    if (!menuButton || !menu) {
      return;
    }

    menu.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Open navigation menu');
  }

  if (menuButton && menu) {
    menuButton.addEventListener('click', function () {
      var isOpen = menu.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(isOpen));
      menuButton.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
    });

    menu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMenu);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menu.classList.contains('is-open')) {
        closeMenu();
        menuButton.focus();
      }
    });
  }

  document.querySelectorAll('.contact-form input, .contact-form textarea').forEach(function (field) {
    field.addEventListener('invalid', function () {
      field.setAttribute('aria-invalid', 'true');
    });

    field.addEventListener('input', function () {
      if (field.checkValidity()) {
        field.removeAttribute('aria-invalid');
      }
    });
  });
}());
