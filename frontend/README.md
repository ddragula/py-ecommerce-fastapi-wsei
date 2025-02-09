# Frontend - Vite + React

This is the frontend for the FastAPI e-commerce project, built using **Vite** and **React**.

## Getting Started

### 1. Install Dependencies
```sh
npm install
```

### 2. Development Mode
```sh
npm run dev
```
🔗 Open: [http://localhost:5173](http://localhost:5173)

### 3. Build for Production
```sh
npm run build
```
This will generate static files in `../static/`, served by FastAPI.

---

## 🔧 Configuration
### API Proxy Setup
API requests to `/api/**` are forwarded to `http://127.0.0.1:8000` in `vite.config.js`:
```javascript
proxy: {
  '/api': 'http://127.0.0.1:8000'
}
```

### Static Deployment
After running `npm run build`, the frontend will be served at `/` via FastAPI.
