# Quick Start Guide

## Running the Web Application

1. **Make sure dependencies are installed:**
```bash
pip install -r requirements.txt
```

2. **Ensure documents are ingested (if not already done):**
```bash
python ingest_documents.py
```

3. **Start the web application:**
```bash
python run_app.py
```

4. **Open your browser:**
   - Navigate to: **http://localhost:8000**
   - You'll see a beautiful chatbot interface

5. **Try asking questions:**
   - "What is the probation period?"
   - "How many annual leave days do employees get?"
   - "What is the increment percentage after probation?"
   - "What are the working hours?"

## API Endpoints

- **Frontend**: `http://localhost:8000/` - Chatbot interface
- **API Docs**: `http://localhost:8000/docs` - Swagger UI
- **Health Check**: `http://localhost:8000/health`
- **Ask Question**: `POST http://localhost:8000/api/ask`
- **Stats**: `GET http://localhost:8000/api/stats`

## Example API Request

```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the probation period?"}'
```

## Features

✅ Beautiful, modern chatbot UI
✅ Real-time Q&A with source citations
✅ Responsive design
✅ Example questions for quick start
✅ Loading indicators
✅ Error handling

Enjoy your Employee Policy Q&A Bot! 🚀
