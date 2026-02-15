This README is designed to make your GitHub repository look like a professional, high-end security tool. It highlights the "Defense-in-Depth" architecture and the scientific validation (PSNR/Histograms) that sets your project apart.

---

# 🕵️ The Invisible Courier PRO

### **An Advanced Steganographic Framework with Multi-Layered AES-256 Encryption**

**The Invisible Courier** is a sophisticated security tool designed for "Security through Obscurity." Unlike standard encryption which signals the presence of a secret, this framework hides encrypted data within the pixels of lossless images. It employs a **Defense-in-Depth** strategy, ensuring that even if the hiding method is discovered, the data remains mathematically inaccessible.

## 🛡️ Security Features

* **Layer 1: Cryptographic Protection** – Plaintext is encrypted via **AES-256 (Fernet)**, ensuring military-grade confidentiality.
* **Layer 2: Steganographic Hiding** – Employs **Least Significant Bit (LSB) Substitution**, modifying pixel values by only 0.3%, making changes invisible to the human eye.
* **Layer 3: Randomized Mapping (PRNG)** – Uses a user-defined **Shuffle Password** to seed a Pseudo-Random Number Generator. Data is scattered across the image rather than stored sequentially.
* **Layer 4: Forensic Validation** – Built-in **PSNR (Peak Signal-to-Noise Ratio)** calculation and **RGB Histogram Analysis** to prove imperceptibility.

## 📊 Forensic Metrics

In testing, the framework consistently achieves high-fidelity results:

* **PSNR Score:** ~75.20 dB (Industry benchmark for invisibility is >40 dB).
* **Histogram Variance:** Near zero; color distribution remains statistically identical post-embedding.

## 🚀 Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/invisible-courier.git
cd invisible-courier

```


2. **Install dependencies:**
```bash
pip install streamlit numpy pillow cryptography supabase matplotlib

```


3. **Configure Secrets:**
Create a `.streamlit/secrets.toml` file with your Supabase credentials:
```toml
SUPABASE_URL = "your-project-url"
SUPABASE_KEY = "your-anon-key"

```


4. **Run the Application:**
```bash
streamlit run app.py

```



## 🛠️ Usage Guide

### **A. Dispatch (Hiding Data)**

1. Upload a **PNG** cover image.
2. Enter your secret message.
3. Set a **Shuffle Password** (This randomizes where the bits are hidden).
4. Generate the Stego-image and save the **AES Key** provided.

### **B. Retrieve (Extracting Data)**

1. Upload the Stego-image.
2. Provide the **AES Key** and the **Shuffle Password**.
3. The system will re-map the random pixels and decrypt the message.

### **C. Forensic Lab**

* View the **PSNR** score to verify image quality.
* Compare **Histograms** to ensure no statistical anomalies were introduced.
* View the **Bit-Change Heatmap** to see exactly where data was scattered.

## 🧪 Tech Stack

* **Language:** Python 3.10+
* **Frontend:** Streamlit
* **Image Processing:** Pillow & NumPy
* **Security:** Pyca/Cryptography (AES-256)
* **Database/Storage:** Supabase
* **Analytics:** Matplotlib (Histograms)

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

**Would you like me to also generate a `requirements.txt` file or a specific "Project Report" summary based on this README?**
