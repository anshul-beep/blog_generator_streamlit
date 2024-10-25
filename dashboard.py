import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Serverless Blog Generation System",
    layout="wide"
)

# Title and Description
st.title("Serverless Blog Generation System")
st.markdown("An automated blog generation system using AWS Lambda, Hugging Face, and S3")

# Create columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("System Architecture")
    # Display the system architecture image
    # Note: Replace 'architecture.png' with your actual image path
    st.image('Amazon API Gateway (2).png', caption='Serverless Blog Generation System Architecture', use_column_width=True)

with col2:
    st.subheader("System Components")
    with st.expander("API Request (Query)", expanded=False):
        st.write("""
        - Initiates blog generation request
        - Sends parameters and requirements
        - Handles user inputs and preferences
        """)
    
    with st.expander("Amazon API Gateway", expanded=False):
        st.write("""
        - Manages API endpoints
        - Handles incoming requests
        - Provides authentication
        - Routes requests to Lambda function
        """)
    
    with st.expander("AWS Lambda", expanded=False):
        st.write("""
        - Processes blog generation requests
        - Communicates with Hugging Face API
        - Handles content formatting
        - Manages S3 storage operations
        """)
    
    with st.expander("S3 Bucket Storage", expanded=False):
        st.write("""
        - Stores generated blog content in blogcontent.txt
        - Maintains version history of blogs
        - Enables quick content retrieval
        - Provides secure storage with encryption
        - Allows for backup and archival
        """)
    
    with st.expander("Hugging Face Model", expanded=False):
        st.write("""
        - Provides LLM capabilities
        - Generates blog content
        - Handles natural language processing
        - Ensures content quality
        """)

# Links section
st.subheader("Important Links")
cols = st.columns(3)

with cols[0]:
    st.markdown("### API Endpoint")
    api_endpoint = st.text_input(
        "API URL",
        value="https://api.example.com/blog-generator",
        key="api_endpoint"
    )
    if st.button("Open API Documentation"):
        st.markdown(f"[API Documentation]({api_endpoint})")

with cols[1]:
    st.markdown("### GitHub Repository")
    github_repo = st.text_input(
        "Repository URL",
        value="https://github.com/yourusername/blog-generator",
        key="github_repo"
    )
    if st.button("Open GitHub Repository"):
        st.markdown(f"[Repository]({github_repo})")

with cols[2]:
    st.markdown("### Blog UI")
    blog_ui = st.text_input(
        "Blog UI URL",
        value="https://bloggeneratorui.streamlit.app/",
        key="blog_ui"
    )
    if st.button("Open Blog UI"):
        st.markdown(f"[Blog UI]({blog_ui})")





# Requirements section
st.sidebar.title("Requirements")
st.sidebar.markdown("""
### Dependencies
```
streamlit==1.24.0
Pillow==9.5.0
pandas==1.5.3
```

### Installation
```bash
pip install streamlit Pillow pandas
```

### Run the app
```bash
streamlit run app.py
```
""")

