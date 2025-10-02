# Better Budget Tracker Frontend Plan

## Goals
- Provide a polished React single-page application for budget tracking.
- Offer a simple authentication gateway that leads to a budgeting dashboard.
- Enable monthly budget monitoring, quick transaction capture, and yearly recurring projections.
- Build a foundation that is easy to extend with a future backend or design system.

## User Journey
1. **Authentication landing** – users see a focused login card with brand messaging.
2. **Dashboard entry** – successful sign-in reveals the main budgeting workspace.
3. **Monthly management** – users adjust the target monthly budget, add transactions, and review totals.
4. **Yearly planning** – recurring transactions surface in a yearly projection grid for long-term insight.

## Functional Requirements
- Client-side login form (no backend integration yet).
- Persistent layout with:
  - Monthly overview cards (budget, income, expenses, remaining balance).
  - Transaction form for income/expense entry with recurring flags.
  - Monthly transaction list.
  - Yearly projection view driven by recurring transactions.
- Reusable state container to share data and derived totals across components.

## Non-Functional Requirements
- Responsive layout that works on desktop and tablet viewports.
- Accessible form markup with labels and semantic HTML elements.
- Modular component structure with clear responsibilities.
- Documented architecture and future improvement opportunities.

## Implementation Steps
1. **Project bootstrap** – configure Vite + React project structure, scripts, and global styling.
2. **State management** – implement `BudgetContext` with helper selectors for monthly totals and yearly projections.
3. **Authentication gate** – create a controlled login form that toggles dashboard visibility when successful.
4. **Dashboard skeleton** – assemble layout sections (overview, forms, tables, projection) and shared UI patterns.
5. **Transaction workflows** – wire the form to push data into context state and refresh dependent views.
6. **Recurring logic** – calculate yearly projections by expanding recurring transactions across months.
7. **Styling polish** – craft cohesive visual design with gradients, cards, and responsive adjustments.
8. **Documentation** – capture architecture decisions, state shape, and extension ideas for future work.

## Future Enhancements
- Integrate real authentication and persistence through APIs.
- Add editing/deleting of transactions and categories.
- Introduce data visualisations (charts) for monthly trends.
- Persist preferences and transactions in local storage or a backend service.
- Expand recurring scheduling to allow custom intervals and end dates.
