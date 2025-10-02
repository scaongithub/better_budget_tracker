import React, { useState } from 'react';
import { format } from 'date-fns';
import { useBudget } from '../context/BudgetContext.jsx';

const defaultForm = {
  type: 'expense',
  description: '',
  amount: '',
  category: '',
  date: format(new Date(), 'yyyy-MM-dd'),
  isRecurring: false,
  recurrence: 'monthly',
};

const recurrenceOptions = [
  { value: 'monthly', label: 'Monthly' },
  { value: 'quarterly', label: 'Quarterly' },
  { value: 'yearly', label: 'Yearly' },
];

function TransactionForm() {
  const { addTransaction } = useBudget();
  const [form, setForm] = useState(defaultForm);

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setForm((previous) => ({
      ...previous,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!form.description || !form.amount) {
      return;
    }

    addTransaction({
      ...form,
      amount: Number(form.amount),
      date: new Date(form.date).toISOString(),
    });

    setForm((prev) => ({
      ...defaultForm,
      type: prev.type,
    }));
  };

  return (
    <section className="panel">
      <header className="panel-header">
        <div>
          <h2>Add income or expense</h2>
          <p>Capture new transactions and mark them as recurring when applicable.</p>
        </div>
      </header>
      <form className="transaction-form" onSubmit={handleSubmit}>
        <div className="form-row">
          <label>
            <span>Type</span>
            <select name="type" value={form.type} onChange={handleChange}>
              <option value="income">Income</option>
              <option value="expense">Expense</option>
            </select>
          </label>
          <label>
            <span>Amount</span>
            <input
              type="number"
              name="amount"
              min="0"
              step="0.01"
              value={form.amount}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            <span>Date</span>
            <input type="date" name="date" value={form.date} onChange={handleChange} required />
          </label>
        </div>
        <div className="form-row">
          <label className="full-width">
            <span>Description</span>
            <input
              type="text"
              name="description"
              placeholder="e.g. Groceries, Freelance project"
              value={form.description}
              onChange={handleChange}
              required
            />
          </label>
        </div>
        <div className="form-row">
          <label className="full-width">
            <span>Category</span>
            <input
              type="text"
              name="category"
              placeholder="e.g. Housing, Utilities, Transportation"
              value={form.category}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-row form-row-inline">
          <label className="checkbox">
            <input type="checkbox" name="isRecurring" checked={form.isRecurring} onChange={handleChange} />
            <span>Recurring transaction</span>
          </label>
          {form.isRecurring ? (
            <label>
              <span>Frequency</span>
              <select name="recurrence" value={form.recurrence} onChange={handleChange}>
                {recurrenceOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
          ) : null}
        </div>
        <div className="form-actions">
          <button type="submit">Save transaction</button>
        </div>
      </form>
    </section>
  );
}

export default TransactionForm;
