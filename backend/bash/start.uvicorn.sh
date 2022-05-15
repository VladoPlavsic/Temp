
pip install -r requirements.txt && rm -rf /root/.cache/pip && uvicorn app.api.server:app --reload --host 0.0.0.0 --port 1337