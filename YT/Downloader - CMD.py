import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp


class YouTubeDownloaderApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Baixador do YouTube (MP3 & MP4 / Playlist)")
    self.root.geometry("600x420")
    self.root.resizable(False, False)

    # Estilo visual
    style = ttk.Style()
    style.theme_use("clam")

    # URL
    ttk.Label(
        root,
        text="Cole o Link do YouTube (Vídeo ou Playlist):",
        font=("Arial", 10, "bold"),
    ).pack(anchor="w", padx=20, pady=(20, 5))
    self.url_entry = ttk.Entry(root, width=70)
    self.url_entry.pack(padx=20, pady=5)

    # Formato
    ttk.Label(
        root, text="Escolha o Formato:", font=("Arial", 10, "bold")
    ).pack(anchor="w", padx=20, pady=(15, 5))
    self.format_var = tk.StringVar(value="mp3")

    frame_radio = ttk.Frame(root)
    frame_radio.pack(anchor="w", padx=20, pady=5)
    ttk.Radiobutton(
        frame_radio, text="Áudio (MP3)", variable=self.format_var, value="mp3"
    ).pack(side="left", padx=(0, 20))
    ttk.Radiobutton(
        frame_radio, text="Vídeo (MP4)", variable=self.format_var, value="mp4"
    ).pack(side="left")

    # Botão de Download
    self.download_btn = ttk.Button(
        root, text="Baixar Agora", command=self.iniciar_thread_download
    )
    self.download_btn.pack(padx=20, pady=(25, 10), ipadx=10, ipady=5)

    # Status
    self.status_label = ttk.Label(
        root, text="Status: Aguardando link...", font=("Arial", 9)
    )
    self.status_label.pack(anchor="w", padx=20, pady=(10, 5))

    self.progress_bar = ttk.Progressbar(
        root, orient="horizontal", length=560, mode="indeterminate"
    )
    self.progress_bar.pack(padx=20, pady=5)

  def iniciar_thread_download(self):
    url = self.url_entry.get().strip()
    if not url:
      messagebox.showerror("Erro", "Por favor, insira um link válido!")
      return

    self.download_btn.config(state="disabled")
    self.progress_bar.start(10)
    self.status_label.config(
        text="Status: Baixando... (Isso pode levar alguns minutos)"
    )

    threading.Thread(
        target=self.executar_download, args=(url,), daemon=True
    ).start()

  def executar_download(self, url):
    pasta_destino = os.path.join(
        os.path.expanduser("~"), "Downloads", "YouTubeDownloads"
    )
    os.makedirs(pasta_destino, exist_ok=True)
    formato = self.format_var.get()

    ydl_opts = {
        "outtmpl": os.path.join(pasta_destino, "%(title)s.%(ext)s"),
        "ignoreerrors": True,  # Pula vídeos privados/indisponíveis em playlists
    }

    if formato == "mp3":
      ydl_opts.update({
          "format": "bestaudio/best",
          "postprocessors": [{
              "key": "FFmpegExtractAudio",
              "preferredcodec": "mp3",
              "preferredquality": "192",
          }],
      })
    else:
      ydl_opts.update({
          "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
      })

    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
      self.root.after(
          0,
          lambda: self.download_concluido(
              True, f"Salvo com sucesso na pasta:\n{pasta_destino}"
          ),
      )
    except Exception as e:
      self.root.after(0, lambda: self.download_concluido(False, str(e)))

  def download_concluido(self, sucesso, mensagem):
    self.progress_bar.stop()
    self.download_btn.config(state="normal")
    if sucesso:
      self.status_label.config(text="Status: Download Concluído!")
      messagebox.showinfo("Sucesso", mensagem)
    else:
      self.status_label.config(text="Status: Erro no download.")
      messagebox.showerror("Erro", f"Ocorreu um erro:\n{mensagem}")


if __name__ == "__main__":
  root = tk.Tk()
  app = YouTubeDownloaderApp(root)
  root.mainloop()