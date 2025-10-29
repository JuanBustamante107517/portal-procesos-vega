// frontend/src/pages/LoginPage.jsx
import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

// --- Estilos Manuales (Estos no cambian) ---
const styles = {
  container: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    backgroundColor: '#991b1b', // Fondo Rojo Oscuro
    fontFamily: 'system-ui, sans-serif'
  },
  card: {
    width: '100%',
    maxWidth: '400px', // Barras más cortas
    padding: '32px',
    backgroundColor: 'white',
    borderRadius: '16px',
    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.1)'
  },
  title: {
    fontSize: '30px',
    fontWeight: 'bold',
    color: '#1e293b',
    textAlign: 'center'
  },
  subtitle: {
    marginTop: '8px',
    color: '#64748b',
    textAlign: 'center'
  },
  form: {
    marginTop: '24px',
    display: 'flex',
    flexDirection: 'column',
    gap: '16px'
  },
  label: {
    display: 'block',
    fontSize: '14px',
    fontWeight: '500',
    color: '#334155',
    marginBottom: '4px'
  },
  input: {
    width: '100%',
    padding: '12px 16px',
    color: '#1e293b',
    border: '1px solid #cbd5e1',
    borderRadius: '8px',
    boxSizing: 'border-box'
  },
  button: {
    padding: '12px 24px',
    fontWeight: '500',
    color: 'white',
    backgroundColor: '#2563eb', // Azul
    borderRadius: '8px',
    border: 'none',
    cursor: 'pointer'
  },
  link: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#2563eb', // Azul
    textDecoration: 'none'
  },
  error: {
    padding: '12px',
    textAlign: 'center',
    fontSize: '14px',
    color: '#b91c1c', // Rojo
    backgroundColor: '#fee2e2', // Fondo rojo claro
    borderRadius: '8px'
  }
};
// --- Fin de Estilos ---

function LoginPage() {
  // --- SECCIÓN CORREGIDA ---
  // Ahora cada variable tiene su función correcta:
  // username -> setUsername
  // password -> setPassword
  const [username, setUsername] = useState(''); // <-- ARREGLADO
  const [password, setPassword] = useState(''); // <-- ARREGLADO
  const [error, setError] = useState(null);
  // --- FIN DE LA CORRECCIÓN ---

  const { loginUser } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      // Ahora usamos 'password' (el nombre limpio)
      await loginUser(username, password); 
    } catch (err) {
      setError('Usuario o contraseña incorrectos.');
      console.error(err);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={{ textAlign: 'center' }}>
          <h1 style={styles.title}>Portal de Procesos</h1>
          <p style={styles.subtitle}>Bienvenido</p>
        </div>

        <form style={styles.form} onSubmit={handleSubmit}>
          {error && (
            <div style={styles.error}>
              {error}
            </div>
          )}

          <div>
            <label htmlFor="username" style={styles.label}>
              Nombre de Usuario
            </label>
            <input
              id="username"
              type="text"
              required
              value={username}
              // Ahora setUsername SÍ existe y funcionará
              onChange={(e) => setUsername(e.target.value)} 
              style={styles.input}
              placeholder="ej: admin"
            />
          </div>

          <div>
            <label htmlFor="password" style={styles.label}>
              Contraseña
            </label>
            <input
              id="password"
              type="password"
              required
              value={password} // <-- CORREGIDO
              onChange={(e) => setPassword(e.target.value)} // <-- CORREGIDO
              style={styles.input}
              placeholder="••••••••"
            />
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '8px' }}>
            <a href="#" style={styles.link}>
              ¿Olvidaste tu contraseña?
            </a>
            <button type="submit" style={styles.button}>
              Entrar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;