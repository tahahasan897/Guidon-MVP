FROM node:20-slim
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install --legacy-peer-deps
COPY frontend /app
EXPOSE 3000
CMD ["bash", "-lc", "npm run dev -- --hostname 0.0.0.0"]
