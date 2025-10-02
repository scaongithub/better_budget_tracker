import React from 'react';
import { useBudget } from '../context/BudgetContext.jsx';

function YearlyProjection() {
  const { getYearlyProjection, selectedMonth } = useBudget();
  const projection = getYearlyProjection(selectedMonth);

  return (
    <section className="panel">
      <header className="panel-header">
        <div>
          <h2>Yearly recurring outlook</h2>
          <p>
            Understand how your recurring income and expenses influence your cash flow across the
            year.
          </p>
        </div>
      </header>
      <div className="yearly-grid">
        {projection.map((month) => (
          <div key={month.label} className="yearly-card">
            <span className="month-label">{month.label}</span>
            <div className="yearly-amounts">
              <div>
                <span className="label">Income</span>
                <span className="value income">${month.income.toLocaleString()}</span>
              </div>
              <div>
                <span className="label">Expenses</span>
                <span className="value expense">${month.expenses.toLocaleString()}</span>
              </div>
            </div>
            <div className={`yearly-balance ${month.balance >= 0 ? 'positive' : 'negative'}`}>
              {month.balance >= 0 ? 'Surplus' : 'Deficit'} ${Math.abs(month.balance).toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default YearlyProjection;
