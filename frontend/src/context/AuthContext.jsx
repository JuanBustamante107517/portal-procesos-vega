// frontend/src/context/AuthContext.jsx
import { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode'; // ¡Ups! Nos faltó esta, la instalamos en el sig. paso

// Creamos la URL base de nuestra API
const API_URL = 'http://127.0.0.1:8001'; // Usaremos el puerto 8000 por defecto

const AuthContext = createContext();

// Esta es la función que usaremos en nuestros componentes
export function useAuth() {
  return useContext(AuthContext);
}

// Este es el "proveedor" que envuelve nuestra app
export function AuthProvider({ children }) {
  const [authTokens, setAuthTokens] = useState(() => 
    localStorage.getItem('authTokens')
      ? JSON.parse(localStorage.getItem('authTokens'))
      : null
  );
  const [user, setUser] = useState(() => 
    localStorage.getItem('authTokens')
      ? jwtDecode(localStorage.getItem('authTokens'))
      : null
  );

  // Función de Login: Llama a nuestra API de Django
  const loginUser = async (username, password) => {
    const response = await axios.post(`${API_URL}/api/users/login/`, {
      username: username,
      password: password
    });

    if (response.status === 200) {
      const data = response.data;
      setAuthTokens(data);
      setUser(jwtDecode(data.access)); // Decodificamos el token para obtener el rol
      localStorage.setItem('authTokens', JSON.stringify(data));
      return data; // Devuelve los datos por si acaso
    } else {
      // Si axios falla, lanzará un error que atraparemos en el formulario
      throw new Error('Respuesta no fue OK');
    }
  };

  // Función de Logout
  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
  };

  // El "valor" que compartiremos con toda la app
  const contextData = {
    user: user,           // Contiene el 'rol' y 'username'
    authTokens: authTokens, // Contiene el token de 'access' y 'refresh'
    loginUser: loginUser,   // La función para iniciar sesión
    logoutUser: logoutUser  // La función para cerrar sesión
  };

  // Esto hace que los 'children' (nuestra App) puedan acceder al 'contextData'
  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  );
}