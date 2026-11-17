<div align="center">

# ♞ Chess Coach Live

**Chess analysis and training for Windows, powered by Stockfish.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) ![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white) ![Engine](https://img.shields.io/badge/Engine-Stockfish-3A8F56) ![Languages](https://img.shields.io/badge/Languages-10-blueviolet)

**Français · English · Español · Italiano · Deutsch · Português · Русский · 中文 · 日本語 · 한국어**

</div>

---

## 🇫🇷 Français

### Présentation

**Chess Coach Live** est une application Windows d'entraînement et d'analyse aux échecs. Elle combine le moteur **Stockfish**, un échiquier interactif et une reconnaissance visuelle expérimentale des positions affichées à l'écran.

### Fonctionnalités

- ♟️ Analyse des positions avec Stockfish et affichage d'**un seul coup recommandé**.
- 👁️ Reconnaissance visuelle expérimentale des déplacements et suivi de l'échiquier.
- 🖥️ Interface sombre avec indication visuelle du déplacement proposé.
- ⚙️ Réglages de la langue, du temps d'analyse et de l'intervalle de détection.
- 🌍 **10 langues**, sélectionnables dès le premier lancement.
- 📦 Construction d'un **EXE Windows** via GitHub Actions, sans compilation locale.
- 🧠 **Stockfish inclus** dans les ressources de compilation ; pas de téléchargement séparé pour les utilisateurs de l'EXE.

### Télécharger l'application

1. Ouvrez l'onglet **Actions** du dépôt GitHub.
2. Sélectionnez **Build Windows EXE**, puis **Run workflow** (si l'exécution manuelle est activée).
3. Une fois la compilation terminée, téléchargez l'artifact **ChessCoachLive-Windows-x64**.
4. Décompressez l'archive et lancez `ChessCoachLive.exe`.

> **Remarque :** le dépôt contient le code source et les ressources de compilation. La disponibilité de l'EXE dépend de la réussite du workflow Windows. La reconnaissance à l'écran reste expérimentale et peut manquer certains coups.

### Compiler sur son PC

Sur Windows, lancez `BUILD_EXE.bat` avec Python installé. Le résultat est créé dans `dist/`. Les utilisateurs de l'EXE compilé n'ont pas besoin d'installer Python ou Stockfish séparément.

### Utilisation responsable

L'application est destinée à l'entraînement, à l'analyse de parties terminées et aux contextes où l'aide d'un moteur est **explicitement autorisée**. Une assistance non autorisée pendant une partie en ligne peut entraîner la suspension ou le bannissement d'un compte.

**Avertissement :** utilisation à vos risques et périls. Le développeur décline toute responsabilité pour les avertissements, suspensions ou bannissements liés à une utilisation contraire aux règles des plateformes, dans les limites prévues par la loi.

### Licence et crédits

Chess Coach Live utilise **Stockfish**, distribué sous **GPLv3**. Retrouvez les notices, la licence et les sources correspondantes dans `stockfish/`. La licence propre au code de Chess Coach Live doit être indiquée séparément avant une publication sous licence open source. Projet indépendant, non affilié à Chess.com ni à l'équipe Stockfish.

---

<details>
<summary>🇬🇧 <strong>English</strong></summary>

### About

**Chess Coach Live** is a Windows chess training and analysis app powered by **Stockfish**, with an interactive board and experimental on-screen position recognition.

### Features

- ♟️ Stockfish analysis displaying **one recommended move**.
- 👁️ Experimental board tracking and move detection.
- 🖥️ Dark interface with a visual move indicator.
- ⚙️ Settings for language, analysis time, and detection interval.
- 🌍 Ten interface languages with first-launch selection.
- 📦 Windows EXE builds through GitHub Actions.
- 🧠 Stockfish bundled in the build resources.

### Download & build

Go to **Actions → Build Windows EXE → Run workflow**. When the workflow succeeds, download the **ChessCoachLive-Windows-x64** artifact, extract it, and run `ChessCoachLive.exe`. Alternatively, on Windows run `BUILD_EXE.bat` with Python installed. Screen recognition is experimental and may miss moves.

### Fair play & disclaimer

For training, completed-game analysis, bot practice where permitted, and other situations **explicitly allowing engine assistance**. Unauthorized assistance in online games can lead to account penalties. **Use at your own risk.** The developer disclaims responsibility for account warnings, suspensions, or bans resulting from rule-breaking use, to the extent allowed by law.

### Licenses

Stockfish is licensed under **GPLv3**; see `stockfish/` for notices and corresponding source. The application code requires its own clearly specified license before open-source distribution. Not affiliated with Chess.com or the Stockfish team.

</details>

<details>
<summary>🇪🇸 <strong>Español</strong></summary>

### Descripción

**Chess Coach Live** es una aplicación de entrenamiento y análisis de ajedrez para Windows, impulsada por **Stockfish**, con tablero interactivo y reconocimiento visual experimental.

### Funciones

- ♟️ Análisis con Stockfish que muestra **una sola jugada recomendada**.
- 👁️ Seguimiento experimental del tablero y detección de movimientos.
- 🖥️ Interfaz oscura con indicación visual de las jugadas.
- ⚙️ Ajustes de idioma, tiempo de análisis e intervalo de detección.
- 🌍 Diez idiomas y elección durante el primer inicio.
- 📦 Compilación del EXE de Windows mediante GitHub Actions, con Stockfish incluido.

### Descarga

Abre **Actions → Build Windows EXE → Run workflow**. Cuando termine correctamente, descarga el artefacto **ChessCoachLive-Windows-x64**, extráelo y ejecuta `ChessCoachLive.exe`. También puedes compilar con `BUILD_EXE.bat` en Windows. El reconocimiento visual puede fallar en algunos movimientos.

### Uso responsable y licencias

Solo para entrenamiento, análisis de partidas terminadas o contextos donde la ayuda de un motor esté permitida. El uso no autorizado puede ocasionar sanciones o bloqueos de cuentas. **Uso bajo tu propia responsabilidad**; el desarrollador no se responsabiliza de sanciones derivadas de infringir las normas, dentro de los límites legales. Stockfish se distribuye bajo **GPLv3**; consulta `stockfish/`. Proyecto no afiliado a Chess.com ni a Stockfish.

</details>

<details>
<summary>🇮🇹 <strong>Italiano</strong></summary>

### Descrizione

**Chess Coach Live** è un'app Windows per allenamento e analisi degli scacchi, basata su **Stockfish**, con scacchiera interattiva e riconoscimento visivo sperimentale.

### Funzionalità

- ♟️ Analisi Stockfish con **una sola mossa consigliata**.
- 👁️ Rilevamento sperimentale delle mosse sullo schermo.
- 🖥️ Interfaccia scura e indicazione visiva della mossa.
- ⚙️ Impostazioni per lingua, tempo di analisi e intervallo di rilevamento.
- 🌍 Dieci lingue con scelta al primo avvio.
- 📦 Compilazione EXE Windows tramite GitHub Actions con Stockfish incluso.

### Download

Vai su **Actions → Build Windows EXE → Run workflow**. Al termine, scarica l'artifact **ChessCoachLive-Windows-x64**, estrailo ed esegui `ChessCoachLive.exe`. In alternativa, compila su Windows usando `BUILD_EXE.bat`. Il rilevamento visivo è sperimentale e può perdere alcune mosse.

### Uso corretto e licenze

Usa il programma solo per allenamento, analisi di partite concluse o contesti in cui l'assistenza del motore è consentita. Un uso non autorizzato può causare sospensioni o ban. **Uso a proprio rischio**; lo sviluppatore non è responsabile delle sanzioni derivanti dalla violazione delle regole, nei limiti di legge. Stockfish è distribuito con licenza **GPLv3**; vedi `stockfish/`. Progetto non affiliato a Chess.com o Stockfish.

</details>

<details>
<summary>🇩🇪 <strong>Deutsch</strong></summary>

### Über das Projekt

**Chess Coach Live** ist eine Windows-Anwendung für Schachtraining und -analyse mit **Stockfish**, interaktivem Brett und experimenteller Bildschirmerkennung.

### Funktionen

- ♟️ Stockfish-Analyse mit **genau einem empfohlenen Zug**.
- 👁️ Experimentelle Zugerkennung und Brettverfolgung.
- 🖥️ Dunkle Oberfläche mit visueller Zuganzeige.
- ⚙️ Einstellungen für Sprache, Analysezeit und Erkennungsintervall.
- 🌍 Zehn Sprachen, auswählbar beim ersten Start.
- 📦 Windows-EXE-Erstellung über GitHub Actions, Stockfish enthalten.

### Download

Unter **Actions → Build Windows EXE → Run workflow** den Build starten. Nach erfolgreichem Abschluss **ChessCoachLive-Windows-x64** herunterladen, entpacken und `ChessCoachLive.exe` starten. Alternativ unter Windows `BUILD_EXE.bat` verwenden. Die Bilderkennung ist experimentell und erkennt nicht jeden Zug zuverlässig.

### Fair Play und Lizenzen

Nur für Training, Analyse abgeschlossener Partien und Situationen, in denen Engine-Hilfe ausdrücklich erlaubt ist. Unerlaubte Nutzung kann zu Kontosperren führen. **Nutzung auf eigene Gefahr**; der Entwickler übernimmt im gesetzlich zulässigen Umfang keine Verantwortung für Sanktionen wegen Regelverstößen. Stockfish steht unter **GPLv3**; siehe `stockfish/`. Keine Verbindung zu Chess.com oder dem Stockfish-Team.

</details>

<details>
<summary>🇵🇹 <strong>Português</strong></summary>

### Sobre

**Chess Coach Live** é uma aplicação Windows para treino e análise de xadrez, com **Stockfish**, tabuleiro interativo e reconhecimento visual experimental.

### Funcionalidades

- ♟️ Análise com Stockfish mostrando **apenas uma jogada recomendada**.
- 👁️ Deteção experimental de jogadas e acompanhamento do tabuleiro.
- 🖥️ Interface escura e indicação visual de movimentos.
- ⚙️ Definições de idioma, tempo de análise e intervalo de deteção.
- 🌍 Dez idiomas, escolhidos no primeiro início.
- 📦 Compilação do EXE Windows via GitHub Actions, com Stockfish incluído.

### Transferir

Acede a **Actions → Build Windows EXE → Run workflow**. Após uma compilação bem-sucedida, transfere **ChessCoachLive-Windows-x64**, extrai e executa `ChessCoachLive.exe`. Também podes compilar em Windows com `BUILD_EXE.bat`. O reconhecimento visual é experimental e pode falhar algumas jogadas.

### Utilização responsável e licenças

Apenas para treino, análise de partidas terminadas ou situações em que a assistência de um motor é permitida. A utilização não autorizada pode levar à suspensão ou bloqueio da conta. **Utiliza por tua conta e risco**; o programador não assume responsabilidade por penalizações decorrentes da violação das regras, nos limites legais. Stockfish usa a licença **GPLv3**; consulta `stockfish/`. Sem afiliação à Chess.com ou à equipa Stockfish.

</details>

<details>
<summary>🇷🇺 <strong>Русский</strong></summary>

### О проекте

**Chess Coach Live** — приложение для Windows для обучения и анализа шахмат с движком **Stockfish**, интерактивной доской и экспериментальным распознаванием позиции на экране.

### Возможности

- ♟️ Анализ Stockfish с отображением **только одного рекомендуемого хода**.
- 👁️ Экспериментальное отслеживание доски и распознавание ходов.
- 🖥️ Тёмный интерфейс с визуальной подсветкой хода.
- ⚙️ Настройки языка, времени анализа и интервала распознавания.
- 🌍 Десять языков с выбором при первом запуске.
- 📦 Сборка Windows EXE через GitHub Actions; Stockfish включён.

### Загрузка

Откройте **Actions → Build Windows EXE → Run workflow**. После успешной сборки загрузите артефакт **ChessCoachLive-Windows-x64**, распакуйте его и запустите `ChessCoachLive.exe`. Для локальной сборки в Windows используйте `BUILD_EXE.bat`. Распознавание ходов экспериментальное и может допускать ошибки.

### Честная игра и лицензии

Используйте программу только для обучения, анализа завершённых партий и там, где помощь движка явно разрешена. Запрещённая помощь может привести к блокировке аккаунта. **Используйте на свой риск**; разработчик не несёт ответственности за санкции из-за нарушения правил в пределах, допускаемых законом. Stockfish распространяется по лицензии **GPLv3**; см. `stockfish/`. Проект не связан с Chess.com или командой Stockfish.

</details>

<details>
<summary>🇨🇳 <strong>中文</strong></summary>

### 项目简介

**Chess Coach Live** 是一款适用于 Windows 的国际象棋训练与分析工具，使用 **Stockfish** 引擎，提供交互式棋盘及实验性的屏幕棋局识别功能。

### 主要功能

- ♟️ Stockfish 分析，**仅显示一个推荐走法**。
- 👁️ 实验性的棋盘跟踪与走棋识别。
- 🖥️ 深色界面与走棋高亮提示。
- ⚙️ 可设置语言、分析时间和识别间隔。
- 🌍 支持十种语言，首次启动时可选择。
- 📦 通过 GitHub Actions 构建 Windows EXE，并集成 Stockfish。

### 下载方式

打开 **Actions → Build Windows EXE → Run workflow**。构建成功后下载 **ChessCoachLive-Windows-x64**，解压并运行 `ChessCoachLive.exe`。也可在 Windows 上使用 `BUILD_EXE.bat` 自行构建。屏幕识别仍处于实验阶段，可能漏掉部分走法。

### 公平使用与许可

仅限训练、已结束对局的复盘以及明确允许引擎辅助的场景。未经许可在在线对局中使用可能导致账号受到处罚或封禁。**请自行承担使用风险**；在法律允许范围内，开发者不对违反平台规则而造成的处罚负责。Stockfish 使用 **GPLv3** 许可，详见 `stockfish/`。本项目与 Chess.com 和 Stockfish 团队无关联。

</details>

<details>
<summary>🇯🇵 <strong>日本語</strong></summary>

### 概要

**Chess Coach Live** は、**Stockfish** を使用した Windows 向けのチェストレーニング・解析アプリです。操作できる盤面と、画面上の局面を認識する実験的な機能を備えています。

### 主な機能

- ♟️ Stockfish による解析と、**最善候補を1手だけ表示**する機能。
- 👁️ 実験的な盤面追跡・指し手検出。
- 🖥️ 指し手を視覚的に示すダークテーマ。
- ⚙️ 言語、解析時間、検出間隔の設定。
- 🌍 初回起動時に選択できる10言語。
- 📦 GitHub Actions による Windows EXE ビルド（Stockfish 同梱）。

### ダウンロード

**Actions → Build Windows EXE → Run workflow** を実行します。成功後、**ChessCoachLive-Windows-x64** をダウンロードして展開し、`ChessCoachLive.exe` を起動してください。Windows で `BUILD_EXE.bat` を使ったビルドも可能です。画面認識は実験段階のため、指し手を見逃すことがあります。

### フェアプレーとライセンス

学習、終了した対局の解析、エンジン支援が明示的に許可された場面でのみ使用してください。禁止された支援はアカウント停止の対象となる場合があります。**利用は自己責任**です。法令で認められる範囲で、規約違反による処分について開発者は責任を負いません。Stockfish は **GPLv3** ライセンスです。詳細は `stockfish/` を参照してください。Chess.com および Stockfish チームとは無関係です。

</details>

<details>
<summary>🇰🇷 <strong>한국어</strong></summary>

### 소개

**Chess Coach Live**는 **Stockfish** 엔진을 기반으로 한 Windows용 체스 훈련 및 분석 프로그램입니다. 대화형 체스판과 실험적인 화면 인식 기능을 제공합니다.

### 주요 기능

- ♟️ Stockfish 분석으로 **추천 수 한 개만 표시**.
- 👁️ 실험적인 체스판 추적 및 수 감지.
- 🖥️ 추천 수를 시각적으로 표시하는 다크 인터페이스.
- ⚙️ 언어, 분석 시간 및 감지 간격 설정.
- 🌍 첫 실행 시 선택할 수 있는 10개 언어.
- 📦 GitHub Actions를 통한 Windows EXE 빌드 및 Stockfish 포함.

### 다운로드

**Actions → Build Windows EXE → Run workflow**를 실행하세요. 빌드가 성공하면 **ChessCoachLive-Windows-x64** 아티팩트를 다운로드하고 압축을 풀어 `ChessCoachLive.exe`를 실행하세요. Windows에서 `BUILD_EXE.bat`로 직접 빌드할 수도 있습니다. 화면 인식은 실험적 기능으로 일부 수를 놓칠 수 있습니다.

### 공정한 이용 및 라이선스

훈련, 종료된 경기 분석, 엔진 보조가 명시적으로 허용된 환경에서만 사용하세요. 허용되지 않은 보조는 계정 정지나 차단으로 이어질 수 있습니다. **사용에 따른 위험은 본인이 부담합니다.** 법률이 허용하는 범위에서 개발자는 규칙 위반으로 인한 제재에 책임지지 않습니다. Stockfish는 **GPLv3** 라이선스를 사용하며 자세한 내용은 `stockfish/`를 참고하세요. 이 프로젝트는 Chess.com 또는 Stockfish 팀과 관련이 없습니다.

</details>

---

<div align="center">

**Made for chess learning and analysis · Play fair ♟️**

</div>
