# Sketch3D (2D → 3D)
End-to-end CV + geometry pipeline that converts a **single orthographic engineering drawing sheet** into a browser-viewable GLB model.

## Run backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run frontend
```bash
cd frontend
npm install
npm run dev
```

## API usage
```bash
curl -F "drawing=@sample_drawing.png" http://localhost:8000/api/reconstruct
```

## Notes
- Supports 1/2/3 detected views.
- Pipeline is data-driven from CV + OCR outputs.
- Exports `model.glb` per job at `/tmp/sketch3d/<job_id>/model.glb`.


## Windows note (Python 3.11)
`open3d` is not published for some Windows/Python combos. This project marks `open3d` as optional on Windows so installation succeeds; `/api/health` will report `"open3d": "not-installed"` in that case.

Install optional packages (non-Windows):
```bash
pip install -r requirements-optional.txt
```


Backend startup no longer fails if Tesseract is missing; OCR-dependent extraction degrades gracefully and `/api/health` reports `tesseract: not-installed`.
