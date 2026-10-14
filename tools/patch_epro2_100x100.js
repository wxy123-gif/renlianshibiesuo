const fs = require('fs');
const path = require('path');
const srcDir = process.argv[2];
const outDir = process.argv[3];
const srcEpru = path.join(srcDir, '智慧门锁.epru');
const outEpru = path.join(outDir, '智慧门锁_100x100.epru');
const BOARD = { minX: -100, maxX: 3837, minY: -3300, maxY: 500 };
const INSET_MIL = 15;
const POURED = { minX: (BOARD.minX + INSET_MIL) / 10, maxX: (BOARD.maxX - INSET_MIL) / 10, minY: (BOARD.minY + INSET_MIL) / 10, maxY: (BOARD.maxY - INSET_MIL) / 10 };
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
function clampPair(arr, i, b) { arr[i] = clamp(arr[i], b.minX, b.maxX); arr[i + 1] = clamp(arr[i + 1], b.minY, b.maxY); }
function clampSubpath(sub, b) {
  if (!Array.isArray(sub) || sub.length < 2) return;
  clampPair(sub, 0, b);
  let i = 2;
  while (i < sub.length) {
    const t = sub[i];
    if (t === 'L') {
      i++;
      while (i + 1 < sub.length && typeof sub[i] === 'number' && typeof sub[i + 1] === 'number') { clampPair(sub, i, b); i += 2; }
    } else if (t === 'ARC') {
      if (i + 3 < sub.length && typeof sub[i + 1] === 'number' && typeof sub[i + 2] === 'number' && typeof sub[i + 3] === 'number') {
        clampPair(sub, i + 2, b); i += 4;
      } else i++;
    } else if (typeof t === 'number' && typeof sub[i + 1] === 'number') {
      clampPair(sub, i, b); i += 2;
    } else i++;
  }
}
const raw = fs.readFileSync(srcEpru, 'utf8');
const hadFinalNewline = raw.endsWith('\n');
const out = raw.split(/\r?\n/).map((line) => {
  if (!line || !line.includes('||') || !line.endsWith('|')) return line;
  const pos = line.indexOf('||');
  const dataText = line.slice(0, pos);
  const markerText = line.slice(pos + 2, -1);
  let data, marker;
  try { data = JSON.parse(dataText); marker = JSON.parse(markerText); } catch { return line; }
  if (data.type === 'POLY' && marker.layerId === 11) {
    marker.path = ['R', BOARD.minX, BOARD.maxY, BOARD.maxX - BOARD.minX, BOARD.maxY - BOARD.minY, 0, 0];
  }
  if (data.type === 'POUR' && (marker.layerId === 1 || marker.layerId === 2)) {
    for (const p of marker.path || []) if (Array.isArray(p) && p[0] === 'R') {
      p[1] = BOARD.minX + INSET_MIL;
      p[2] = BOARD.maxY - INSET_MIL;
      p[3] = (BOARD.maxX - BOARD.minX) - 2 * INSET_MIL;
      p[4] = (BOARD.maxY - BOARD.minY) - 2 * INSET_MIL;
    }
  }
  if (data.type === 'POURED' && Array.isArray(marker.pourFill)) {
    for (const fill of marker.pourFill) for (const sub of fill.path || []) clampSubpath(sub, POURED);
  }
  return dataText + '||' + JSON.stringify(marker) + '|';
});
fs.writeFileSync(outEpru, out.join('\n') + (hadFinalNewline ? '\n' : ''), 'utf8');
console.log(JSON.stringify({outEpru, POURED}));
