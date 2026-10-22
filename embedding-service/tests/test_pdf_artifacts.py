"""First-use download of the docling models: marker file decides, an aborted download is retried."""
import sys
import types

import pdf


def _fake_downloader(monkeypatch, calls, fail=False):
    def download_models(output_dir=None, *, with_code_formula=True, with_picture_classifier=True, with_rapidocr=True, with_easyocr=False):
        calls.append((output_dir, with_code_formula, with_rapidocr))
        (output_dir / "layout").mkdir(parents=True, exist_ok=True)
        if fail:
            raise OSError("network down")

    module = types.ModuleType("docling.utils.model_downloader")
    module.download_models = download_models
    monkeypatch.setitem(sys.modules, "docling.utils.model_downloader", module)


def test_downloads_once_and_skips_unused_models(tmp_path, monkeypatch):
    calls = []
    _fake_downloader(monkeypatch, calls)
    pdf._ensure_artifacts(str(tmp_path / "models"))
    pdf._ensure_artifacts(str(tmp_path / "models"))
    assert calls == [(tmp_path / "models", False, False)]


def test_aborted_download_is_retried(tmp_path, monkeypatch):
    calls = []
    _fake_downloader(monkeypatch, calls, fail=True)
    try:
        pdf._ensure_artifacts(str(tmp_path / "models"))
    except OSError:
        pass
    assert (tmp_path / "models" / "layout").exists()  # half-populated dir, but no marker
    _fake_downloader(monkeypatch, calls)
    pdf._ensure_artifacts(str(tmp_path / "models"))
    assert len(calls) == 2


def test_skip_env_never_downloads(tmp_path, monkeypatch):
    calls = []
    _fake_downloader(monkeypatch, calls)
    monkeypatch.setenv("DOCLING_SKIP_MODEL_DOWNLOAD", "true")
    pdf._ensure_artifacts(str(tmp_path / "models"))
    assert calls == []
