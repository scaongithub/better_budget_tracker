import React from 'react';
import { format } from 'date-fns';
import { useBudget } from '../context/BudgetContext.jsx';

function TransactionTable() {
  const { getMonthlyTransactions, selectedMonth } = useBudget();
  const transactions = getMonthlyTransactions(selectedMonth);

  if (transactions.length === 0) {
    return (
      <section className="panel">
        <header className="panel-header">
          <div>
            <h2>This month&apos;s transactions</h2>
            <p>No transactions yet. Add your first expense or income to get started.</p>
          </div>
        </header>
      </section>
    );
  }

  return (
    <section className="panel">
      <header className="panel-header">
        <div>
          <h2>This month&apos;s transactions</h2>
          <p>Review the inflows and outflows affecting your monthly budget.</p>
        </div>
      </header>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th align="left">Date</th>
              <th align="left">Description</th>
              <th align="left">Category</th>
              <th align="right">Amount</th>
              <th align="left">Type</th>
              <th align="left">Recurring</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.id}>
                <td>{format(new Date(transaction.date), 'MMM d')}</td>
                <td>{transaction.description}</td>
                <td>{transaction.category || '—'}</td>
                <td className={transaction.type === 'income' ? 'income' : 'expense'}>
                  {transaction.type === 'income' ? '+' : '-'}${transaction.amount.toLocaleString()}
                </td>
                <td>{transaction.type}</td>
                <td>{transaction.isRecurring ? `Every ${transaction.recurrence}` : 'One-time'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default TransactionTable;
