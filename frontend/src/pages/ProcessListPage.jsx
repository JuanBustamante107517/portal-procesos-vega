// frontend/src/pages/ProcessListPage.jsx
import React, { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

// --- Estilos Manuales (El método a prueba de fallos) ---
const styles = {
  page: {
    minHeight: '100vh',
    backgroundColor: '#991b1b', // Fondo Rojo
    padding: '24px',
    color: 'white',
    fontFamily: 'system-ui, sans-serif'
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '32px'
  },
  backButton: {
    padding: '8px 12px', // Ligeramente más grande
    marginRight: '16px',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    border: 'none',
    borderRadius: '50%',
    color: 'white',
    cursor: 'pointer',
    fontSize: '24px', // Flecha más grande
    lineHeight: '1'
  },
  headerTitle: {
    fontSize: '30px',
    fontWeight: 'bold'
  },
  loadingText: {
    textAlign: 'center',
    fontSize: '18px',
    marginTop: '40px'
  },
  // Estilo para las tarjetas de Proceso (Licitación, etc.)
  card: {
    display: 'block',
    padding: '24px',
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    textDecoration: 'none',
    color: '#1e293b',
    marginBottom: '16px', // Espacio entre tarjetas
  },
  cardTitle: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#1d4ed8',
    marginBottom: '8px'
  },
  cardDescription: {
    fontSize: '16px',
    lineHeight: '1.6',
    color: '#334155',
  }
};
// --- Fin de Estilos ---

function ProcessListPage() {
  const navigate = useNavigate();
  const { authTokens } = useAuth();
  const { tipoVenta } = useParams(); // 'b2b' o 'b2c'

  const [procesos, setProcesos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const pageTitle = tipoVenta.toUpperCase() === 'B2B' ? 'Ventas B2B' : 'Ventas B2C';

  useEffect(() => {
    const fetchProcesos = async () => {
      // --- Verificación previa ---
      if (!authTokens || !authTokens.access) {
        setError("No estás autenticado. Por favor, inicia sesión.");
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        // --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
        // Aseguramos que la cabecera Authorization tenga el formato
        // EXACTO: "Bearer <espacio> <token>"
        // REEMPLAZAR DESDE AQUÍ
        const token = localStorage.getItem('access'); // Recuperamos el token guardado

        const response = await axios.get(
          // CAMBIO 1: Poner la IP pública de AWS, no localhost
          `http://44.203.244.176:8001/api/processes/?tipo_venta=${tipoVenta.toUpperCase()}`,
          {
            // CAMBIO 2: Agregar los headers para que no salga 401
            headers: {
              'Authorization': `Bearer ${token}`
            }
          }
        );
        // HASTA AQUÍ

        setProcesos(response.data);
      } catch (err) {
        console.error("Error al cargar procesos:", err.response || err.message); // Log más detallado
        if (err.response && err.response.status === 403) {
          setError('Error 403: No tienes permiso para ver estos procesos.');
        } else {
          setError('No se pudieron cargar los procesos. Revisa la consola.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProcesos();
  }, [tipoVenta, authTokens]); // Dependencias sin cambios


  return (
    <div style={styles.page}>

      <header style={styles.header}>
        <button onClick={() => navigate(-1)} style={styles.backButton} title="Volver">
          &#8592;
        </button>
        <h1 style={styles.headerTitle}>{pageTitle}</h1>
      </header>

      <section>
        {loading && <p style={styles.loadingText}>Cargando procesos...</p>}
        {error && <p style={styles.loadingText}>{error}</p>}

        {!loading && !error && (
          <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            {procesos.length > 0 ? (
              procesos.map((proceso) => (
                <Link
                  to={`/process-detail/${proceso.id}`} // Enlazamos a la "Página 5"
                  key={proceso.id}
                  style={styles.card}
                >
                  <h3 style={styles.cardTitle}>{proceso.titulo}</h3>
                  {/* ¡USAMOS LA DESCRIPCIÓN CON EMPEÑO! */}
                  <p style={styles.cardDescription}>{proceso.descripcion}</p>
                </Link>
              ))
            ) : (
              <p style={styles.loadingText}>No se encontraron procesos para '{pageTitle}'.</p>
            )}
          </div>
        )}
      </section>
    </div>
  );
}

export default ProcessListPage;