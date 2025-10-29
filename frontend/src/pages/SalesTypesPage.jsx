// frontend/src/pages/SalesTypesPage.jsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

// --- Estilos Manuales ---
const styles = {
  page: {
    minHeight: '100vh',
    backgroundColor: '#991b1b', // ¡Fondo Rojo Oscuro!
    padding: '24px',
    color: 'white', // Texto blanco para contrastar
    fontFamily: 'system-ui, sans-serif'
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '32px'
  },
  backButton: {
    padding: '8px',
    marginRight: '16px',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    border: 'none',
    borderRadius: '50%',
    color: 'white',
    cursor: 'pointer'
  },
  headerTitle: {
    fontSize: '30px',
    fontWeight: 'bold',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)', // 2 columnas
    gap: '24px'
  },
  card: {
    display: 'block',
    padding: '24px',
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    textDecoration: 'none',
    color: '#1e293b', // Texto oscuro dentro de la tarjeta
  },
  cardTitle: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#1d4ed8', // Azul
    marginBottom: '12px'
  }
};
// --- Fin de Estilos ---

function SalesTypesPage() {
  const navigate = useNavigate(); // Hook para el botón "Volver"

  return (
    <div style={styles.page}>
      
      <header style={styles.header}>
        <button onClick={() => navigate(-1)} style={styles.backButton} title="Volver">
          {/* Un ícono simple de flecha */}
          &#8592; 
        </button>
        <h1 style={styles.headerTitle}>Tipos de Venta</h1>
      </header>

      {/* --- PÁGINA 3: Módulos de Venta B2B y B2C --- */}
      <section>
        <div style={styles.grid}>
          {/* Tarjeta B2B */}
          <Link to="/processes/b2b" style={styles.card}>
            <h3 style={styles.cardTitle}>Ventas B2B</h3>
            <p>
              Accede a los procesos de licitaciones y campañas 
              (Navidad, Fiestas Patrias, etc.).
            </p>
          </Link>
          
          {/* Tarjeta B2C */}
          <Link to="/processes/b2c" style={styles.card}>
            <h3 style={styles.cardTitle}>Ventas B2C</h3>
            <p>
              Consulta los procedimientos para E-commerce y tiendas físicas.
            </p>
          </Link>
        </div>
      </section>
    </div>
  );
}

export default SalesTypesPage;