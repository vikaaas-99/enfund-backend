# Backend Assignment

## **How to Run Locally**

1. Clone the repository:
```sh
git clone https://github.com/vikaaas-99/enfund-backend.git
```

2. Create and activate virtual environment:
```sh
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```sh
pip install -r requirements.txt
python manage.py migrate
```

4. Run server:
```sh
daphne -b 0.0.0.0 -p 8000 enfund_backend.asgi:application
```

## **API Documentation**

| Method |	Endpoint |	Description |
| ------ | ---------| ---------|
| GET |	/auth/login/ |	Get Google Auth URL |
| POST |	/drive/connect/ |	Connect Google Drive
POST	/drive/upload/	Upload file to Drive
GET	/drive/files/	List Google Drive files
GET	/drive/download/<file_id>/	Download file
WS	ws://your-app.onrender.com/ws/chat/	WebSocket for chat