/* ═══════════════════════════════════════════════
   Junaid Motors — Main JavaScript & Charts
   ═══════════════════════════════════════════════ */

// ─── PKR Formatter ───
function formatPKR(amount) {
  if (!amount && amount !== 0) return 'Rs. 0';
  return 'Rs. ' + Number(amount).toLocaleString('en-PK');
}

// ─── Auto-dismiss Django messages as Bootstrap Toasts ───
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.toast').forEach(function (el) {
    new bootstrap.Toast(el, { delay: 4500 }).show();
  });
});

// ─── Real-time clock (Pakistan Standard Time UTC+5) ───
function updateClock() {
  const clock = document.getElementById('live-clock');
  if (!clock) return;
  const now = new Date();
  const pkTime = new Date(now.getTime() + (5 * 60 * 60 * 1000));
  const timeStr = pkTime.toISOString().replace('T', ' ').substring(0, 19) + ' PKT';
  clock.textContent = timeStr;
}
setInterval(updateClock, 1000);
updateClock();

// ─── Confirm delete dialogs ───
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      const msg = el.getAttribute('data-confirm') || 'Are you sure?';
      if (!confirm(msg)) e.preventDefault();
    });
  });
});

// ─── Print invoice ───
function printInvoice() {
  window.print();
}

// ─── Installment Calculator (new_sale.html) ───
function initInstallmentCalc() {
  const paymentType = document.getElementById('id_payment_type');
  const installSection = document.getElementById('installment-section');
  const downPayment = document.getElementById('id_down_payment');
  const monthly = document.getElementById('id_monthly_installment');
  const months = document.getElementById('id_installment_months');
  const totalAmount = document.getElementById('id_total_amount');
  const previewTable = document.getElementById('installment-preview');

  if (!paymentType) return;

  function toggleInstallSection() {
    if (paymentType.value === 'installment') {
      installSection && installSection.classList.remove('d-none');
    } else {
      installSection && installSection.classList.add('d-none');
      generateInstallmentPreview();
    }
  }

  function calculateTotal() {
    if (paymentType.value === 'installment') {
      const dp = parseFloat(downPayment?.value || 0);
      const m = parseFloat(monthly?.value || 0);
      const mo = parseInt(months?.value || 0);
      const total = dp + (m * mo);
      if (totalAmount) totalAmount.value = total.toFixed(2);
      updateProfitPreview();
      generateInstallmentPreview();
    }
    updateProfitPreview();
  }

  function generateInstallmentPreview() {
    if (!previewTable) return;
    const m = parseFloat(monthly?.value || 0);
    const mo = parseInt(months?.value || 0);
    if (paymentType.value !== 'installment' || mo === 0) {
      previewTable.innerHTML = '';
      return;
    }
    let rows = '';
    const today = new Date();
    for (let i = 1; i <= mo; i++) {
      const due = new Date(today);
      due.setDate(due.getDate() + 30 * i);
      const dateStr = due.toLocaleDateString('en-PK', { day: '2-digit', month: 'short', year: 'numeric' });
      rows += `<tr>
        <td>${i}</td>
        <td>${dateStr}</td>
        <td>${formatPKR(m)}</td>
        <td><span class="badge badge-pending">Pending</span></td>
      </tr>`;
    }
    previewTable.innerHTML = rows;
  }

  paymentType?.addEventListener('change', toggleInstallSection);
  downPayment?.addEventListener('input', calculateTotal);
  monthly?.addEventListener('input', calculateTotal);
  months?.addEventListener('input', calculateTotal);
  toggleInstallSection();
}

// ─── Car AJAX Detail (new_sale.html) ───
function initCarDetailAjax() {
  const carSelect = document.getElementById('id_car');
  const carInfo = document.getElementById('car-info-box');
  if (!carSelect) return;

  carSelect.addEventListener('change', function () {
    const carId = this.value;
    if (!carId) { carInfo && (carInfo.innerHTML = ''); return; }

    fetch(`/inventory/${carId}/json/`)
      .then(r => r.json())
      .then(data => {
        if (!carInfo) return;
        carInfo.innerHTML = `
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <div class="fw-bold">${data.name}</div>
              <div class="text-muted-custom" style="font-size:0.8rem">Purchase Cost: ${formatPKR(data.purchase_price)}</div>
              <div class="text-muted-custom" style="font-size:0.8rem">Suggested Price: ${formatPKR(data.selling_price)}</div>
            </div>
            <div class="text-end">
              <div class="text-profit fw-bold">${formatPKR(data.profit_margin)}</div>
              <div style="font-size:0.72rem;color:var(--text-muted)">Profit Margin</div>
            </div>
          </div>`;
        // Pre-fill total amount
        const totalAmount = document.getElementById('id_total_amount');
        if (totalAmount && !totalAmount.value) totalAmount.value = data.selling_price;
        updateProfitPreview();
      })
      .catch(() => { if (carInfo) carInfo.innerHTML = ''; });
  });
}

