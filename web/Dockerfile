# Use a lightweight Node.js image suitable for development
FROM node:20-alpine

# Install compatibility libs (useful for sharp and other native deps)
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Install dependencies first (better layer caching)
COPY package.json ./
# If you later add a lockfile, copy it here for reproducible builds
# COPY package-lock.json ./

# Install deps (dev dependencies included for local development)
RUN npm install

# Copy the rest of the app
COPY . .

EXPOSE 3100

# Run Next.js dev server on 0.0.0.0 for Docker networking
CMD ["npm", "run", "dev", "--", "-p", "3100", "-H", "0.0.0.0"]
