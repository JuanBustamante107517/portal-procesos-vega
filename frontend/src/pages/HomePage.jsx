// frontend/src/pages/HomePage.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// --- Estilos Manuales (Nuestro método a prueba de fallos) ---
const styles = {
  // Página completa
  page: {
    minHeight: '100vh',
    backgroundColor: '#991b1b', // ¡Fondo Rojo Oscuro!
    padding: '24px',
    color: 'white',
    fontFamily: 'system-ui, sans-serif'
  },
  // Cabecera (Bienvenido + Botón Salir)
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '32px',
  },
  headerText: {
    headerTitle: { fontSize: '30px', fontWeight: 'bold' },
    headerSubtitle: { fontSize: '16px', color: '#fecaca' }
  },
  logoutButton: {
    padding: '8px 16px',
    fontSize: '14px',
    fontWeight: '500',
    color: '#dc2626', // Rojo
    backgroundColor: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
  },
  // La tarjeta blanca principal
  section: {
    padding: '32px', // Más padding
    backgroundColor: '#ffffff',
    borderRadius: '16px',
    color: '#1e293b', // Texto oscuro
    boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)'
  },
  // --- Nuevos estilos para el contenido ---
  sectionTitle: {
    fontSize: '24px', // Título más grande
    fontWeight: 'bold',
    color: '#1e293b',
    marginBottom: '24px',
    borderBottom: '2px solid #e2e8f0', // Un separador
    paddingBottom: '8px'
  },
  subHeading: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#dc2626', // Títulos de Misión/Visión en Rojo
    marginTop: '24px',
    marginBottom: '8px',
  },
  paragraph: {
    fontSize: '16px',
    lineHeight: '1.6',
    color: '#334155',
    marginBottom: '16px',
  },
  // Para la sección "Desde 1996"
  splitSection: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr', // 2 columnas
    gap: '24px',
    alignItems: 'center',
    marginTop: '24px',
  },
  growthList: {
    listStyleType: 'none',
    paddingLeft: '0',
  },
  growthListItem: {
    color: '#334155',
    marginBottom: '8px',
    position: 'relative',
    paddingLeft: '28px',
  },
  // El botón para ir a la Página 3
  actionButton: {
    display: 'inline-block',
    padding: '12px 24px',
    marginTop: '32px',
    fontWeight: 'bold',
    color: 'white',
    backgroundColor: '#2563eb', // Azul
    borderRadius: '8px',
    textDecoration: 'none',
    fontSize: '16px'
  }
};
// --- Fin de Estilos ---

function HomePage() {
  const { user, logoutUser } = useAuth();

  return (
    <div style={styles.page}>
      
      {/* --- Cabecera (Sin cambios) --- */}
      <header style={styles.header}>
        <div>
          <h1 style={styles.headerText.headerTitle}>¡Bienvenido, {user?.username || 'Usuario'}!</h1>
          <p style={styles.headerText.headerSubtitle}>Rol: {user?.role || 'Desconocido'}</p>
        </div>
        <button 
          onClick={logoutUser}
          style={styles.logoutButton}
          title="Cerrar Sesión"
        >
          Salir
        </button>
      </header>

      {/* --- PÁGINA 2: "Acerca de Vega" con TODO el contenido --- */}
      <section style={styles.section}>
         <h2 style={styles.sectionTitle}>Acerca de Vega</h2>
         
         {/* --- Misión y Visión (de image_050b84.png) --- */}
         <div>
            <h3 style={styles.subHeading}>MISIÓN</h3>
            <p style={styles.paragraph}>
              Proveer la mejor experiencia de compra a nuestros clientes, que buscan la
              combinación entre la calidad de los productos, los mejores precios del mercado y
              un amplio surtido, sostenido por el compromiso de nuestros colaboradores.
            </p>
            
            <h3 style={styles.subHeading}>VISIÓN</h3>
            <p style={styles.paragraph}>
              Ser líder en la venta de consumo masivo al por mayor y menor en el Perú.
            </p>
         </div>

         <hr style={{border: 'none', borderTop: '1px solid #e2e8f0', margin: '32px 0'}} />

         {/* --- Historia (de image_050b9d.png) --- */}
         <div>
            <h3 style={styles.subHeading}>HISTORIA</h3>
            <p style={styles.paragraph}>
              VEGA, es un sueño que nació a principios de los años ochenta. Michel
              Vega Paredes, impulsado por sus aliados, emprendió el modelo de
              negocio en el pujante distrito de Comas, en Lima Perú. Su primera tienda
              se llamó: “Comercial Vega” y luego, El 15 de agosto de 1996, nació
              Corporación Vega SAC. Hoy, ese mismo entusiasmo con el que se
              abrieron las puertas el primer día, sigue intacto, y se lo dedicamos a cada
              cliente a través de nuestro trabajo.
            </p>
         </div>
         
         <hr style={{border: 'none', borderTop: '1px solid #e2e8f0', margin: '32px 0'}} />

         {/* --- Contenido de image_050b65.jpg y image_050b7e.png --- */}
         <div style={styles.splitSection}>
            {/* Columna Izquierda (Desde 1996) */}
            <div>
              <h3 style={{...styles.subHeading, color: '#1e293b'}}>Desde 1996</h3>
              <p style={{...styles.paragraph, fontSize: '18px', fontWeight: '500'}}>
                Somos una empresa retail <br/>
                <span style={{color: '#dc2626', fontWeight: 'bold'}}>100% peruana,</span><br/>
                Que crece para ti.
              </p>
            </div>
            
            {/* Columna Derecha (Crecimiento Sostenido) */}
            <div>
              <h3 style={{...styles.subHeading, color: '#1e293b'}}>Crecimiento Sostenido</h3>
              <p style={styles.paragraph}>
                Desde que iniciamos nuestras operaciones hemos tenido un crecimiento sostenido basado en:
              </p>
              <ul style={styles.growthList}>
                {/* Usamos 'span' para simular los íconos de check */}
                <li style={styles.growthListItem}><span style={{position: 'absolute', left: 0, color: '#dc2626'}}>✓</span>Basado en una eficiente estrategia de expansión</li>
                <li style={styles.growthListItem}><span style={{position: 'absolute', left: 0, color: '#dc2626'}}>✓</span>Un equipo humano comprometido</li>
                <li style={styles.growthListItem}><span style={{position: 'absolute', left: 0, color: '#dc2626'}}>✓</span>La identificación con las necesidades de nuestros clientes</li>
                <li style={styles.growthListItem}><span style={{position: 'absolute', left: 0, color: '#dc2626'}}>✓</span>La inversión en tecnología</li>
                <li style={styles.growthListItem}><span style={{position: 'absolute', left: 0, color: '#dc2626'}}>✓</span>La innovación frente a la competencia</li>
                <li style={styles.growthListItem}><span style={{position: 'absolute', left: 0, color: '#dc2626'}}>✓</span>La rapidez estratégica para adecuarse a los cambios</li>
              </ul>
            </div>
         </div>


         {/* --- BOTÓN NUEVO (Página 3) --- */}
         <div style={{textAlign: 'center'}}> {/* Centramos el botón */}
           <Link to="/sales-types" style={styles.actionButton}>
              Revisar Tipos de Venta
           </Link>
         </div>
      </section>

    </div>
  );
}

export default HomePage;