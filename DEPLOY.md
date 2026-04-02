# Deployment Guide: Backend on Render 🚀

This guide provides instructions on how to deploy your FastAPI backend to **Render**, connect it to **MongoDB Atlas**, and ensure your **Flutter app** can communicate with the live server.

---

## 🏗️ 1. Prepare Your Repository

Ensure your project structure is clean. Render should point to your **GitHub/GitLab/Bitbucket** repository.

### Project Structure Check:
- Your backend code should be in a folder named `/backend`.
- `requirements.txt` should be at the root of that `/backend` folder.
- `main.py` should be the entry point.

---

## ⚡ 2. Create a Render Web Service

1.  Log in to the [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** and select **Web Service**.
3.  Connect your repository where the project is stored.
4.  Configure the following settings:
    - **Name**: `tablenow-backend` (or your choice)
    - **Environment**: `Python 3`
    - **Region**: Choose the one closest to your users.
    - **Branch**: `main` (the branch you want to deploy)
    - **Root Directory**: `backend` (Crucial: Render should look inside the `backend` folder)
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## 🔐 3. Configure Environment Variables

Navigate to the **Environment** tab in your Render service and add:

| Key | Value |
| :--- | :--- |
| `MONGODB_URI` | `mongodb+srv://<user>:<password>@cluster0...` |
| `DATABASE_NAME` | `tablenow` |
| `PYTHON_VERSION` | `3.10.0` (Recommended) |

---

## 📱 4. Connect Your Flutter App

Once the deployment is successful, Render will provide a URL (e.g., `https://tablenow-backend.onrender.com`).

1.  Open **`tablenow_app/lib/services/api_service.dart`**.
2.  Change the `baseUrl`:
    ```dart
    final String baseUrl = "https://tablenow-backend.onrender.com";
    ```
3.  **Rebuild** your app for production.

---

## 🛠️ Troubleshooting

### 💡 Common Issues:
- **Port Error**: Ensure you use the `--port $PORT` variable in the Start Command. Render handles the port dynamically.
- **Dependency Issues**: If a build fails, check that your `requirements.txt` is complete. 
- **CORS Errors**: The backend is already configured to allow all origins (`allow_origins=["*"]`), which is fine for development. For production, you may want to restrict this later.

### 📊 Health Check:
You can visit `https://tablenow-backend.onrender.com/docs` to see the live Swagger documentation and test your endpoints.

---

> [!TIP]
> Render's **Free Tier** will "spin down" after inactivity. This means the first request after a break might take 30-50 seconds. For a smoother experience, consider the **Starter Tier**.
