# Frontend Architecture Overview

## Tech Stack
- **React 18** with functional components and hooks.
- **Vite** for fast development server and production builds.
- **date-fns** to format dates and power monthly/yearly calculations.
- Vanilla CSS with a single `global.css` file for layout and theming.

## Directory Structure
```
src/
  App.jsx              # Authentication gate and root layout
  main.jsx             # React entry point
  context/
    BudgetContext.jsx  # Shared state + derived selectors
  components/
    Login.jsx          # Login screen
    Dashboard.jsx      # Dashboard composition and layout
    MonthlyOverview.jsx
    TransactionForm.jsx
    TransactionTable.jsx
    YearlyProjection.jsx
  styles/
    global.css         # Global styles and component-specific classes
```

## State Management
`BudgetContext` centralises budgeting data:
- `monthlyBudget`: numeric budget target for the selected month.
- `transactions`: array of income and expense entries.
- `selectedMonth`: Date object for the currently focused month.

The provider exposes helper selectors and actions:
- `addTransaction(transaction)` adds a new transaction (with generated id/date defaults).
- `updateMonthlyBudget(value)` updates the monthly target.
- `setSelectedMonth(date)` toggles which month is visible.
- `getMonthlyTransactions(date)` returns transactions within the month.
- `monthlyTotals` computed totals (income, expenses, balance, remaining).
- `getYearlyProjection(date)` generates a 12-month view factoring in recurring items.

## Components
- **Login** – Collects email/password and signals successful login with `onLogin` callback.
- **Dashboard** – Provides top-level layout with logout control and arranges the main panels.
- **MonthlyOverview** – Displays month selector, budget input, and summary cards.
- **TransactionForm** – Handles new income/expense creation and recurring flags.
- **TransactionTable** – Lists current month transactions in a responsive table.
- **YearlyProjection** – Summarises recurring effects across the year in a grid layout.

## Data Flow
1. User submits login form and `App` toggles authenticated state.
2. Dashboard loads components that consume `BudgetContext` values.
3. Adding a transaction via `TransactionForm` updates context state.
4. Derived selectors recompute monthly totals, transaction list, and yearly projection automatically.

## Styling Approach
- Neon-inspired dark theme with gradient backgrounds and glassmorphism cards.
- CSS classes grouped by component sections to keep specificity low.
- Responsive breakpoints adjust padding, grids, and control layouts below 768px.

## Extensibility Notes
- Replace mock login with real authentication by integrating API requests in `Login` and storing tokens.
- Persist transactions via local storage or remote API by wrapping context setters with fetch logic.
- Introduce routing (e.g., React Router) if the app grows beyond two screens.
- Add tests (unit + integration) once backend endpoints and more business logic exist.
