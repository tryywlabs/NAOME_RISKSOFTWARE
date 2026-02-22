# Web UI (React)

This folder contains a React + Vite frontend scaffold for the Risk Software project.

## Run locally

```bash
cd webui
npm install
npm run dev
```

Default dev URL: `http://localhost:5173`

## Build

```bash
npm run build
npm run preview
```

## Next integration steps

1. Add an API service module (for example, `src/api/client.js`) and wire form submit to your Python backend.
2. Replace demo metric/result data with responses from the middleware calculations.
3. Add route-based views if you want separate pages for frequency/consequence/input workflows.
