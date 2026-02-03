# Employee Policy Q&A System v2.0

A **multi-user Retrieval-Augmented Generation (RAG)** system for answering questions about employee policies with secure authentication, document upload, and AI-powered chatbot.

---

## 🎯 Implementation Status: ✅ 100% COMPLETE

All features are **fully implemented**, tested, and production-ready.

## 🚀 Quick Start (30 Seconds)

### Windows:
```bash
Double-click: run_windows.bat
Open: http://localhost:8000
```

### Mac/Linux:
```bash
chmod +x run.sh
./run.sh
Open: http://localhost:8000
```

### Manual:
```bash
python -m venv venv
source venv/bin/activate         # Mac/Linux
# or venv\Scripts\activate.bat   # Windows

pip install -r requirements.txt

# Create .env file with your credentials (see below for DATABASE SETUP)

python -c "from src.models import init_db; init_db()"

uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## � Prerequisites

- **Python 3.10+**: https://www.python.org/
- **PostgreSQL 12+**: https://www.postgresql.org/download/
- **OpenAI API Key**: https://platform.openai.com/api-keys

---

## 🗄️ Database Setup (Step-by-Step) - IMPORTANT!

### Step 1: Install PostgreSQL

**Windows:**
1. Download: https://www.postgresql.org/download/windows/
2. Run installer
3. Set password for `postgres` user (remember it!)
4. Default port: **5432**
5. Finish installation

**Mac (Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Create Database & User

**Option A: Using pgAdmin GUI (EASIEST)**
1. Open pgAdmin (comes with PostgreSQL installation)
2. Right-click Databases → Create → Database
3. **Name**: `employee_policy_qa`
4. Click Save
5. Right-click Login/Group Roles → Create
6. **Name**: `policy_user`
7. Go to "Definition" tab
8. **Password**: `your_secure_password` (e.g., `PolicyPass123!`)
9. Click Save
10. Right-click database → Properties → Security
11. Grant `policy_user` all privileges

**Option B: Command Line**
```bash
psql -U postgres

# Type these commands:
CREATE DATABASE employee_policy_qa;
CREATE USER policy_user WITH PASSWORD 'your_secure_password';
ALTER ROLE policy_user SET client_encoding TO 'utf8';
ALTER ROLE policy_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE employee_policy_qa TO policy_user;

\q
```

### Step 3: Verify Connection

```bash
psql -U policy_user -d employee_policy_qa -h localhost

# Should show: employee_policy_qa=>
# Type: \q to exit
```

### Step 4: Create .env File

Create file named `.env` in your project root directory:

```env
# REQUIRED: OpenAI API Key
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-your-key-here

# REQUIRED: PostgreSQL Connection URL
# Format: postgresql://username:password@hostname:port/database_name
DATABASE_URL=postgresql://policy_user:your_secure_password@localhost:5432/employee_policy_qa

# REQUIRED: JWT Secret (32+ random characters)
# Generate: python -c 'import secrets; print(secrets.token_urlsafe(32))'
JWT_SECRET=your-random-32-character-secret-key-here

# OPTIONAL: CORS origins
ALLOWED_ORIGINS=http://localhost:8000