// ─── Live Profit Preview ───
function updateProfitPreview() {
  const carSelect = document.getElementById('id_car');
  const totalAmount = document.getElementById('id_total_amount');
  const profitPreview = document.getElementById('profit-preview');
  if (!profitPreview || !carSelect || !totalAmount) return;

  const selectedOption = carSelect.options[carSelect.selectedIndex];
  const purchasePrice = parseFloat(selectedOption?.dataset?.purchasePrice || 0);
  const total = parseFloat(totalAmount.value || 0);
  const profit = total - purchasePrice;

  profitPreview.textContent = formatPKR(profit);
  profitPreview.className = profit >= 0 ? 'text-profit fw-bold' : 'text-loss fw-bold';
}

// ─── Dashboard Charts (Executive White & Blue Theme) ───
function initDashboardCharts(monthlySalesData, carsData) {
  const revenueCtx = document.getElementById('revenueChart');
  const doughnutCtx = document.getElementById('statusChart');

  if (revenueCtx && monthlySalesData) {
    new Chart(revenueCtx, {
      type: 'bar',
      data: {
        labels: monthlySalesData.map(d => d.month),
        datasets: [{
          label: 'Revenue',
          data: monthlySalesData.map(d => d.revenue),
          backgroundColor: 'rgba(37, 99, 235, 0.75)',
          borderColor: '#2563EB',
          borderWidth: 1.5,
          borderRadius: 6,
        }, {
          label: 'Cars Sold',
          data: monthlySalesData.map(d => d.count),
          backgroundColor: 'rgba(14, 165, 233, 0.65)',
          borderColor: '#0EA5E9',
          borderWidth: 1.5,
          borderRadius: 6,
          yAxisID: 'y1',
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { labels: { color: '#475569', font: { size: 11, weight: '600' } } },
        },
        scales: {
          x: { grid: { color: '#E2E8F0' }, ticks: { color: '#64748B', font: { size: 10 } } },
          y: { grid: { color: '#E2E8F0' }, ticks: { color: '#64748B', font: { size: 10 }, callback: v => 'Rs.' + (v/1000).toFixed(0) + 'K' } },
          y1: { position: 'right', grid: { drawOnChartArea: false }, ticks: { color: '#64748B', font: { size: 10 } } },
        }
      }
    });
  }

  if (doughnutCtx && carsData) {
    new Chart(doughnutCtx, {
      type: 'doughnut',
      data: {
        labels: ['Available', 'Sold', 'Reserved', 'Under Repair'],
        datasets: [{
          data: [carsData.available, carsData.sold, carsData.reserved, carsData.repair],
          backgroundColor: ['rgba(37, 99, 235, 0.85)', 'rgba(239, 68, 68, 0.85)', 'rgba(14, 165, 233, 0.85)', 'rgba(100, 116, 139, 0.85)'],
          borderColor: ['#2563EB', '#EF4444', '#0EA5E9', '#64748B'],
          borderWidth: 1.5,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '68%',
        plugins: {
          legend: { position: 'bottom', labels: { color: '#475569', font: { size: 11, weight: '600' }, padding: 12 } },
        }
      }
    });
  }
}

// ─── PnL Report Chart ───
function initPnlChart(monthlyData) {
  const ctx = document.getElementById('pnlChart');
  if (!ctx || !monthlyData) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: monthlyData.map(d => d.month),
      datasets: [{
        label: 'Profit',
        data: monthlyData.map(d => parseFloat(d.profit)),
        backgroundColor: 'rgba(16, 185, 129, 0.75)',
        borderColor: '#10B981',
        borderWidth: 1.5,
        borderRadius: 6,
      }, {
        label: 'Revenue',
        data: monthlyData.map(d => parseFloat(d.revenue)),
        backgroundColor: 'rgba(37, 99, 235, 0.5)',
        borderColor: '#2563EB',
        borderWidth: 1.5,
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#475569', font: { size: 11, weight: '600' } } },
      },
      scales: {
        x: { grid: { color: '#E2E8F0' }, ticks: { color: '#64748B', font: { size: 10 } } },
        y: { grid: { color: '#E2E8F0' }, ticks: { color: '#64748B', font: { size: 10 }, callback: v => 'Rs.' + (v/1000).toFixed(0) + 'K' } },
      }
    }
  });
}

// ─── Init on DOM ready ───
document.addEventListener('DOMContentLoaded', function () {
  initInstallmentCalc();
  initCarDetailAjax();
});
