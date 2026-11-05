import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

# 1. Judul Aplikasi
st.title("🎨 Aplikasi Ekstraksi Fitur Warna Citra")
st.write(
    "Aplikasi sederhana untuk mengekstrak fitur statistik warna (RGB) dari sebuah gambar."
)

# 2. Upload Gambar
uploaded_file = st.file_uploader(
    "Pilih atau Unggah Gambar (.jpg / .png):", type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:
    # Membaca gambar yang diunggah
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # Tampilkan Gambar Asli
    st.subheader("1. Gambar Asli")
    st.image(image, caption="Gambar yang Diunggah", use_container_width=True)

    # Mencegah error jika gambar hitam-putih
    if len(img_array.shape) == 2:
        st.warning(
            "Gambar ini adalah gambar Grayscale (Hitam-Putih). Harap unggah gambar berwarna (RGB)."
        )
    else:
        # Memisahkan Kanal Warna R, G, B
        R = img_array[:, :, 0]
        G = img_array[:, :, 1]
        B = img_array[:, :, 2]

        # 3. Menghitung Fitur Statistik Warna
        mean_R, std_R = np.mean(R), np.std(R)
        mean_G, std_G = np.mean(G), np.std(G)
        mean_B, std_B = np.mean(B), np.std(B)

        # 4. Menampilkan Tabel Hasil
        st.subheader("2. Hasil Ekstraksi Fitur Warna")

        data_fitur = {
            "Kanal Warna": ["Red (Merah)", "Green (Hijau)", "Blue (Biru)"],
            "Mean (Rata-rata)": [
                f"{mean_R:.2f}",
                f"{mean_G:.2f}",
                f"{mean_B:.2f}",
            ],
            "Std Deviasi (Sebaran Warna)": [
                f"{std_R:.2f}",
                f"{std_G:.2f}",
                f"{std_B:.2f}",
            ],
        }

        df_fitur = pd.DataFrame(data_fitur)
        st.dataframe(df_fitur, use_container_width=True)

        # 5. Grafik Batang Berwarna (Red, Green, Blue)
        st.subheader("3. Grafik Perbandingan Mean Warna")

        # Data untuk grafik
        kanal = ["Red (Merah)", "Green (Hijau)", "Blue (Biru)"]
        nilai_mean = [mean_R, mean_G, mean_B]
        warna_bar = ["red", "green", "blue"]  # Pewarnaan khusus tiap batang

        # Membuat grafik menggunakan Matplotlib
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(kanal, nilai_mean, color=warna_bar)

        # Mengatur tampilan grafik agar cocok dengan tema gelap/terang Streamlit
        ax.set_ylabel("Nilai Mean", fontsize=10)
        ax.set_title("Rata-rata Intensitas Warna", fontsize=12)

        # Menambahkan angka nilai mean di atas tiap batang
        for bar in bars:
            yval = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                yval + 1,
                f"{yval:.2f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

        # Tampilkan grafik Matplotlib di Streamlit
        st.pyplot(fig)