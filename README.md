# TechFlow Solutions - Data Automation Project

**Author:** Kypraios Chariton
**Assessment:** AthenaGen AI - Solutions Engineer Position
**Date:** December 2025

---

## Project Overview

This is the **implementation folder** for the TechFlow Solutions Data Automation Assessment. All deliverables for the Solutions Engineer position at AthenaGen AI are contained within this directory.

The solution provides an automated data extraction system with **human-in-the-loop controls** for processing contact forms, emails, and invoices, with centralized data storage integration.

## Deliverables Structure

```
Athena-Assignment/
├── README.md                       # Project overview
├── .gitignore                      # Git ignore rules
│
├── Part_A_Proposal/              # Technical Proposal (30%)
│   ├── TechFlow_Presentation.pptx  # 10-15 slide presentation
│   ├── architecture_diagram.svg    # System architecture
│   ├── Executive_Summary.pdf       # Executive summary document
│   ├── Needs_Analysis.pdf          # Client needs analysis
│   ├── Technical_Proposal.pdf      # Detailed technical proposal
│   └── ROI_Analysis.pdf            # ROI calculations
│
├── Part_B_Implementation/          # Implementation + Testing (60% + 10%)
│   ├── docker-compose.yml          # Container orchestration (Monorepo)
│   ├── backend/                    # Backend Service (FastAPI)
│   │   ├── Dockerfile              # Backend container
│   │   ├── app/                    # Source code (API, Extractors, Models)
│   │   ├── tests/                  # Backend tests
│   │   └── requirements.txt        # Python dependencies
│   ├── frontend/                   # Frontend Service (Next.js)
│   │   ├── Dockerfile              # Frontend container
│   │   ├── app/                    # App Router pages
│   │   ├── components/             # React components
│   │   └── package.json            # Node.js dependencies
│   ├── demo/                       # Demo video & script
│   └── config/                     # Configuration files
│
└── docs/                           # Documentation
    ├── INITIAL_SETUP.md            # Initial configuration guide
    ├── User_Manual.md              # User guide
    └── GOOGLE_SHEETS_SETUP.md      # Google Sheets API setup
```

## Initial Setup

> **Important:** Before starting the project, you need to configure the configuration files.

📄 **See the full guide:** [docs/INITIAL_SETUP.md](docs/INITIAL_SETUP.md)

### Quick Setup

```bash
# 1. Create .env files
cd Part_B_Implementation/backend
cp .env.example .env

cd ../frontend
cp .env.example .env.local

# 2. Edit backend/.env
# - Configure DATABASE_URL (Docker vs local)
# - (Optional) HUGGINGFACE_TOKEN for AI Search
# - Google Sheets credentials
```

## Quick Start

### Option 1: Docker (Recommended)

```bash
cd Part_B_Implementation

# Production mode
docker compose --profile prod up --build -d

# Development mode (with hot reload)
docker compose --profile dev up --build

# Run tests
docker compose --profile test run --rm test

# Build (BuildKit is enabled by default in recent Docker versions)
docker compose --profile prod build
```

### Option 2: Local Development

```bash
cd Part_B_Implementation/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations (requires PostgreSQL)
alembic upgrade head

# Run the backend
uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload
```

## Key Features

### Human-in-the-Loop Controls
- Real-time monitoring dashboard
- Approval/Rejection workflow for each extraction
- Manual edit capability before final submission
- Error detection with clear warnings
- Full user control at every stage
- Complete audit trail

### Data Sources
| Source | Files | Format | Extraction |
|--------|-------|--------|------------|
| Contact Forms | 5 | HTML | Name, Email, Phone, Company, Service, Priority |
| Client Emails | 10 | EML | Contact info, Service needs, Invoice refs |
| Invoices | 10 | HTML | Invoice #, Date, Amounts, VAT (24%) |

### Target Integration
- Google Sheets or Excel for centralized data storage
- Automated sync with manual approval gates
- Export capabilities in multiple formats

## Technology Stack

### Backend
- **Python:** 3.12 (slim-bookworm)
- **API Framework:** FastAPI
- **Database:** PostgreSQL 16 + pgvector
- **ORM:** SQLAlchemy 2.0 (async)
- **Data Processing:** Pandas, BeautifulSoup4
- **AI/ML:** LangChain, EmbeddingGemma (308M), sentence-transformers

### Frontend
- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** TailwindCSS, Shadcn/ui
- **State:** React Query (TanStack Query)
- **Charts:** Recharts

### Infrastructure
- **Containerization:** Docker (Compose v2, multi-stage builds)
- **Testing:** pytest, pytest-cov, Vitest, Playwright
- **Code Quality:** ruff, black, mypy, ESLint, Prettier

## Docker Commands

```bash
cd Part_B_Implementation

# Build the image
docker compose --profile prod build

# Run in production
docker compose --profile prod up -d

# View logs
docker compose logs -f

# Stop all services
docker compose --profile prod down

# Run with fresh build
docker compose --profile prod up --build

# Run tests with coverage
docker compose --profile test run --rm test
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | Environment mode | `production` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `DATA_PATH` | Path to data files | `/app/data` |
| `OUTPUT_PATH` | Path for exports | `/app/output` |

## Project Deliverables

| Part | Deliverable | Weight |
|------|-------------|--------|
| A | Technical Proposal | 30% |
| B | Implementation + Testing | 60% + 10% |

## Best Practices Applied (December 2025)

- Multi-stage Docker builds for smaller images
- Docker Compose v2 syntax (no deprecated `version` field)
- Non-root container user for security
- Health checks for container monitoring
- `.dockerignore` for optimized builds
- Type hints throughout Python code
- Comprehensive test coverage

---

**Kypraios Chariton**
Solutions Engineer Candidate
AthenaGen AI Assessment

*This project demonstrates enterprise-grade automation capabilities with emphasis on user control, data integrity, and scalable architecture.*
