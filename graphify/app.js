/* ══════════════════════════════
   GRAPHIFY — app.js
   Core Application Logic
   ══════════════════════════════ */

'use strict';

// ── COLOR PALETTES ──────────────────────────────────────────────────────────
const PALETTES = {
  cosmic:  ['#7c3aed','#3b82f6','#34d399','#f59e0b','#ec4899','#06b6d4','#a78bfa','#818cf8'],
  sunrise: ['#f97316','#ef4444','#f59e0b','#fbbf24','#fb923c','#fca5a5','#fde68a','#fed7aa'],
  ocean:   ['#0ea5e9','#06b6d4','#3b82f6','#38bdf8','#67e8f9','#93c5fd','#0284c7','#0369a1'],
  forest:  ['#16a34a','#65a30d','#0d9488','#15803d','#4d7c0f','#0f766e','#84cc16','#22c55e'],
  candy:   ['#ec4899','#a855f7','#f43f5e','#d946ef','#e879f9','#f472b6','#c084fc','#fb7185'],
  mono:    ['#e2e8f0','#94a3b8','#475569','#cbd5e1','#64748b','#334155','#f1f5f9','#1e293b'],
};

let currentPalette = PALETTES.cosmic;

// ── STATE ────────────────────────────────────────────────────────────────────
let chartInstance = null;
let currentType   = 'bar';
let datasets      = [];   // [{label, values:[num], color}]

// ── DOM REFS ─────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const mainCanvas       = $('main-chart');
const ctx              = mainCanvas.getContext('2d');
const chartTitleInput  = $('chart-title');
const dataLabelsInput  = $('data-labels');
const datasetsWrapper  = $('datasets-wrapper');
const statsBar         = $('stats-bar');
const chartTitleDisplay= $('chart-title-display');

// ── INIT ─────────────────────────────────────────────────────────────────────
function init() {
  // Default 2 datasets with demo data
  addDataset('Revenue',  [42, 78, 56, 90, 67, 110], currentPalette[0]);
  addDataset('Expenses', [28, 45, 38, 62, 48, 74],  currentPalette[1]);
  renderChart();
  animateCounters();
}

// ── DATASET MANAGEMENT ───────────────────────────────────────────────────────
function addDataset(label = 'Dataset', values = [10,20,30,40,50,60], color = null) {
  const idx   = datasets.length;
  const clr   = color || currentPalette[idx % currentPalette.length];
  const ds    = { label, values, color: clr };
  datasets.push(ds);
  renderDatasetRow(ds, datasets.length - 1);
}

function renderDatasetRow(ds, idx) {
  const row = document.createElement('div');
  row.className = 'dataset-row';
  row.id = `ds-row-${idx}`;
  row.innerHTML = `
    <div class="dataset-row-header">
      <input type="color" class="dataset-color-swatch" value="${ds.color}" title="Pick color"
             id="ds-color-${idx}" data-idx="${idx}" />
      <input type="text" class="dataset-name-input" placeholder="Dataset name"
             value="${ds.label}" id="ds-name-${idx}" data-idx="${idx}" />
      <button class="dataset-delete" id="ds-del-${idx}" data-idx="${idx}" title="Remove dataset" aria-label="Remove dataset">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/>
          <path d="M9 6V4h6v2"/>
        </svg>
      </button>
    </div>
    <input type="text" class="dataset-values-input" placeholder="e.g. 10, 25, 40, 55, 70, 90"
           value="${ds.values.join(', ')}" id="ds-vals-${idx}" data-idx="${idx}" />
  `;
  datasetsWrapper.appendChild(row);

  // Wire events
  row.querySelector(`#ds-color-${idx}`).addEventListener('input', e => {
    datasets[e.target.dataset.idx].color = e.target.value;
  });
  row.querySelector(`#ds-name-${idx}`).addEventListener('input', e => {
    datasets[e.target.dataset.idx].label = e.target.value;
  });
  row.querySelector(`#ds-vals-${idx}`).addEventListener('input', e => {
    datasets[e.target.dataset.idx].values = parseValues(e.target.value);
  });
  row.querySelector(`#ds-del-${idx}`).addEventListener('click', e => {
    const i = parseInt(e.currentTarget.dataset.idx);
    if (datasets.length === 1) { showToast('⚠️ Need at least one dataset'); return; }
    datasets.splice(i, 1);
    rebuildDatasetUI();
    renderChart();
  });
}

function rebuildDatasetUI() {
  datasetsWrapper.innerHTML = '';
  const copy = [...datasets];
  datasets = [];
  copy.forEach((ds, i) => {
    datasets.push(ds);
    renderDatasetRow(ds, i);
  });
}

