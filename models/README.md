Drop your trained, exported model files here with these exact names —
`model_loader.py` looks for them on startup:

| File                  | Format         | Loaded by   |
|-----------------------|-----------------|-------------|
| yield_model.pkl       | joblib (.pkl)   | joblib.load |
| disease_model.pt      | torch (.pt)     | torch.load  |
| price_model.pkl       | joblib (.pkl)   | joblib.load |
| livestock_model.pkl   | joblib (.pkl)   | joblib.load |
| drought_model.pkl     | joblib (.pkl)   | joblib.load |

Missing or broken files don't crash the app — that model's status just shows
as "not_found" / "unavailable" on GET /health, and its endpoint returns a
clean 503 instead of a server error. Check /health before every demo run.

If any file here exceeds ~50MB, don't commit it to GitHub — see the
"Deployment notes" section in the root README.md for the Hugging Face
Spaces alternative.
