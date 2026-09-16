# --- Étape de base ---
FROM node:22-alpine AS base
WORKDIR /usr/src/app
COPY package*.json ./

# --- Étape de Développement ---
FROM base AS development
# On installe toutes les dépendances (y compris devDependencies pour TypeORM CLI, linter, etc.)
RUN npm install
COPY . .
# Le hot-reload sera géré par la commande dans le docker-compose

# --- Étape de Build (intermédiaire) ---
FROM base AS builder
RUN npm install
COPY . .
RUN npm run build

# --- Étape de Production ---
FROM base AS production
# On n'installe que les dépendances nécessaires pour la prod
RUN npm ci --only=production && npm cache clean --force
COPY --from=builder /usr/src/app/dist ./dist
CMD ["node", "dist/main"]