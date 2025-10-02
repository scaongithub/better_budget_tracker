import React, { createContext, useContext, useMemo, useState } from 'react';
import {
  differenceInMonths,
  eachMonthOfInterval,
  endOfYear,
  format,
  isSameMonth,
  startOfMonth,
  startOfYear,
} from 'date-fns';

const BudgetContext = createContext(undefined);

const defaultTransactions = [
  {
    id: '1',
    type: 'income',
    description: 'Salary',
    amount: 4500,
    category: 'Salary',
    date: new Date().toISOString(),
    isRecurring: true,
    recurrence: 'monthly',
  },
  {
    id: '2',
    type: 'expense',
    description: 'Rent',
    amount: 1500,
    category: 'Housing',
    date: new Date().toISOString(),
    isRecurring: true,
    recurrence: 'monthly',
  },
];

const recurrenceMap = {
  monthly: 1,
  quarterly: 3,
  yearly: 12,
};

export function BudgetProvider({ children }) {
  const [monthlyBudget, setMonthlyBudget] = useState(4000);
  const [transactions, setTransactions] = useState(defaultTransactions);
  const [selectedMonth, setSelectedMonth] = useState(startOfMonth(new Date()));

  const value = useMemo(() => {
    const addTransaction = (transaction) => {
      setTransactions((prev) => [
        {
          ...transaction,
          id: crypto.randomUUID(),
          date: transaction.date || new Date().toISOString(),
        },
        ...prev,
      ]);
    };

    const updateMonthlyBudget = (value) => {
      setMonthlyBudget(Number(value));
    };

    const getMonthlyTransactions = (monthDate = selectedMonth) =>
      transactions.filter((transaction) =>
        isSameMonth(new Date(transaction.date), monthDate),
      );

    const getMonthlyTotals = (monthDate = selectedMonth) => {
      const monthlyTransactions = getMonthlyTransactions(monthDate);
      const income = monthlyTransactions
        .filter((transaction) => transaction.type === 'income')
        .reduce((sum, transaction) => sum + Number(transaction.amount), 0);
      const expenses = monthlyTransactions
        .filter((transaction) => transaction.type === 'expense')
        .reduce((sum, transaction) => sum + Number(transaction.amount), 0);

      return {
        income,
        expenses,
        balance: income - expenses,
        remaining: monthlyBudget - expenses,
      };
    };

    const getRecurringTransactionsForMonth = (month) => {
      const recurring = transactions.filter((transaction) => transaction.isRecurring);
      const monthlyTransactionIds = new Set(
        getMonthlyTransactions(month).map((transaction) => transaction.id),
      );

      return recurring
        .filter((transaction) => {
          const startMonth = startOfMonth(new Date(transaction.date));
          const interval = recurrenceMap[transaction.recurrence] ?? 1;

          if (startMonth > month) {
            return false;
          }

          const diff = differenceInMonths(month, startMonth);
          return diff % interval === 0;
        })
        .map((transaction) => {
          const startMonth = startOfMonth(new Date(transaction.date));
          const occursThisMonth = isSameMonth(startMonth, month);

          if (occursThisMonth && monthlyTransactionIds.has(transaction.id)) {
            return null;
          }

          return {
            ...transaction,
            id: `${transaction.id}-${format(month, 'yyyyMM')}`,
            date: month.toISOString(),
          };
        })
        .filter(Boolean);
    };

    const getYearlyProjection = (yearDate = selectedMonth) => {
      const months = eachMonthOfInterval({
        start: startOfYear(yearDate),
        end: endOfYear(yearDate),
      });

      return months.map((month) => {
        const monthTransactions = getMonthlyTransactions(month);
        const recurringTransactions = getRecurringTransactionsForMonth(month);
        const combined = [...monthTransactions, ...recurringTransactions];

        const income = combined
          .filter((transaction) => transaction.type === 'income')
          .reduce((sum, transaction) => sum + Number(transaction.amount), 0);

        const expenses = combined
          .filter((transaction) => transaction.type === 'expense')
          .reduce((sum, transaction) => sum + Number(transaction.amount), 0);

        return {
          label: format(month, 'MMM'),
          income,
          expenses,
          balance: income - expenses,
        };
      });
    };

    return {
      monthlyBudget,
      monthlyTotals: getMonthlyTotals(),
      transactions,
      selectedMonth,
      setSelectedMonth,
      addTransaction,
      updateMonthlyBudget,
      getMonthlyTransactions,
      getYearlyProjection,
    };
  }, [monthlyBudget, selectedMonth, transactions]);

  return <BudgetContext.Provider value={value}>{children}</BudgetContext.Provider>;
}

export const useBudget = () => {
  const context = useContext(BudgetContext);
  if (!context) {
    throw new Error('useBudget must be used within a BudgetProvider');
  }
  return context;
};
