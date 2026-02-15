import streamlit as st
import numpy as np
from PIL import Image
from cryptography.fernet import Fernet
from supabase import create_client, Client
import io
import matplotlib.pyplot as plt
import math

# ==========================================
# 1. CORE LOGIC ENGINES (ADVANCED)
# ==========================================

def get_psnr(img1, img2):
    array1 = np.array(img1.convert('RGB')).astype(np.float64)
    array2 = np.array(img2.convert('RGB')).astype(np.float64)
    mse = np.mean((array1 - array2) ** 2)
    if mse == 0: return 100
    return 20 * math.log10(255.0 / math.sqrt(mse))

def msg_to_bin(msg):
    if isinstance(msg, str): return ''.join([format(ord(i), "08b") for i in msg])
    elif isinstance(msg, bytes): return ''.join([format(i, "08b") for i in msg])
    return ""

def embed_data(image, secret_msg, user_password):
    try:
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_msg = f.encrypt(secret_msg.encode())
        bin_msg = msg_to_bin(encrypted_msg) + '1111111111111110'
        
        img_array = np.array(image.convert('RGB'))
        shape = img_array.shape
        flat_img = img_array.flatten().astype(np.uint8)
        
        if len(bin_msg) > len(flat_img): return None, "Error: Payload exceeds capacity!"

        seed = sum([ord(c) for c in user_password])
        np.random.seed(seed)
        indices = np.arange(len(flat_img))
        np.random.shuffle(indices)

        for i in range(len(bin_msg)):
            idx = indices[i]
            flat_img[idx] = (int(flat_img[idx]) & 254) | int(bin_msg[i])
            
        return Image.fromarray(flat_img.reshape(shape).astype('uint8')), key.decode()
    except Exception as e: return None, str(e)

def extract_data(stego_image, secret_key, user_password):
    try:
        img_array = np.array(stego_image.convert('RGB'))
        flat_img = img_array.flatten()
        seed = sum([ord(c) for c in user_password])
        np.random.seed(seed)
        indices = np.arange(len(flat_img))
        np.random.shuffle(indices)
        
        binary_data = ""
        for i in range(len(flat_img)):
            idx = indices[i]
            binary_data += str(flat_img[idx] & 1)
            if binary_data.endswith('1111111111111110'): break
            
        binary_data = binary_data[:-16]
        all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
        decoded_data = bytes([int(byte, 2) for byte in all_bytes])
        return Fernet(secret_key.encode()).decrypt(decoded_data).decode()
    except Exception: return "Error: Decryption failed. Invalid keys."

def get_histogram(image, title):
    img_array = np.array(image)
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('none') # Transparent background for Light/Dark mode
    for i, col in enumerate(('red', 'green', 'blue')):
        hist, bin_edges = np.histogram(img_array[:, :, i], bins=256, range=(0, 255))
        ax.plot(bin_edges[0:-1], hist, color=col, label=col.capitalize())
    ax.set_title(title, color='grey')
    return fig

# ==========================================
# 2. UI/UX ENHANCEMENTS & CONFIG
# ==========================================

st.set_page_config(page_title="Invisible Courier PRO", layout="wide", page_icon="🕵️")

# Custom CSS for UI/UX
st.markdown("""
    <style>
    .main { background-color: transparent; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    .stTextInput>div>div>input { border-radius: 5px; }
    .css-1kyx603 { border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# State Management
if 'stego_img' not in st.session_state: st.session_state.stego_img = None
if 'cover_img' not in st.session_state: st.session_state.cover_img = None

# Sidebar Content
with st.sidebar:
    st.title("🛠️ Control Panel")
    st.info("System automatically switches between Light/Dark mode based on your device settings.")
    if st.session_state.cover_img:
        st.subheader("Image Stats")
        w, h = st.session_state.cover_img.size
        st.write(f"Dimensions: {w}x{h}")
        st.write(f"Total Pixels: {w*h:,}")

# ==========================================
# 3. MAIN DASHBOARD
# ==========================================

st.title("🕵️ The Invisible Courier PRO")
st.caption("Military-Grade Steganography Dashboard")

t1, t2, t3 = st.tabs(["📤 Secure Dispatch", "📥 Secure Retrieve", "📊 Forensic Lab"])

with t1:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("### 1. Prepare Payload")
        file = st.file_uploader("Upload Cover Image", type=['png'], help="Use PNG to avoid lossy compression.")
        if file:
            st.session_state.cover_img = Image.open(file)
            cap = (st.session_state.cover_img.size[0] * st.session_state.cover_img.size[1] * 3) // 8
            st.write(f"Capacity: `{cap:,}` chars")
            
        msg = st.text_area("Message to Hide", placeholder="Enter your secret data...")
        pwd = st.text_input("Shuffle Password", type="password", help="The secret seed for bit randomization.")

    with col2:
        st.markdown("### 2. Output")
        if st.button("🚀 Encrypt & Hide Data"):
            if file and msg and pwd:
                res, k = embed_data(st.session_state.cover_img, msg, pwd)
                if res:
                    st.session_state.stego_img = res
                    st.image(res, caption="Generated Stego-Image")
                    
                    buf = io.BytesIO()
                    res.save(buf, format="PNG")
                    st.download_button("💾 Download Protected Image", buf.getvalue(), "stego_secure.png", "image/png")
                    st.text_input("YOUR AES KEY (COPY THIS):", value=k, key="k_disp")
                else: st.error(res)
            else: st.error("Please fill all fields.")

with t2:
    st.markdown("### 📥 Extract Secret Data")
    c_ret1, c_ret2 = st.columns(2)
    with c_ret1:
        s_file = st.file_uploader("Upload Stego-Image", type=['png'], key="ext_u")
        s_key = st.text_input("AES Secret Key", type="password")
        s_pwd = st.text_input("Shuffle Password", type="password", key="ext_p")
    
    with c_ret2:
        if st.button("🔍 Extract & Decrypt"):
            if s_file and s_key and s_pwd:
                result = extract_data(Image.open(s_file), s_key, s_pwd)
                if "Error" in result: st.error(result)
                else: 
                    st.success("Message Successfully Decrypted!")
                    st.code(result)

with t3:
    st.markdown("### 📊 Forensic Integrity Lab")
    if st.session_state.cover_img and st.session_state.stego_img:
        psnr = get_psnr(st.session_state.cover_img, st.session_state.stego_img)
        st.metric("PSNR Fidelity Score", f"{psnr:.2f} dB", delta="Optimal: >40dB")
        
        col_hist_a, col_hist_b = st.columns(2)
        col_hist_a.pyplot(get_histogram(st.session_state.cover_img, "Cover Histogram"))
        col_hist_b.pyplot(get_histogram(st.session_state.stego_img, "Stego Histogram"))
        
        # Difference visualization
        st.markdown("### Bit-Change Heatmap")
        arr_c = np.array(st.session_state.cover_img.convert('RGB')).astype(float)
        arr_s = np.array(st.session_state.stego_img.convert('RGB')).astype(float)
        st.image(np.abs(arr_c - arr_s) * 255, caption="Visualization of hidden bit distribution.", clamp=True)
    else:
        st.info("Awaiting data... Use the Dispatch tab to generate forensic metrics.")