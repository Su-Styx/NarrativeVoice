import json
from pathlib import Path
from pypdf import PdfReader
from celery import shared_task
from django.conf import settings

from pipeline.nlp_module.api_endpoint import run_pipeline as run_nlp_pipeline

from .models import Document

PROFILE = "per-chunk-profile.YAML"
DEFAULT_PAGES = "0-inf"  # set this to whatever chunking.py --pages expects


@shared_task
def run_pipeline(document_id):
    doc = Document.objects.get(pk=document_id)
    doc.status = "running"
    doc.save(update_fields=["status"])
    try:
        run_dir = Path(settings.MEDIA_ROOT) / "runs" / str(doc.id)
        (run_dir / "extractions").mkdir(parents=True, exist_ok=True)
        page_count = len(PdfReader(doc.pdf.path).pages)

        values = {
            "pdf": doc.pdf.path,
            "chunk_out": str(run_dir / "chunks.txt"),
            "doc-id": str(doc.id),
            "title": doc.title,
            "pages": f"1-{page_count}",
            "profile": PROFILE,
            "input": str(run_dir / "chunks.txt"),
            "output": str(run_dir / "extractions"),
        }
        result = run_nlp_pipeline(values)
        (run_dir / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        doc.result = result
        doc.status = "done"
    except Exception as e:
        doc.status = "failed"
        doc.error = str(e)[-2000:]
        raise
    finally:
        doc.save(update_fields=["status", "result", "error"])