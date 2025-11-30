FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (including Angular CLI)
RUN npm install

# Copy source code
COPY . .

EXPOSE 4200

# Default command for development (can be overridden in docker-compose)
CMD ["npm", "start", "--", "--host", "0.0.0.0", "--port", "4200", "--disable-host-check"]
