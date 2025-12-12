# ETAPA 1: Construcción (Build)
FROM node:18-alpine as build

WORKDIR /app

# Copiamos package.json e instalamos dependencias
COPY package.json package-lock.json ./
RUN npm install

# Copiamos el código y construimos la versión final (dist)
COPY . .
RUN npm run build

# ETAPA 2: Servidor Web (Producción)
FROM nginx:alpine

# Copiamos los archivos construidos en la etapa anterior a la carpeta de Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copiamos una configuración básica de Nginx (Opcional, por ahora usa la default)
# Exponemos el puerto 80
EXPOSE 80

# Arrancamos Nginx
CMD ["nginx", "-g", "daemon off;"]