import os

os.system("uvicorn app.api.server:app --reload --workers 1 --host 0.0.0.0 --port 1337")