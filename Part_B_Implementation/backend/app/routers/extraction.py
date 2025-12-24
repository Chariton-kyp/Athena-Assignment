"""
Extraction router for file processing endpoints.
Handles form, email, and invoice extraction with optional database persistence.
Integrates with AI embedding service for semantic search.
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.similarity import SimilaritySearchService
from app.core.config import settings
from app.core.logging import get_logger
from app.db.database import get_db
from app.db.repositories import RecordRepository
from app.extractors import EmailExtractor, FormExtractor, InvoiceExtractor, PDFInvoiceExtractor
from app.services.record_service import RecordService

logger = get_logger(__name__)

router = APIRouter(prefix="/extract", tags=["extraction"])


# Dependency for RecordService with AI integration
async def get_record_service(db: AsyncSession = Depends(get_db)) -> RecordService:
    """Get RecordService with database session and AI embedding service."""
    repository = RecordRepository(db)
    similarity_service = SimilaritySearchService(db)
    return RecordService(repository, similarity_service)


@router.get("/files")
async def list_available_files() -> dict[str, Any]:
    """
    List all available files for processing.

    Returns:
        Dictionary with file lists by type and total count.
    """
    data_path = settings.data_path
    files: dict[str, list[str]] = {
        "forms": [],
        "emails": [],
        "invoices": [],
    }

    forms_path = data_path / "forms"
    emails_path = data_path / "emails"
    invoices_path = data_path / "invoices"

    if forms_path.exists():
        files["forms"] = sorted([f.name for f in forms_path.glob("*.html")])

    if emails_path.exists():
        files["emails"] = sorted([f.name for f in emails_path.glob("*.eml")])

    if invoices_path.exists():
        # Support both HTML and PDF invoices
        html_invoices = [f.name for f in invoices_path.glob("*.html")]
        pdf_invoices = [f.name for f in invoices_path.glob("*.pdf")]
        files["invoices"] = sorted(html_invoices + pdf_invoices)

    return {
        "data_path": str(data_path),
        "files": files,
        "total_count": sum(len(f) for f in files.values()),
    }


@router.post("/form/{filename}")
async def extract_form(
    filename: str,
    save_record: bool = Query(False, description="Save to database for approval"),
    service: RecordService = Depends(get_record_service),
) -> dict[str, Any]:
    """
    Extract data from a contact form.

    Args:
        filename: Name of the HTML form file.
        save_record: If True, save extraction to database for approval workflow.
        service: RecordService dependency.

    Returns:
        Extraction result with optional record_id.
    """
    file_path = settings.data_path / "forms" / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Form file not found: {filename}")

    extractor = FormExtractor()
    result = extractor.extract(file_path)

    if result.has_errors:
        raise HTTPException(status_code=422, detail=result.errors)

    response: dict[str, Any] = {"extraction": result}

    if save_record:
        record = await service.create_from_extraction(result)
        response["record_id"] = str(record.id)
        response["message"] = "Record created and pending approval"

    return response


@router.post("/email/{filename}")
async def extract_email(
    filename: str,
    save_record: bool = Query(False, description="Save to database for approval"),
    service: RecordService = Depends(get_record_service),
) -> dict[str, Any]:
    """
    Extract data from an email file.

    Args:
        filename: Name of the EML email file.
        save_record: If True, save extraction to database for approval workflow.
        service: RecordService dependency.

    Returns:
        Extraction result with optional record_id.
    """
    file_path = settings.data_path / "emails" / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Email file not found: {filename}")

    extractor = EmailExtractor()
    result = extractor.extract(file_path)

    if result.has_errors:
        raise HTTPException(status_code=422, detail=result.errors)

    response: dict[str, Any] = {"extraction": result}

    if save_record:
        record = await service.create_from_extraction(result)
        response["record_id"] = str(record.id)
        response["message"] = "Record created and pending approval"

    return response


@router.post("/invoice/{filename}")
async def extract_invoice(
    filename: str,
    save_record: bool = Query(False, description="Save to database for approval"),
    service: RecordService = Depends(get_record_service),
) -> dict[str, Any]:
    """
    Extract data from an invoice file (HTML or PDF).

    Args:
        filename: Name of the invoice file (HTML or PDF).
        save_record: If True, save extraction to database for approval workflow.
        service: RecordService dependency.

    Returns:
        Extraction result with optional record_id.
    """
    file_path = settings.data_path / "invoices" / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Invoice file not found: {filename}")

    # Use appropriate extractor based on file type
    if file_path.suffix.lower() == ".pdf":
        if not PDFInvoiceExtractor.is_supported():
            raise HTTPException(
                status_code=501,
                detail="PDF extraction not supported - pdfplumber not installed"
            )
        extractor = PDFInvoiceExtractor()
    else:
        extractor = InvoiceExtractor()
    result = extractor.extract(file_path)

    if result.has_errors:
        raise HTTPException(status_code=422, detail=result.errors)

    response: dict[str, Any] = {"extraction": result}

    if save_record:
        record = await service.create_from_extraction(result)
        response["record_id"] = str(record.id)
        response["message"] = "Record created and pending approval"

    return response


@router.post("/all")
async def extract_all_files(
    save_records: bool = Query(False, description="Save all to database for approval"),
    service: RecordService = Depends(get_record_service),
) -> dict[str, Any]:
    """
    Extract data from all available files.

    Args:
        save_records: If True, save all extractions to database.
        service: RecordService dependency.

    Returns:
        Results for all files with summary statistics.
    """
    results: dict[str, list[dict[str, Any]]] = {
        "forms": [],
        "emails": [],
        "invoices": [],
    }
    errors: list[dict[str, Any]] = []
    records_created = 0

    data_path = settings.data_path

    # Process forms
    form_extractor = FormExtractor()
    forms_path = data_path / "forms"
    if forms_path.exists():
        for form_file in sorted(forms_path.glob("*.html")):
            try:
                result = form_extractor.extract(form_file)
                entry: dict[str, Any] = {
                    "file": form_file.name,
                    "success": not result.has_errors,
                    "confidence": result.confidence_score,
                    "data": result.form_data.model_dump() if result.form_data else None,
                    "warnings": result.warnings,
                }

                if save_records and not result.has_errors:
                    record = await service.create_from_extraction(result)
                    entry["record_id"] = str(record.id)
                    records_created += 1

                results["forms"].append(entry)
            except Exception as e:
                logger.error("form_extraction_failed", file=form_file.name, error=str(e))
                errors.append({"file": form_file.name, "error": str(e)})

    # Process emails
    email_extractor = EmailExtractor()
    emails_path = data_path / "emails"
    if emails_path.exists():
        for email_file in sorted(emails_path.glob("*.eml")):
            try:
                result = email_extractor.extract(email_file)
                entry = {
                    "file": email_file.name,
                    "success": not result.has_errors,
                    "confidence": result.confidence_score,
                    "data": result.email_data.model_dump() if result.email_data else None,
                    "warnings": result.warnings,
                }

                if save_records and not result.has_errors:
                    record = await service.create_from_extraction(result)
                    entry["record_id"] = str(record.id)
                    records_created += 1

                results["emails"].append(entry)
            except Exception as e:
                logger.error("email_extraction_failed", file=email_file.name, error=str(e))
                errors.append({"file": email_file.name, "error": str(e)})

    # Process invoices (HTML and PDF)
    html_invoice_extractor = InvoiceExtractor()
    pdf_invoice_extractor = PDFInvoiceExtractor() if PDFInvoiceExtractor.is_supported() else None
    invoices_path = data_path / "invoices"
    if invoices_path.exists():
        # Process both HTML and PDF invoices
        invoice_files = list(invoices_path.glob("*.html")) + list(invoices_path.glob("*.pdf"))
        for invoice_file in sorted(invoice_files):
            try:
                # Choose extractor based on file type
                if invoice_file.suffix.lower() == ".pdf":
                    if not pdf_invoice_extractor:
                        errors.append({"file": invoice_file.name, "error": "PDF extraction not supported"})
                        continue
                    result = pdf_invoice_extractor.extract(invoice_file)
                else:
                    result = html_invoice_extractor.extract(invoice_file)
                entry = {
                    "file": invoice_file.name,
                    "success": not result.has_errors,
                    "confidence": result.confidence_score,
                    "data": result.invoice_data.model_dump() if result.invoice_data else None,
                    "warnings": result.warnings,
                }

                if save_records and not result.has_errors:
                    record = await service.create_from_extraction(result)
                    entry["record_id"] = str(record.id)
                    records_created += 1

                results["invoices"].append(entry)
            except Exception as e:
                logger.error("invoice_extraction_failed", file=invoice_file.name, error=str(e))
                errors.append({"file": invoice_file.name, "error": str(e)})

    return {
        "results": results,
        "summary": {
            "forms_processed": len(results["forms"]),
            "emails_processed": len(results["emails"]),
            "invoices_processed": len(results["invoices"]),
            "total_errors": len(errors),
            "records_created": records_created if save_records else None,
        },
        "errors": errors if errors else None,
    }
