from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

import streamlit as st

from enigma_usage.file_crypto import decrypt_uploaded_file, encrypt_uploaded_file


def main() -> None:
    st.set_page_config(page_title="Enigma File Encryption", layout="centered")

    st.title("Enigma File Encryption")

    with st.sidebar:
        st.header("Settings")
        mode = st.radio("Mode", ("Encrypt", "Decrypt"), horizontal=True)

        if mode == "Encrypt":
            cost = st.slider("Cost factor", min_value=8, max_value=14, value=10)
        else:
            cost = 10

        threads = st.number_input(
            "Worker threads",
            min_value=0,
            max_value=64,
            value=1,
            help="Use 0 to let Enigma use all available CPU cores.",
        )
        io_buf_mb = st.number_input(
            "I/O buffer (MiB)",
            min_value=1,
            max_value=256,
            value=4,
        )

        st.caption(_enigma_version_label())

    password = st.text_input("Password", type="password")

    uploaded_file = st.file_uploader(
        "Choose a file",
        accept_multiple_files=False,
    )

    if uploaded_file is not None:
        st.write(f"Selected: `{uploaded_file.name}` ({_format_size(uploaded_file.size)})")
    else:
        st.info("Upload a file to continue.")

    if uploaded_file is not None and not password:
        st.info("Enter the password to enable encryption or decryption.")

    can_process = uploaded_file is not None and bool(password)
    button_label = "Encrypt file" if mode == "Encrypt" else "Decrypt file"

    if st.button(button_label, type="primary", disabled=not can_process):
        if uploaded_file is None:
            st.warning("Choose a file first.")
            return
        if not password:
            st.warning("Enter a password.")
            return

        with st.spinner(f"{mode}ing with Enigma..."):
            try:
                file_bytes = uploaded_file.getvalue()
                if mode == "Encrypt":
                    result = encrypt_uploaded_file(
                        uploaded_file.name,
                        file_bytes,
                        password,
                        cost=cost,
                        threads=int(threads),
                        io_buf_mb=int(io_buf_mb),
                    )
                    mime = "application/octet-stream"
                else:
                    result = decrypt_uploaded_file(
                        uploaded_file.name,
                        file_bytes,
                        password,
                        threads=int(threads),
                        io_buf_mb=int(io_buf_mb),
                    )
                    mime = "application/octet-stream"
            except (TypeError, ValueError, RuntimeError) as exc:
                st.error(f"Enigma could not {mode.lower()} this file: {exc}")
                return

        st.success(f"{mode}ion complete.")
        st.download_button(
            "Download result",
            data=result.data,
            file_name=result.file_name,
            mime=mime,
        )

    with st.expander("Run from Python"):
        st.code(
            _python_example(mode),
            language="python",
        )


def _enigma_version_label() -> str:
    try:
        package_version = version("enigma-encryption")
    except PackageNotFoundError:
        package_version = "editable/local"
    return f"Using enigma-encryption: {package_version}"


def _format_size(size: int | None) -> str:
    if size is None:
        return "unknown size"

    value = float(size)
    units = ("B", "KiB", "MiB", "GiB")
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} {unit}"
        value /= 1024

    return f"{size} B"


def _python_example(mode: str) -> str:
    if mode == "Encrypt":
        return (
            "import enigma\n\n"
            "enigma.encrypt_file(\n"
            '    "plain_file.txt",\n'
            '    "plain_file.txt.enigma",\n'
            '    "your-password",\n'
            "    cost=10,\n"
            "    threads=1,\n"
            "    io_buf_mb=4,\n"
            ")\n"
        )

    return (
        "import enigma\n\n"
        "enigma.decrypt_file(\n"
        '    "plain_file.txt.enigma",\n'
        '    "plain_file.txt",\n'
        '    "your-password",\n'
        "    threads=1,\n"
        "    io_buf_mb=4,\n"
        ")\n"
    )


if __name__ == "__main__":
    main()
