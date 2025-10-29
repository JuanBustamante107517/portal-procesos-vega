// frontend/src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import SalesTypesPage from './pages/SalesTypesPage';
import ProcessListPage from './pages/ProcessListPage'; // <-- 1. IMPORTA LA PÁGINA 4

function App() {
  const { user } = useAuth(); 

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={!user ? <LoginPage /> : <Navigate to="/" />} />
        <Route path="/" element={user ? <HomePage /> : <Navigate to="/login" />} />
        <Route path="/sales-types" element={user ? <SalesTypesPage /> : <Navigate to="/login" />} />
        
        {/* --- 2. ¡AÑADE ESTA NUEVA RUTA DINÁMICA! --- */}
        {/* El ':tipoVenta' será 'b2b' o 'b2c' */}
        <Route 
          path="/processes/:tipoVenta" 
          element={user ? <ProcessListPage /> : <Navigate to="/login" />} 
        />
        
        {/* (Aquí pondremos /process-detail/:id después) */}
        <Route path="*" element={<Navigate to={user ? "/" : "/login"} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;