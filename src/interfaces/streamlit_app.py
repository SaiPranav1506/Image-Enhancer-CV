"""
Enhanced Streamlit Web Interface for Image Enhancement
Interactive web application with multi-page navigation and comprehensive metrics
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import sys
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.web_scraper import WebScraper
from modules.blur_detector import BlurDetector
from modules.image_enhancer import ImageEnhancer
from modules.quality_metrics import QualityMetrics


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'web_scraper' not in st.session_state:
        st.session_state.web_scraper = WebScraper(output_dir='temp_images')
    if 'blur_detector' not in st.session_state:
        st.session_state.blur_detector = BlurDetector(threshold=100)
    if 'image_enhancer' not in st.session_state:
        st.session_state.image_enhancer = ImageEnhancer(output_dir='output')
    if 'quality_metrics' not in st.session_state:
        st.session_state.quality_metrics = QualityMetrics()
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None


def apply_custom_css():
    """Apply custom CSS for better styling"""
    st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 0 1rem;
    }
    
    /* Custom buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-size: 16px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    /* Interactive horizontal navigation */
    .nav-container {
        display: flex;
        gap: 10px;
        justify-content: center;
        margin-bottom: 30px;
        flex-wrap: wrap;
        animation: slideDown 0.5s ease;
    }
    
    .nav-button {
        padding: 12px 24px;
        border-radius: 25px;
        border: 2px solid #6B4423;
        background: white;
        color: #6B4423;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .nav-button:hover {
        background: #1f77b4;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
    }
    
    /* Smooth transitions */
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    .page-content {
        animation: fadeIn 0.4s ease;
    }
    
    /* Action buttons with hover effects */
    .action-button {
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .action-button:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Cards styling */
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: all 0.3s ease;
        color: #6B4423;
    }
    
    .metric-card p {
        color: #6B4423 !important;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    
    /* Headers */
    h1 {
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        animation: slideIn 0.5s ease;
    }
    
    h2 {
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 10px;
        animation: slideIn 0.5s ease 0.1s both;
    }
    
    /* Stats boxes */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stat-box:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    
    .stat-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
        animation: slideIn 0.5s ease 0.2s both;
    }
    
    .stat-label {
        font-size: 14px;
        opacity: 0.9;
    }
    
    /* Input field text visibility */
    input[type="text"],
    input[type="number"],
    input[type="email"],
    input[type="url"],
    textarea,
    .stTextInput input,
    .stNumberInput input {
        color: #6B4423 !important;
        background-color: #ffffff !important;
    }
    
    input[type="text"]::placeholder,
    input[type="number"]::placeholder,
    textarea::placeholder {
        color: #8B6F47 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def create_home_page():
    """Create engaging home page"""
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px;'>
        <h1 style='font-size: 48px; color: #1f77b4; margin-bottom: 10px;'>
            🖼️ Image Enhancement Suite
        </h1>
        <p style='font-size: 20px; color: #6B4423; margin-bottom: 40px;'>
            Transform Your Blurry Images into Crystal Clear Masterpieces
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero image section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://via.placeholder.com/500x300/1f77b4/ffffff?text=Image+Enhancement+Demo", 
                use_container_width=True, caption="Transform Your Images")
    
    st.markdown("---")
    
    # Features section
    st.markdown("<h2>✨ Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='text-align: center; color: #1f77b4;'>🌐 Web Scraping</h3>
            <p style='text-align: center; color: #6B4423;'>
                Download images directly from websites and enhance them in bulk.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='text-align: center; color: #1f77b4;'>📊 Blur Detection</h3>
            <p style='text-align: center; color: #6B4423;'>
                Intelligent blur analysis using advanced Laplacian variance detection.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='text-align: center; color: #1f77b4;'>✨ Enhancement</h3>
            <p style='text-align: center; color: #6B4423;'>
                Professional-grade image sharpening and contrast enhancement.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Uses and Applications
    st.markdown("<h2>🎯 Applications & Use Cases</h2>", unsafe_allow_html=True)
    
    uses = {
        "📸 Photography": "Restore old photos and enhance smartphone pictures",
        "🔬 Medical Imaging": "Improve clarity of X-rays and medical scans",
        "📱 Mobile Photography": "Fix low-light and blurry photos from devices",
        "🛰️ Satellite Imagery": "Enhance resolution of satellite and aerial photos",
        "🎥 Video Content": "Process individual frames for video enhancement",
        "📚 Document Scanning": "Improve clarity of scanned documents and receipts",
        "🎨 Digital Art": "Sharpen artwork and restore artistic images",
        "🤖 Machine Vision": "Pre-process images for better AI model input"
    }
    
    col1, col2 = st.columns(2)
    for idx, (use, description) in enumerate(uses.items()):
        if idx % 2 == 0:
            with col1:
                st.markdown(f"### {use}\n{description}")
        else:
            with col2:
                st.markdown(f"### {use}\n{description}")
    
    st.markdown("---")
    
    # Benefits section
    st.markdown("<h2>🌟 Why Use Image Enhancement?</h2>", unsafe_allow_html=True)
    
    benefits_col1, benefits_col2, benefits_col3 = st.columns(3)
    
    with benefits_col1:
        st.markdown("""
        **⚡ Fast Processing**
        - Real-time enhancement
        - Batch processing support
        - Instant results
        """)
    
    with benefits_col2:
        st.markdown("""
        **🎯 High Quality**
        - Professional algorithms
        - 60-80% improvement
        - Detailed metrics
        """)
    
    with benefits_col3:
        st.markdown("""
        **📊 Detailed Analytics**
        - Sharpness tracking
        - Contrast measurement
        - Before/after comparison
        """)
    
    st.markdown("---")
    
    # Call to action
    st.markdown("<h2 style='text-align: center; margin-top: 50px;'>Ready to Enhancement Your Images?</h2>", 
               unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Interactive CTA button with smooth transition
        if st.button("🚀 Get Started Now", key="start_btn", use_container_width=True):
            # Add smooth transition feedback
            with st.spinner('✨ Preparing your upload environment...'):
                import time
                time.sleep(0.3)  # Mini delay for visual effect
                st.session_state.page = 'upload'
                st.rerun()
    
    st.markdown("""
    <div style='text-align: center; color: #6B4423; font-size: 12px; margin-top: 40px;'>
        <p>Scroll down to explore more</p>
        <p style='font-size: 24px; animation: bounce 1s infinite;'>↓</p>
    </div>
    """, unsafe_allow_html=True)


def create_tech_section():
    """Show technology section at bottom of home"""
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>⚙️ Powered By Advanced Technology</h2>", 
               unsafe_allow_html=True)
    
    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
    
    technologies = [
        ("OpenCV", "Advanced image processing and computer vision"),
        ("NumPy", "High-performance numerical computing"),
        ("Laplacian", "Edge detection and blur analysis"),
        ("Histogram EQ", "Contrast enhancement algorithm")
    ]
    
    for col, (tech, desc) in zip([tech_col1, tech_col2, tech_col3, tech_col4], technologies):
        with col:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <strong style='color: #6B4423;'>{tech}</strong><br>
                <small style='color: #6B4423;'>{desc}</small>
            </div>
            """, unsafe_allow_html=True)


