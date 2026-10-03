// Bandeirinha: bandeira do Brasil (proporção 20:14) com olhos e perninhas.
window.flagSvg = function () {
  const stars = [[330, 225], [372, 215], [400, 240], [300, 255], [345, 290], [420, 285], [318, 205]]
    .map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3.2" fill="#fff"/>`)
    .join('');
  return `
<svg viewBox="0 0 720 710" xmlns="http://www.w3.org/2000/svg" aria-label="Bandeirinha do Brasil">
  <ellipse cx="360" cy="690" rx="230" ry="16" fill="#00000055"/>
  <g class="leg l1"><rect x="215" y="490" width="44" height="170" rx="20" fill="#ffdf00"/><ellipse cx="237" cy="672" rx="62" ry="24" fill="#fff" stroke="#009c3b" stroke-width="8"/></g>
  <g class="leg l2"><rect x="461" y="490" width="44" height="170" rx="20" fill="#ffdf00"/><ellipse cx="483" cy="672" rx="62" ry="24" fill="#fff" stroke="#009c3b" stroke-width="8"/></g>
  <rect class="pole" x="-6" y="0" width="22" height="600" rx="10" fill="#ffdf00" stroke="#0b1c3d" stroke-width="3"/>
  <g class="cloth">
    <clipPath id="c"><rect x="0" y="0" width="720" height="504"/></clipPath>
    <g clip-path="url(#c)">
      <rect width="720" height="504" fill="#009c3b"/>
      <polygon points="61,252 360,61 659,252 360,443" fill="#ffdf00"/>
      <circle cx="360" cy="252" r="126" fill="#002776"/>
      <clipPath id="d"><circle cx="360" cy="252" r="126"/></clipPath>
      <g clip-path="url(#d)">
        ${stars}
        <path id="band" d="M 232 300 Q 360 250 488 200" fill="none" stroke="#fff" stroke-width="30"/>
        <text font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#009c3b">
          <textPath href="#band" startOffset="50%" text-anchor="middle" dy="5">ORDEM E PROGRESSO</textPath>
        </text>
      </g>
    </g>
    <g class="eyes">
      <ellipse cx="270" cy="400" rx="26" ry="32" fill="#fff"/><circle class="pupil" cx="276" cy="404" r="13" fill="#0b1c3d"/>
      <ellipse cx="450" cy="400" rx="26" ry="32" fill="#fff"/><circle class="pupil" cx="456" cy="404" r="13" fill="#0b1c3d"/>
    </g>
    <path d="M 325 430 Q 360 470 395 430" fill="none" stroke="#0b1c3d" stroke-width="7" stroke-linecap="round"/>
  </g>
</svg>`;
};
