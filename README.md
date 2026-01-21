# Employee Policy Q&A System

A Retrieval-Augmented Generation (RAG) system for answering questions about employee policies, HR handbooks, and employment contracts.

## Project Structure

```
EmployeePolicy_Q&A_System/
├── documents/                          # PDF documents directory
│   ├── Employment_Contract_XCorp.pdf
│   ├── HR_Policy_Handbook_XCorp.pdf
│   └── Increment_and_Probation_Policy_XCorp.pdf
├── src/                                # Source code directory
│   ├── __init__.py
│   ├── config.py                      # Configuration settings
│   ├── document_processor.py          # PDF extraction and preprocessing
│   ├── text_chunker.py                # Text chunking logic
│   ├── embeddings_generator.py        # Embedding generation
│   ├── vector_store.py               # Vector database operations
│   ├── rag_pipeline.py               # Main RAG pipeline
│   └── qa_system.py                   # Q&A system
├── utils/                              # Utility scripts
│   ├── __init__.py
│   ├── create_documents.py           # Script to generate PDF documents
│   └── extract_pdfs.py               # PDF text extraction utility
├── vector_db/                          # Vector database storage (created automatically)
├── data/                               # Data directory (for future use)
├── app.py                             # FastAPI web application
├── run_app.py                         # Script to run the web app
├── main.py                            # Command-line Q&A system
├── ingest_documents.py                # Script to ingest documents
├── static/                             # Static files (frontend)
│   └── index.html                     # Chatbot frontend
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore file
└── README.md                          # This file
```

## Features

- **PDF Document Processing**: Extracts and processes text from PDF documents
- **Intelligent Chunking**: Splits documents into manageable chunks with overlap
- **Embedding Generation**: Creates vector embeddings using sentence transformers or OpenAI
- **Vector Database**: Stores embeddings in ChromaDB or FAISS
- **Q&A System**: Answers questions using RAG with LLM integration
- **Realistic Documents**: All policy documents include complete, realistic information

## Quick Start (Docker - Recommended)

### Local Development with Docker

1. **Install Docker** (if not already installed)
   - Download from [docker.com](https://www.docker.com/products/docker-desktop)

2. **Run with Docker Compose**:
```bash
docker-compose up --build
```

3. **Open your browser**:
   - Frontend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Traditional Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables** (required for OpenAI features):
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### 1. Run the Web Application

Start the FastAPI web application with the chatbot interface:

```bash
python run_app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Then open your browser and navigate to:
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc

The web interface provides a beautiful, interactive chatbot where you can ask questions about employee policies.

### 2. Generate Documents (if needed)

If you need to regenerate the PDF documents with realistic values:

```bash
python utils/create_documents.py
```

This will create three PDF documents in the `documents/` folder:
- Employment Contract (with filled employee details, dates, salary, etc.)
- HR Policy Handbook (complete with all policies)
- Increment & Probation Policy (detailed policy document)

### 3. Ingest Documents into Vector Database

Run the RAG pipeline to process and store documents:

```bash
python ingest_documents.py
```

This will:
- Extract text from all PDF documents in the `documents/` folder
- Chunk the documents intelligently
- Generate embeddings
- Store them in the vector database

### 4. Run the Command-Line Q&A System (Optional)

For command-line interface instead of web app:

```bash
python main.py
```

Example questions:
- "What is the probation period?"
- "How many annual leave days do employees get?"
- "What is the increment percentage after probation?"
- "What are the working hours?"
- "Who is the Chief Human Resources Officer?"

## Configuration

Edit `src/config.py` to customize:

- **PDF Files**: List of PDF documents to process
- **Chunking**: Chunk size and overlap
- **Embeddings**: Choose between local (sentence-transformers) or OpenAI embeddings
- **Vector DB**: Choose between ChromaDB or FAISS
- **LLM**: Configure LLM model for Q&A generation

## Document Details

All documents have been created with realistic, complete information:

### Employment Contract
- Employee: Ahmed Hassan
- Position: Senior Software Engineer
- Department: Software Development
- Supervisor: Sarah Malik
- Base Salary: PKR 150,000
- Start Date: February 1, 2024
- Contract Date: January 15, 2024
- All sections fully filled with realistic details

### HR Policy Handbook
- Complete company information
- All policies detailed with specific numbers and procedures
- Contact information included
- Version and effective dates specified

### Increment & Probation Policy
- Detailed evaluation criteria
- Specific increment percentages
- Approval process outlined
- Signed by CHRO and CEO with dates

## System Architecture

1. **Document Processing**: PDFs → Text extraction → Cleaning
2. **Chunking**: Text → Overlapping chunks with metadata
3. **Embedding**: Chunks → Vector embeddings
4. **Storage**: Embeddings → Vector database
5. **Retrieval**: Query → Embedding → Similarity search
6. **Generation**: Context + Query → LLM → Answer

## Requirements

- Python 3.8+
- See `requirements.txt` for all dependencies

## Deployment

### Deploy to Render (Recommended)

The project is fully configured for deployment on Render with Docker:

1. **Push to GitHub**:
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Create a new Web Service from your GitHub repo
   - Select **Docker** as runtime
   - Add your `OPENAI_API_KEY` environment variable
   - Deploy!

3. **Your app will be live** at: `https://your-app-name.onrender.com`

See [RENDER_DEPLOY.md](RENDER_DEPLOY.md) for detailed deployment instructions.

## Notes

- The system uses local embeddings by default (sentence-transformers)
- For OpenAI embeddings, set `USE_OPENAI_EMBEDDINGS = True` in `src/config.py`
- Vector database is stored locally in `./vector_db/`
- Documents are automatically reprocessed when running the ingestion pipeline
- All documents include realistic, complete information (no placeholders)
- Docker support is included for easy local development and cloud deployment

## License

This project is for educational/demonstration purposes.
