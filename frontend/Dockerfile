# Multi-stage build for optimized production image

# Stage 1: Build the React application
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
# Need devDependencies because vite is required to build the app
RUN npm ci

# Copy source code
COPY . .

# Build the application
# This creates optimized production files in the 'dist' folder
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built application from builder stage
# We're only taking the built files, not the source code or Node.js
COPY --from=builder /app/dist /usr/share/nginx/html

# Install curl for health checks (Alpine doesn't include it by default)
RUN apk add --no-cache curl

# The nginx:alpine image already has nginx user/group configured properly
# So we don't need to create them again!

# Expose port 80
EXPOSE 80

# Health check for nginx
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]