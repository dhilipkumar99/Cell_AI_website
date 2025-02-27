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

# CSS for enhanced styling with increased spacing
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
        padding: 70px 20px;  /* Increased padding for more internal spacing */
        margin-bottom: 40px;  /* Added margin-bottom for spacing between sections */
    }
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    }
    .hero {
        text-align: center;
        color: white;
        padding: 120px 20px;  /* Increased padding for a taller hero section */
        background-size: cover;
        background-position: center;
    }
    .hero h1 {
        font-size: 3em;
    }
    .footer {
        background-color: #333;
        color: white;
        padding: 30px;
        text-align: center;
        margin-top: 50px;  /* Added margin-top for spacing above footer */
    }
    .spacer {
        height: 40px;  /* Custom spacer class for additional control */
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
        <a href="#support">Support</a>
        <a href="#how-it-works">How It Works</a>
        <a href="#about">About Us</a>
        <a href="#pricing">Pricing</a>
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
        padding: 120px 20px;
        background-image: url({hero_image_base64});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    <div class="hero">
        <h1>Welcome to CellAI</h1>
        <p>Empowering Biological Discovery with Automated ROI Selection</p>
        <p>CellAI harnesses the power of artificial intelligence to transform fluorescence microscopy analysis, delivering unparalleled speed, precision, and simplicity to researchers worldwide.</p>
        <button style="padding: 15px 30px; font-size: 18px; background-color: #ff6347; color: white; border: none; border-radius: 5px; cursor: pointer;">Get Started Today</button>
    </div>
    """,
    unsafe_allow_html=True,
)

# Spacer after Hero
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# Introductory Section
st.markdown(
    """
    <section class="section" style="background-color:#f7d9d9;">
        <div class="card">
            <h3>Revolutionizing Fluorescence Microscopy with CellAI</h3>
            <p>For researchers in biology and biomedical sciences, analyzing fluorescence microscopy images can be a daunting task. Hours spent manually annotating regions of interest (ROIs) in tools like ImageJ detract from the real work of scientific discovery. Enter CellAI—a game-changing solution that automates ROI selection with cutting-edge AI and machine learning technology.</p>
            <p>Our mission is simple: to save you time, improve your accuracy, and let you focus on what matters most—unlocking the secrets of cellular behavior. Whether you're studying protein localization, cell morphology, or dynamic processes in living cells, CellAI streamlines your workflow by identifying and mapping fluorescent regions of interest with unmatched efficiency. Say goodbye to tedious manual labeling and hello to a smarter, faster way to process your image datasets.</p>
            <p>Built by a team of experts in computer vision, machine learning, and biological research, CellAI integrates seamlessly with ImageJ, the gold standard in microscopy image analysis. Our service is tailored specifically for fluorescence microscopy data, ensuring that your unique research needs are met with precision and care.</p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# Spacer after Intro
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# Features Section
st.markdown("<a id='features'></a>", unsafe_allow_html=True)
st.markdown("### Why Choose CellAI? Discover the Benefits")

col1, col2 = st.columns([2, 3])
with col1:
    st.image("draganddrop.png", caption="Save Time with Automation", use_container_width=True)
    st.image("micro_man.png", caption="Increase Precision in Analysis", use_container_width=True)
with col2:
    st.markdown(
        """
        <div class="card">
            <h4>A Smarter Approach to Image Segmentation</h4>
            <p>Fluorescence microscopy generates vast amounts of data, and manually selecting regions of interest can take hours—or even days—depending on the complexity of your dataset. CellAI changes that by leveraging state-of-the-art computer vision algorithms to automate the process. Our AI-powered segmentation tool identifies fluorescent regions with pinpoint accuracy, drawing ROI polygons that are ready to use in ImageJ. This not only speeds up your workflow but also ensures consistency across your analyses, eliminating the variability that comes with human annotation.</p>
            <p>But CellAI is more than just a time-saver. Our models are trained on diverse fluorescence microscopy datasets, enabling them to detect subtle variations in intensity and structure that might be missed by the human eye. Whether you're working with fixed cells, live-cell imaging, or multi-channel fluorescence, CellAI delivers reliable, reproducible results that enhance the quality of your research.</p>
            <p>We’ve designed CellAI with accessibility in mind. You don’t need to be a computational expert to use it—just upload your images, and let our intuitive platform do the rest. From graduate students to seasoned principal investigators, CellAI empowers researchers at all levels to integrate advanced image analysis into their work without a steep learning curve.</p>
            <ul>
                <li><strong>Save Time:</strong> Process entire datasets in minutes, not hours, with automated ROI selection tailored for fluorescence microscopy.</li>
                <li><strong>Increase Precision:</strong> Achieve consistent, high-accuracy segmentation that captures even the finest details of your fluorescent images.</li>
                <li><strong>User-Friendly:</strong> Enjoy a seamless interface designed for biologists, not just coders, with no advanced technical skills required.</li>
                <li><strong>Scalable Solution:</strong> Handle small experiments or massive datasets with ease—CellAI grows with your research needs.</li>
                <li><strong>Seamless Integration:</strong> Export ROIs directly into ImageJ for further analysis, fitting perfectly into your existing workflow.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Spacer after Features
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# Expanded Testimonials/Support Section
st.markdown("<a id='support'></a>", unsafe_allow_html=True)
st.markdown("### Partner with CellAI: Set Up Your Lab Account")

user1_base64 = "data:image/jpeg;base64," + image_to_base64("user1.jpeg")
user2_base64 = "data:image/jpeg;base64," + image_to_base64("user2.jpeg")

st.markdown(
    f"""
    <section class="section">
        <div class="card">
            <h3>Collaborate with Us for Cutting-Edge Research</h3>
             <p>At CellAI, we aim to partner with any labs that are still using manual methods, saving their menbers precious time and brainpower by giving them access to our premium image segmentation service. Our subscription model is designed to meet the needs of modern research teams, offering unlimited data processing and rapid turnaround times. Whether you’re annotating a handful of images or thousands, CellAI scales effortlessly to support your work.</p>
            <p>Once your lab subscribes, your team can upload fluorescence microscopy datasets in bulk via our secure platform. Our AI processes the images in minutes, generating annotated ROIs that you can load directly into ImageJ for further analysis. It’s that simple—no data caps, no delays, just results. Plus, our dedicated support team is here to assist with onboarding, troubleshooting, and optimizing your workflow.</p>
            <p>Ready to bring CellAI to your lab? Contact our sales representative, Dhilip Raman, at <a href="mailto:cell.ai.solutions@gmail.com">cell.ai.solutions@gmail.com</a> to discuss pricing, set up a demo, or ask any questions about how we can support your research goals.</p>
            <h2 style="margin-bottom: 20px;">Meet Our Team</h2>
            <div style="display: flex; justify-content: space-around;">
                <div style="text-align: center;">
                    <img src="{user1_base64}" style="width: 120px; height: 150px; border-radius: 50%; object-fit: cover; margin-bottom: 15px;">
                    <p><em>“I’m passionate about connecting researchers with tools that accelerate their discoveries.”</em></p>
                    <p>- Dhilip Raman, Sales Representative</p>
                </div>
                <div style="text-align: center;">
                    <img src="{user2_base64}" style="width: 120px; height: 150px; border-radius: 50%; object-fit: cover; margin-bottom: 15px;">
                    <p><em>“Building technology that empowers science is what drives me every day.”</em></p>
                    <p>- Avneesh Mehta, Principal Engineer</p>
                </div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# Spacer after Support
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# How It Works Section
st.markdown("<a id='how-it-works'></a>", unsafe_allow_html=True)
st.markdown("### How CellAI Works: From Upload to Analysis")

st.markdown(
    """
    <section class="section" style="background-color:#e3f2fd;">
        <div class="card">
            <h4>A Streamlined Process for Busy Researchers</h4>
            <p>CellAI takes the complexity out of fluorescence microscopy analysis, delivering a straightforward, three-step process that gets you from raw images to actionable results in no time. Here’s how it works:</p>
            <div style="display: flex; justify-content: space-between;">
                <div style="width: 30%;">
                    <h4>Step 1: Upload Your Dataset</h4>
                    <p>Gather your fluorescence microscopy images—whether they’re single files or an entire experiment’s worth—and package them into a .zip file. Upload them securely through our platform with just a few clicks. We support a wide range of file formats commonly used in microscopy, ensuring compatibility with your existing data.</p>
                </div>
                <div style="width: 30%;">
                    <h4>Step 2: Automated Segmentation</h4>
                    <p>Once uploaded, CellAI’s advanced algorithms spring into action. Our AI identifies fluorescent regions of interest based on intensity, shape, and context, then maps them with precision. Using cutting-edge segmentation techniques, it draws ROI polygons around each object of interest, ready for use in downstream analysis.</p>
                </div>
                <div style="width: 30%;">
                    <h4>Step 3: Download and Analyze</h4>
                    <p>Within minutes, you’ll receive a downloadable .zip file containing your annotated ROIs. Simply import them into ImageJ to continue your analysis—whether that’s quantifying fluorescence intensity, tracking cellular dynamics, or preparing publication-quality figures. It’s fast, easy, and reliable.</p>
                </div>
            </div>
            <p style="margin-top: 20px;">Our platform is designed to handle datasets of any size, from small pilot studies to large-scale screens. And because we know every experiment is unique, CellAI offers customizable settings to fine-tune segmentation parameters, giving you control over the results without sacrificing simplicity.</p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# Spacer after How It Works
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# About Us Section
st.markdown("<a id='about'></a>", unsafe_allow_html=True)
st.markdown("### About CellAI: Our Mission and Vision")

st.markdown(
    """
    <section class="section" style="background-color:#f7d9d9;">
        <div class="card">
            <h3>Driven by Science, Powered by Innovation</h3>
            <p>CellAI was born out of a shared frustration among researchers: the time and effort spent on manual image analysis was holding back scientific progress. Our founders, a team of biologists, computer scientists, and engineers, set out to create a tool that would bridge the gap between cutting-edge AI technology and the practical needs of the lab bench.</p>
            <p>Today, CellAI is a leader in automated image segmentation for fluorescence microscopy, serving a growing community of researchers across academia and industry. Our mission is to accelerate scientific discovery by providing tools that are not only powerful but also intuitive and accessible. We believe that every hour saved on data processing is an hour gained for hypothesis testing, collaboration, and breakthroughs.</p>
            <p>Looking ahead, we’re committed to expanding CellAI’s capabilities—adding support for new imaging modalities, enhancing our AI models with community feedback, and fostering partnerships with research institutions worldwide. Our vision is a future where image analysis is no longer a bottleneck, but a catalyst for discovery.</p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# Spacer after About Us
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# Pricing Section
st.markdown("<a id='pricing'></a>", unsafe_allow_html=True)
st.markdown("### Pricing Plans: Flexible Options for Every Lab")

st.markdown(
    """
    <section class="section" style="background-color:#e3f2fd;">
        <div class="card">
            <h3>Affordable Access to Premium Segmentation</h3>
            <p>We offer a range of subscription plans to suit labs of all sizes and budgets. Each plan includes unlimited data processing, priority support, and regular updates to our AI models. Contact us at <a href="mailto:cell.ai.solutions@gmail.com">cell.ai.solutions@gmail.com</a> for detailed pricing and to request a quote tailored to your team.</p>
            <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                <div style="width: 30%; text-align: center;">
                    <h4>Starter Plan</h4>
                    <p>Perfect for small labs or individual researchers. Includes core segmentation features and email support.</p>
                    <p><strong>Starting at $99/month</strong></p>
                </div>
                <div style="width: 30%; text-align: center;">
                    <h4>Professional Plan</h4>
                    <p>Ideal for mid-sized labs with multiple users. Adds priority processing and customizable settings.</p>
                    <p><strong>Starting at $299/month</strong></p>
                </div>
                <div style="width: 30%; text-align: center;">
                    <h4>Enterprise Plan</h4>
                    <p>Designed for large institutions and companies. Offers dedicated support, API access, and advanced analytics.</p>
                    <p><strong>Contact us for pricing</strong></p>
                </div>
            </div>
            <p style="margin-top: 20px;">Not sure which plan is right for you? Schedule a free consultation with our team to discuss your needs and explore how CellAI can fit into your budget and workflow.</p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# Spacer before Footer
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# Footer Section
st.markdown("<a id='contact'></a>", unsafe_allow_html=True)
st.markdown(
    """
    <footer class="footer">
        <p>CellAI is committed to accelerating scientific discovery through innovation.</p>
        <p>For support, inquiries, or partnership opportunities, reach out at <a href="mailto:cell.ai.solutions@gmail.com" style="color: lightblue;">cell.ai.solutions@gmail.com</a>.</p>
        <p>Stay connected with us on <a href="#" style="color: lightblue;">Twitter</a>, <a href="#" style="color: lightblue;">LinkedIn</a>, and <a href="#" style="color: lightblue;">GitHub</a> for updates, tips, and community resources.</p>
        <p>© 2025 CellAI Solutions. All rights reserved.</p>
    </footer>
    """,
    unsafe_allow_html=True,
)
