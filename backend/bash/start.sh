echo "Instaling requirements..."
pip install -r requirements.txt
echo "Deleting cache files..."
rm -rf /root/.cache/pip
echo "Starting server"
gunicorn app.api.server:app --workers 4 --reload --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:1337