# OPTIONAL: Server port
PORT=8000
```

### Step 5: Initialize Database Tables

```bash
python -c "from src.models import init_db; init_db()"
```

Should print: `Database tables created successfully!`

### Step 6: Verify Tables

```bash
psql -U policy_user -d employee_policy_qa
\dt
# Should show: users, documents, chat_history
\q
```

---

## 🔑 Database Connection URL Format

```
postgresql://username:password@hostname:port/database_name
```

**Examples:**

**Local Computer:**
```
postgresql://policy_user:PolicyPass123!@localhost:5432/employee_policy_qa
```

**Remote Server:**
```
postgresql://policy_user:PolicyPass123!@db.example.com:5432/employee_policy_qa
```

**Render.com (After Deployment):**
```
postgresql://user:pass@internal-db-host-xxx.postgres.render.com:5432/employee_policy_qa
```

**Key Points:**
- `username` = `policy_user` (user you created)
- `password` = Your password (what you set)
- `hostname` = `localhost` (local) or domain (remote)
- `port` = `5432` (default PostgreSQL)
- `database_name` = `employee_policy_qa` (database name)

## 📁 Project Structure

```
EmployeePolicy_Q&A_System/
├── app.py                    # FastAPI application (350+ lines)
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose
├── render.yaml               # Render deployment config
├── .env.example              # Environment template
├── run_windows.bat           # Windows quick start
├── run.sh                    # Mac/Linux quick start
│
├── src/
│   ├── models.py            # Database models (User, Document, ChatHistory)
│   ├── auth.py              # JWT authentication
│   ├── schemas.py           # Pydantic validation
│   ├── config.py            # Configuration
│   ├── rag_pipeline.py      # RAG orchestration
│   ├── qa_system.py         # Q&A logic
│   ├── vector_store.py      # Vector database
│   ├── embeddings_generator.py
│   ├── text_chunker.py
│   └── document_processor.py
│
├── static/
│   └── index.html           # Frontend UI (800+ lines)
│
├── uploads/                 # Document uploads (auto-created)
├── vector_db/               # Vector storage (auto-created)
└── documents/               # Sample documents
```

## 💾 Database Schema

### Users Table
```sql
id              INTEGER PRIMARY KEY
username        VARCHAR(50) UNIQUE NOT NULL
email           VARCHAR(255) UNIQUE NOT NULL
hashed_password VARCHAR(255) NOT NULL
full_name       VARCHAR(255)
is_active       BOOLEAN DEFAULT true
created_at      TIMESTAMP DEFAULT NOW()
updated_at      TIMESTAMP DEFAULT NOW()
```

### Documents Table
```sql
id                      INTEGER PRIMARY KEY
user_id                 INTEGER FOREIGN KEY (references users)
filename                VARCHAR(255)
original_filename       VARCHAR(255)
file_path               TEXT
file_size               INTEGER
document_type           VARCHAR(50)
chunk_count             INTEGER DEFAULT 0
is_processed            BOOLEAN DEFAULT false
vector_collection_name  VARCHAR(100)
created_at              TIMESTAMP DEFAULT NOW()
processed_at            TIMESTAMP
```

### Chat History Table
```sql
id                INTEGER PRIMARY KEY
user_id           INTEGER FOREIGN KEY (references users)
session_id        VARCHAR(100)
question          TEXT NOT NULL
answer            TEXT NOT NULL
confidence_score  FLOAT DEFAULT 0.0
sources           TEXT (JSON)
created_at        TIMESTAMP DEFAULT NOW()
```

## 🚀 Running the Application

### Automated (Easiest)

**Windows:**
```bash
run_windows.bat
```

**Mac/Linux:**
```bash
chmod +x run.sh
./run.sh
```

### Manual

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
source venv/bin/activate           # Mac/Linux
# or venv\Scripts\activate.bat     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (follow Database Setup section above)

# 5. Initialize database
python -c "from src.models import init_db; init_db()"

# 6. Run application
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Access Your App

- **Frontend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

## � Usage Steps

### 1. Register Account
1. Go to http://localhost:8000
2. Click "Sign up"
3. Enter username, email, password, full name
4. Click "Sign Up"

### 2. Login
1. Enter email and password
2. Click "Login"
3. Token automatically saved

### 3. Upload Document
1. Click "📄 My Documents"
2. Click or drag PDF file
3. Wait for processing
4. Document appears in list

### 4. Ask Questions
1. Click "💬 Chat"
2. Type your question
3. Get answer with sources

### 5. View Statistics
1. Click "📊 Statistics"
2. See document and chunk counts

## 🧪 Test the API (cURL Examples)

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "full_name": "Test User"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
# Copy the "access_token" from response
```

### Get Current User
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Upload Document
```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@path/to/document.pdf"
```

### Ask Question
```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the probation period?",
    "session_id": "session_123"
  }'
```

### Get Chat History
```bash
curl -X GET http://localhost:8000/api/chat-history \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Statistics
```bash
curl -X GET http://localhost:8000/api/stats \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## � Troubleshooting

### "Database connection refused"
- Verify PostgreSQL is running
- Check DATABASE_URL in .env (use correct password and port 5432)
- Test: `psql -U policy_user -d employee_policy_qa`

### "ModuleNotFoundError"
```bash
pip install --upgrade -r requirements.txt
```

### "Port 8000 already in use"
```bash
uvicorn app:app --port 8001
```

### "OpenAI API error"
1. Get key: https://platform.openai.com/api-keys
2. Add to .env: `OPENAI_API_KEY=sk-proj-...`
3. Restart app

### "JWT_SECRET not set"
```bash
# Add to .env
JWT_SECRET=your-random-key
# Generate: python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

### "Login fails"
1. Clear browser cache: Ctrl+Shift+Delete
2. Check JWT_SECRET in .env
3. Verify user in database: `psql -U policy_user -d employee_policy_qa -c "SELECT * FROM users;"`

### "Document upload fails"
- Verify uploads/ directory exists
- Check file is valid PDF
- Verify disk space available

---

## 🌐 Deployment on Render.com

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Multi-user Q&A v2.0"
git push origin main
```

### Step 2: Create PostgreSQL Database
1. Go to https://render.com
2. Click "New" → "PostgreSQL"
3. Name: `employee-policy-db`
4. Click "Create Database"
5. **Copy Internal Database URL** (save it!)

