echo "Instaling requirements..."
pip install -r requirements.txt
echo "Deleting cache files..."
rm -rf /root/.cache/pip
echo "Starting server"
uvicorn app.api.server:app --host 0.0.0.0 --port 5000 --proxy-headers --reload
