# Healthcare Helper – Monorepo

A modular AI-powered assistant for healthcare cost transparency and insurance analysis. This monorepo is designed for easy contribution, reproducible development, and clear separation of concerns across frontend, backend, and analysis tools.

---

## Repo Structure
healthcare-helper/ 
├── frontend/              
#### React UI for user interaction 
├── backend/               
#### FastAPI server for API endpoints and orchestration 
├── insurance-analyzer/   
#### Python tools for parsing and analyzing insurance data 
├── data-ingestion/       
#### Utilities for importing, cleaning, and chunking raw data 
├── vector-db/            
#### Embedding and retrieval logic using a vector database 
├── cost-comparison/      
#### Engine for comparing healthcare costs across providers 
├── tests/                
#### Shared test suite for all modules 
└── README.md 


---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/healthcare-helper.git
cd healthcare-helper
```
### 2. Backend Setup (Recommended: Docker)
To work on this project, start by building and running the backend using the Dockerfile in the main folder:
```bash
docker build -t healthcare-helper .
docker run -p 8000:8000 healthcare-helper
```

This ensures all dependencies are installed and the backend runs in a reproducible environment.

---

If you prefer manual setup, you can still install dependencies in each folder:
```bash
cd frontend
npm install

cd ../backend
pip install -r requirements.txt
```
## Goals
- Transparent healthcare cost comparison
- Modular architecture for easy contribution
- Beginner-friendly onboarding and reproducible environments
- Playful, welcoming UI design

  ## Frontend Setup

1. **Install dependencies:**
   ```sh
   cd frontend/frontend_folder
   npm install
   ```

2. **Configure the backend URL:**
   - Create a file named `.env` in the `frontend/frontend_folder` directory.
   - Add the following line to the `.env` file:
     ```
     REACT_APP_BACKEND_URL=<your-backend-url>
     ```
     Replace `<your-backend-url>` with the URL where your backend is running (for example, your Codespace URL or `http://localhost:8000`).

3. **Start the frontend:**
   ```sh
   npm start
   ```

4. **Open the app:**
   ```sh
   $BROWSER http://localhost:3000
   ```

**Note:**  
If you are running the backend in a Codespace or remote environment, make sure to use the correct forwarded/public URL for your backend.





