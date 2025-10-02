# Better Budget Tracker Frontend

A polished React single-page application that showcases a budgeting dashboard with monthly management and yearly recurring projections. The experience starts on a login screen and transitions into a dashboard once authenticated.

## Getting Started

```bash
npm install
npm run dev
```

> **Note:** If npm registry access is restricted in your environment, dependency installation may fail. The application relies only on `react`, `react-dom`, `date-fns`, and `vite`.

## Available Scripts
- `npm run dev` – Launches the Vite development server.
- `npm run build` – Creates an optimised production build.
- `npm run preview` – Serves the production build locally.

## Features
- **Login gateway** – Simple sign-in form that guards the dashboard.
- **Monthly overview** – Budget, income, expense, balance, and remaining budget cards.
- **Transaction capture** – Add income and expenses with recurring frequency controls.
- **Transaction list** – Review monthly transactions in a responsive table.
- **Yearly projection** – Visualise how recurring income/expense items affect each month.

## Project Structure
See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the detailed breakdown and [docs/PLAN.md](docs/PLAN.md) for the delivery plan.

## Future Work
- Persist data via API or local storage.
- Support transaction editing and deletion.
- Enhance projections with chart visualisations and scenario planning.
