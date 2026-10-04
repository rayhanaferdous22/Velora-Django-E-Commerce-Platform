# Run Velora

Extract this archive to `D:\` and open the extracted `velora-clean` folder in VS Code.

## Backend terminal

```powershell
cd D:\velora-clean
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
```

## Frontend terminal

```powershell
cd D:\velora-clean\frontend
npm ci
npm run dev -- --port 5173
```

Open `http://localhost:5173`.
