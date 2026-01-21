import streamlit as st
import csv
import io

def process_iccids(iccid_list):
    """
    Process ICCIDs: trim to 19 digits if longer than 19.

    Args:
        iccid_list: List of ICCID strings

    Returns:
        List of tuples (original_iccid, processed_iccid)
    """
    processed_data = []

    for iccid in iccid_list:
        iccid = iccid.strip()
        
        if not iccid:  # Skip empty lines
            continue

        if len(iccid) > 19:
            # Trim to 19 digits if longer
            processed = iccid[:19]
        else:
            # Keep as is if 19 digits or shorter
            processed = iccid

        processed_data.append((iccid, processed))

    return processed_data

def create_csv_string(data):
    """
    Create CSV string with processed ICCID duplicated in first two columns.

    Args:
        data: List of tuples (original_iccid, processed_iccid)

    Returns:
        CSV content as string
    """
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    
    
    # Write data - processed ICCID in both columns
    for original, processed in data:
        writer.writerow([processed, processed])
    
    return output.getvalue()

def create_range_csv_string(start_iccids, end_iccids):
    """
    Create CSV string with start ICCIDs in first column and end ICCIDs in second column.

    Args:
        start_iccids: List of starting ICCID strings
        end_iccids: List of ending ICCID strings

    Returns:
        CSV content as string
    """
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    
   
    
    # Write data - pair each start with corresponding end
    max_length = max(len(start_iccids), len(end_iccids))
    
    for i in range(max_length):
        start = start_iccids[i] if i < len(start_iccids) else ""
        end = end_iccids[i] if i < len(end_iccids) else ""
        writer.writerow([start, end])
    
    return output.getvalue()

