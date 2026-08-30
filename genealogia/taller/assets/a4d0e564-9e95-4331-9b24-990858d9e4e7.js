/* Shared type/layout rules for the Genealogía reader.
   Same HTML is used by the paginator's measurer and by the rendered page,
   so measured heights and painted heights are identical.
   Sizes come from the printed volume (memoir, 15.5 × 23 cm). */

export const C = { vino: '#7D4343', tinta: '#1C1B1A', gris: '#767070', crema: '#F7F4EF' };
export const TRIM = { w: 439.37, h: 651.97, top: 56.7, side: 62.4, bottom: 82.2 };
export const BODY = 'var(--font-body)';
export const HEAD = 'var(--font-heading)';

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/* ---------- guionizacion espanola ----------
   El Chromium de composicion no trae diccionario de particion, asi que la
   justificacion quedaba floja. Se insertan guiones blandos por silabeo
   regular del espanol (grupos de ataque, digrafos, diptongos e hiatos);
   los no usados no dejan rastro en la capa de texto del PDF y los usados
   imprimen el guion de fin de linea, como en la edicion XeLaTeX. */
function silabas(w) {
  const V = 'aeiouáéíóúü';
  const lw = w.toLowerCase();
  const isV = (c) => V.includes(c);
  const onset = { pr:1, br:1, tr:1, dr:1, cr:1, gr:1, fr:1, kr:1,
                  pl:1, bl:1, cl:1, gl:1, fl:1, kl:1, ch:1, ll:1, rr:1 };
  const fuertes = 'aeoáéó';
  const tildeDebil = 'íú';
  const out = []; let cur = ''; let i = 0; const n = w.length;
  while (i < n) {
    cur += w[i];
    if (!isV(lw[i])) { i++; continue; }
    while (i + 1 < n && isV(lw[i + 1])) {
      const a = lw[i], b = lw[i + 1];
      if (fuertes.includes(a) && fuertes.includes(b)) break;   // hiato a-e
      if (tildeDebil.includes(a) || tildeDebil.includes(b)) break; // hiato con tilde
      cur += w[i + 1]; i++;
    }
    let j = i + 1, cons = '';
    while (j < n && !isV(lw[j])) { cons += lw[j]; j++; }
    if (j >= n) { cur += w.slice(i + 1); out.push(cur); return out; }
    let keep;
    if (cons.length === 0) keep = 0;
    else if (cons.length === 1) keep = 1;
    else keep = onset[cons.slice(-2)] ? 2 : 1;
    const stay = cons.length - keep;
    cur += w.slice(i + 1, i + 1 + stay);
    out.push(cur); cur = '';
    i = i + 1 + stay;
  }
  if (cur) out.push(cur);
  return out;
}
function guionizar(texto) {
  return String(texto).replace(/[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{7,}/g, (w) => {
    const sil = silabas(w);
    if (sil.length < 2) return w;
    let outp = sil[0]; let izq = sil[0].length;
    for (let k = 1; k < sil.length; k++) {
      const der = sil.slice(k).join('').length;
      if (izq >= 3 && der >= 3) outp += '\u00ad';
      outp += sil[k]; izq += sil[k].length;
    }
    return outp;
  });
}

/* ---------- inline ---------- */
export function partsHtml(parts, o = {}) {
  let out = '';
  for (const p of parts || []) {
    if (p.br) { out += '<br>'; continue; }
    let x = esc(o.hyph && !p.url ? guionizar(p.x) : p.x);
    if (p.cap) { out += x; continue; }  // capitular retirada por decisión del compilador: letra normal
    if (p.sc) x = `<span style="font-variant:small-caps;text-transform:lowercase">${x}</span>`;
    if (p.ls) x = `<span style="letter-spacing:0.1em;word-spacing:-0.1em">${x}</span>`;
    if (p.i) x = `<em>${x}</em>`;
    if (p.b) x = `<strong style="font-weight:600">${x}</strong>`;
    if (p.sup) x = `<sup style="font-size:0.66em;line-height:0">${x}</sup>`;
    // Las direcciones se componen como texto, no como enlace vivo: el aparato
    // debe leerse igual en pantalla y fuera de ella, y una referencia no
    // depende de que su destino siga en pie.
    if (p.url) x = `<span style="overflow-wrap:anywhere">${x}</span>`;
    out += x;
  }
  return out;
}

export const blockText = (b) => (b.parts ? b.parts.map((p) => (p.br ? ' ' : p.x || '')).join('')
  : b.lines ? b.lines.map((l) => l.map((p) => p.x || '').join(' ')).join(' ')
  : b.title ? b.title + (b.sub ? ' ' + b.sub : '') : '');

/* ---------- word slicing (page splits) ---------- */
export function wordCount(b) {
  // Debe contar exactamente como indexa sliceBlock(), que recorre fragmento por
  // fragmento. blockText() concatena los fragmentos sin separador, de modo que
  // una palabra repartida entre dos —una versalita o una cursiva pegada a su
  // puntuacion, «siglo xiii.»— valia una aqui y dos alli. El paginador acota su
  // busqueda con este numero: si el corte caia justo en el tope, la cola del
  // bloque quedaba fuera de la pagina y no se componia en ninguna otra, sin
  // dejar rastro. Hoy no se pierde texto en el libro, pero la trampa seguia
  // armada para la proxima edicion.
  if (!b.parts) return blockText(b).trim().split(/\s+/).filter(Boolean).length;
  let n = 0;
  for (const p of b.parts) {
    if (p.br) continue;
    n += (p.x || '').split(/\s+/).filter(Boolean).length;
  }
  return n;
}
export function sliceBlock(b, from, to) {
  if (from == null && to == null) return b;
  const parts = [];
  let n = 0;
  for (const p of b.parts || []) {
    if (p.br) { if (n > (from || 0) && n < (to == null ? Infinity : to)) parts.push(p); continue; }
    const words = (p.x || '').split(/(\s+)/);
    const lead = /^\s/.test(p.x || '') ? ' ' : '';   // el espacio inicial del fragmento
    let kept = '';                                    // se perdia al cortar: se conserva
    for (const w of words) {
      if (w === '') continue;                         // el split deja cadenas vacias
      if (/^\s+$/.test(w)) { if (kept) kept += ' '; continue; }
      const idx = n++;
      if (idx >= (from || 0) && idx < (to == null ? Infinity : to)) kept += (kept && !/\s$/.test(kept) ? ' ' : '') + w;
    }
    if (kept.trim()) parts.push({ ...p, x: lead + kept });
  }
  return { ...b, parts, w: [from || 0, to == null ? n : to] };
}

/* ---------- block styles ---------- */
function css(o) {
  // El letter-spacing de un texto plano (no envuelto palabra por palabra en
  // spans) se suma tambien tras el caracter de espacio, de modo que el hueco
  // entre palabras crece el doble que el hueco entre letras -- se lee como
  // un espacio de mas. Un word-spacing negativo, igual al letter-spacing,
  // cancela ese doble conteo sin tocar cada sitio de llamada.
  if (o.letterSpacing !== undefined && o.letterSpacing !== null && o.wordSpacing === undefined) {
    const m = /^(-?[\d.]+)em$/.exec(String(o.letterSpacing));
    if (m) o = { ...o, wordSpacing: (-parseFloat(m[1])) + 'em' };
  }
  return Object.entries(o).filter(([, v]) => v !== undefined && v !== null)
    .map(([k, v]) => k.replace(/[A-Z]/g, (m) => '-' + m.toLowerCase()) + ':' + v).join(';');
}

export function blockStyle(b, k, ts) {
  const u = (pt) => (pt * k) + 'px';          // geometric lengths (margins, rules)
  const f = (pt) => (pt * k * ts) + 'px';     // type sizes
  const base = { margin: 0, fontFamily: BODY, color: C.tinta, textWrap: 'pretty' };
  const cont = b.contFrom;
  switch (b.t) {
    case 'major': return { ...base, fontFamily: HEAD, fontSize: f(19), lineHeight: 1.22, fontWeight: 400,
      fontVariant: 'small-caps', letterSpacing: '0.015em', color: C.vino, textAlign: 'left',
      textWrap: 'balance', margin: `0 0 ${u(2)}` };
    case 'sec': return { ...base, fontFamily: HEAD, fontSize: f(12.5), lineHeight: 1.28, fontWeight: 600,
      fontVariant: 'small-caps', letterSpacing: '0.04em', color: C.vino, margin: `${u(14)} 0 ${u(9)}` };
    case 'sub': return { ...base, fontSize: f(10.5), lineHeight: 1.24, fontStyle: 'italic', margin: `${u(9)} 0 ${u(4)}` };
    case 'ficha': return { ...base, fontFamily: HEAD, fontSize: f(19), lineHeight: 1.22, fontWeight: 400,
      fontVariant: 'small-caps', letterSpacing: '0.015em', color: C.vino, textAlign: 'left',
      textWrap: 'balance', margin: `0 0 ${u(6)}` };
    // Jerarquia: 'major' y 'ficha' son H1 (cada Mesa Directiva abre su propia
    // pagina, al mismo nivel que un capitulo o un testimonio), 'sec' la seccion
    // (H2), 'rot' el
    // rotulo de subseccion (H3). El antetitulo que anuncia la clase de pieza
    // («Testimonio») no es un H3: se compone subordinado, en gris y sin el peso
    // del rotulo, para que no compita con las subsecciones que vienen despues.
    case 'rot': return b.kicker
      ? { ...base, fontFamily: HEAD, fontSize: f(6.8), lineHeight: 1.4, fontWeight: 400,
          textTransform: 'uppercase', letterSpacing: '0.1em', color: C.gris, margin: `0 0 ${u(2)}` }
      : { ...base, fontFamily: HEAD, fontSize: f(7.6), lineHeight: 1.4, fontWeight: 600,
          textTransform: 'uppercase', letterSpacing: '0.1em', color: C.vino, margin: `${u(11)} 0 ${u(4)}` };
    case 'field': return { ...base, fontSize: f(8.6), lineHeight: 1.35,
      textAlign: 'justify', hyphens: 'auto', margin: `0 0 ${u(4)}` };
    case 'fclose': return { ...base, fontFamily: HEAD, fontSize: f(7), lineHeight: 1.4, fontWeight: 600,
      textTransform: 'uppercase', letterSpacing: '0.1em', color: C.vino, margin: `${u(12)} 0 ${u(4)}` };
    // Las dos clases de cita en bloque comparten sangria: la voz transcrita
    // ('epi') y la nota de encuadre ('ent') se retiran del margen lo mismo, de
    // modo que el lector las lea como un mismo escalon respecto del cuerpo.
    // Columna angosta (sangria a ambos lados) mas texto italico: el
    // justificado del navegador, sin el algoritmo de LaTeX, estira algunos
    // renglones cortos hasta que el espacio entre palabras se lee como un
    // espacio doble. Es el defecto senalado por el compilador. Convencion
    // tipografica estandar para citas en bloque angostas: bandera (alineado
    // a la izquierda), nunca justificado.
    case 'epi': return { ...base, fontSize: f(10), lineHeight: 1.4, fontStyle: 'italic',
      textAlign: 'left', hyphens: 'auto', margin: `${u(cont ? 0 : 6)} ${u(25.5)} ${u(8)} ${u(25.5)}` };
    case 'ent': return { ...base, fontSize: f(8.6), lineHeight: 1.35, fontStyle: 'italic', textAlign: 'left',
      hyphens: 'auto', margin: `${u(cont ? 0 : 4)} ${u(25.5)} ${u(9)} ${u(25.5)}` };
    case 'note': return { ...base, fontSize: f(8.6), lineHeight: 1.35, color: C.tinta,
      textAlign: 'justify', hyphens: 'auto', margin: `0 0 ${u(5)}`, overflowWrap: 'anywhere' };
    case 'ref': return { ...base, fontSize: f(8.6), lineHeight: 1.35,
      textAlign: 'justify', hyphens: 'auto', paddingLeft: u(13), textIndent: u(-13), margin: `0 0 ${u(6)}`, overflowWrap: 'anywhere' };
    case 'fnote': return { ...base, fontFamily: HEAD, fontSize: f(7.6), lineHeight: 1.42, color: C.tinta,
      textAlign: 'justify', hyphens: 'auto', margin: `${u(6)} 0 ${u(4)}` };
    case 'auth': return { ...base, fontSize: f(8), lineHeight: 1.38, fontStyle: 'italic', color: C.tinta,
      textAlign: 'justify', hyphens: 'auto', margin: `${u(3)} 0 ${u(9)}` };
    case 'attrib': return { ...base, fontFamily: HEAD, fontSize: f(7.4), lineHeight: 1.35, color: C.gris,
      textAlign: 'right', margin: `${u(3)} 0 ${u(6)}` };
    case 'center': return { ...base, fontSize: f(10), lineHeight: 1.4, textAlign: 'center', margin: `${u(6)} 0` };
    default: return { ...base, fontSize: f(b.s || 10.9), lineHeight: b.s ? 1.35 : 1.376, textAlign: 'justify',
      hyphens: 'auto', textIndent: (b.ni || cont) ? 0 : '1.2em',
      margin: b.gap ? `0 0 ${u(4)}` : 0 };
  }
}

export function blockHtml(b, k, ts) {
  const u = (pt) => (pt * k) + 'px';
  if (b.t === 'pb') return '';
  // Disciplina de una sola raya: la raya decorativa pertenece a la cornisa y al
  // folio, y a ningun otro sitio del cuerpo. Lo que antes eran filetes sueltos
  // (tras los titulos, bajo las fichas, sobre las notas) pasa a ser aire.
  if (b.t === 'rule') {
    return `<div style="${css({ margin: `${u(6)} 0 ${u(8)}` })}"></div>`;
  }
  if (b.t === 'orn') {
    // el separador de seccion conserva su punto, sin los brazos de raya
    const dot = Math.max(2, 2.4 * k) + 'px';
    return `<div style="${css({ display: 'flex', alignItems: 'center', justifyContent: 'center', margin: `${u(11)} 0` })}">
      <span style="${css({ width: dot, height: dot, borderRadius: '50%', background: C.vino, opacity: 0.7 })}"></span>
    </div>`;
  }
  if (b.t === 'cardStart') {
    return `<div style="${css({ fontFamily: HEAD, fontSize: (6.6 * k * ts) + 'px', letterSpacing: '0.1em', textTransform: 'uppercase', color: C.vino, background: C.crema, display: 'inline-block', padding: `${u(2)} ${u(4)}`, margin: `${u(10)} 0 ${u(3)}`, border: '1px solid ' + C.vino })}">${esc((b.label || 'Ficha de catalogación').replace(/\.$/, ''))}</div>`;
  }
  if (b.t === 'cardEnd') return '';
  if (b.t === 'field') {
    // el rotulo entra en linea y en cursiva: conserva el sentido del campo
    // (fuentes primarias / sin consultar / limites) sin el grito tipografico
    const lab = b.label ? `<em style="color:${C.gris}">${esc(b.label)}: </em>` : '';
    return `<div style="${css({ ...blockStyle(b, k, ts), margin: `0 0 ${u(5)}` })}">${lab}${partsHtml(b.parts, { hyph: true })}</div>`;
  }
  if (b.t === 'fnote') {
    // Dos notas al pie seguidas se componian distinto: la primera con filete
    // y su rotulo en cursiva, la segunda sin filete y con su «Nota de edicion.»
    // corriendo dentro del cuerpo. Ahora el filete abre el grupo una sola vez
    // (b.noRule marca las continuaciones) y toda nota destaca su formula de
    // entrada con el mismo peso.
    let parts = b.parts, lab = '';
    if (b.label) {
      lab = `<em style="color:${C.gris}">${esc(b.label)}${/Nota/.test(b.label) ? '' : ' ·'}</em> `;
    } else if (parts && parts.length && typeof parts[0].x === 'string') {
      const m = parts[0].x.match(/^(Nota[^.]{0,24}\.)\s*/);
      if (m) {
        lab = `<em style="color:${C.gris}">${esc(m[1])}</em> `;
        parts = [{ ...parts[0], x: parts[0].x.slice(m[0].length) }, ...parts.slice(1)];
      }
    }
    // sin filete: el grupo de notas se abre con aire, no con raya
    return `<div style="${css({ margin: `${u(b.noRule ? 2 : 7)} 0 ${u(4)}` })}"><div style="${css({ ...blockStyle(b, k, ts), margin: 0 })}">${lab}${partsHtml(parts, { hyph: true })}</div></div>`;
  }
  if (b.t === 'resumen') {
    // Caja de resumen y puntos clave: misma familia visual que las fichas
    // (borde fino, rotulo en versalitas vino), abre cada capitulo de la
    // Primera Parte con lo esencial en tres a cinco asientos.
    const f2 = (pt) => (pt * k * (ts || 1)) + 'px';
    const items = [];
    let cur = [];
    for (const p of b.parts || []) {
      if (p.br) { if (cur.length) items.push(cur); cur = []; continue; }
      cur.push(p);
    }
    if (cur.length) items.push(cur);
    const li = items.map((ps) =>
      `<div style="${css({ display: 'flex', gap: u(5), marginBottom: u(3) })}">
        <span style="${css({ fontFamily: BODY, color: C.vino, flex: 'none' })}">·</span>
        <span style="${css({ fontFamily: BODY, fontSize: f2(9.2), lineHeight: 1.34, color: C.tinta, textAlign: 'justify', hyphens: 'auto', flex: '1' })}">${partsHtml(ps, { hyph: true })}</span>
      </div>`).join('');
    return `<div style="${css({ border: '1px solid #c9bdbd', padding: `${u(9)} ${u(9)} ${u(6)}`, margin: `${u(8)} 0 ${u(10)}`, position: 'relative' })}">
      <div style="${css({ position: 'absolute', top: u(-4.6), left: u(12), background: '#fff', padding: `0 ${u(5)}`, fontFamily: HEAD, fontSize: f2(6.9), fontWeight: 600, letterSpacing: '0.1em', textTransform: 'uppercase', color: C.vino })}">${esc(b.label || 'Resumen y puntos clave')}</div>
      ${li}
    </div>`;
  }
  if (b.t === 'major') {
    // Titulo con ordinal («Capitulo I.», «Apendice IV.»): el ordinal se compone
    // como antetitulo -- pequeno, gris, sin punto --, y el titulo real queda
    // solo en su jerarquia, igual que el antetitulo «Testimonio» de las piezas.
    const parts = b.parts || [];
    const m = parts.length >= 3 && parts[1] && parts[1].br
      && typeof parts[0].x === 'string'
      && (parts[0].x.match(/^(Capítulo|Apéndice)\s+[IVX]+\.?\s*$/)
        || parts[0].x.match(/^(Primer|Segundo|Tercer|Cuarto)\s+Episodio\.?\s*$/));
    if (m) {
      // Jerarquia dictada: el ordinal («Apéndice I», «Primer Episodio») es el
      // H1; el nombre tematico baja a H2, compuesto como una seccion.
      const kicker = parts[0].x.trim().replace(/\.$/, '');
      const resto = parts.slice(2);
      const f2 = (pt) => (pt * k * (ts || 1)) + 'px';
      return `<div style="${css({ margin: `0 0 ${u(6)}` })}">
        <div style="${css({ ...blockStyle(b, k, ts), margin: 0 })}">${esc(kicker)}</div>
        <div style="${css({ fontFamily: HEAD, fontSize: f2(12.5), fontWeight: 600, fontVariant: 'small-caps', letterSpacing: '0.04em', color: C.vino, marginTop: u(2) })}">${partsHtml(resto)}</div>
      </div>`;
    }
  }
  if (b.t === 'fbox') {
    // Etapa del diagrama de flujo del metodo: caja con filete y, salvo en la
    // primera, flecha descendente dibujada con CSS (sin depender de glifos).
    const f2 = (pt) => (pt * k * (ts || 1)) + 'px';
    const arrow = b.first ? '' : `<div style="${css({ width: 0, margin: '0 auto', borderLeft: '1px solid ' + C.vino, height: u(4) })}"></div><div style="${css({ width: 0, height: 0, margin: '0 auto', borderLeft: '4px solid transparent', borderRight: '4px solid transparent', borderTop: '5px solid ' + C.vino })}"></div>`;
    return `<div style="${css({ margin: b.first ? `${u(4)} 0 0` : 0 })}">${arrow}<div style="${css({ border: '1px solid ' + C.vino, background: C.crema, padding: `${u(3.5)} ${u(5)}`, fontFamily: BODY, fontSize: f2(8.6), lineHeight: 1.35, textAlign: 'justify', hyphens: 'auto', color: C.tinta })}">${partsHtml(b.parts, { hyph: true })}</div></div>`;
  }
  if (b.t === 'thead' || b.t === 'trow') {
    const f2 = (pt) => (pt * k * (ts || 1)) + 'px';
    const groups = [];
    let cur = [];
    for (const p of (b.parts || [])) {
      if (p.br) { groups.push(cur); cur = []; } else cur.push(p);
    }
    groups.push(cur);
    const w = (b.cw && b.cw.length === groups.length) ? b.cw : groups.map(() => 100 / groups.length);
    const head = b.t === 'thead';
    const cellCss = head
      ? { fontFamily: HEAD, fontSize: f2(7), fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.1em', color: C.vino, padding: `0 0 ${u(1.5)}` }
      : { fontFamily: BODY, fontSize: f2(8.6), lineHeight: 1.35, textAlign: 'left', hyphens: 'auto', overflowWrap: 'anywhere', padding: `${u(1.5)} 0` };
    const cells = groups.map(g => `<div style="${css(cellCss)}">${partsHtml(g, { hyph: !head })}</div>`).join('');
    return `<div style="${css({ display: 'grid', gridTemplateColumns: w.map(x => `minmax(0, ${x}fr)`).join(' '), columnGap: u(4), borderBottom: head ? ('1px solid ' + C.vino) : ('0.5px solid rgba(0,0,0,0.18)'), margin: head ? `${u(3)} 0 0` : 0 })}">${cells}</div>`;
  }
  if (b.t === 'ficha') {
    const txt = blockText(b).trim();
    const m = txt.match(/^([0-9]{4}\s*[-\u2013]\s*[0-9]{4})\.?\s*(.*)$/);
    const years = m ? m[1] : '';
    const name = m ? m[2] : txt;
    const f2 = (pt) => (pt * k * (ts || 1)) + 'px';
    return `<div style="${css({ margin: `0 0 ${u(10)}` })}">
      ${years ? `<div style="${css({ fontFamily: HEAD, fontSize: f2(12.5), fontWeight: 600, fontVariant: 'small-caps', letterSpacing: '0.04em', color: C.vino, marginBottom: u(2) })}">${esc(years)}</div>` : ''}
      <div style="${css(blockStyle(b, k, ts))}">${esc(name)}</div>
      ${b.foot ? `<div style="${css({ fontFamily: BODY, fontSize: f2(7.6), fontStyle: 'italic', color: C.gris, marginTop: u(3) })}">${esc(b.foot)}</div>` : ''}
    </div>`;
  }
  const tag = b.t === 'p' || b.t === 'note' || b.t === 'ref' || b.t === 'epi' || b.t === 'ent' ? 'p' : 'div';
  const dropSize = b.t === 'p' ? 2.1 : 1.8;
  const hyph = ['p', 'note', 'ref', 'epi', 'ent', 'auth', 'center'].includes(b.t) && !b.ragged;
  const st = blockStyle(b, k, ts);
  if (b.cols === 2) { st.columns = '2'; st.columnGap = u(16); st.textAlign = 'left'; }
  return `<${tag} style="${css(st)}">${partsHtml(b.parts, { dropSize, hyph })}</${tag}>`;
}

export const pageHtml = (items, k, ts) => (items || []).map((b) => blockHtml(b, k, ts)).join('');

/* ---------- full-page plates ---------- */
export function plateHtml(b, k, ts) {
  const u = (pt) => (pt * k) + 'px';
  const inset = u(31.7);
  if (b.t === 'plate') {
    // la portadilla declara el ordinal de su parte: el volumen se ordena en
    // tres partes (historia, voces, cierre) y el lector debe verlas como tales
    const ORDINAL = { 'El gremio': 'Primera parte', 'Perspectivas': 'Segunda parte', 'Conclusión': 'Tercera parte' };
    const ord = ORDINAL[b.title] || '';
    const rule = `<div style="${css({ width: u(46), height: Math.max(1, 0.45 * k) + 'px', background: 'rgba(247,244,239,.65)' })}"></div>`;
    return `<div style="${css({ position: 'absolute', inset: 0, background: C.vino, overflow: 'hidden' })}">
      <div style="${css({ position: 'absolute', top: inset, right: inset, bottom: inset, left: inset, border: `1px solid rgba(247,244,239,.5)` })}"></div>
      <div style="${css({ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: u(13), padding: u(70), textAlign: 'center' })}">
        ${ord ? `<div style="${css({ fontFamily: HEAD, fontSize: (7.2 * k * ts) + 'px', letterSpacing: '0.12em', textTransform: 'uppercase', color: 'rgba(247,244,239,.78)' })}">${esc(ord)}</div>${rule}` : ''}
        <div style="${css({ fontFamily: HEAD, fontSize: (21 * k * ts) + 'px', lineHeight: 1.2, fontVariant: 'small-caps', letterSpacing: '0.08em', color: C.crema })}">${esc(b.title || '')}</div>
        ${b.sub ? `<div style="${css({ fontFamily: BODY, fontSize: (10 * k * ts) + 'px', lineHeight: 1.55, fontStyle: 'italic', color: 'rgba(247,244,239,.85)', maxWidth: u(250), textWrap: 'balance' })}">${esc(b.sub)}</div>` : ''}
      </div>
    </div>`;
  }
  // display page (title page, dedication, epigraph plate) — typography captured from the TeX nodes
  const dark = !!b.dark;
  const COLMAP = { vino: C.vino, crema: C.crema, gris: C.gris, tinta: C.tinta };
  const rows = (b.rows || []).map((r) => {
    const t = r.parts.map((p) => (p.br ? ' ' : p.x || '')).join('').trim();
    if (/^[·\s]+$/.test(t)) {
      const arm = u(34), dot = Math.max(2, 2.2 * k) + 'px';
      const c = dark ? C.crema : C.vino;
      return `<div style="${css({ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: u(6), margin: `${u(4)} 0` })}">
        <span style="${css({ width: arm, height: Math.max(1, 0.45 * k) + 'px', background: c, opacity: 0.75 })}"></span>
        <span style="${css({ width: dot, height: dot, borderRadius: '50%', background: c })}"></span>
        <span style="${css({ width: arm, height: Math.max(1, 0.45 * k) + 'px', background: c, opacity: 0.75 })}"></span>
      </div>`;
    }
    const st = {
      fontFamily: r.sans || r.sc ? HEAD : BODY,
      fontSize: (r.size * k * ts) + 'px',
      lineHeight: r.lead && r.size ? (r.lead / r.size).toFixed(3) : 1.4,
      fontStyle: r.it ? 'italic' : 'normal',
      fontVariant: r.sc ? 'small-caps' : undefined,
      fontWeight: r.sc || r.sans ? 600 : 400,
      letterSpacing: r.ls ? (r.ls / 100) + 'em' : undefined,
      textTransform: r.sans && !r.sc ? 'uppercase' : undefined,
      color: COLMAP[r.color] || (dark ? C.crema : C.tinta),
      maxWidth: r.width ? u(r.width * 28.3465) : u(300),
      textAlign: 'center',
      textWrap: 'balance'
    };
    return `<div style="${css(st)}">${partsHtml(r.parts)}</div>`;
  }).join('');
  return `<div style="${css({ position: 'absolute', inset: 0, background: dark ? C.vino : 'transparent', overflow: 'hidden' })}">
    ${dark ? `<div style="${css({ position: 'absolute', top: inset, right: inset, bottom: inset, left: inset, border: '1px solid rgba(247,244,239,.4)' })}"></div>` : ''}
    <div style="${css({ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: u(11), padding: u(56) })}">${rows}</div>
  </div>`;
}

/* ---------- generated contents page ---------- */
export function tocHtml(toc, pageOf, k, ts) {
  const u = (pt) => (pt * k) + 'px';
  const rows = toc.map((t) => {
    const p = pageOf[t.i];
    const lab = `<span style="${css({ paddingLeft: t.lvl ? u(10) : 0 })}">${esc(t.label)}</span>`;
    if (t.lvl === 0 && !p) return `<div style="${css({ fontFamily: HEAD, fontSize: (7 * k * ts) + 'px', letterSpacing: '0.1em', textTransform: 'uppercase', color: C.vino, margin: `${u(9)} 0 ${u(3)}` })}">${esc(t.label)}</div>`;
    return `<div style="${css({ display: 'flex', alignItems: 'baseline', gap: u(4), fontFamily: BODY, fontSize: (8.6 * k * ts) + 'px', lineHeight: 1.75, color: C.tinta })}">
      ${lab}<span style="${css({ flex: 1, borderBottom: `1px dotted ${C.gris}`, transform: 'translateY(-0.2em)', opacity: 0.6 })}"></span>
      <span style="${css({ fontVariantNumeric: 'tabular-nums', color: C.gris })}">${p || ''}</span></div>`;
  }).join('');
  return `<div>
    <div style="${css({ fontFamily: HEAD, fontSize: (19 * k * ts) + 'px', fontVariant: 'small-caps', letterSpacing: '0.05em', color: C.vino })}">Contenido</div>
    <div style="${css({ width: u(79), height: Math.max(1, 0.45 * k) + 'px', background: C.vino, margin: `${u(7)} 0 ${u(11)}` })}"></div>
    ${rows}
    <div style="${css({ fontFamily: HEAD, fontSize: (6.6 * k * ts) + 'px', lineHeight: 1.5, color: C.gris, marginTop: u(14) })}">Los folios del impreso se conservan al margen; la numeración de esta pantalla corresponde a la edición en flipbook.</div>
  </div>`;
}

/* ---------- cover ----------
   Doble filete (marco clásico de volumen histórico) y título en dos cuerpos:
   «Genealogía» lleva la página y la razón social queda como objeto del
   estudio, dentro del propio título — antes el nombre de la Asociación se
   imprimía dos veces a pesos que competían entre sí. La institución cierra
   la cubierta como sello editorial al pie, que es su sitio. */
export function coverHtml(k, ts) {
  const u = (pt) => (pt * k) + 'px';
  const f = (pt) => (pt * k * ts) + 'px';
  const line = (top, style, html) => `<div style="${css({ position: 'absolute', top: u(top), left: u(44), right: u(44), textAlign: 'center', ...style })}">${html}</div>`;
  const arm = u(41), dot = Math.max(2, 2.6 * k) + 'px';
  const orn = `<div style="${css({ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: u(7) })}">
      <span style="${css({ width: arm, height: Math.max(1, 0.5 * k) + 'px', background: 'rgba(247,244,239,.7)' })}"></span>
      <span style="${css({ width: dot, height: dot, borderRadius: '50%', background: C.crema })}"></span>
      <span style="${css({ width: arm, height: Math.max(1, 0.5 * k) + 'px', background: 'rgba(247,244,239,.7)' })}"></span>
    </div>`;
  return `<div style="${css({ position: 'absolute', inset: 0, background: C.vino, overflow: 'hidden' })}">
    <div style="${css({ position: 'absolute', top: u(28), right: u(28), bottom: u(28), left: u(28), border: '1px solid rgba(247,244,239,.5)' })}"></div>
    <div style="${css({ position: 'absolute', top: u(33.5), right: u(33.5), bottom: u(33.5), left: u(33.5), border: Math.max(1, 0.45 * k) + 'px solid rgba(247,244,239,.28)' })}"></div>
    ${line(76, { fontFamily: HEAD, fontSize: f(7.2), letterSpacing: '0.11em', textTransform: 'uppercase', color: 'rgba(247,244,239,.78)' }, 'Sexagésimo Aniversario · 1966–2026')}
    ${line(168, { fontFamily: HEAD, fontSize: f(30), lineHeight: 1.1, fontVariant: 'small-caps', letterSpacing: '0.05em', color: C.crema }, 'Genealogía')}
    ${line(222, { fontFamily: HEAD, fontSize: f(12.5), lineHeight: 1.5, fontVariant: 'small-caps', letterSpacing: '0.08em', color: C.crema },
      'de la Asociación Psiquiátrica<br>Mexicana, A.C.')}
    ${line(292, {}, orn)}
    ${line(318, { fontFamily: BODY, fontSize: f(11.5), fontStyle: 'italic', color: 'rgba(247,244,239,.92)' }, 'Gran Proyecto Historiográfico')}
    ${line(424, { fontFamily: BODY, fontSize: f(10.5), color: C.crema }, 'José Carlos Medina Rodríguez')}
    ${line(442, { fontFamily: HEAD, fontSize: f(6.4), letterSpacing: '0.12em', textTransform: 'uppercase', color: 'rgba(247,244,239,.7)' }, 'Historiador Compilador')}
    ${line(464, { fontFamily: BODY, fontSize: f(10.5), color: C.crema }, 'David Eduardo Saucedo Martínez')}
    ${line(482, { fontFamily: HEAD, fontSize: f(6.4), letterSpacing: '0.12em', textTransform: 'uppercase', color: 'rgba(247,244,239,.7)' }, 'Editor')}
    ${line(524, { fontFamily: HEAD, fontSize: f(9.5), fontVariant: 'small-caps', letterSpacing: '0.1em', color: C.crema }, 'XXX Congreso Nacional')}
    ${line(541, { fontFamily: HEAD, fontSize: f(6.4), lineHeight: 1.5, letterSpacing: '0.10em', textTransform: 'uppercase', color: 'rgba(247,244,239,.7)' },
      'Expo Santa Fe, Ciudad de México · 10 a 12 de septiembre de 2026')}
    ${line(586, {}, `<div style="${css({ width: u(120), height: Math.max(1, 0.35 * k) + 'px', background: 'rgba(247,244,239,.45)', margin: '0 auto' })}"></div>`)}
    ${line(594, { fontFamily: HEAD, fontSize: f(6.6), letterSpacing: '0.12em', textTransform: 'uppercase', color: 'rgba(247,244,239,.8)' }, 'Asociación Psiquiátrica Mexicana, A.C.')}
  </div>`;
}

/* ---------- back cover ---------- */
export function backCoverHtml(k, ts) {
  const u = (pt) => (pt * k) + 'px';
  const f = (pt) => (pt * k * ts) + 'px';
  const inset = u(31.7);
  const arm = u(41), dot = Math.max(2, 2.6 * k) + 'px';
  const orn = `<div style="${css({ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: u(7), margin: `${u(14)} 0` })}">
      <span style="${css({ width: arm, height: Math.max(1, 0.5 * k) + 'px', background: 'rgba(247,244,239,.7)' })}"></span>
      <span style="${css({ width: dot, height: dot, borderRadius: '50%', background: C.crema })}"></span>
      <span style="${css({ width: arm, height: Math.max(1, 0.5 * k) + 'px', background: 'rgba(247,244,239,.7)' })}"></span>
    </div>`;
  return `<div style="${css({ position: 'absolute', inset: 0, background: C.vino, overflow: 'hidden' })}">
    <div style="${css({ position: 'absolute', top: u(28), right: u(28), bottom: u(28), left: u(28), border: '1px solid rgba(247,244,239,.5)' })}"></div>
    <div style="${css({ position: 'absolute', top: u(33.5), right: u(33.5), bottom: u(33.5), left: u(33.5), border: Math.max(1, 0.45 * k) + 'px solid rgba(247,244,239,.28)' })}"></div>
    <div style="${css({ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: `0 ${u(52)}`, textAlign: 'center' })}">
      <div style="${css({ fontFamily: HEAD, fontSize: f(11.5), lineHeight: 1.35, fontVariant: 'small-caps', letterSpacing: '0.07em', color: C.crema, width: u(290), maxWidth: '100%' })}">Genealogía de la Asociación<br>Psiquiátrica Mexicana, A.C.</div>
      ${orn}
      <div style="${css({ fontFamily: BODY, fontSize: f(9.4), lineHeight: 1.65, color: 'rgba(247,244,239,.94)', maxWidth: u(280) })}">Obra que reúne la Historia documentada del Gremio, la relación de quienes lo presidieron y las perspectivas de sus expresidentes, en conmemoración del Sexagésimo Aniversario de su fundación.</div>
      <div style="${css({ fontFamily: BODY, fontSize: f(9.4), lineHeight: 1.65, color: 'rgba(247,244,239,.94)', maxWidth: u(280), marginTop: u(9) })}">El libro nace de una pregunta empírica —¿qué pasó?— y no de una fundamental. Explica cuando el hecho lo permite e interpreta cuando el registro calla, con los métodos científicos propios de la Historia —el historiográfico, el hermenéutico y el fenomenológico—. Reúne hechos validados y oficialmente registrados, recuperados en persona o mediante Testimonio —un rescate historiográfico, material y personal, con resultados de investigación metodológica y prosopográfica—, para pasar de las lagunas de la hagiografía a la Historia del Gremio. Es así como la Historia hoy no se inventa ni simplemente se cuenta: se investiga, se cura y se interpreta, y, como todo constructo científico, permanece dinámica y susceptible de modificarse. Lo que el lector tiene ante sí es, por ende, Historia: no una confección conveniente, sino el resultado de sistemas robustos, validados y cruzados, de raíz constructivista, antropológica, social e histórica. El libro se ordena en tres partes: la Historia en cuatro episodios, las perspectivas de los expresidentes en sus Testimonios, y una conclusión seguida de quince apéndices con la línea del tiempo, el método, las series verificadas y las rutas de consulta.</div>
      <div style="${css({ fontFamily: BODY, fontSize: f(9), fontStyle: 'italic', color: 'rgba(247,244,239,.85)', marginTop: u(16) })}">Compilación de José Carlos Medina Rodríguez<br>Edición de David Eduardo Saucedo Martínez</div>
    </div>
    <div style="${css({ position: 'absolute', left: u(64), right: u(64), bottom: u(52), textAlign: 'center' })}">
      <div style="${css({ width: '100%', height: Math.max(1, 0.3 * k) + 'px', background: 'rgba(247,244,239,.5)', marginBottom: u(9) })}"></div>
      <div style="${css({ fontFamily: HEAD, fontSize: f(6.6), lineHeight: 1.7, letterSpacing: '0.10em', textTransform: 'uppercase', color: 'rgba(247,244,239,.8)' })}">Asociación Psiquiátrica Mexicana, A.C. · Primera Edición<br>Ciudad de México, 2026 · Acceso abierto · CC BY-NC-ND 4.0<br>DOI 10.5281/zenodo.22035217</div>
    </div>
  </div>`;
}