function parseValues(str) {
  return str.split(',').map(s => {
    const n = parseFloat(s.trim());
    return isNaN(n) ? 0 : n;
  });
}

function getLabels() {
  return dataLabelsInput.value.split(',').map(s => s.trim()).filter(Boolean);
}

// ── RENDER CHART ─────────────────────────────────────────────────────────────
function renderChart() {
  if (chartInstance) { chartInstance.destroy(); }

  // Sync dataset values from inputs (in case user typed without event issue)
  document.querySelectorAll('.dataset-values-input').forEach(el => {
    const i = parseInt(el.dataset.idx);
    if (datasets[i]) datasets[i].values = parseValues(el.value);
  });
  document.querySelectorAll('.dataset-name-input').forEach(el => {
    const i = parseInt(el.dataset.idx);
    if (datasets[i]) datasets[i].label = el.value;
  });
  document.querySelectorAll('.dataset-color-swatch').forEach(el => {
    const i = parseInt(el.dataset.idx);
    if (datasets[i]) datasets[i].color = el.value;
  });

  const labels    = getLabels();
  const title     = chartTitleInput.value || 'My Chart';
  chartTitleDisplay.textContent = title;

  const legend    = $('opt-legend').checked;
  const grid      = $('opt-grid').checked;
  const animate   = $('opt-animate').checked;
  const fill      = $('opt-fill').checked;
  const isDark    = !document.documentElement.hasAttribute('data-theme') ||
                    document.documentElement.getAttribute('data-theme') !== 'light';

  const textColor    = isDark ? '#9898b8' : '#5a5a7a';
  const gridColor    = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.06)';
  const isRound      = ['pie','doughnut','polarArea','radar'].includes(currentType);

  const chartDatasets = datasets.map((ds, i) => {
    const bgAlpha = isRound ? 0.85 : (fill ? 0.25 : 0.75);
    const colors  = isRound
      ? currentPalette.map(c => hexToRgba(c, 0.85))
      : hexToRgba(ds.color, bgAlpha);
    const borders = isRound
      ? currentPalette.map(c => hexToRgba(c, 1))
      : ds.color;

    return {
      label:           ds.label,
      data:            ds.values,
      backgroundColor: colors,
      borderColor:     borders,
      borderWidth:     isRound ? 2 : 2.5,
      tension:         0.42,
      fill:            fill && currentType === 'line',
      pointRadius:     currentType === 'line' ? 5 : 0,
      pointHoverRadius: currentType === 'line' ? 8 : 0,
      pointBackgroundColor: ds.color,
      borderRadius:    currentType === 'bar' ? 6 : 0,
      borderSkipped:   false,
    };
  });

  const options = {
    responsive:         true,
    maintainAspectRatio: true,
    animation: {
      duration: animate ? 800 : 0,
      easing: 'easeInOutQuart',
    },
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: {
        display: legend,
        labels: {
          color: textColor,
          font: { family: 'Inter', size: 12, weight: '600' },
          padding: 20,
          usePointStyle: true,
          pointStyleWidth: 12,
        },
      },
      tooltip: {
        backgroundColor: isDark ? 'rgba(17,17,32,0.95)' : 'rgba(255,255,255,0.97)',
        titleColor:      isDark ? '#e8e8f0' : '#1a1a2e',
        bodyColor:       isDark ? '#9898b8' : '#5a5a7a',
        borderColor:     isDark ? 'rgba(124,58,237,0.3)' : 'rgba(124,58,237,0.2)',
        borderWidth:     1,
        cornerRadius:    12,
        padding:         12,
        titleFont:       { family: 'Outfit', size: 13, weight: '700' },
        bodyFont:        { family: 'Inter', size: 12 },
        callbacks: {
          label: ctx => ` ${ctx.dataset.label}: ${ctx.parsed.y ?? ctx.parsed ?? ctx.raw}`,
        },
      },
    },
    scales: isRound ? {} : {
      x: {
        display:    true,
        grid:       { display: grid, color: gridColor, drawBorder: false },
        ticks:      { color: textColor, font: { family: 'Inter', size: 11 } },
        border:     { display: false },
      },
      y: {
        display:    true,
        grid:       { display: grid, color: gridColor, drawBorder: false },
        ticks:      { color: textColor, font: { family: 'Inter', size: 11 } },
        border:     { display: false },
        beginAtZero: true,
      },
    },
  };

  chartInstance = new Chart(ctx, {
    type:    currentType,
    data:    { labels, datasets: chartDatasets },
    options,
  });

  updateStatsBar();
}

