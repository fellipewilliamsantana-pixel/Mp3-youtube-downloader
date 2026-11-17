@echo off
echo Atualizando/Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install yt-dlp

echo Iniciando o aplicativo...
python app.py
pause