# Page configuration
st.set_page_config(
    page_title="ICCID Processor",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Card-like containers */
    .stApp > div {
        background: transparent;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 14px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 25px !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Success/Error messages */
    .stAlert {
        border-radius: 12px !important;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        border-radius: 8px !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Table styling */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    /* Info box */
    .info-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    h1 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    h2, h3 {
        color: white !important;
    }
    
    /* Card container */
    div[data-testid="column"] {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Header section
st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-bottom: 0.5rem;'>📱 ICCID Processor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; font-size: 1.2rem; margin-bottom: 3rem;'>Transform your ICCIDs with ease and precision</p>", unsafe_allow_html=True)

# Main content area
col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    # Create tabs for better organization
    tab1, tab2 = st.tabs(["🔧 Process ICCIDs", "📚 Instructions"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Mode selection
        mode = st.radio(
            "Choose processing mode:",
            ["📝 List Mode - Process multiple ICCIDs", "🔢 Range Mode - Generate from start to end"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Initialize variables
        iccid_input = ""
        start_iccid = ""
        end_iccid = ""
        
        if mode == "📝 List Mode - Process multiple ICCIDs":
            # Input section for list mode
            st.markdown("### 📝 Enter Your ICCIDs")
            st.markdown("<p style='color: #666; margin-bottom: 1rem;'>Paste your ICCIDs below, one per line</p>", unsafe_allow_html=True)
            
            iccid_input = st.text_area(
                "ICCIDs",
                height=250,
                placeholder="8988228066623425355\n8988228066627262560\n8988228066627262660\n8988228066627262760\n8988228066627262860\n...",
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Generate button
            col_btn1, col_btn2, col_btn3 = st.columns([3, 2, 3])
            with col_btn2:
                generate_button = st.button("🚀 Generate CSV", type="primary", use_container_width=True)
        
        else:
            # Range mode
            st.markdown("### 🔢 Enter ICCID Range")
            st.markdown("<p style='color: #666; margin-bottom: 1rem;'>Enter start and end ICCIDs (one per line, pairs will be matched)</p>", unsafe_allow_html=True)
            
            col_range1, col_range2 = st.columns(2)
            
            with col_range1:
                start_iccid = st.text_area(
                    "Start ICCIDs",
                    height=250,
                    placeholder="8988228066623425355\n8988228066623425365\n8988228066623425375\n...",
                    help="Enter starting ICCIDs (one per line)"
                )
            
            with col_range2:
                end_iccid = st.text_area(
                    "End ICCIDs",
                    height=250,
                    placeholder="8988228066623425360\n8988228066623425370\n8988228066623425380\n...",
                    help="Enter ending ICCIDs (one per line)"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Generate button for range mode
            col_btn1, col_btn2, col_btn3 = st.columns([3, 2, 3])
            with col_btn2:
                generate_button = st.button("🚀 Generate CSV", type="primary", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Process and display results
        if generate_button:
            if mode == "📝 List Mode - Process multiple ICCIDs":
                # List mode processing
                if not iccid_input.strip():
                    st.error("⚠️ Please enter at least one ICCID to process.")
                else:
                    # Parse input
                    iccids = [line.strip() for line in iccid_input.strip().split('\n') if line.strip()]
                    
                    # Process ICCIDs
                    with st.spinner('Processing ICCIDs...'):
                        processed_data = process_iccids(iccids)
                    
                    if not processed_data:
                        st.error("⚠️ No valid ICCIDs found. Please check your input.")
                    else:
                        # Create CSV content
                        csv_content = create_csv_string(processed_data)
                        
                        # Display success message with stats
                        st.success(f"✅ Successfully processed {len(processed_data)} ICCID(s)!")
                        
                        # Statistics cards
                        stat_col1, stat_col2, stat_col3 = st.columns(3)
                        
                        with stat_col1:
                            st.markdown(f"""
                            <div class='stat-card'>
                                <p class='stat-number'>{len(processed_data)}</p>
                                <p class='stat-label'>ICCIDs Processed</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with stat_col2:
                            trimmed_count = sum(1 for orig, proc in processed_data if len(orig) > 19)
                            st.markdown(f"""
                            <div class='stat-card'>
                                <p class='stat-number'>{trimmed_count}</p>
                                <p class='stat-label'>Trimmed</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with stat_col3:
                            st.markdown(f"""
                            <div class='stat-card'>
                                <p class='stat-number'>{len(processed_data) - trimmed_count}</p>
                                <p class='stat-label'>Unchanged</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Show preview
                        with st.expander("👀 Preview Processed Data", expanded=True):
                            preview_data = processed_data[:10]
                            
                            preview_df = {
                                '📋 Original ICCID': [orig for orig, _ in preview_data],
                                '✨ Processed ICCID': [proc for _, proc in preview_data],
                                '📏 Length': [len(proc) for _, proc in preview_data]
                            }
                            
                            st.dataframe(preview_df, use_container_width=True, height=400)
                            
                            if len(processed_data) > 10:
                                st.info(f"📊 Showing 10 of {len(processed_data)} total rows")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Download button
                        col_dl1, col_dl2, col_dl3 = st.columns([2, 4, 2])
                        with col_dl2:
                            st.download_button(
                                label="⬇️ Download CSV File",
                                data=csv_content,
                                file_name="iccids_output.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
            
            else:
                # Range mode processing
                if not start_iccid.strip() or not end_iccid.strip():
                    st.error("⚠️ Please enter both start and end ICCIDs.")
                else:
                    # Parse input - split by lines
                    start_iccids = [line.strip() for line in start_iccid.strip().split('\n') if line.strip()]
                    end_iccids = [line.strip() for line in end_iccid.strip().split('\n') if line.strip()]
                    
                    if not start_iccids or not end_iccids:
                        st.error("⚠️ Please enter valid ICCIDs.")
                    else:
                        # Process the ICCIDs (trim if needed)
                        start_processed = [s[:19] if len(s) > 19 else s for s in start_iccids]
                        end_processed = [e[:19] if len(e) > 19 else e for e in end_iccids]
                        
                        # Create CSV content
                        csv_content = create_range_csv_string(start_processed, end_processed)
                        
                        # Display success message
                        st.success("✅ ICCID range CSV generated successfully!")
                        
                        # Statistics cards
                        stat_col1, stat_col2, stat_col3 = st.columns(3)
                        
                        with stat_col1:
                            st.markdown(f"""
                            <div class='stat-card'>
                                <p class='stat-number'>{len(start_processed)}</p>
                                <p class='stat-label'>Start ICCIDs</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with stat_col2:
                            st.markdown(f"""
                            <div class='stat-card'>
                                <p class='stat-number'>{len(end_processed)}</p>
                                <p class='stat-label'>End ICCIDs</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with stat_col3:
                            total_pairs = max(len(start_processed), len(end_processed))
                            st.markdown(f"""
                            <div class='stat-card'>
                                <p class='stat-number'>{total_pairs}</p>
                                <p class='stat-label'>Total Rows</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Show preview
                        with st.expander("👀 Preview Range Data", expanded=True):
                            preview_count = min(10, max(len(start_processed), len(end_processed)))
                            
                            preview_starts = start_processed[:preview_count]
                            preview_ends = end_processed[:preview_count]
                            
                            # Pad lists to same length for display
                            while len(preview_starts) < preview_count:
                                preview_starts.append("")
                            while len(preview_ends) < preview_count:
                                preview_ends.append("")
                            
                            preview_df = {
                                '🎯 Start ICCID': preview_starts,
                                '🏁 End ICCID': preview_ends,
                            }
                            
                            st.dataframe(preview_df, use_container_width=True, height=400)
                            
                            total_rows = max(len(start_processed), len(end_processed))
                            if total_rows > 10:
                                st.info(f"📊 Showing 10 of {total_rows} total rows")
                            
                            # Warning if lists are different lengths
                            if len(start_processed) != len(end_processed):
                                st.warning(f"⚠️ Note: You have {len(start_processed)} start ICCIDs and {len(end_processed)} end ICCIDs. Empty cells will be added where needed.")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Download button
                        col_dl1, col_dl2, col_dl3 = st.columns([2, 4, 2])
                        with col_dl2:
                            st.download_button(
                                label="⬇️ Download CSV File",
                                data=csv_content,
                                file_name="iccids_range_output.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
    
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Instructions
        st.markdown("### 🎯 How to Use")
        
        st.markdown("""
        #### 📝 List Mode
        Process multiple ICCIDs at once:
        - Paste your ICCIDs (one per line)
        - Click "Generate CSV"
        - Get a CSV with duplicate columns for each processed ICCID
        
        #### 🔢 Range Mode
        Generate a CSV with start and end ICCIDs:
        - Enter a starting ICCID
        - Enter an ending ICCID
        - Click "Generate CSV"
        - Get a CSV with start in first column, end in second column
        
        ---
        """)
        
        col_inst1, col_inst2 = st.columns(2)
        
        with col_inst1:
            st.markdown("""
            #### Step 1: Input
            - Paste your ICCIDs in the text area
            - One ICCID per line
            - Empty lines will be ignored
            
            #### Step 2: Process
            - Click the "Generate CSV" button
            - ICCIDs will be processed automatically
            - See statistics and preview
            """)
        
        with col_inst2:
            st.markdown("""
            #### Processing Rules
            - **ICCIDs > 19 digits**: Trimmed to 19 digits
            - **ICCIDs ≤ 19 digits**: Kept unchanged
            - **Output format**: CSV with duplicate columns
            
            #### Step 3: Download
            - Review the preview
            - Click "Download CSV File"
            - Save to your device
            """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Example
        st.markdown("### 💡 Example Input")
        st.code("""8988228066623425355
8988228066627262560
8988228066627262660
8988228066627262760
8988228066627262860""", language=None)
        
        st.markdown("### 📤 Example Output")
        st.code("""ICCID,ICCID
8988228066623425355,8988228066623425355
8988228066627262560,8988228066627262560
8988228066627262660,8988228066627262660""", language="csv")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; opacity: 0.7;'>Made with ❤️ for efficient ICCID processing</p>", unsafe_allow_html=True)
