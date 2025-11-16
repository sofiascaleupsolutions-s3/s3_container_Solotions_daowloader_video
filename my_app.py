# my_app.py
import streamlit as st
import shutil
import time
import sys
import os

# --- CORREÇÃO DE IMPORTAÇÃO (SOLUÇÃO DEFINITIVA) ---
# Adiciona o diretório atual ao caminho de pesquisa de módulos do Python para encontrar Downloader.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
# --------------------------------------------------

# Importa o módulo Downloader
from Downloader import download_video

# --- Configuração da Página ---
st.title("SOFIA SACALEUP SOLUTIONS")
st.header("S3-DOWLOADER")

# --- Opções de Download ---
RESOLUTIONS = ["4K (2160p)", "FullHD (1080p)", "HD (720p)", "SD (480p)"]
CODECS = ["MP4 (H.264)", "MP4 (H.265/HEVC)", "MKV (H.264)"]

# --- Input do URL ---
url_input = st.text_input(
    "🔗 Cole o link do Vídeo (YouTube, Instagram, etc.)",
    key="url_input",
    placeholder="Ex: https://www.youtube.com/watch?v=..."
)

# --- Controles em Duas Colunas ---
col1, col2 = st.columns(2)

with col1:
    resolution_choice = st.selectbox(
        "📐 Escolha a Resolução",
        RESOLUTIONS,
        index=1,
        key="resolution_select"
    )

with col2:
    # --- CORREÇÃO APLICADA AQUI ---
    codec_choice = st.selectbox(
        "🖥️ Escolha o Codec de Saída",
        CODECS,
        index=0,
        key="codec_select"
    )

# --- Botão de Download ---
if st.button("⬇️ INICIAR DOWNLOAD", key="download_button", type="primary"):
    if not url_input:
        st.error("Por favor, insira um URL válido para iniciar o download.")
    else:
        try:
            # 1. Cria a pasta temporária
            temp_dir = os.path.join(BASE_DIR, "temp_downloads")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            with st.spinner(f"A processar e converter para {resolution_choice} e {codec_choice}... Pode demorar!"):

                # 2. Inicia o download
                final_file_path = download_video(
                    url=url_input,
                    resolution=resolution_choice,
                    codec=codec_choice,
                    output_path=temp_dir
                )

                if os.path.exists(final_file_path):
                    st.success(f"✅ Download e Conversão Concluídos! Ficheiro: {os.path.basename(final_file_path)}")

                    # 3. Botão para o Utilizador Baixar
                    with open(final_file_path, "rb") as file:
                        st.download_button(
                            label="📥 Clicar para Guardar o Ficheiro",
                            data=file,
                            file_name=os.path.basename(final_file_path),
                            mime="video/mp4" if 'mp4' in final_file_path else "video/x-matroska",
                            key="final_download_button"
                        )

                    # 4. Limpeza
                    time.sleep(2)
                    os.remove(final_file_path)
                    st.info("Ficheiro temporário limpo do servidor.")
                else:
                    st.error("Ocorreu um erro: O ficheiro final não foi encontrado.")

        except Exception as e:
            st.error(f"Ocorreu um erro crítico durante o processamento: {e}")
            st.warning("Verifique se o URL está correto e se o **FFmpeg** está instalado e acessível.")

# --- Caixa de Seleção para Tema (Informação) ---
st.sidebar.markdown("### Aparência do App")
st.sidebar.markdown(
    "O Streamlit permite que o utilizador escolha o **Tema Escuro** ou **Claro** no menu de **Settings** (⚙️ canto superior direito)."
)
st.title("Powered by Top Board Studio")
st.title("Created and developed by Jair Sousa")
