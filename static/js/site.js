(function () {
  // Mobile menu
  var mb = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (mb) mb.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    mb.setAttribute('aria-expanded', open);
  });

  // Hero: balloon ring built around the neon sign
  var ring = document.getElementById('ring');
  if (ring) {
    var seed = 11;
    var rnd = function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
    var palette = ['#f7b5cf', '#ef7fa6', '#8e5bd6', '#b99af0', '#f6f0ff', '#e4b04a', '#d99a86', '#c9ccd6'];
    var N = 56, frag = document.createDocumentFragment();
    for (var i = 0; i < N; i++) {
      var a = (i / N) * Math.PI * 2 - Math.PI / 2;
      var r = 43 + (rnd() - 0.5) * 3;
      var size = 9 + rnd() * 6;
      var b = document.createElement('i');
      b.className = 'b' + (rnd() > 0.7 ? ' chrome' : '');
      b.style.cssText = '--x:' + (50 + r * Math.cos(a)).toFixed(2) + '%;--y:' + (50 + r * Math.sin(a)).toFixed(2) +
        '%;--s:' + size.toFixed(1) + '%;--c:' + palette[Math.floor(i / 4 + rnd() * 1.6) % palette.length] +
        ';--d:' + (i * 22) + 'ms';
      frag.appendChild(b);
    }
    ring.appendChild(frag);
    var input = document.getElementById('nameInput'), out = document.getElementById('neonName');
    input.addEventListener('input', function () { out.textContent = input.value.trim() || 'Your name'; });
  }

  // Lightbox
  var lb = document.getElementById('lightbox');
  var grid = document.querySelector('.lb');
  if (lb && grid) {
    var big = lb.querySelector('img');
    var open = function (fig) { big.src = fig.querySelector('img').src; big.alt = fig.querySelector('img').alt; lb.showModal(); };
    grid.addEventListener('click', function (e) { var f = e.target.closest('figure'); if (f) open(f); });
    grid.addEventListener('keydown', function (e) { if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('figure')) { e.preventDefault(); open(e.target); } });
    lb.addEventListener('click', function () { lb.close(); });
  }

  // Gallery filter
  document.querySelectorAll('.chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
      document.querySelectorAll('.chip').forEach(function (c) { c.classList.toggle('on', c === chip); });
      var f = chip.dataset.filter;
      document.querySelectorAll('#grid figure').forEach(function (fig) { fig.hidden = !(f === 'all' || fig.dataset.cat === f); });
    });
  });
})();