def create_settings_section():
    """Show interactive settings section at bottom of home"""
    st.markdown("---")
    
    with st.expander("⚙️ Advanced Settings", expanded=False):
        st.markdown("### Detection & Enhancement Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            blur_threshold = st.slider(
                "🔍 Blur Detection Threshold",
                min_value=50,
                max_value=200,
                value=100,
                step=10,
                help="Lower values are more sensitive to blur. Higher values require more blur to detect."
            )
            st.session_state.blur_detector.set_threshold(blur_threshold)
        
        with col2:
            st.info(f"📊 Current Threshold: **{blur_threshold}**\nVariance below this indicates blur")
        
        st.markdown("---")
        st.markdown("### About This Application")
        st.markdown("""
        **Image Enhancement Suite v1.0**
        
        A professional image enhancement tool featuring:
        - 🌐 **Web Scraping** - Download and process images from websites
        - 📊 **Blur Detection** - Analyze image sharpness with Laplacian variance
        - ✨ **Enhancement** - Advanced sharpening and contrast improvement
        - 📈 **Detailed Metrics** - Comprehensive before/after analysis
        
        **Powered by:**
        - OpenCV for image processing
        - NumPy for numerical computation
        - Streamlit for interactive UI
        - Plotly for data visualization
        """)


def create_upload_page():
    """Create image upload page"""
    st.markdown("<h1>📤 Upload Your Image</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6B4423; font-size: 16px; margin-bottom: 30px;'>Choose your method to get started</p>", unsafe_allow_html=True)
    
    # Tabs for different input methods
    tab1, tab2 = st.tabs(["📁 Upload Image", "🌐 Image URL"])
    
    with tab1:
        st.markdown("### Upload Image from Computer")
        uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png', 'bmp', 'webp'])
        
        if uploaded_file:
            # Save temporary file
            temp_path = os.path.join('temp_images', uploaded_file.name)
            os.makedirs('temp_images', exist_ok=True)
            
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            # Show preview
            st.markdown("### Preview")
            st.image(Image.open(temp_path), use_container_width=True)
            
            # Processing options
            st.markdown("### Enhancement Options")
            col1, col2 = st.columns(2)
            with col1:
                apply_sharpen = st.checkbox("Apply Sharpening", value=True)
            with col2:
                apply_histogram = st.checkbox("Apply Contrast Enhancement", value=True)
            
            if st.button("✨ Enhance Image", use_container_width=True, type="primary"):
                # Interactive processing with progress feedback
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                with st.spinner("🔄 Enhancing your image..."):
                    import time
                    for i in range(0, 100, 20):
                        progress_bar.progress(i)
                        status_text.text(f"Processing: {i}%...")
                        time.sleep(0.1)
                    
                    process_and_show_results(temp_path, apply_sharpen, apply_histogram)
                    progress_bar.progress(100)
                    status_text.text("✅ Complete! Redirecting to results...")
                    time.sleep(0.5)
    
    with tab2:
        st.markdown("### Download from URL")
        url = st.text_input("Enter image URL:")
        image_limit = st.slider("Number of variations to try", 1, 5, 1)
        
        if st.button("📥 Download from URL", use_container_width=True, type="primary"):
            if url:
                # Interactive download with progress feedback
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                with st.spinner("🌐 Downloading images..."):
                    import time
                    status_text.text("📥 Fetching images...")
                    progress_bar.progress(25)
                    time.sleep(0.3)
                    
                    scraper = st.session_state.web_scraper
                    images = scraper.scrape_images(url, image_limit)
                    
                    progress_bar.progress(75)
                    status_text.text("✅ Images downloaded successfully!")
                    
                    if images:
                        st.success(f"✅ Downloaded {len(images)} image(s)")
                        
                        # Select which image to process
                        selected_idx = st.slider("Select image to enhance", 0, len(images)-1)
                        selected_image = images[selected_idx]
                        
                        st.image(Image.open(selected_image), use_container_width=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            apply_sharpen = st.checkbox("Apply Sharpening", value=True, key="url_sharpen")
                        with col2:
                            apply_histogram = st.checkbox("Apply Contrast Enhancement", value=True, key="url_histogram")
                        
                        if st.button("✨ Enhance This Image", use_container_width=True, type="primary"):
                            # Interactive processing with progress feedback
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            with st.spinner("🔄 Enhancing your image..."):
                                import time
                                for i in range(0, 100, 20):
                                    progress_bar.progress(i)
                                    status_text.text(f"Processing: {i}%...")
                                    time.sleep(0.1)
                                
                                process_and_show_results(selected_image, apply_sharpen, apply_histogram)
                                progress_bar.progress(100)
                                status_text.text("✅ Complete! Redirecting to results...")
                                time.sleep(0.5)
                    else:
                        st.error("❌ Could not download images from URL")
            else:
                st.warning("⚠️ Please enter a valid URL")


def process_and_show_results(image_path, apply_sharpen, apply_histogram):
    """Process image and redirect to results page"""
    try:
        enhancer = st.session_state.image_enhancer
        metrics = st.session_state.quality_metrics
        
        # Enhance image
        result = enhancer.enhance_image(
            image_path,
            apply_sharpen=apply_sharpen,
            apply_histogram=apply_histogram,
            save=False
        )
        
        if result['enhanced'] is not None:
            # Calculate metrics
            comparison = metrics.compare_images(result['original'], result['enhanced'])
            
            # Store data in session
            st.session_state.processed_data = {
                'original': result['original'],
                'enhanced': result['enhanced'],
                'comparison': comparison,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'filename': os.path.basename(image_path)
            }
            
            st.session_state.page = 'results'
            st.rerun()
        else:
            st.error("❌ Enhancement failed")
    except Exception as e:
        st.error(f"❌ Error: {e}")


def create_results_page():
    """Create comprehensive results page with metrics and charts"""
    
    if st.session_state.processed_data is None:
        st.warning("⚠️ No processed image. Please upload an image first.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Go Back to Upload", use_container_width=True):
                with st.spinner('🔄 Redirecting...'):
                    import time
                    time.sleep(0.3)
                    st.session_state.page = 'upload'
                    st.rerun()
        return
    
    data = st.session_state.processed_data
    
    # Header
    st.markdown(f"""
    <div style='text-align: center; padding: 20px;'>
        <h1>📊 Enhancement Results</h1>
        <p style='color: #6B4423;'>File: <strong>{data['filename']}</strong> | 
        Time: <strong>{data['timestamp']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Overall improvement metric
    comparison = data['comparison']
    overall_improvement = comparison['overall_improvement_%']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-label'>Overall Improvement</div>
            <div class='stat-value'>{overall_improvement:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        sharpness_imp = comparison['improvements']['sharpness_improvement_%']
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-label'>Sharpness Boost</div>
            <div class='stat-value'>+{sharpness_imp:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        contrast_imp = comparison['improvements']['contrast_improvement_%']
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-label'>Contrast Improvement</div>
            <div class='stat-value'>+{contrast_imp:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Image comparison
    st.markdown("<h2>🖼️ Before & After Comparison</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Original Image")
        original_pil = Image.fromarray(cv2.cvtColor(data['original'], cv2.COLOR_BGR2RGB))
        st.image(original_pil, use_container_width=True)
    
    with col2:
        st.markdown("### Enhanced Image")
        enhanced_pil = Image.fromarray(cv2.cvtColor(data['enhanced'], cv2.COLOR_BGR2RGB))
        st.image(enhanced_pil, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed metrics tabs
    st.markdown("<h2>📈 Detailed Metrics</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Original Metrics", "Enhanced Metrics", "Visual Comparison", "Progress Chart"])
    
    with tab1:
        # Original image metrics
        st.markdown("### 📸 Original Image Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🎯 Sharpness", f"{comparison['original']['sharpness']:.2f}")
            st.metric("🌈 Contrast", f"{comparison['original']['contrast']:.2f}")
            st.metric("☀️ Brightness", f"{comparison['original']['brightness']:.2f}")
        
        with col2:
            st.metric("💾 Entropy", f"{comparison['original']['entropy']:.2f}")
            st.metric("🔍 Edge Density", f"{comparison['original']['edge_density']:.2f}%")
        
        st.markdown("---")
        
        # Detailed breakdown
        st.markdown("### Detailed Original Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            **Sharpness**  
            {comparison['original']['sharpness']:.4f}
            
            Measures image clarity and focus
            """)
        
        with col2:
            st.markdown(f"""
            **Contrast**  
            {comparison['original']['contrast']:.4f}
            
            Measures brightness variation
            """)
        
        with col3:
            st.markdown(f"""
            **Brightness**  
            {comparison['original']['brightness']:.4f}
            
            Average pixel intensity
            """)
    
    with tab2:
        # Enhanced image metrics
        st.markdown("### ✨ Enhanced Image Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🎯 Sharpness", f"{comparison['enhanced']['sharpness']:.2f}", 
                     f"↑ +{comparison['enhanced']['sharpness'] - comparison['original']['sharpness']:.2f}")
            st.metric("🌈 Contrast", f"{comparison['enhanced']['contrast']:.2f}", 
                     f"↑ +{comparison['enhanced']['contrast'] - comparison['original']['contrast']:.2f}")
            st.metric("☀️ Brightness", f"{comparison['enhanced']['brightness']:.2f}", 
                     f"↑ {comparison['enhanced']['brightness'] - comparison['original']['brightness']:+.2f}")
        
        with col2:
            st.metric("💾 Entropy", f"{comparison['enhanced']['entropy']:.2f}", 
                     f"↑ +{comparison['enhanced']['entropy'] - comparison['original']['entropy']:.2f}")
            st.metric("🔍 Edge Density", f"{comparison['enhanced']['edge_density']:.2f}%", 
                     f"↑ +{comparison['enhanced']['edge_density'] - comparison['original']['edge_density']:.2f}%")
        
        st.markdown("---")
        
        # Detailed breakdown
        st.markdown("### Detailed Enhanced Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            **Sharpness**  
            {comparison['enhanced']['sharpness']:.4f}
            
            Improvement: {comparison['improvements']['sharpness_improvement_%']:.2f}% ✅
            """)
        
        with col2:
            st.markdown(f"""
            **Contrast**  
            {comparison['enhanced']['contrast']:.4f}
            
            Improvement: {comparison['improvements']['contrast_improvement_%']:.2f}% ✅
            """)
        
        with col3:
            st.markdown(f"""
            **Brightness**  
            {comparison['enhanced']['brightness']:.4f}
            
            Change: {comparison['improvements']['brightness_change']:+.2f} units
            """)
    
    with tab3:
        # Side-by-side comparison chart
        metrics_labels = ["Sharpness", "Contrast", "Brightness", "Entropy", "Edge Density"]
        
        original_values = [
            comparison['original']['sharpness'],
            comparison['original']['contrast'],
            comparison['original']['brightness'],
            comparison['original']['entropy'],
            comparison['original']['edge_density']
        ]
        
        enhanced_values = [
            comparison['enhanced']['sharpness'],
            comparison['enhanced']['contrast'],
            comparison['enhanced']['brightness'],
            comparison['enhanced']['entropy'],
            comparison['enhanced']['edge_density']
        ]
        
        fig = go.Figure(data=[
            go.Bar(name='Original', x=metrics_labels, y=original_values, marker_color='#ef553b'),
            go.Bar(name='Enhanced', x=metrics_labels, y=enhanced_values, marker_color='#00cc96')
        ])
        
        fig.update_layout(
            title="Metrics Comparison: Original vs Enhanced",
            barmode='group',
            height=500,
            hovermode='x unified',
            xaxis_title="Metrics",
            yaxis_title="Value"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Multi-line progress chart showing enhancement progression
        st.markdown("### 📊 Enhancement Progress Chart")
        st.markdown("*Multi-line visualization showing metrics progression from original to enhanced*")
        
        metrics_list = ["Sharpness", "Contrast", "Brightness", "Entropy", "Edge Density"]
        
        # Create progress data
        fig = go.Figure()
        
        # Add lines for each metric showing original and enhanced
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        for idx, metric_name in enumerate(metrics_list):
            original_val = comparison['original'][metric_name.lower().replace(' ', '_')]
            enhanced_val = comparison['enhanced'][metric_name.lower().replace(' ', '_')]
            
            fig.add_trace(go.Scatter(
                x=['Original', 'Enhanced'],
                y=[original_val, enhanced_val],
                mode='lines+markers',
                name=metric_name,
                line=dict(width=3, color=colors[idx]),
                marker=dict(size=10),
                hovertemplate=f'<b>{metric_name}</b><br>' +
                            'Stage: %{x}<br>' +
                            'Value: %{y:.2f}<extra></extra>'
            ))
        
        fig.update_layout(
            title="📈 Metric Progression: Original → Enhanced",
            xaxis_title="Processing Stage",
            yaxis_title="Metric Value",
            height=600,
            hovermode='x unified',
            plot_bgcolor='rgba(240,240,240,0.5)',
            paper_bgcolor='white',
            font=dict(size=12),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99,
                bgcolor="rgba(255,255,255,0.8)"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.markdown("---")
        st.markdown("### 📈 Improvement Summary")
        
        comp_col1, comp_col2, comp_col3, comp_col4, comp_col5 = st.columns(5)
        
        with comp_col1:
            sharpness_imp = comparison['improvements']['sharpness_improvement_%']
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <strong style='color: #6B4423;'>Sharpness</strong><br>
                <span style='font-size: 24px; color: #FF6B6B; font-weight: bold;'>
                +{sharpness_imp:.1f}%
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        with comp_col2:
            contrast_imp = comparison['improvements']['contrast_improvement_%']
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <strong style='color: #6B4423;'>Contrast</strong><br>
                <span style='font-size: 24px; color: #4ECDC4; font-weight: bold;'>
                +{contrast_imp:.1f}%
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        with comp_col3:
            brightness_change = comparison['improvements']['brightness_change']
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <strong style='color: #6B4423;'>Brightness</strong><br>
                <span style='font-size: 24px; color: #45B7D1; font-weight: bold;'>
                {brightness_change:+.1f}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        with comp_col4:
            entropy_imp = comparison['improvements']['entropy_improvement_%']
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <strong style='color: #6B4423;'>Entropy</strong><br>
                <span style='font-size: 24px; color: #FFA07A; font-weight: bold;'>
                +{entropy_imp:.1f}%
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        with comp_col5:
            edge_imp = comparison['improvements']['edge_improvement_%']
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <strong style='color: #6B4423;'>Edges</strong><br>
                <span style='font-size: 24px; color: #98D8C8; font-weight: bold;'>
                +{edge_imp:.1f}%
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed improvement breakdown
    st.markdown("<h2>📋 Detailed Improvement Breakdown</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Enhancement Improvements")
        st.markdown(f"""
        - **Sharpness Improvement:** {comparison['improvements']['sharpness_improvement_%']:.2f}% ✨
        - **Contrast Improvement:** {comparison['improvements']['contrast_improvement_%']:.2f}% 📊
        - **Entropy Improvement:** {comparison['improvements']['entropy_improvement_%']:.2f}% 💾
        - **Edge Improvement:** {comparison['improvements']['edge_improvement_%']:.2f}% 🔍
        """)
    
    with col2:
        st.markdown("### Color Information")
        brightness_change = comparison['improvements']['brightness_change']
        st.markdown(f"""
        - **Brightness Change:** {brightness_change:+.2f} units
        - **Original Brightness:** {comparison['original']['brightness']:.2f}
        - **Enhanced Brightness:** {comparison['enhanced']['brightness']:.2f}
        """)
    
    st.markdown("---")
    
    # Interactive action buttons with smooth transitions
    st.markdown("### 🎯 What's Next?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ Process Another Image", use_container_width=True, key="back_upload"):
            with st.spinner("🔄 Preparing upload environment..."):
                import time
                time.sleep(0.4)
                st.session_state.page = 'upload'
                st.rerun()
    
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True, key="back_home"):
            with st.spinner("🔄 Returning home..."):
                import time
                time.sleep(0.4)
                st.session_state.page = 'home'
                st.rerun()
    
    with col3:
        if st.button("💾 Download Enhanced Image", use_container_width=True, key="download_btn"):
            # Show download progress
            with st.spinner("📦 Preparing download..."):
                import time
                time.sleep(0.2)
                
                enhanced_pil = Image.fromarray(cv2.cvtColor(data['enhanced'], cv2.COLOR_BGR2RGB))
                
                from io import BytesIO
                img_byte_arr = BytesIO()
                enhanced_pil.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                
                time.sleep(0.2)
                st.success("✅ Download ready!")
            
            st.download_button(
                label="⬇️ Click to Download",
                data=img_byte_arr.getvalue(),
                file_name=f"enhanced_{data['filename']}",
                mime="image/png"
            )


def create_top_navigation():
    """Create interactive horizontal navigation bar"""
    pages = {
        "🏠 Home": "home",
        "📤 Upload & Process": "upload",
        "📊 Results": "results"
    }
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        nav_cols = st.columns(len(pages))
        for idx, (page_name, page_key) in enumerate(pages.items()):
            with nav_cols[idx]:
                is_active = st.session_state.page == page_key
                if st.button(
                    page_name,
                    use_container_width=True,
                    key=f"nav_{page_key}",
                    type="primary" if is_active else "secondary"
                ):
                    st.session_state.page = page_key
                    st.rerun()
    
    st.markdown("---")


def main():
    """Main application with multi-page navigation"""
    
    # Page configuration - NO SIDEBAR
    st.set_page_config(
        page_title="Image Enhancement Suite",
        page_icon="🖼️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Apply custom CSS
    apply_custom_css()
    
    # Add horizontal top navigation
    create_top_navigation()
    
    # Page content wrapper for smooth transitions
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    
    # Page routing
    if st.session_state.page == 'home':
        create_home_page()
        create_tech_section()
        create_settings_section()
    
    elif st.session_state.page == 'upload':
        create_upload_page()
    
    elif st.session_state.page == 'results':
        create_results_page()
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()

