# Enigma File Encryption Usage

This folder contains a Streamlit app that encrypts and decrypts files with the
`enigma-encryption` Python package.

## Folder Structure

```text
usage/
├── .streamlit/
│   └── config.toml
├── README.md
├── requirements.txt
├── streamlit_app.py
└── enigma_usage/
    ├── __init__.py
    └── file_crypto.py
```

## Setup

From this folder:

```powershell
pip install -r requirements.txt
```

For local development against the sibling `../enigma` source tree:

```powershell
pip install -e ..\enigma
```

## Run

```powershell
streamlit run streamlit_app.py
```

The app allows uploads up to 1024 MB through `usage/.streamlit/config.toml`.

## Python Usage

```python
import enigma

enigma.encrypt_file("plain_file.txt", "plain_file.txt.enigma", "your-password", cost=10)
enigma.decrypt_file("plain_file.txt.enigma", "plain_file.txt", "your-password")
```
