@echo off
setlocal
cd /d "%~dp0"
title Chess Coach Live - Build Windows EXE
where py >nul 2>nul
if errorlevel 1 (echo Python with py launcher is required. & pause & exit /b 1)
if not exist "stockfish\stockfish.exe" (
  if not exist "stockfish\stockfish-engine.zip" (echo Missing stockfish engine archive. & pause & exit /b 1)
  echo Extracting bundled Stockfish...
  py -c "import zipfile;zipfile.ZipFile('stockfish/stockfish-engine.zip').extractall('stockfish')"
  if errorlevel 1 goto fail
)
py -m pip install -r requirements.txt "pyinstaller>=6,<7"
if errorlevel 1 goto fail
py -m PyInstaller --noconfirm --clean --onefile --windowed --name ChessCoachLive --icon "assets\ChessCoachLive.ico" --add-data "assets\ChessCoachLive.ico;assets" --add-binary "stockfish\stockfish.exe;stockfish" chess_coach_live.py
if errorlevel 1 goto fail
echo Built dist\ChessCoachLive.exe
pause
exit /b 0
:fail
echo Build failed.
pause
exit /b 1
