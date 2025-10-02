import React, { useState } from 'react';
import { BudgetProvider } from './context/BudgetContext.jsx';
import Dashboard from './components/Dashboard.jsx';
import Login from './components/Login.jsx';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <BudgetProvider>
      <div className="app-shell">
        {isAuthenticated ? (
          <Dashboard onLogout={() => setIsAuthenticated(false)} />
        ) : (
          <Login onLogin={() => setIsAuthenticated(true)} />
        )}
      </div>
    </BudgetProvider>
  );
}

export default App;
