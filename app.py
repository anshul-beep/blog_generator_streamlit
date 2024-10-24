import streamlit as st
import requests
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="✍️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f2f6, #e0e5ea);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .system-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .blog-input {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .blog-output {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Constants
API_URL = "https://04akvtn4gg.execute-api.ap-southeast-2.amazonaws.com/dev_environment/blog-generation"

def fetch_blog_from_api(blog_topic: str) -> str:
    """Send blog topic to your API and get the generated blog"""
    try:
        payload = {"blog_topic": blog_topic}
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('blog_content', 'No content generated.')
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# Header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("✍️ AI Blog Generator")
st.markdown("Transform your ideas into engaging blog posts with AI")
st.markdown('</div>', unsafe_allow_html=True)

# Create two columns with adjusted ratio
col1, col2 = st.columns([1, 3])

# Left Column - System Design Info
with col1:
    st.markdown('<div class="system-card">', unsafe_allow_html=True)
    st.subheader("🔧 System Architecture")
    
    # System components with emoji icons
    st.markdown("""
    #### Key Components:
    
    🌐 **API Gateway**
    - Secure HTTP endpoint
    - Request routing
    
    ⚡ **AWS Lambda**
    - Blog generation logic
    - API integration
    
    🤖 **Hugging Face API**
    - GPT-2 model
    - Text generation
    
    🎯 **Streamlit UI**
    - User interface
    - Content display
    """)
    
    # Process flow
    st.markdown("#### Process Flow:")
    st.markdown("""
    1. User submits topic ➡️
    2. API Gateway receives request ➡️
    3. Lambda processes content ➡️
    4. Blog displayed to user ✨
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Right Column - Blog Generation UI
with col2:
    # Input Section
    st.markdown('<div class="blog-input">', unsafe_allow_html=True)
    st.subheader("🎨 Create Your Blog")
    blog_topic = st.text_input(
        "What would you like to blog about?",
        placeholder="Enter your blog topic here...",
        help="Enter a topic, and our AI will generate a blog post for you!"
    )
    
    col_button, col_space = st.columns([1,4])
    with col_button:
        generate_button = st.button("✨ Generate Blog", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Output Section
    if generate_button:
        if blog_topic:
            st.markdown('<div class="blog-output">', unsafe_allow_html=True)
            with st.spinner('🤖 AI is crafting your blog post...'):
                blog_content = fetch_blog_from_api(blog_topic)
                
                # Display metadata
                st.caption(f"Generated on: {datetime.now().strftime('%B %d, %Y, %H:%M:%S')}")
                st.caption(f"Topic: {blog_topic}")
                
                # Display the blog content
                st.markdown("### 📝 Generated Blog Post")
                st.write(blog_content)
                
                # Add sharing options
                st.markdown("---")
                st.markdown("### Share this blog:")
                share_col1, share_col2, share_col3 = st.columns(3)
                with share_col1:
                    st.button("📋 Copy to Clipboard")
                with share_col2:
                    st.button("📥 Download as PDF")
                with share_col3:
                    st.button("📧 Share via Email")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("🎯 Please enter a blog topic to generate content.")