# Better Budget Tracker API

This project provides the backend for a budget tracking web application built with [FastAPI](https://fastapi.tiangolo.com/). It offers authentication for two default profiles (Carlo and Paola), and endpoints to manage income and expense transactions with support for recurring items. Monthly and yearly dashboard summaries are exposed for consumption by a front-end client.

## Features

- OAuth2 password-based login with in-memory access tokens.
- Pre-seeded demo profiles for Carlo and Paola including representative transactions.
- CRUD endpoint to register incomes and expenses.
- Monthly dashboard summary combining single and recurring transactions.
- Yearly overview aggregating recurring transactions across the calendar year.

## Getting Started

### Installation

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Alternatively, install dependencies directly from the project:

```bash
pip install -r <(python -c "import tomllib; print('\n'.join(tomllib.load(open('pyproject.toml', 'rb'))['project']['dependencies']))")
```

### Running the Application

Start the API with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The server will automatically create the SQLite database (`budget.db`) and seed the default users and example transactions.

### Authentication

Use the `/auth/login` endpoint to obtain an access token. Example credentials:

- **Carlo** — username: `carlo`, password: `carlo123`
- **Paola** — username: `paola`, password: `paola123`

Submit a `POST` request with form data (`username`, `password`) and use the returned bearer token for subsequent requests.

### Dashboard Endpoints

- `GET /dashboard/monthly?year=2024&month=5` — Monthly summary for the specified month.
- `GET /dashboard/yearly?year=2024` — Yearly summary aggregating recurring transactions.
- `POST /dashboard/transactions` — Add an income or expense.
- `GET /dashboard/transactions` — List all recorded transactions for the authenticated user.

Each dashboard endpoint requires the `Authorization: Bearer <token>` header.

## Project Structure

```
app/
├── auth.py
├── crud.py
├── database.py
├── main.py
├── models.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   └── dashboard.py
├── schemas.py
├── seed.py
├── security.py
└── services.py
```

The SQLite database file `budget.db` is generated at runtime.

## Testing the API

You can interact with the API using the automatically generated OpenAPI docs at `http://localhost:8000/docs` after starting the server.

## License

This project is provided under the terms of the [MIT License](LICENSE).
=======
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
