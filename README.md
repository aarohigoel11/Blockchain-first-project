# Document Notarization System

A blockchain-based document notarization system that allows users to upload, notarize, and verify documents using a simple web interface. Supports both single document and batch processing modes.

## Features

- Upload and notarize single documents
- Batch process entire directories of documents
- Generate SHA-256 hashes of documents
- Store document hashes in a blockchain
- Verify document authenticity
- View notarization history
- Persistent blockchain storage
- Progress tracking for batch operations

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Single Document Notarization**
   - Go to the "Single Document" tab
   - Click "Choose a file" to select a document
   - The system will display the document's hash
   - Click "Notarize Document" to store the hash in the blockchain

2. **Batch Document Processing**
   - Go to the "Batch Processing" tab
   - Enter the full path to the directory containing documents
   - Click "Process Directory" to start batch processing
   - Monitor progress with the progress bar
   - View detailed results in the expandable section

3. **Verify Documents**
   - Go to the "Verify Documents" tab
   - Upload the document you want to verify
   - Click "Verify Document"
   - The system will check if the document has been previously notarized

4. **View Notarized Records**
   - Scroll down to see all notarized documents
   - Click on any block to view its details

## Technical Details

- Uses SHA-256 for document hashing
- Implements a basic blockchain structure
- Stores blockchain data in `blockchain.json`
- Built with Streamlit for the user interface
- Supports recursive directory processing
- Handles errors gracefully during batch processing 