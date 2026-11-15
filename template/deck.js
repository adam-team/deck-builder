/* Движок презентации Deck Builder: один файл без зависимостей.
   Слайды — <section class="slide"> внутри .deck. Переход задаётся классом на <body>: t-fade, t-slide, t-zoom, t-convex,
   t-cube, t-flip, t-cards, t-orbit, t-none. Появление элементов (.f) по шагам: a-up, a-zoom, a-blur, a-left.
   Управление: → пробел PageDown — дальше, ← PageUp — назад, F — во весь экран, Home/End, клик по правой/левой половине, свайп.
   Параметры адреса: #5 — открыть слайд 5; ?autoplay=1800 — листать само (мс на шаг); ?print — все слайды подряд для PDF. */
(function () {
  var body = document.body, stage = document.querySelector('.stage'), deck = document.querySelector('.deck');
  var slides = [].slice.call(document.querySelectorAll('.slide'));
  var params = new URLSearchParams(location.search);
  var cur = 0, step = 0, busy = false, DUR = 900;

  if (params.has('print')) { body.classList.add('print'); slides.forEach(function (s) { s.classList.add('on'); }); return; }

  function fit() {
    var w = deck.offsetWidth, h = deck.offsetHeight;
    var k = Math.min(innerWidth / w, innerHeight / h);
    stage.style.transform = 'translate(-50%,-50%) scale(' + k + ')';
  }
  addEventListener('resize', fit); fit();

  function frags(i) { return [].slice.call(slides[i].querySelectorAll('.f')); }
  function setFrags(i, n) { frags(i).forEach(function (f, k) { f.classList.toggle('shown', k < n); }); }

  var bar = document.querySelector('.progress i'), num = document.querySelector('.counter');
  function ui() {
    if (bar) bar.style.width = ((cur + 1) / slides.length * 100) + '%';
    if (num) num.textContent = (cur + 1) + ' / ' + slides.length;
    history.replaceState(null, '', '#' + (cur + 1));
  }

  function show(i, dir) {
    if (i === cur || i < 0 || i >= slides.length || busy) return;
    var a = slides[cur], b = slides[i];
    busy = true;
    var cls = dir > 0 ? ['out-next', 'in-next'] : ['out-prev', 'in-prev'];
    a.classList.add(cls[0]); b.classList.add('on', cls[1]);
    setFrags(i, dir > 0 ? 0 : frags(i).length);
    setTimeout(function () {
      a.classList.remove('on', cls[0]); b.classList.remove(cls[1]);
      busy = false;
    }, body.classList.contains('t-none') ? 0 : DUR);
    cur = i; step = dir > 0 ? 0 : frags(i).length; ui();
  }

  function next() { var f = frags(cur); if (step < f.length) { f[step].classList.add('shown'); step++; return; } show(cur + 1, 1); }
  function prev() { if (step > 0) { step--; frags(cur)[step].classList.remove('shown'); return; } show(cur - 1, -1); }

  addEventListener('keydown', function (e) {
    if (['ArrowRight', 'ArrowDown', ' ', 'PageDown', 'Enter'].indexOf(e.key) >= 0) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].indexOf(e.key) >= 0) { e.preventDefault(); prev(); }
    else if (e.key === 'Home') show(0, -1);
    else if (e.key === 'End') show(slides.length - 1, 1);
    else if (e.key === 'f' || e.key === 'F' || e.key === 'а' || e.key === 'А') {
      if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen().catch(function () {});
    }
  });
  addEventListener('click', function (e) { if (e.target.closest('a,button')) return; (e.clientX > innerWidth / 3 ? next : prev)(); });
  var x0 = null;
  addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  addEventListener('touchend', function (e) { if (x0 === null) return; var d = e.changedTouches[0].clientX - x0; if (Math.abs(d) > 40) (d < 0 ? next : prev)(); x0 = null; });

  var start = Math.max(0, Math.min(slides.length - 1, (parseInt(location.hash.slice(1)) || 1) - 1));
  cur = start; slides[cur].classList.add('on'); setFrags(cur, 0); ui();

  // Автолистание (для показа и записи превью): слайды сами сменяются, элементы появляются волной без кликов.
  function autoplay(ms) {
    body.classList.add('auto');
    function wave() { frags(cur).forEach(function (f, k) { setTimeout(function () { f.classList.add('shown'); }, 250 + k * 160); }); step = frags(cur).length; }
    wave();
    setInterval(function () { if (cur < slides.length - 1) { show(cur + 1, 1); setTimeout(wave, DUR * 0.6); } }, ms);
  }
  window.deckAuto = autoplay;
  var auto = parseInt(params.get('autoplay'));
  if (auto) autoplay(auto);
})();
