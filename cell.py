import streamlit as st
from PIL import Image
import zipfile
import os
import base64

# Set up page config
st.set_page_config(page_title="CellAI - Automated ROI Selection", layout="wide", page_icon="🤖")

# Convert an image file to a base64 string
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# CSS for enhanced styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
    }
    .navbar {
        position: sticky;
        top: 0;
        z-index: 1000;
        background-color: #333;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        color: white;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        margin: 0 10px;
    }
    .navbar a:hover {
        text-decoration: underline;
    }
    .section {
        padding: 50px 20px;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    }
    .hero {
        text-align: center;
        color: white;
        padding: 100px 20px;
        background-image: url('hero_image.jpg');
        background-size: cover;
        background-position: center;
    }
    .hero h1 {
        font-size: 3em;
    }
    .footer {
        background-color: #333;
        color: white;
        padding: 20px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation Bar
st.markdown(
    """
    <div class="navbar">
        <a href="#">Home</a>
        <a href="#features">Features</a>
        <a href="#testimonials">Testimonials</a>
        <a href="#how-it-works">How It Works</a>
        <a href="#faq">FAQ</a>
        <a href="#contact">Contact</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Convert the hero image to base64
hero_image_base64 = "data:image/jpeg;base64," + image_to_base64("hero_image.jpg")

# Hero Section with embedded image
st.markdown(
    f"""
    <style>
    .hero {{
        text-align: center;
        color: white;
        padding: 100px 20px;
        background-image: url({hero_image_base64});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    <div class="hero">
        <h1>Welcome to CellAI</h1>
        <p>Accelerating scientific discovery with automated ROI selection</p>
        <button style="padding: 15px 30px; font-size: 18px; background-color: #ff6347; color: white; border: none; border-radius: 5px; cursor: pointer;">Get Started</button>
    </div>
    """,
    unsafe_allow_html=True,
)


# Introductory Section
st.markdown(
    """
    <section class="section" style="background-color:#f7d9d9;">
        <div class="card">
            <h3>CellAI revolutionizes the way scientists analyze image datasets.</h3>
            <p>Are you spending hours manually labeling fluorescence microscopy images? Let CellAI revolutionize your workflow. 
            By leveraging cutting-edge computer vision, our AI-driven segmentation model, CellAI, automates Region of Interest (ROI) selection in ImageJ, 
            significantly reducing the time and effort required for manual labeling. CellAI empowers researchers to focus on their 
            discoveries rather than labor-intensive tasks.</p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# Features Section
st.markdown("<a id='features'></a>", unsafe_allow_html=True)
st.markdown("### Why Choose CellAI?")

col1, col2 = st.columns([2, 3])
with col1:
    st.image("draganddrop.png", caption="Save Time", use_container_width=True)
    st.image("micro_man.png", caption="Increase Precision", use_container_width=True)
with col2:
    st.markdown(
        """
        <div class="card">
        <ul>
            <p>Automated segmentation for Region of Interest (ROI) selection in ImageJ significantly enhances the efficiency and accuracy of 
            fluorescent microscopy analysis. Traditional manual ROI selection is time-consuming and prone to variability, especially when dealing with large datasets. 
            By leveraging advanced computer vision techniques, our AI-driven segmentation service eliminates the need for labor-intensive labeling, allowing 
            researchers to focus on data interpretation rather than tedious annotation tasks. This automation ensures consistency in image processing, 
            reducing human error and enhancing reproducibility across experiments, which is crucial for high-quality research outcomes.<p>
            <p>Beyond efficiency, automated segmentation improves precision in identifying and classifying cellular structures. Our AI models are trained to detect 
            subtle fluorescence variations, distinguishing between relevant biological features with high accuracy. This not only benefits researchers studying 
            complex cellular dynamics but also aids in standardizing image analysis workflows across labs. The intuitive interface allows users of all experience 
            levels to easily integrate this technology into their research pipeline, making cutting-edge image analysis accessible without requiring extensive 
            computational expertise.<p>
            <li><strong>Save Time:</strong> Upload your datasets and let CellAI handle the ROI selection in minutes.</li>
            <li><strong>Increase Precision:</strong> Benefit from consistent and accurate image segmentation.</li>
            <li><strong>User-Friendly:</strong> Our intuitive interface is designed for researchers of all experience levels.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Testimonials Section
st.markdown("<a id='testimonials'></a>", unsafe_allow_html=True)
st.markdown("### What Our Users Say")

user1_base64 = "data:image/jpeg;base64," + image_to_base64("user1.jpeg")
user2_base64 = "data:image/jpeg;base64," + image_to_base64("user2.jpeg")

st.markdown(
    f"""
    <section class="section">
        <div class="card">
            <div style="display: flex; justify-content: space-around;">
                <div style="text-align: center;">
                    <img src="{user1_base64}" style="width: 120px; height: 150px; border-radius: 50%; object-fit: cover; margin-bottom: 15px;">
                    <p><em>"CellAI saved us weeks of manual work!"</em></p>
                    <p>- Deevya Shalini, Wake Forrest University</p>
                </div>
                <div style="text-align: center;">
                    <img src="{user2_base64}" style="width: 120px; height: 150px; border-radius: 50%; object-fit: cover; margin-bottom: 15px;">
                    <p><em>"Highly recommend for any lab working with image datasets."</em></p>
                    <p>- Dr. Spencer Gang, UC San Diego</p>
                </div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# How It Works Section
st.markdown("<a id='how-it-works'></a>", unsafe_allow_html=True)
st.markdown("### How It Works")

st.markdown(
    """
    <section class="section" style="background-color:#e3f2fd;">
        <div class="card">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <h4>Step 1</h4>
                    <p>Upload your image datasets in a .zip file.</p>
                </div>
                <div>
                    <h4>Step 2</h4>
                    <p>CellAI processes your images using cutting-edge segmentation algorithms.</p>
                </div>
                <div>
                    <h4>Step 3</h4>
                    <p>Download the output .zip file containing annotated ROIs for all objects of interest. It's that simple!</p>
                </div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# Footer Section
st.markdown("<a id='contact'></a>", unsafe_allow_html=True)
st.markdown(
    """
    <footer class="footer">
        <p>CellAI is committed to accelerating scientific discovery through innovation.</p>
        <p>For support or inquiries, contact us at <a href="mailto:cell.ai.solutions@gmail.com" style="color: lightblue;">cell.ai.solutions@gmail.com</a>.</p>
        <p>Follow us on <a href="#" style="color: lightblue;">Twitter</a>, <a href="#" style="color: lightblue;">LinkedIn</a>, and <a href="#" style="color: lightblue;">GitHub</a>.</p>
    </footer>
    """,
    unsafe_allow_html=True,
)