// ── STATS BAR ────────────────────────────────────────────────────────────────
function updateStatsBar() {
  const allValues = datasets.flatMap(d => d.values.filter(v => !isNaN(v)));
  if (!allValues.length) { statsBar.innerHTML = ''; return; }

  const total   = allValues.reduce((a, b) => a + b, 0);
  const max     = Math.max(...allValues);
  const min     = Math.min(...allValues);
  const avg     = (total / allValues.length).toFixed(1);
  const points  = allValues.length;

  statsBar.innerHTML = `
    <div class="stat-card"><div class="stat-card-value">${fmt(total)}</div><div class="stat-card-label">Total</div></div>
    <div class="stat-card"><div class="stat-card-value">${fmt(max)}</div><div class="stat-card-label">Peak</div></div>
    <div class="stat-card"><div class="stat-card-value">${fmt(min)}</div><div class="stat-card-label">Min</div></div>
    <div class="stat-card"><div class="stat-card-value">${avg}</div><div class="stat-card-label">Average</div></div>
    <div class="stat-card"><div class="stat-card-value">${points}</div><div class="stat-card-label">Data Points</div></div>
  `;
}

function fmt(n) {
  if (n >= 1e6) return (n/1e6).toFixed(1)+'M';
  if (n >= 1e3) return (n/1e3).toFixed(1)+'K';
  return n;
}

// ── EXPORT ───────────────────────────────────────────────────────────────────
function exportPNG() {
  const link = document.createElement('a');
  link.download = `graphify-${Date.now()}.png`;
  link.href = mainCanvas.toDataURL('image/png');
  link.click();
  showToast('✅ PNG exported!');
}
function exportJPG() {
  const link = document.createElement('a');
  link.download = `graphify-${Date.now()}.jpg`;
  link.href = mainCanvas.toDataURL('image/jpeg', 0.95);
  link.click();
  showToast('✅ JPG exported!');
}
function exportJSON() {
  const data = {
    title:    chartTitleInput.value,
    labels:   getLabels(),
    datasets: datasets.map(d => ({ label: d.label, values: d.values, color: d.color })),
    type:     currentType,
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const link = document.createElement('a');
  link.download = `graphify-data-${Date.now()}.json`;
  link.href = URL.createObjectURL(blob);
  link.click();
  showToast('✅ JSON data exported!');
}

// ── COPY CHART ────────────────────────────────────────────────────────────────
async function copyChart() {
  try {
    mainCanvas.toBlob(async blob => {
      await navigator.clipboard.write([
        new ClipboardItem({ 'image/png': blob }),
      ]);
      showToast('📋 Chart copied to clipboard!');
    });
  } catch {
    showToast('⚠️ Copy not supported in this browser');
  }
}

// ── FULLSCREEN ────────────────────────────────────────────────────────────────
let fsChart = null;
function openFullscreen() {
  const overlay  = $('fs-overlay');
  const fsCanvas = $('fs-chart');
  overlay.classList.add('active');
  document.body.style.overflow = 'hidden';

  if (fsChart) fsChart.destroy();
  fsChart = new Chart(fsCanvas, {
    type:    chartInstance.config.type,
    data:    JSON.parse(JSON.stringify(chartInstance.data)),
    options: JSON.parse(JSON.stringify(chartInstance.options)),
  });
}
function closeFullscreen() {
  $('fs-overlay').classList.remove('active');
  document.body.style.overflow = '';
  if (fsChart) { fsChart.destroy(); fsChart = null; }
}

// ── TOAST ────────────────────────────────────────────────────────────────────
let toastTimer;
function showToast(msg) {
  const t = $('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 3000);
}

// ── COUNTER ANIMATION ────────────────────────────────────────────────────────
function animateCounters() {
  document.querySelectorAll('.stat-num[data-target]').forEach(el => {
    const target = parseInt(el.dataset.target);
    if (isNaN(target)) return;
    let current = 0;
    const step  = Math.ceil(target / 40);
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current;
      if (current >= target) clearInterval(timer);
    }, 20);
  });
}

