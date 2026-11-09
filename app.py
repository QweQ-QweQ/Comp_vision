import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="VisionLab AI - Image Processing Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Tampilan Tema Gelap (Dark Mode) & Aksen Warna RGB
st.markdown(
    """
<style>
    /* Latar Belakang Utama Gelap */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Judul Bergradasi RGB */
    h1 {
        background: linear-gradient(90deg, #ff4b4b, #00e676, #29b6f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0px;
    }
    
    /* Sidebar Gelap */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Kartu Informasi Bergaya RGB */
    .rgb-card-red {
        border-left: 5px solid #ff4b4b;
        background-color: #1f1f2e;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    .rgb-card-green {
        border-left: 5px solid #00e676;
        background-color: #1f1f2e;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    .rgb-card-blue {
        border-left: 5px solid #29b6f6;
        background-color: #1f1f2e;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 3. Header Utama Aplikasi
st.title("👁️ VisionLab AI Studio")
st.write(
    "Aplikasi Pembelajaran Computer Vision: Pemrosesan Citra & Ekstraksi Fitur Warna (RGB)."
)
st.markdown("---")

# 4. Sidebar Navigasi Sederhana & Rapi untuk Pemula
st.sidebar.title("🎛️ Menu Laboratorium")
menu_opsi = st.sidebar.radio(
    "Pilih Modul Pembelajaran:",
    [
        "🏠 Panduan Pemula",
        "🎨 Ekstraksi Fitur Warna (Pertemuan 6)",
        "⚡ Edge Detection Studio (Sobel/Canny)",
        "⚙️ Pra-pemrosesan & Segmentasi (Otsu)",
    ],
)

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader(
    "📂 Unggah Gambar Uji (.jpg / .png):", type=["jpg", "png", "jpeg"]
)

img_array = None
if uploaded_file is not None:
    image_input = Image.open(uploaded_file)
    img_array = np.array(image_input)

# -----------------------------------------------------------------------------
# MODUL 1: PANDUAN PEMULA
# -----------------------------------------------------------------------------
if menu_opsi == "🏠 Panduan Pemula":
    st.subheader("📌 Panduan Penggunaan Aplikasi")
    st.markdown(
        """
    Selamat datang di **VisionLab AI Studio**! Aplikasi ini telah disederhanakan agar mudah dipahami:
    
    1. **Unggah Citra:** Klik tombol **Browse files** di sidebar kiri untuk mengunggah gambar.
    2. **Pilih Modul:**
       * 🎨 **Ekstraksi Fitur Warna:** Menghitung statistik *Mean* dan *Std Dev* pada kanal Red, Green, Blue.
       * ⚡ **Edge Detection Studio:** Menguji garis tepi objek (Sobel, Canny, Prewitt, Roberts, Laplacian)[cite: 1, 2].
       * ⚙️ **Pra-pemrosesan & Segmentasi:** Mengonversi gambar ke abu-abu (*grayscale*) dan *Otsu Binarization*[cite: 1].
    """
    )
    if img_array is not None:
        st.image(
            image_input, caption="Gambar yang Diunggah", use_container_width=True
        )

# -----------------------------------------------------------------------------
# MODUL 2: EKSTRAKSI FITUR WARNA (INTEGRASI TUGAS PERTEMUAN 6)
# -----------------------------------------------------------------------------
elif menu_opsi == "🎨 Ekstraksi Fitur Warna (Pertemuan 6)":
    st.subheader("🎨 Ekstraksi Fitur Statistik Warna (RGB)")
    st.write(
        "Menghitung nilai statistik rata-rata (*Mean*) dan sebaran warna (*Standard Deviation*)[cite: 1]."
    )

    if img_array is None:
        st.warning(
            "Silakan unggah gambar di menu Sidebar sebelah kiri terlebih dahulu!"
        )
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.image(
                image_input, caption="Gambar Asli", use_container_width=True
            )

        if len(img_array.shape) == 2 or img_array.shape[2] == 1:
            st.error(
                "Gambar ini berbentuk Grayscale. Harap unggah gambar berwarna (RGB)!"
            )
        else:
            R = img_array[:, :, 0]
            G = img_array[:, :, 1]
            B = img_array[:, :, 2]

            mean_R, std_R = np.mean(R), np.std(R)
            mean_G, std_G = np.mean(G), np.std(G)
            mean_B, std_B = np.mean(B), np.std(B)

            with col2:
                st.markdown(
                    f'<div class="rgb-card-red">🔴 <b>Kanal Merah (Red):</b><br>Mean: <b>{mean_R:.2f}</b> | Std Dev: <b>{std_R:.2f}</b></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="rgb-card-green">🟢 <b>Kanal Hijau (Green):</b><br>Mean: <b>{mean_G:.2f}</b> | Std Dev: <b>{std_G:.2f}</b></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="rgb-card-blue">🔵 <b>Kanal Biru (Blue):</b><br>Mean: <b>{mean_B:.2f}</b> | Std Dev: <b>{std_B:.2f}</b></div>',
                    unsafe_allow_html=True,
                )

            st.markdown("---")
            st.subheader("📊 Visualisasi Grafik Dominansi Warna (RGB)")
            fig, ax = plt.subplots(figsize=(7, 3))
            fig.patch.set_facecolor("#161b22")
            ax.set_facecolor("#0e1117")

            bars = ax.bar(
                ["Red (Merah)", "Green (Hijau)", "Blue (Biru)"],
                [mean_R, mean_G, mean_B],
                color=["#ff4b4b", "#00e676", "#29b6f6"],
            )
            ax.set_ylabel("Nilai Mean", color="white")
            ax.tick_params(colors="white")

            for bar in bars:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 2,
                    f"{bar.get_height():.2f}",
                    ha="center",
                    va="bottom",
                    color="white",
                )
            st.pyplot(fig)

# -----------------------------------------------------------------------------
# MODUL 3: EDGE DETECTION STUDIO
# -----------------------------------------------------------------------------
elif menu_opsi == "⚡ Edge Detection Studio (Sobel/Canny)":
    st.subheader("⚡ Deteksi Tepi Objek (Edge Detection)")
    if img_array is None:
        st.warning(
            "Silakan unggah gambar di menu Sidebar sebelah kiri terlebih dahulu!"
        )
    else:
        img_gray = (
            cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            if len(img_array.shape) == 3
            else img_array.copy()
        )
        operator = st.selectbox(
            "Pilih Operator Deteksi Tepi:",
            [
                "Canny Edge Detection",
                "Sobel Operator",
                "Prewitt Operator",
                "Roberts Operator",
                "Laplacian Operator",
            ],
        )

        hasil_deteksi = None

        if operator == "Canny Edge Detection":
            t_lower = st.slider("Threshold 1", 0, 255, 100)
            t_upper = st.slider("Threshold 2", 0, 255, 200)
            hasil_deteksi = cv2.Canny(img_gray, t_lower, t_upper)
        elif operator == "Sobel Operator":
            sobelx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
            hasil_deteksi = np.uint8(
                np.clip(cv2.magnitude(sobelx, sobely), 0, 255)
            )
        elif operator == "Prewitt Operator":
            kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
            kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
            hasil_deteksi = cv2.filter2D(img_gray, -1, kernelx) + cv2.filter2D(
                img_gray, -1, kernely
            )
        elif operator == "Roberts Operator":
            kernelx = np.array([[1, 0], [0, -1]])
            kernely = np.array([[0, 1], [-1, 0]])
            hasil_deteksi = cv2.filter2D(img_gray, -1, kernelx) + cv2.filter2D(
                img_gray, -1, kernely
            )
        elif operator == "Laplacian Operator":
            hasil_deteksi = np.uint8(
                np.absolute(cv2.Laplacian(img_gray, cv2.CV_64F))
            )

        col1, col2 = st.columns(2)
        with col1:
            st.image(
                img_gray,
                caption="Input Grayscale",
                use_container_width=True,
                channels="GRAY",
            )
        with col2:
            st.image(
                hasil_deteksi,
                caption=f"Hasil {operator}",
                use_container_width=True,
                channels="GRAY",
            )

# -----------------------------------------------------------------------------
# MODUL 4: PREPROCESSING & OTSU BINARIZATION
# -----------------------------------------------------------------------------
elif menu_opsi == "⚙️ Pra-pemrosesan & Segmentasi (Otsu)":
    st.subheader("⚙️ Segmentasi Citra (Otsu Binarization)")
    if img_array is None:
        st.warning(
            "Silakan unggah gambar di menu Sidebar sebelah kiri terlebih dahulu!"
        )
    else:
        img_gray = (
            cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            if len(img_array.shape) == 3
            else img_array.copy()
        )
        blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
        thresh_val, otsu_img = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        st.success(f"Nilai Ambang Otomatis Otsu: {thresh_val:.0f}")

        col1, col2 = st.columns(2)
        with col1:
            st.image(
                img_gray,
                caption="Input Grayscale",
                use_container_width=True,
                channels="GRAY",
            )
        with col2:
            st.image(
                otsu_img,
                caption="Hasil Otsu Binarization",
                use_container_width=True,
                channels="GRAY",
            )