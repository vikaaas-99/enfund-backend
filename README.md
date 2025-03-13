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

| **Method** |	**Endpoint** |	**Description** |
| ------ | ---------| ---------|
| **GET** |	`/auth/login/` |	Get Google Auth URL |
| **POST** |	`/drive/connect/` |	Connect Google Drive |
| **POST** |	`/drive/upload/` |	Upload file to Drive |
| **GET** |	`/drive/files/` |	List Google Drive files |
| **GET** |	`/drive/download/<file_id>/` |	Download file |
| **WS** |	`ws://enfund-backend-2qer.onrender.com/ws/chat/` |	WebSocket for chat |

## **Postman Collection**

[Authentication and Drive APIs](https://github.com/vikaaas-99/enfund-backend/blob/main/enfund_backend.postman_collection.json)

### **WebSockets (Real-Time Chat) - Testing in Postman**

Postman does not allow WebSockets in collections, so follow these steps to test WebSockets manually.

#### 1️⃣ Open Postman
- Click **New Request** → Select **WebSocket Request** from the dropdown.

#### 2️⃣ Enter WebSocket URL
`wss://enfund-backend-2qer.onrender.com/ws/chat/`

#### 3️⃣ Connect to WebSocket
- Click **Connect**.

#### 4️⃣ Send a Chat Message
- Click **+ New Message**
- Send the following JSON:
```json
{
    "message": "Hello from Postman!",
    "sender": "Vikas"
}
```
- Click Send.

#### 5️⃣ Open Another WebSocket Tab
- Open a second WebSocket connection.
- Send a message, and you should see it appear in real-time in both tabs.
