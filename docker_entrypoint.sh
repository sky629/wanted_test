
echo "1. FastAPI database migrations..."
sleep 3
alembic revision --autogenerate -m "init"
alembic upgrade head

echo "2. initial data setting..."
python app/scripts/init_data.py

echo "1. FastAPI run..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
