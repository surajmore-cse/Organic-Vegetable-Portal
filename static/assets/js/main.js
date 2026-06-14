/**
* Organic Vegetable Portal - Safe Main JS (FIXED VERSION)
* This version prevents null errors + loading freeze
*/

(function () {
  "use strict";

  /**
   * Helper: Safe query selector
   */
  const select = (el, all = false) => {
    el = el.trim();
    if (all) {
      return [...document.querySelectorAll(el)];
    } else {
      return document.querySelector(el);
    }
  };

  /**
   * Helper: Event listener safe
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all);
    if (!selectEl) return;

    if (all) {
      selectEl.forEach(e => e.addEventListener(type, listener));
    } else {
      selectEl.addEventListener(type, listener);
    }
  };

  /**
   * Mobile nav toggle (FIXED)
   */
  const mobileNavToggleBtn = select('.mobile-nav-toggle');

  if (mobileNavToggleBtn) {
    on('click', '.mobile-nav-toggle', function () {
      document.body.classList.toggle('mobile-nav-active');

      mobileNavToggleBtn.classList.toggle('bi-list');
      mobileNavToggleBtn.classList.toggle('bi-x');
    });
  }

  /**
   * Preloader remove (FIXED loading freeze issue)
   */
  const preloader = select('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button (safe)
   */
  const scrollTop = select('.scroll-top');

  if (scrollTop) {
    const toggleScrollTop = () => {
      if (window.scrollY > 100) {
        scrollTop.classList.add('active');
      } else {
        scrollTop.classList.remove('active');
      }
    };

    window.addEventListener('load', toggleScrollTop);
    document.addEventListener('scroll', toggleScrollTop);

    on('click', '.scroll-top', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  /**
   * AOS init (safe)
   */
  window.addEventListener('load', () => {
    if (typeof AOS !== 'undefined') {
      AOS.init({
        duration: 600,
        easing: 'ease-in-out',
        once: true,
        mirror: false
      });
    }
  });

})();