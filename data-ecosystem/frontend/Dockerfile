# Stage 1: Build the React app
FROM node:19 AS builder

WORKDIR /app

# Install dependencies only when package.json or package-lock.json changes
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy the rest of the app and build it
COPY . .
RUN npm run build

# Stage 2: Serve the app with a lightweight server
# FROM nginx:alpine

# WORKDIR /usr/share/nginx/html

# # Remove the default Nginx static files
# RUN rm -rf ./*

# # Copy the built files from the previous stage
# COPY --from=builder /app/.next /usr/share/nginx/html

# # Expose the default Nginx port
# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]


# Expose port 3000
EXPOSE 3000

# Start the Next.js application
CMD ["npm", "start"]