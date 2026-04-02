# TableNow Project Guide 🍽️

This guide explains the project structure and provides step-by-step instructions to run the entire TableNow ecosystem (Backend + Flutter App).

---

## 🏗️ Project Architecture

1.  **Backend (`/backend`)**: A FastAPI Python server that handles restaurant data, bookings, and user auth using **MongoDB Atlas**.
2.  **Frontend (`/tablenow_app`)**: A Flutter mobile application for users to explore restaurants and book tables.
3.  **Database**: 
    - **Primary**: MongoDB Atlas (Cloud).
    - **Legacy**: `tablenow.db` (SQLite file used for the initial data migration).

---

## 🛠️ Prerequisites

Before running the project, ensure you have:
- [Python 3.10+](https://www.python.org/downloads/)
- [Flutter SDK](https://docs.flutter.dev/get-started/install)
- [MongoDB Atlas Account](https://www.mongodb.com/cloud/atlas)
- [Supabase Account](https://supabase.com/)

---

## 🚀 Step 1: Backend Setup (FastAPI + MongoDB)

### 1. Configure Environment Variables
Open `backend/.env` and fill in your MongoDB Atlas URI:
```env
MONGODB_URI=your_mongodb_atlas_connection_string
DATABASE_NAME=tablenow
```

### 2. Install Dependencies
Open your terminal in the `backend` folder:
```powershell
pip install -r requirements.txt
```

### 3. Migrate Data (One-time)
If you have data in the legacy `tablenow.db` file, run the migration script:
```powershell
python scripts/migrate_to_mongo.py
```

### 4. Run the Server
Start the FastAPI server:
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
> [!TIP]
> The server will be available at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

---

## 📱 Step 2: Frontend Setup (Flutter)

### 1. Configuration
- **Supabase**: Ensure `lib/main.dart` has your correct Supabase URL and Anon Key.
- **Google Auth**: Ensure `lib/Auth.md` steps for Google Cloud Console are completed and the Client IDs are updated in your code.

### 2. Install Dependencies
Open your terminal in the `tablenow_app` folder:
```powershell
flutter pub get
```

### 3. Run the App
Connect a device or start an emulator/simulator, then run:
```powershell
flutter run
```
> [!IMPORTANT]
> If you are using an **Android Emulator**, the app is configured to connect to the backend at `http://10.0.2.2:8000` (which refers to your local machine's localhost).

---

## 📝 Audit Notes
- **Authentication**: The app uses a hybrid approach. Supabase is used in the Flutter app for initial session management, while the FastAPI backend handles custom user storage and booking logic in MongoDB.
- **Data Integrity**: Ensure the backend is running *before* attempting to log in or book in the Flutter app.
- **Security**: Never commit your `.env` file or `google-services.json` to public version control.

---

> [!NOTE]
> For detailed instructions on Google Sign-In setup, refer to `tablenow_app/Auth.md`.