// ── DEMO DATA ────────────────────────────────────────────────────────────────
function loadDemo() {
  const demos = [
    {
      title:  'Monthly Revenue vs Expenses',
      labels: 'Jan, Feb, Mar, Apr, May, Jun',
      datasets: [
        { label: 'Revenue',  values: [42, 78, 56, 90, 67, 110], color: '#7c3aed' },
        { label: 'Expenses', values: [28, 45, 38, 62, 48, 74],  color: '#3b82f6' },
      ],
    },
    {
      title:  'Social Media Engagement',
      labels: 'Instagram, Twitter, YouTube, TikTok, Facebook, LinkedIn',
      datasets: [
        { label: 'Followers (K)', values: [120, 85, 200, 310, 95, 40], color: '#ec4899' },
      ],
    },
    {
      title:  'Quarterly Performance',
      labels: 'Q1, Q2, Q3, Q4',
      datasets: [
        { label: 'Sales',    values: [340, 490, 380, 620], color: '#34d399' },
        { label: 'Target',   values: [400, 450, 420, 580], color: '#f59e0b' },
        { label: 'Last Year',values: [280, 390, 310, 510], color: '#60a5fa' },
      ],
    },
  ];
  const demo = demos[Math.floor(Math.random() * demos.length)];
  chartTitleInput.value  = demo.title;
  dataLabelsInput.value  = demo.labels;
  datasetsWrapper.innerHTML = '';
  datasets = [];
  demo.datasets.forEach(d => addDataset(d.label, d.values, d.color));
  renderChart();
  showToast('🎲 Demo data loaded!');
}

// ── COLOR UTIL ────────────────────────────────────────────────────────────────
function hexToRgba(hex, alpha = 1) {
  const r = parseInt(hex.slice(1,3), 16);
  const g = parseInt(hex.slice(3,5), 16);
  const b = parseInt(hex.slice(5,7), 16);
  return `rgba(${r},${g},${b},${alpha})`;
}

// ── EVENT BINDINGS ────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  init();

  // Chart type selection
  document.querySelectorAll('.chart-type-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.chart-type-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentType = btn.dataset.type;
      renderChart();
    });
  });

  // Palette selection
  document.querySelectorAll('.palette-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.palette-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentPalette = PALETTES[btn.dataset.palette];
      // Update dataset colors to match new palette
      datasets.forEach((ds, i) => {
        ds.color = currentPalette[i % currentPalette.length];
        const swatch = document.getElementById(`ds-color-${i}`);
        if (swatch) swatch.value = ds.color;
      });
      renderChart();
    });
  });

  // Render button
  $('btn-render').addEventListener('click', () => {
    const btn = $('btn-render');
    btn.classList.add('animate-pulse');
    setTimeout(() => btn.classList.remove('animate-pulse'), 400);
    renderChart();
    showToast('📈 Chart rendered!');
  });

  // Add dataset
  $('btn-add-dataset').addEventListener('click', () => {
    const i = datasets.length;
    addDataset(`Dataset ${i + 1}`, [10, 20, 30, 40, 50, 60], currentPalette[i % currentPalette.length]);
    renderChart();
  });

  // Live preview on toggle changes
  ['opt-legend','opt-grid','opt-animate','opt-fill'].forEach(id => {
    $(id).addEventListener('change', renderChart);
  });

  // Title live update
  chartTitleInput.addEventListener('input', () => {
    chartTitleDisplay.textContent = chartTitleInput.value || 'My Chart';
  });
  dataLabelsInput.addEventListener('input', renderChart);

  // Theme toggle
  $('btn-theme').addEventListener('click', () => {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-theme') !== 'light';
    html.setAttribute('data-theme', isDark ? 'light' : 'dark');
    $('icon-moon').style.display = isDark ? 'none' : '';
    $('icon-sun').style.display  = isDark ? '' : 'none';
    setTimeout(renderChart, 50);
    showToast(isDark ? '☀️ Light mode' : '🌙 Dark mode');
  });

  // Export modal
  $('btn-export').addEventListener('click', () => $('modal-overlay').classList.add('active'));
  $('modal-close').addEventListener('click', () => $('modal-overlay').classList.remove('active'));
  $('modal-overlay').addEventListener('click', e => {
    if (e.target === $('modal-overlay')) $('modal-overlay').classList.remove('active');
  });
  $('exp-png').addEventListener('click',  () => { exportPNG();  $('modal-overlay').classList.remove('active'); });
  $('exp-jpg').addEventListener('click',  () => { exportJPG();  $('modal-overlay').classList.remove('active'); });
  $('exp-json').addEventListener('click', () => { exportJSON(); $('modal-overlay').classList.remove('active'); });

  // Copy chart
  $('btn-copy').addEventListener('click', copyChart);

  // Fullscreen
  $('btn-fullscreen').addEventListener('click', openFullscreen);
  $('fs-close').addEventListener('click', closeFullscreen);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeFullscreen();
  });

  // Hero buttons
  $('hero-start-btn').addEventListener('click', () => {
    document.getElementById('builder').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  $('hero-demo-btn').addEventListener('click', loadDemo);

  // Navbar shadow on scroll
  window.addEventListener('scroll', () => {
    const nav = $('navbar');
    nav.style.boxShadow = window.scrollY > 10
      ? '0 4px 30px rgba(0,0,0,0.3)'
      : 'none';
  });
});
