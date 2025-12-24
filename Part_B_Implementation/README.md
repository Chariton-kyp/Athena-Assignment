# TechFlow Data Automation Platform

**Enterprise-grade data extraction and management system with human-in-the-loop controls**

[![Backend Tests](https://img.shields.io/badge/tests-79%20passed-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-80%25-green)]()
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)]()
[![Next.js](https://img.shields.io/badge/Next.js-15-black)]()
[![Docker](https://img.shields.io/badge/docker-compose%20v2-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## Overview

TechFlow Data Automation is a complete solution for extracting, managing, and exporting data from multiple sources including HTML forms, email files (.eml), and invoices. Built for **TechFlow Solutions** (IT Services, 50-100 employees) to automate their manual data management processes.

### Key Principles

- **Human-in-the-Loop**: Every extraction requires user approval before final recording
- **Full Control**: Users can approve, reject, or edit any extraction at any time
- **Real-time Monitoring**: Dashboard with live statistics and activity feeds
- **Multi-language**: Full Greek and English support

---

## Features

### Core Functionality

| Feature | Description |
|---------|-------------|
| **Form Extraction** | Parse HTML contact forms - extracts name, email, phone, company, service interest, message, priority |
| **Email Processing** | Parse .eml files - distinguishes inquiries (60%) from invoice notifications (40%) |
| **Invoice Extraction** | Parse HTML invoices - extracts invoice number, date, client, amounts, VAT (24%), line items |
| **Approval Workflow** | Review, approve, reject, or edit every extraction before recording |
| **Batch Operations** | Process multiple files and approve/reject records in bulk |
| **Multi-format Export** | Export to CSV, Excel (.xlsx), or JSON |
| **Google Sheets Integration** | Auto-sync approved records to Google Sheets with multi-sheet organization |

### Advanced Features

| Feature | Description |
|---------|-------------|
| **AI Semantic Search** | Search records in Greek or English using embeddings (pgvector) |
| **Real-time Notifications** | WebSocket-based live updates on all actions |
| **Confidence Scoring** | AI-generated confidence levels for each extraction |
| **Validation Warnings** | Automatic detection of potential data issues |
| **Audit Trail** | Complete history of all actions and changes |
| **Responsive Design** | Works on desktop, tablet, and mobile |

---

## Tech Stack

### Backend
- **Python 3.12+** with FastAPI
- **PostgreSQL 16** with pgvector extension
- **SQLAlchemy 2.0** (async) + Alembic migrations
- **Pydantic v2** for validation
- **structlog** for structured logging
- **BeautifulSoup4** for HTML parsing
- **sentence-transformers** for embeddings

### Frontend
- **Next.js 15** (App Router)
- **React 19** with TypeScript
- **TailwindCSS** + shadcn/ui components
- **TanStack Query** for server state
- **Recharts** for visualizations
- **next-intl** for i18n (Greek/English)

### Infrastructure
- **Docker Compose v2** (multi-stage builds)
- **GitHub Actions** CI/CD
- **Trivy** security scanning

---

## Quick Start

### Prerequisites

- **Docker** 24.0+ with Compose v2
- **Git**

### One-Command Setup (Production)

```bash
# Clone and start
cd Part_B_Implementation
docker compose --profile prod up --build -d
```

Access the application:
- **Frontend**: http://localhost:7002
- **Backend API**: http://localhost:7000
- **API Docs**: http://localhost:7000/docs

### Development Mode (with hot reload)

```bash
docker compose --profile dev up --build
```

### Stop Services

```bash
docker compose --profile prod down    # Production
docker compose --profile dev down     # Development
docker compose down -v                # Remove volumes too
```

---

## Manual Installation

### Backend

```bash
cd Part_B_Implementation/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your database connection

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload
```

### Frontend

```bash
cd Part_B_Implementation/frontend

# Install dependencies
npm ci

# Set environment
echo "NEXT_PUBLIC_API_URL=http://localhost:7000" > .env.local
echo "NEXT_PUBLIC_WS_URL=ws://localhost:7000/ws/notifications" >> .env.local

# Development
npm run dev

# Production build
npm run build
npm start
```

### Database

```bash
# Using Docker for database only
docker run -d \
  --name techflow-db \
  -e POSTGRES_USER=techflow \
  -e POSTGRES_PASSWORD=techflow_dev_password \
  -e POSTGRES_DB=techflow_automation \
  -p 7001:5432 \
  pgvector/pgvector:pg16
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | Environment mode | `development` |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `LOG_LEVEL` | Logging level | `INFO` |
| `DATA_PATH` | Input files directory | `/app/data` |
| `OUTPUT_PATH` | Export output directory | `/app/output` |
| `EXTRACTION_CONFIDENCE_THRESHOLD` | Min confidence for suggestions | `0.8` |
| `ENABLE_AI_EXTRACTION` | Enable AI features | `true` |
| `HUGGINGFACE_TOKEN` | Token for gated models | Optional |

### Google Sheets Integration

See [docs/GOOGLE_SHEETS_SETUP.md](docs/GOOGLE_SHEETS_SETUP.md) for detailed setup instructions.

| Variable | Description |
|----------|-------------|
| `GOOGLE_CREDENTIALS_PATH` | Path to service account JSON |
| `GOOGLE_SPREADSHEET_ID` | Target spreadsheet ID |
| `GOOGLE_SHEETS_AUTO_SYNC` | Auto-sync on approve/reject |
| `GOOGLE_SHEETS_MULTI_SHEET` | Organize data in multiple sheets |

---

## Usage Guide

### 1. Dashboard

The main dashboard shows:
- **Statistics Cards**: Total records, pending review, approved, rejected
- **Status Chart**: Visual breakdown by status (pie chart)
- **Type Chart**: Distribution by type (Forms/Emails/Invoices)
- **Recent Activity**: Latest extraction records

### 2. Data Extraction

1. Navigate to **Extraction** page
2. Browse available files by type (Forms, Emails, Invoices)
3. Click **Preview** to see extracted data before saving
4. Review confidence scores and warnings
5. Click **Save for Review** or use **Extract All** for batch processing

### 3. Record Management

1. Navigate to **Records** page
2. Filter by status (Pending, Approved, Rejected, Edited)
3. Filter by type (Form, Email, Invoice)
4. Click a record to view full details
5. **Approve**: Mark as verified and ready for export
6. **Reject**: Provide reason and exclude from export
7. **Edit**: Modify extracted data before approval

### 4. Batch Operations

1. Select multiple records using checkboxes
2. Use toolbar actions:
   - **Approve All**: Approve selected pending records
   - **Reject All**: Reject with a common reason

### 5. Export

1. Click **Export** button (or use auto-export settings)
2. Choose format: CSV, Excel, or JSON
3. Optionally include rejected records
4. Download or sync to Google Sheets

---

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:7000/docs
- **ReDoc**: http://localhost:7000/redoc

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/records` | List records with filtering |
| GET | `/api/v1/records/stats` | Dashboard statistics |
| GET | `/api/v1/records/{id}` | Get single record |
| POST | `/api/v1/records/{id}/approve` | Approve record |
| POST | `/api/v1/records/{id}/reject` | Reject record |
| PUT | `/api/v1/records/{id}` | Edit record data |
| POST | `/api/v1/records/export` | Export records |
| POST | `/api/v1/records/approve-batch` | Batch approve |
| POST | `/api/v1/records/reject-batch` | Batch reject |
| POST | `/api/v1/extraction/form/{filename}` | Extract form |
| POST | `/api/v1/extraction/email/{filename}` | Extract email |
| POST | `/api/v1/extraction/invoice/{filename}` | Extract invoice |
| GET | `/api/v1/records/sheets/status` | Google Sheets status |
| POST | `/api/v1/records/sheets/sync` | Sync to Google Sheets |

---

## Testing

### Run Backend Tests

```bash
cd Part_B_Implementation/backend

# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=app --cov-report=html

# Specific test file
pytest tests/test_form_extractor.py -v
```

### Run via Docker

```bash
docker compose --profile test up --build
```

### Test Coverage

| Module | Coverage |
|--------|----------|
| Extractors | 95% |
| API Routes | 88% |
| Services | 85% |
| **Total** | **80%+** |

### Frontend Tests

```bash
cd Part_B_Implementation/frontend
npm test
```

---

## Project Structure

```
Part_B_Implementation/
├── backend/
│   ├── app/
│   │   ├── api/           # API version router
│   │   ├── core/          # Config, logging, settings
│   │   ├── db/            # Database models, repositories
│   │   ├── extractors/    # Form, Email, Invoice extractors
│   │   ├── models/        # Pydantic schemas
│   │   ├── routers/       # FastAPI route handlers
│   │   └── services/      # Business logic layer
│   ├── tests/             # Pytest test suite
│   ├── alembic/           # Database migrations
│   └── credentials/       # Google API credentials
├── frontend/
│   ├── app/               # Next.js App Router pages
│   ├── components/        # React components
│   │   ├── dashboard/     # Stats, charts, activity
│   │   ├── extraction/    # File browser, preview
│   │   ├── records/       # Approval workflow, edit forms
│   │   └── export/        # Export dialogs
│   ├── lib/               # API client, hooks, types
│   └── messages/          # i18n translations (en, el)
├── docs/                  # User manual, setup guides
├── docker-compose.yml     # Container orchestration
└── README.md              # This file
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js 15)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Dashboard  │  │ Extraction  │  │   Records   │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          │                                       │
│                    TanStack Query + WebSocket                    │
└──────────────────────────┼───────────────────────────────────────┘
                           │
                      HTTP/REST + WS
                           │
┌──────────────────────────┼───────────────────────────────────────┐
│                     Backend (FastAPI)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Extractors │  │  Services   │  │   Routers   │              │
│  │ Form/Email/ │  │ Record/     │  │ /records    │              │
│  │   Invoice   │  │ Export/     │  │ /extraction │              │
│  └─────────────┘  │ Sheets      │  └─────────────┘              │
│         │         └─────────────┘        │                       │
│         └────────────────┼───────────────┘                       │
│                          │                                       │
│                   SQLAlchemy (Async)                             │
└──────────────────────────┼───────────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              │                         │
    ┌─────────▼─────────┐    ┌─────────▼─────────┐
    │   PostgreSQL 16   │    │   Google Sheets   │
    │   + pgvector      │    │   (Optional)      │
    └───────────────────┘    └───────────────────┘
```

---

## Troubleshooting

### Common Issues

**Database connection failed**
```bash
# Check if PostgreSQL is running
docker compose ps db
# Check logs
docker compose logs db
```

**Frontend can't connect to backend**
```bash
# Verify NEXT_PUBLIC_API_URL is correct
# Check backend health
curl http://localhost:7000/health
```

**Google Sheets sync fails**
1. Verify credentials file exists in `backend/credentials/`
2. Check service account has Editor access to spreadsheet
3. See [GOOGLE_SHEETS_SETUP.md](docs/GOOGLE_SHEETS_SETUP.md)

**Port conflicts**
```bash
# Change ports in docker-compose.yml
# Default ports: 7000 (backend), 7001 (db), 7002 (frontend)
```

### Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

---

## Development

### Code Quality

```bash
# Backend
cd backend
ruff check app/          # Linting
black app/               # Formatting
mypy app/                # Type checking

# Frontend
cd frontend
npm run lint             # ESLint
npm run type-check       # TypeScript
```

### Adding New Extractors

1. Create class in `backend/app/extractors/`
2. Inherit from `BaseExtractor`
3. Implement `extract()` and `validate()` methods
4. Add tests in `backend/tests/`
5. Register in extraction router

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## License

This project was created for the **AthenaGen AI Solutions Engineer Assessment**.

**Author**: Kypraios Chariton (Κυπραίος Χαρίτων)

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [shadcn/ui](https://ui.shadcn.com/) - UI components
- [pgvector](https://github.com/pgvector/pgvector) - Vector similarity for PostgreSQL
- [Recharts](https://recharts.org/) - Charting library
