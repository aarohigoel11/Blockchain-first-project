import streamlit as st
import time
from blockchain import Blockchain
from utils import calculate_file_hash, format_timestamp, process_directory
import os
from pathlib import Path

# Initialize session state
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain.load_from_file()

st.title("Document Notarization System")
st.write("Upload and verify documents using blockchain technology")

# Create tabs for different operations
tab1, tab2, tab3 = st.tabs(["Single Document", "Batch Processing", "Verify Documents"])

# Single Document Tab
with tab1:
    st.header("Upload Single Document")
    uploaded_file = st.file_uploader("Choose a file", type=None)

    if uploaded_file is not None:
        # Calculate and display file hash
        file_hash = calculate_file_hash(uploaded_file)
        st.write("File Hash:", file_hash)
        
        # Notarize button
        if st.button("Notarize Document", key="single_notarize"):
            # Add block to blockchain
            new_block = st.session_state.blockchain.add_block(file_hash)
            st.session_state.blockchain.save_to_file()
            
            st.success(f"Document notarized successfully! Block #{new_block.index} created.")
            st.write("Block Hash:", new_block.hash)
            st.write("Timestamp:", format_timestamp(new_block.timestamp))

# Batch Processing Tab
with tab2:
    st.header("Batch Document Processing")
    
    # Directory input
    directory_path = st.text_input("Enter directory path to process", "")
    
    if st.button("Process Directory", key="batch_process"):
        if directory_path:
            try:
                with st.spinner("Processing files..."):
                    results = process_directory(directory_path)
                    
                    # Create a progress bar
                    progress_bar = st.progress(0)
                    total_files = len(results)
                    
                    # Process each file
                    for i, result in enumerate(results):
                        if 'hash' in result:
                            # Add to blockchain
                            new_block = st.session_state.blockchain.add_block(result['hash'])
                            result['block_index'] = new_block.index
                            result['block_hash'] = new_block.hash
                            result['timestamp'] = new_block.timestamp
                        
                        # Update progress
                        progress_bar.progress((i + 1) / total_files)
                    
                    # Save blockchain
                    st.session_state.blockchain.save_to_file()
                    
                    # Display results
                    st.success(f"Processed {total_files} files successfully!")
                    
                    # Show detailed results
                    with st.expander("View Processing Results"):
                        for result in results:
                            if 'error' in result:
                                st.error(f"Error processing {result['file_name']}: {result['error']}")
                            else:
                                st.write(f"File: {result['file_name']}")
                                st.write(f"Hash: {result['hash']}")
                                st.write(f"Block: #{result['block_index']}")
                                st.write(f"Timestamp: {format_timestamp(result['timestamp'])}")
                                st.write("---")
                
            except Exception as e:
                st.error(f"Error processing directory: {str(e)}")
        else:
            st.warning("Please enter a directory path")

# Verify Documents Tab
with tab3:
    st.header("Verify Document")
    verify_file = st.file_uploader("Choose a file to verify", type=None, key="verify")

    if verify_file is not None:
        verify_hash = calculate_file_hash(verify_file)
        st.write("File Hash:", verify_hash)
        
        if st.button("Verify Document", key="verify_doc"):
            result = st.session_state.blockchain.find_block_by_data(verify_hash)
            if result["found"]:
                st.success("Document verified! This document has been notarized.")
                st.write("Block Number:", result["block_index"])
                st.write("Notarization Time:", format_timestamp(result["timestamp"]))
                st.write("Block Hash:", result["hash"])
            else:
                st.error("Document not found in blockchain. This document has not been notarized.")

# Display blockchain
st.header("Notarized Records")
if st.session_state.blockchain.chain:
    for block in st.session_state.blockchain.chain:
        with st.expander(f"Block #{block.index}"):
            st.write("Timestamp:", format_timestamp(block.timestamp))
            st.write("Hash:", block.hash)
            st.write("Previous Hash:", block.previous_hash)
            st.write("Data:", block.data)
else:
    st.write("No blocks in the blockchain yet.") 