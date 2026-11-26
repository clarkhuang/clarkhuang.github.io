// The static page contains every entry. Narrow it to calendar periods on demand.
for (const form of document.querySelectorAll('[data-history-filter]')) {
  const scale = form.dataset.historyFilter;
  const input = form.elements.periods;
  const rows = Array.from(document.querySelectorAll('[data-period-number]'));
  const status = form.querySelector('[role="status"]');
  const dateParts = Object.fromEntries(new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Detroit', year: 'numeric', month: 'numeric', day: 'numeric'
  }).formatToParts(new Date()).map(part => [part.type, part.value]));
  const year = Number(dateParts.year);
  const month = Number(dateParts.month) - 1;
  const day = Math.floor(Date.UTC(year, month, Number(dateParts.day)) / 86400000);
  // The UTC ordinal represents a Detroit calendar day, including across DST.
  const current = scale === 'monthly' ? year * 12 + month
    : scale === 'weekly' ? Math.floor((day + 3) / 7) : day;

  function apply(all) {
    let visible = 0;
    for (const row of rows) {
      const age = current - Number(row.dataset.periodNumber);
      row.hidden = !all && !(age >= 0 && age < input.valueAsNumber);
      if (!row.hidden) visible++;
    }
    status.textContent = visible === 0 ? 'No production updates in this window.'
      : 'Showing ' + visible + (visible === 1 ? ' entry.' : ' entries.');
  }
  form.addEventListener('submit', event => {
    event.preventDefault();
    apply(false);
  });
  form.querySelector('[data-show-all]').addEventListener('click', () => apply(true));
  form.hidden = false;
  apply(form.dataset.initialWindow === 'all');
}
