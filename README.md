# mega_tiktaktoe

Local FastAPI backend + static frontend (GitHub Pages).

## Quick start
Frontend (GitHub Pages):
- https://alexanderbowler.github.io/tiktaktoe_web/

Backend (local + tunnel):
1) Create a virtualenv and install deps:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Start the API:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3) Start the tunnel (separate terminal):
```bash
cloudflared tunnel run ttt-backend
```

The backend will be reachable at:
`https://ttt.alexander-bowler.org`

## Point the UI at the backend
`index.html` uses:
```html
window.TTT_API_BASE = "https://ttt.alexander-bowler.org";
```

For local-only testing, change it to:
```html
window.TTT_API_BASE = "http://127.0.0.1:8000";
```

Then refresh the page.

## Helpful endpoints
- `GET /state`
- `POST /move` `{ "index": 0-8 }`
- `POST /reset` `{ "first_player": "X" | "O" }`
- `POST /swap-first`
