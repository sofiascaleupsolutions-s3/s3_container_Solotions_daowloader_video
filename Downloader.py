# Downloader.py
import yt_dlp
import os


# Função para mapear as opções de resolução para o formato yt-dlp
def get_format_string(resolution):
    """Mapeia a resolução escolhida para a string de formato yt-dlp."""
    if resolution == "FullHD (1080p)":
        return 'bestvideo[height<=1080]+bestaudio/best'
    elif resolution == "HD (720p)":
        return 'bestvideo[height<=720]+bestaudio/best'
    elif resolution == "SD (480p)":
        return 'bestvideo[height<=480]+bestaudio/best'
    return 'bestvideo+bestaudio/best'


def download_video(url, resolution, codec, output_path="./temp_downloads"):
    format_string = get_format_string(resolution)

    # --- Mapeamento de Codec e Extensão ---
    ffmpeg_vcodec = ''
    if codec == "MP4 (H.264)":
        final_ext = 'mp4'
        ffmpeg_vcodec = 'libx264'
    elif codec == "MP4 (H.265/HEVC)":
        final_ext = 'mp4'
        ffmpeg_vcodec = 'libx265'
    elif codec == "MKV (H.264)":
        final_ext = 'mkv'
        ffmpeg_vcodec = 'libx264'
    else:
        final_ext = 'mp4'
        ffmpeg_vcodec = 'libx264'

    # --- Argumentos de FFmpeg para Codec e Escala ---
    # Estes argumentos são passados para o FFmpeg para re-codificação
    ffmpeg_args_list = [
        '-c:v', ffmpeg_vcodec,
        '-c:a', 'aac',
        '-crf', '23'  # Fator de qualidade
    ]

    # Adiciona o filtro de redimensionamento (upscale) se for 4K
    if resolution == "4K (2160p)":
        ffmpeg_args_list.extend([
            '-vf', 'scale=3840:2160:flags=lanczos',
        ])

    # --- Opções Base do yt-dlp ---
    ydl_opts = {
        'nocheckcertificate': True,
        'format': format_string,
        # CHAVE DA SOLUÇÃO: Definimos a extensão final aqui, forçando o FFmpeg a usar este container
        'outtmpl': os.path.join(output_path, f'%(title)s.%(resolution)s.{final_ext}'),
        'noplaylist': True,
        'quiet': True,
        # Usamos o merge_output_format para garantir que a junção inicial funcione
        'merge_output_format': final_ext,
        'postprocessors': [],

        # Passamos todos os argumentos de codec e filtro de escala aqui
        'postprocessor_args': ffmpeg_args_list
    }

    # --- Post-Processador de Conversão ---
    # Usamos o Convertor, mas sem argumentos extra, confiando que os postprocessor_args
    # farão a re-codificação e o merge_output_format/outtmpl definirão o container.
    ydl_opts['postprocessors'].append({
        'key': 'FFmpegVideoConvertor',
        'preferedformat': final_ext,
    })

    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)

            # Lógica para obter o caminho final (ajustada para a nova outtmpl)
            if '_filename' in info_dict:
                # O nome do ficheiro agora segue o padrão: TÍTULO.RESOLUÇÃO.EXTENSAO
                temp_filename_base = ydl.prepare_filename(info_dict).rsplit('.', 1)[0]
                final_filepath = f"{temp_filename_base}.{final_ext}"
            else:
                video_title = info_dict.get('title', 'video')
                final_filepath = os.path.join(output_path, f"{video_title}.{final_ext}")

            return final_filepath

    except Exception as e:
        # Levanta uma exceção mais limpa para ser capturada no my_app.py
        raise Exception(f"Erro durante a operação do yt-dlp/FFmpeg: {e}")