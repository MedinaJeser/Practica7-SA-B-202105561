# Etapa 1: Construcción
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar solo los archivos de dependencias primero
COPY package.json package-lock.json ./

# Instalar dependencias de producción y desarrollo
RUN npm ci

# Copiar el resto del código fuente
COPY . .

# Asegurar que NestJS se ejecute correctamente
RUN npx nest build

# Etapa 2: Imagen final optimizada
FROM node:18-alpine

WORKDIR /app

# Copiar solo lo necesario desde la etapa de construcción
COPY --from=builder /app/package.json /app/package-lock.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

# Exponer el puerto
EXPOSE 3002

CMD ["node", "dist/main.js"]
