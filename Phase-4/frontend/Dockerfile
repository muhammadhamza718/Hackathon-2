# Multi-stage build for production-ready Node.js frontend
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first for better caching
COPY package.json package-lock.json ./

# Install all dependencies (including dev dependencies) for building
RUN npm ci

# Copy application source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy package.json to install production dependencies only
COPY package.json package-lock.json ./

# Install production dependencies only
RUN npm ci --only=production && \
    npm cache clean --force && \
    chown -R nextjs:nodejs /app

# Copy built application from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules

# Install curl for health check
RUN apk add --no-cache curl

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check endpoint (adjust based on your actual health check endpoint)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1

# Start the application
CMD ["npm", "start"]