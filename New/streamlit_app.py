import streamlit as st
import os
import uuid
import Anonymizer
from pathlib import Path

def main():
    st.set_page_config(page_title="Document Anonymizer", layout="centered")

    # Use a higher-resolution Unsplash image with better quality
    background_url = (
        "https://images.unsplash.com/photo-1488998427799-e3362cec87c3"
        "?ixlib=rb-4.0.3"
        "&auto=format"
        "&fit=crop"
        "&w=2560"    
        "&q=80"
    )


    st.markdown(
        f"""
        <style>
        /* Set a full-screen background image using Unsplash */
        html, body, [data-testid="stAppViewContainer"] {{
            background: url("{background_url}") no-repeat center center fixed !important;
            background-size: cover !important;
        }}

        /* Fade-in animation for the main container */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Translucent container for app content with fade-in effect */
        [data-testid="stAppViewContainer"] > .main {{
            backdrop-filter: blur(6px);
            background-color: rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            padding: 20px;
            animation: fadeIn 1s ease-in-out;
        }}

        /* Styling for text inputs */
        input[type="text"] {{
            background-color: transparent;
            color: #a19eae;
        }}
        div[data-baseweb="base-input"] {{
            background-color: transparent !important;
        }}

        /* Centering and styling the connection links */
        .connect-links {{
            text-align: center;
            margin-top: 30px;
        }}
        .connect-links a {{
            font-size: 1.8em; /* Bigger links */
            color: #0073b1;  /* Example color for LinkedIn link text */
            text-decoration: none;
            margin: 0 25px;
            display: inline-block;
            transition: transform 0.3s ease;
        }}
        .connect-links a:hover {{
            transform: scale(1.2);
        }}

        /* Styling for the anonymize button: scale up on hover */
        div.stButton > button {{
            transition: transform 0.3s ease;
        }}
        div.stButton > button:hover {{
            transform: scale(1.05);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # App title and instructions
    st.title("Document Anonymizer")
    st.write("Select an input file and enter the desired file name, then click **Anonymize**.")

    # File uploader for input DOCX
    input_file = st.file_uploader("Select Input DOCX File", type=["docx"])

    # Text input for the output file name
    output_file_name = st.text_input("Output File Name (e.g. anonymized.docx)")

    if st.button("Anonymize Document"):
        if not input_file:
            st.warning("Please select an input file.")
            return

        if not output_file_name:
            st.warning("Please provide an output file name (e.g. anonymized.docx).")
            return

        # Ensure the file name ends with '.docx'
        if not output_file_name.lower().endswith(".docx"):
            output_file_name += ".docx"

        # Always save to the user's Downloads folder
        downloads_dir = Path.home() / "Downloads"
        output_path = os.path.join(downloads_dir, output_file_name)

        # Save the uploaded file temporarily
        temp_input_path = f"{uuid.uuid4()}.docx"
        with open(temp_input_path, "wb") as f:
            f.write(input_file.read())

        try:
            # Run the anonymization process
            Anonymizer.run_anonymization(temp_input_path, output_path)
            st.success(f"Anonymized DOCX saved to: {output_path}")
        except Exception as e:
            st.error(f"Error during anonymization: {e}")
        finally:
            if os.path.exists(temp_input_path):
                os.remove(temp_input_path)

    # Horizontal rule for separation
    st.markdown("---")


    st.markdown(
        """
        <div class="connect-links">
            <a href="https://www.linkedin.com/in/mykhailo-karpiuk-b94705199/" target="_blank">LinkedIn</a>
            <a href="https://github.com/S2k22" target="_blank">GitHub</a>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()












