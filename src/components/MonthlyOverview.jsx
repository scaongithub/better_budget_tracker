import React from 'react';
import { format } from 'date-fns';
import { useBudget } from '../context/BudgetContext.jsx';

function StatCard({ label, amount, highlight }) {
  return (
    <div className={`stat-card ${highlight || ''}`}>
      <span className="stat-label">{label}</span>
      <span className="stat-amount">${amount.toLocaleString()}</span>
    </div>
  );
}

function MonthlyOverview() {
  const { monthlyBudget, monthlyTotals, selectedMonth, setSelectedMonth, updateMonthlyBudget } =
    useBudget();

  const handleMonthChange = (event) => {
    const [year, month] = event.target.value.split('-').map(Number);
    setSelectedMonth(new Date(year, month - 1, 1));
  };

  return (
    <section className="panel">
      <header className="panel-header">
        <div>
          <h2>{format(selectedMonth, 'MMMM yyyy')} overview</h2>
          <p>Track how this month&apos;s income and expenses affect your budget.</p>
        </div>
        <div className="controls">
          <label className="control">
            <span>Month</span>
            <input
              type="month"
              value={format(selectedMonth, 'yyyy-MM')}
              onChange={handleMonthChange}
            />
          </label>
          <label className="control">
            <span>Monthly budget</span>
            <input
              type="number"
              min="0"
              value={monthlyBudget}
              onChange={(event) => updateMonthlyBudget(event.target.value)}
            />
          </label>
        </div>
      </header>
      <div className="stats-grid">
        <StatCard label="Total income" amount={monthlyTotals.income} />
        <StatCard label="Total expenses" amount={monthlyTotals.expenses} />
        <StatCard label="Net balance" amount={monthlyTotals.balance} highlight={monthlyTotals.balance >= 0 ? 'positive' : 'negative'} />
        <StatCard label="Budget remaining" amount={monthlyTotals.remaining} highlight={monthlyTotals.remaining >= 0 ? 'positive' : 'negative'} />
      </div>
    </section>
  );
}

export default MonthlyOverview;
