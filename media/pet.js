(function () {
  const vscode = acquireVsCodeApi();
  const stage = document.getElementById('stage');
  const sky = document.getElementById('sky');
  const sizes = { small: 80, medium: 120, large: 170 };
  const speeds = { slow: 0.5, normal: 1, fast: 1.8 };
  const phrases = [
    'Ordem e Progresso!', 'Bora codar! 🇧🇷', 'Deploy na sexta? Coragem!',
    'Salve, dev!', 'Compilou de primeira? Milagre!', 'Bug é só feature sem documentação',
    'Vai, Brasil!', 'Café com pão de queijo ☕', 'Commit feito, alma lavada!',
  ];
  const colors = ['#009c3b', '#ffdf00', '#002776', '#ffffff'];
  // Speeds are px per 16.7ms frame, scaled by real elapsed time so 120/144 Hz screens don't run faster.
  const FRAME_MS = 1000 / 60;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let x = 20, dir = 1, speed = 1, idleUntil = 0, last = 0;

  stage.innerHTML = window.flagSvg();

  function say(text) {
    const old = stage.querySelector('.bubble');
    if (old) old.remove();
    const b = document.createElement('div');
    b.className = 'bubble';
    b.textContent = text || phrases[Math.floor(Math.random() * phrases.length)];
    stage.appendChild(b);
    setTimeout(() => b.remove(), 2500);
  }

  function confetti() {
    for (let i = 0; i < 40; i++) {
      const c = document.createElement('div');
      c.className = 'confetti';
      c.style.left = Math.random() * 100 + '%';
      c.style.background = colors[i % colors.length];
      c.style.setProperty('--h', window.innerHeight + 'px');
      c.style.animationDelay = Math.random() * 0.4 + 's';
      sky.appendChild(c);
      setTimeout(() => c.remove(), 2500);
    }
  }

  function cheer() {
    stage.classList.remove('jump');
    void stage.offsetWidth;
    stage.classList.add('jump');
    say('GOOOOL! 🎉');
    confetti();
  }

  function tick(time) {
    const now = Date.now();
    // Clamp the step so a backgrounded tab doesn't teleport the pet when it resumes.
    const frames = last ? Math.min((time - last) / FRAME_MS, 4) : 1;
    last = time;
    // Reduced motion: the pet stands still instead of pacing across the panel.
    const idle = now < idleUntil || reduceMotion.matches;
    stage.classList.toggle('idle', idle);
    if (!idle) {
      const max = Math.max(0, window.innerWidth - stage.offsetWidth);
      x += dir * speed * frames;
      if (x <= 0 || x >= max) { dir = -dir; x = Math.min(max, Math.max(0, x)); }
      if (Math.random() < 0.002) idleUntil = now + 1500 + Math.random() * 2000;
    }
    stage.style.transform = `translateX(${x}px)`;
    requestAnimationFrame(tick);
  }

  stage.setAttribute('role', 'button');
  stage.setAttribute('tabindex', '0');
  stage.setAttribute('aria-label', 'Bandeirinha: clique para comemorar');
  stage.addEventListener('click', cheer);
  stage.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); cheer(); }
  });
  window.addEventListener('message', ({ data }) => {
    if (data.type === 'cheer') cheer();
    if (data.type === 'config') {
      stage.style.width = (sizes[data.size] || sizes.medium) + 'px';
      speed = speeds[data.speed] || 1;
    }
  });
  vscode.postMessage({ type: 'ready' });
  say('Salve! Sou a Bandeirinha 🇧🇷');
  requestAnimationFrame(tick);
})();
