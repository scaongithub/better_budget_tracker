import React from 'react';
import MonthlyOverview from './MonthlyOverview.jsx';
import TransactionForm from './TransactionForm.jsx';
import TransactionTable from './TransactionTable.jsx';
import YearlyProjection from './YearlyProjection.jsx';

function Dashboard({ onLogout }) {
  return (
    <div className="dashboard">
      <header className="topbar">
        <div>
          <h1>Better Budget Tracker</h1>
          <span className="subtitle">Plan monthly. Anticipate yearly.</span>
        </div>
        <button type="button" onClick={onLogout} className="ghost-button">
          Log out
        </button>
      </header>
      <main className="dashboard-content">
        <MonthlyOverview />
        <div className="grid two-column">
          <TransactionForm />
          <TransactionTable />
        </div>
        <YearlyProjection />
      </main>
    </div>
  );
}

export default Dashboard;
