# Stage 1: Build Angular application
FROM node:20-alpine AS build
WORKDIR /app

# Cache package dependencies
COPY package*.json ./
RUN npm ci

# Copy source and build production bundle
COPY . .
RUN npm run build -- --configuration production

# Stage 2: Serve with lightweight Nginx alpine
FROM nginx:1.27-alpine
WORKDIR /usr/share/nginx/html

# Clean default Nginx website
RUN rm -rf ./*

# Copy built distribution from build stage (dist/library-frontend/browser)
COPY --from=build /app/dist/library-frontend/browser ./

# Copy custom Nginx configuration with SPA fallback
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
