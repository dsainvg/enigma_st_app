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

Use Python 3.10 through 3.13. The current `enigma-encryption` release contains
native wheels for those Python versions and does not support Python 3.14.

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

## Streamlit Community Cloud

Deploy the app with Python 3.13. In Streamlit Community Cloud, choose Python
3.13 from **Advanced settings** while creating the app. Python cannot be changed
for an existing deployment, so delete and redeploy an app that currently uses
Python 3.14.

## Python Usage

```python
import enigma

enigma.encrypt_file("plain_file.txt", "plain_file.txt.enigma", "your-password", cost=10)
enigma.decrypt_file("plain_file.txt.enigma", "plain_file.txt", "your-password")
```
