FROM node:20-alpine as build-stage

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build Angular application
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Install serve to run the application
RUN npm install -g serve

# Copy built application from build stage
COPY --from=build-stage /app/dist/frontend ./dist/frontend

EXPOSE 4200

CMD ["serve", "-s", "dist/frontend", "-l", "4200"]