### Step 3: Create Web Service
1. Click "New" → "Web Service"
2. Select GitHub repository
3. Name: `employee-policy-qa`
4. Runtime: Docker
5. Click "Create Web Service"

### Step 4: Set Environment Variables
In Render dashboard → Settings → Environment:
```
OPENAI_API_KEY=sk-proj-your-key
DATABASE_URL=paste-internal-url-from-step-2
JWT_SECRET=generate-random-string
ALLOWED_ORIGINS=https://your-app-name.onrender.com
PORT=10000
```

### Step 5: Deploy
- Render builds automatically
- Wait for "Live" status

### Step 6: Initialize Database
1. Go to Web Service → Shell tab
2. Run: `python -c "from src.models import init_db; init_db()"`

### Step 7: Access
```
https://your-app-name.onrender.com
```

---

## 📊 Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI 0.109+ |
| Database | PostgreSQL 12+ |
| ORM | SQLAlchemy 2.0+ |
| Validation | Pydantic 2.0+ |
| Auth | JWT + Bcrypt |
| Vector DB | ChromaDB 0.4+ |
| Embeddings | OpenAI text-embedding-ada-002 |
| LLM | GPT-3.5-turbo |
| Frontend | HTML5/CSS3/JavaScript |
| Deployment | Docker + Render |

---

## 🔒 Security Features

✅ **Password Security**: Bcrypt hashing (12 salt rounds)
✅ **Authentication**: JWT tokens (7-day expiration)
✅ **User Isolation**: Separate data at 3 levels:
   - Database queries filtered by user_id
   - File uploads in user-specific directories
   - Vector collections per user
✅ **SQL Protection**: SQLAlchemy ORM prevents injection
✅ **CORS**: Configurable allowed origins
✅ **Input Validation**: Pydantic models
✅ **Error Handling**: No sensitive data exposed
✅ **File Validation**: Only PDFs accepted

---

## ✅ Implementation Checklist (100% Complete)

### Backend
- ✅ FastAPI application (350+ lines)
- ✅ 13 API endpoints fully functional
- ✅ User registration & JWT login
- ✅ Bcrypt password hashing
- ✅ Document upload & processing
- ✅ RAG pipeline integration
- ✅ Chat history persistence
- ✅ Statistics endpoint
- ✅ Error handling & validation
- ✅ CORS configuration
- ✅ Health check endpoint

### Database (PostgreSQL)
- ✅ User model with authentication
- ✅ Document model with file tracking
- ✅ ChatHistory model with sources
- ✅ Proper relationships & constraints
- ✅ Automatic table creation
- ✅ Per-user data isolation
- ✅ Foreign key enforcement

### Frontend
- ✅ Login/Register screens
- ✅ Chat interface with message history
- ✅ Document upload with drag-drop
- ✅ Document listing & deletion
- ✅ Statistics dashboard
- ✅ Navigation sidebar
- ✅ Error handling
- ✅ Responsive design
- ✅ Token persistence in localStorage
- ✅ Real-time status messages
- ✅ Dark theme

### Security (8/8 Features)
- ✅ Password hashing with Bcrypt
- ✅ JWT token authentication
- ✅ User data isolation at 3 levels
- ✅ SQL injection prevention
- ✅ CORS protection
- ✅ Input validation
- ✅ Error message sanitization
- ✅ File type validation

---

## 🎯 Final Summary

**Status**: ✅ **100% PRODUCTION READY**

### What's Implemented:
- ✅ 13 REST API endpoints
- ✅ Multi-user authentication system
- ✅ Document upload & processing
- ✅ RAG-powered Q&A chatbot
- ✅ Chat history with sources
- ✅ User statistics dashboard
- ✅ PostgreSQL database with 3 models
- ✅ Modern responsive web UI
- ✅ Complete security layer
- ✅ Docker deployment ready
- ✅ Render.com ready

### Code Statistics:
- **Backend**: 350+ lines (app.py) + supporting modules
- **Database**: 3 models (User, Document, ChatHistory)
- **Schemas**: 10 Pydantic validation models
- **Frontend**: 800+ lines (HTML/CSS/JS)
- **Total API Endpoints**: 13
- **Security Mechanisms**: 8

### Next Steps:
1. ✅ Set up PostgreSQL database (see Database Setup section)
2. ✅ Create .env file with credentials
3. ✅ Run the application (Windows: run_windows.bat or Mac/Linux: ./run.sh)
4. ✅ Register account and test
5. ✅ Deploy to Render (optional, see Deployment section)

---

**Version**: 2.0.0 | **Status**: ✅ Production Ready | **Date**: January 2026
