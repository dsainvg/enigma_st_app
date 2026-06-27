"""File encryption helpers backed by the enigma Python package."""

from __future__ import annotations

from dataclasses import dataclass
import importlib
from pathlib import Path
import re
import tempfile


ENCRYPTED_SUFFIX = ".enigma"
DECRYPTABLE_SUFFIXES = (".enigma", ".enc")


@dataclass(frozen=True)
class FileCryptoResult:
    """Processed file content ready for a Streamlit download button."""

    file_name: str
    data: bytes


def encrypt_uploaded_file(
    file_name: str,
    data: bytes,
    password: str,
    cost: int,
    threads: int,
    io_buf_mb: int,
) -> FileCryptoResult:
    """Encrypt uploaded file bytes through enigma.encrypt_file."""

    enigma = _load_enigma()
    input_name = _safe_file_name(file_name)
    output_name = _encrypted_file_name(input_name)

    with tempfile.TemporaryDirectory(prefix="enigma_encrypt_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        input_path = tmp_path / input_name
        output_path = tmp_path / output_name

        input_path.write_bytes(data)
        enigma.encrypt_file(
            str(input_path),
            str(output_path),
            password,
            cost=cost,
            threads=threads,
            io_buf_mb=io_buf_mb,
        )

        return FileCryptoResult(file_name=output_name, data=output_path.read_bytes())


def decrypt_uploaded_file(
    file_name: str,
    data: bytes,
    password: str,
    threads: int,
    io_buf_mb: int,
) -> FileCryptoResult:
    """Decrypt uploaded file bytes through enigma.decrypt_file."""

    enigma = _load_enigma()
    input_name = _safe_file_name(file_name)
    output_name = _decrypted_file_name(input_name)

    with tempfile.TemporaryDirectory(prefix="enigma_decrypt_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        input_path = tmp_path / input_name
        output_path = tmp_path / output_name

        input_path.write_bytes(data)
        enigma.decrypt_file(
            str(input_path),
            str(output_path),
            password,
            threads=threads,
            io_buf_mb=io_buf_mb,
        )

        return FileCryptoResult(file_name=output_name, data=output_path.read_bytes())


def _safe_file_name(file_name: str) -> str:
    clean_name = Path(file_name or "uploaded_file").name.strip()
    clean_name = re.sub(r"[^A-Za-z0-9._ -]+", "_", clean_name)
    clean_name = clean_name.strip(" .")
    return clean_name or "uploaded_file"


def _load_enigma():
    try:
        return importlib.import_module("enigma")
    except ImportError as exc:
        raise RuntimeError(
            "The enigma-encryption package is not installed. Run "
            "`pip install -r requirements.txt`, or `pip install -e ..\\enigma` "
            "from this usage folder for local development."
        ) from exc


def _encrypted_file_name(file_name: str) -> str:
    if file_name.lower().endswith(ENCRYPTED_SUFFIX):
        return file_name
    return f"{file_name}{ENCRYPTED_SUFFIX}"


def _decrypted_file_name(file_name: str) -> str:
    path = Path(file_name)
    for suffix in DECRYPTABLE_SUFFIXES:
        if file_name.lower().endswith(suffix):
            return file_name[: -len(suffix)] or "decrypted_file"
    return f"decrypted_{path.name}"
