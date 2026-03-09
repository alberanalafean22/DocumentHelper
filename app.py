import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
import PyPDF2
# Import library lain sesuai kebutuhan (pdf2docx, pdfplumber, pytesseract, dll)

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="DocumentHelper Pro", page_icon="📄", layout="wide")

# --- CSS KUSTOM UNTUK TAMPILAN PROFESIONAL ---
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        color: #1E3A8A;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #1E40AF;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="main-title">DocumentHelper</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Solusi Terpadu Manajemen & Konversi Dokumen Anda</p>', unsafe_allow_html=True)

# --- SIDEBAR MENU ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2911/2911230.png", width=50) # Placeholder logo
    st.title("Menu Navigasi")
    menu = st.radio(
        "Pilih Layanan:",
        ("Merge Dokumen", "PDF ↔ DOCX", "PDF ↔ Excel/CSV", "Compress Dokumen", "PDF ↔ JPG", "OCR PDF")
    )

st.divider()

# --- LOGIKA MENU ---

if menu == "Merge Dokumen":
    st.header("🗂️ Merge Dokumen (Menjadi PDF)")
    st.info("Upload beberapa file PDF untuk digabungkan menjadi satu.")
    
    uploaded_files = st.file_uploader("Upload File PDF", type=['pdf'], accept_multiple_files=True)
    
    if st.button("Gabungkan Dokumen"):
        if uploaded_files and len(uploaded_files) > 1:
            merger = PyPDF2.PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
            
            output = BytesIO()
            merger.write(output)
            st.success("Dokumen berhasil digabungkan!")
            st.download_button(label="📥 Download PDF Gabungan", data=output.getvalue(), file_name="Merged_Document.pdf", mime="application/pdf")
        else:
            st.warning("Mohon upload setidaknya 2 file PDF.")

elif menu == "PDF ↔ DOCX":
    st.header("📝 Konversi PDF & Word")
    mode = st.selectbox("Pilih Mode Konversi", ["PDF ke DOCX", "DOCX ke PDF"])
    
    if mode == "PDF ke DOCX":
        uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
        if uploaded_file and st.button("Konversi ke DOCX"):
            st.info("Logika konversi menggunakan library `pdf2docx` akan berjalan di sini.")
            # Contoh logika (butuh penyesuaian untuk file object Streamlit)
            # from pdf2docx import Converter
            # cv = Converter(pdf_file)
            # cv.convert(docx_file, start=0, None)
            # cv.close()

elif menu == "PDF ↔ Excel/CSV":
    st.header("📊 Ekstraksi Tabel PDF ke Excel")
    uploaded_file = st.file_uploader("Upload PDF berisi Tabel", type=['pdf'])
    
    if uploaded_file and st.button("Ekstrak ke Excel"):
        st.info("Logika konversi menggunakan `pdfplumber` atau `camelot-py` akan berjalan di sini untuk mengekstrak struktur tabel.")

elif menu == "Compress Dokumen":
    st.header("🗜️ Kompresi PDF (Kualitas HD)")
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
    
    if uploaded_file and st.button("Kompres PDF"):
        reader = PyPDF2.PdfReader(uploaded_file)
        writer = PyPDF2.PdfWriter()
        
        for page in reader.pages:
            page.compress_content_streams() # Basic compression
            writer.add_page(page)
            
        output = BytesIO()
        writer.write(output)
        
        st.success("Kompresi selesai!")
        st.download_button("📥 Download PDF Terkompresi", data=output.getvalue(), file_name="Compressed.pdf", mime="application/pdf")

elif menu == "PDF ↔ JPG":
    st.header("🖼️ Konversi PDF & Gambar")
    mode = st.selectbox("Mode", ["PDF ke JPG", "JPG ke PDF"])
    
    if mode == "JPG ke PDF":
        uploaded_images = st.file_uploader("Upload Gambar JPG/PNG", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
        if uploaded_images and st.button("Konversi ke PDF"):
            images = [Image.open(img).convert('RGB') for img in uploaded_images]
            pdf_bytes = BytesIO()
            images[0].save(pdf_bytes, format='PDF', save_all=True, append_images=images[1:])
            st.success("Berhasil diubah ke PDF!")
            st.download_button("📥 Download PDF", data=pdf_bytes.getvalue(), file_name="Images_to_PDF.pdf")

elif menu == "OCR PDF":
    st.header("🔍 Optical Character Recognition (OCR)")
    st.write("Ekstrak teks dari PDF hasil scan atau gambar.")
    uploaded_file = st.file_uploader("Upload Scan PDF/Gambar", type=['pdf', 'jpg', 'png'])
    
    if uploaded_file and st.button("Jalankan OCR"):
        st.info("Memproses OCR... (Pastikan Tesseract OCR sudah terinstal di sistem Anda).")
        # Logika: Konversi PDF ke Gambar menggunakan pdf2image
        # Lalu jalankan pytesseract.image_to_string() pada setiap gambar
        st.code("Teks hasil ekstraksi akan muncul di sini...")
