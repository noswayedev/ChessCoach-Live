# Chess Coach Live — Windows

Desktop chess training and analysis utility, with an experimental screen-recognition feature and Stockfish engine bundled for convenience. **Only use computer-assisted recommendations where permitted** (e.g. post-game study and appropriate bot practice). Using engine assistance in prohibited online play can result in account penalties.

## Download an EXE without compiling locally (GitHub Actions)

1. Create a GitHub repository, then upload **the contents of this folder**, including `.github`, `stockfish/stockfish-engine.zip` and `stockfish/source/` (keep their directory structure).
2. Open the repository → **Actions** → **Build Windows EXE** → **Run workflow** → choose `main` → **Run workflow**.
3. Once the run is successful, click it and find the artifact **ChessCoachLive-Windows-x64** under **Artifacts**.
4. Download the artifact ZIP; extract it to get **ChessCoachLive.exe**. No local build is necessary.

GitHub Actions availability and usage limits depend on repository visibility and your GitHub plan. This package contains **source files, not a prebuilt EXE**. Build success and Windows GUI behavior have not been tested in this environment. Windows/antivirus warnings are possible for unsigned executables.

### Repository notes

- `stockfish/stockfish-engine.zip` contains the Windows Stockfish executable compressed to stay below GitHub's 100 MB *per-file* web upload limit; the build action extracts it automatically.
- `stockfish/source/` and `stockfish/COPYING.txt` contain the bundled engine's upstream source and GPLv3 license notices. Preserve these when distributing.
- Keep `.github/workflows/build-windows.yml` (the `.github` folder can be hidden on Windows).
- Before publishing an open-source release, decide on a license for the Chess Coach Live application's own code, and check the GPLv3 obligations associated with distributing Stockfish.


## Additional details

# Chess Coach Live v1.6.1 — Stockfish included

**No manual Stockfish download or selection is required.** The repository stores a compressed copy of the supplied universal Windows engine, extracted by the build workflow.

## Build a single Windows EXE

1. Install Python for Windows with the `py` launcher (only needed for building).
2. Run `BUILD_EXE.bat` on Windows. It extracts the compressed engine, installs Python dependencies and runs PyInstaller.
3. Distribute `dist\ChessCoachLive.exe`. **Stockfish is embedded inside this single EXE**, along with the application icon. The user does not need to install Python or Stockfish.
4. The application opens without a CMD console. Stockfish runs with `CREATE_NO_WINDOW`.

This Windows executable has **not** been compiled or tested in this Linux environment. Test on a clean Windows machine before releasing to GitHub. On first start, extraction of the ~103 MB engine may take a moment; antivirus software may also scan the package.

## Run from Python source

Install dependencies (`INSTALLER.bat`) and launch `ChessCoachLive.pyw` to run without a CMD console. First extract `stockfish/stockfish-engine.zip` to `stockfish/` so that `stockfish/stockfish.exe` exists. The engine is then detected automatically. A custom Stockfish path can still be set in Settings. If a saved custom path no longer exists, the program falls back to the bundled engine.

## Languages

The welcome wizard is in English, with ten languages: Français, English, Español, Italiano, Deutsch, Português, Русский, 中文, 日本語, 한국어. Language selection is saved locally.

## Open-source license information

**Stockfish is GPLv3 software.** See `stockfish/COPYING.txt` and `stockfish/STOCKFISH_README.md`. The engine and its corresponding supplied upstream source files are under `stockfish/source/` (including its original Makefile, source headers and licensing documents). See `stockfish/SOURCE_NOTICE.md`. The separate chess application may have additional obligations if publicly distributed; choose a compatible license and retain the original author and license notices. This project is not affiliated with the Stockfish developers or Chess.com.

## Fair use

Intended for study, review of completed games, bot practice, and contexts where computer assistance is explicitly allowed. Do not use for unauthorized assistance in competitive online chess.

## Account suspension / ban disclaimer

**Use at your own risk.** Chess Coach Live is intended only for training and situations where engine assistance is permitted. Online chess platforms may suspend or ban accounts for prohibited engine assistance. The developer does not accept responsibility for account warnings, suspensions, or bans resulting from misuse of the software. This notice does not override applicable law or platform rules.
