(function () {
  'use strict';

  var root = document.documentElement;
  var header = document.getElementById('site-header');

  /* ---------- Tema claro / oscuro ---------- */
  var themeToggle = document.getElementById('theme-toggle');
  function updateThemeLabel() {
    var isDark = root.classList.contains('dark');
    themeToggle.setAttribute('aria-label', isDark ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro');
  }
  updateThemeLabel();
  themeToggle.addEventListener('click', function () {
    var isDark = root.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeLabel();
  });

  /* ---------- Encabezado: fondo al hacer scroll y ocultar al bajar ---------- */
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    header.classList.toggle('is-scrolled', y > 12);
    header.classList.toggle('is-hidden', y > lastY && y > 320);
    lastY = y;
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Menú móvil ---------- */
  var menuToggle = document.getElementById('menu-toggle');
  var mobileMenu = document.getElementById('mobile-menu');

  function setMenu(open) {
    header.classList.toggle('is-open', open);
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    mobileMenu.inert = !open;
    document.body.style.overflow = open ? 'hidden' : '';
  }

  menuToggle.addEventListener('click', function () {
    setMenu(!header.classList.contains('is-open'));
  });
  document.querySelectorAll('[data-close-menu]').forEach(function (el) {
    el.addEventListener('click', function () { setMenu(false); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && header.classList.contains('is-open')) setMenu(false);
  });
  window.matchMedia('(min-width: 768px)').addEventListener('change', function (e) {
    if (e.matches) setMenu(false);
  });

  /* ---------- Enlace activo según la sección visible ---------- */
  var navLinks = document.querySelectorAll('.nav-links a');
  var sections = Array.prototype.map.call(navLinks, function (a) {
    return document.querySelector(a.getAttribute('href'));
  }).filter(Boolean);

  if ('IntersectionObserver' in window) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (a) {
          var active = a.getAttribute('href') === '#' + entry.target.id;
          if (active) a.setAttribute('aria-current', 'true');
          else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { sectionObserver.observe(s); });
  }

  /* ---------- Animación de aparición ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var revealObserver = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el) { revealObserver.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- Formulario de reserva ---------- */
  var form = document.getElementById('reservaForm');
  var status = document.getElementById('form-status');

  var rules = {
    clase: function (v) { return !v ? 'Seleccioná una clase.' : ''; },
    name: function (v) { return v.length < 2 ? 'Escribí tu nombre y apellido.' : ''; },
    phone: function (v) { return v.replace(/\D/g, '').length < 8 ? 'Ingresá un teléfono válido (mínimo 8 dígitos).' : ''; },
    day: function (v) { return !v ? 'Seleccioná un día.' : ''; },
    time: function (v) { return !v ? 'Seleccioná un horario.' : ''; },
    entrenador: function (v) { return !v ? 'Seleccioná un entrenador.' : ''; }
  };

  function validateField(name) {
    var input = form.elements[name];
    var error = rules[name](input.value.trim());
    document.getElementById(name + '-error').textContent = error;
    input.setAttribute('aria-invalid', error ? 'true' : 'false');
    return !error;
  }

  Object.keys(rules).forEach(function (name) {
    var input = form.elements[name];
    input.addEventListener('blur', function () {
      if (this.value.trim()) validateField(name);
    });
    input.addEventListener('input', function () {
      if (this.getAttribute('aria-invalid') === 'true') validateField(name);
    });
    input.addEventListener('change', function () {
      if (this.getAttribute('aria-invalid') === 'true') validateField(name);
    });
  });

  // Al elegir una clase se sugiere el entrenador que la dicta.
  form.elements.clase.addEventListener('change', function () {
    var match = form.querySelector('#entrenador option[data-clase="' + this.value + '"]');
    if (match) {
      form.elements.entrenador.value = match.value;
      if (form.elements.entrenador.getAttribute('aria-invalid') === 'true') validateField('entrenador');
    }
  });

  function capitalizar(texto) {
    return texto.charAt(0).toUpperCase() + texto.slice(1);
  }

  // Evita que Excel interprete un texto como fórmula.
  function protegerCelda(valor) {
    return /^[=+\-@]/.test(valor) ? "'" + valor : valor;
  }

  function generarCSV(datos) {
    var encabezado = 'Cliente,Telefono,Clase,Dia,Horario,Entrenador,Nota,Fecha de Reserva';
    var fila = [
      datos.nombre,
      datos.telefono,
      capitalizar(datos.clase),
      datos.dia,
      datos.horario + 'hs',
      datos.entrenador,
      datos.nota || 'Sin nota',
      new Date().toLocaleString()
    ].map(function (dato) {
      return '"' + protegerCelda(String(dato)).replace(/"/g, '""') + '"';
    }).join(',');

    var contenido = encabezado + '\r\n' + fila + '\r\n';
    var archivo = new Blob(['\uFEFF' + contenido], { type: 'text/csv;charset=utf-8;' });

    var enlace = document.createElement('a');
    enlace.href = URL.createObjectURL(archivo);
    enlace.download = 'reserva_gym_' + datos.nombre.replace(/\s+/g, '_') + '_' + new Date().toISOString().split('T')[0] + '.csv';
    document.body.appendChild(enlace);
    enlace.click();
    enlace.remove();
    URL.revokeObjectURL(enlace.href);
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    status.className = 'form-status';

    var results = Object.keys(rules).map(validateField);
    if (results.indexOf(false) !== -1) {
      status.textContent = 'Revisá los campos marcados.';
      status.classList.add('is-error');
      var firstInvalid = form.querySelector('[aria-invalid="true"]');
      if (firstInvalid) firstInvalid.focus();
      return;
    }

    var datos = {
      nombre: form.elements.name.value.trim(),
      telefono: form.elements.phone.value.trim(),
      clase: form.elements.clase.value,
      dia: form.elements.day.value,
      horario: form.elements.time.value,
      entrenador: form.elements.entrenador.value,
      nota: form.elements.note.value.trim()
    };

    generarCSV(datos);

    status.textContent = '¡Reserva realizada! ' + capitalizar(datos.clase) + ' el ' + datos.dia + ' a las ' +
      datos.horario + 'hs con ' + datos.entrenador + '. Se descargó un CSV con los datos.';
    status.classList.add('is-success');

    form.reset();
    Object.keys(rules).forEach(function (n) { form.elements[n].removeAttribute('aria-invalid'); });
  });

  /* ---------- Año del pie ---------- */
  document.getElementById('year').textContent = new Date().getFullYear();
})();
