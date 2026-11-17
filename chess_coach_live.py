import os
import subprocess
import sys
import time
import threading
import queue
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog

try:
    import chess
    import chess.engine
    import chess.pgn
    import numpy as np
    import cv2
    import mss
    from PIL import Image, ImageTk
except ImportError as e:
    root = tk.Tk(); root.withdraw()
    messagebox.showerror('Dépendance manquante', f'{e}\nLance INSTALLER.bat.')
    sys.exit(1)

BG = '#0B1020'
PANEL = '#151D30'
ACCENT = '#54D6AC'
APP_VERSION = '1.6.1'
NAMES = {1:'Pawn', 2:'Knight', 3:'Bishop', 4:'Rook', 5:'Queen', 6:'King'}
GLYPHS = dict(zip('PNBRQKpnbrqk', '♙♘♗♖♕♔♟♞♝♜♛♚'))

LANGUAGES = {'fr': 'Français', 'en': 'English', 'es': 'Español', 'it': 'Italiano', 'de': 'Deutsch', 'pt': 'Português', 'ru': 'Русский', 'zh': '中文', 'ja': '日本語', 'ko': '한국어'}
TRANSLATIONS = {
 'fr': {
  'disclaimer':'L\'utilisation relève de votre responsabilité. L\'éditeur n\'est pas responsable des suspensions ou bannissements de comptes.',
  'subtitle':'LIVE  /  STUDIO D’ANALYSE', 'local':'LOCAL  •  STOCKFISH', 'board':'ÉCHIQUIER',
  'settings':'⚙  Paramètres', 'board_help':'Clique sur l’échiquier pour corriger un coup mal reconnu.',
  'undo':'↶  Annuler', 'reset':'↻  Nouvelle partie', 'flip':'⇅  Inverser',
  'best_title':'01   /   COUP RECOMMANDÉ', 'config_title':'02   /   CONFIGURATION',
  'tools_title':'03   /   OUTILS D’ANALYSE', 'status_title':'04   /   ÉTAT DU SUIVI',
  'engine':'Moteur Stockfish', 'orientation':'Orientation', 'white_bottom':'Blancs en bas',
  'black_bottom':'Noirs en bas', 'calibrate':'⊞  Encadrer l’échiquier',
  'start':'▶  Démarrer le suivi', 'stop':'⏸  Arrêter le suivi',
  'fen':'Importer FEN', 'pgn':'Exporter PGN',
  'footer':'Entraînement et parties autorisant les moteurs uniquement.',
  'turn_white':'Trait : blancs', 'turn_black':'Trait : noirs', 'no_moves':'Aucun coup enregistré.',
  'from':'Départ', 'to':'Arrivée', 'evaluation':'ÉVALUATION BLANCS', 'mate':'Mat en',
  'analyzing':'Analyse…', 'end':'Fin de partie', 'waiting':'RECONNAISSANCE  •  en attente',
  'settings_title':'Paramètres', 'language':'Langue de l’interface',
  'analysis_time':'Durée d’analyse Stockfish', 'poll_time':'Intervalle de détection',
  'save':'Enregistrer', 'cancel':'Annuler', 'welcome':'Bienvenue sur Chess Coach Live',
  'choose_language':'Choisis ta langue pour commencer.', 'continue':'Continuer',
  'saved':'Paramètres enregistrés.', 'engine_missing':'Sélectionne stockfish.exe pour analyser.',
  'ready':'Sélectionne Stockfish, puis calibre l’échiquier à la position initiale.',
  'single_move':'Un seul meilleur coup est affiché pour la position reconnue.',
  'language_hint':'Tu peux modifier ce choix plus tard dans les paramètres.',
  'settings_restart':'Le nouveau réglage s’applique aux prochaines analyses.',
  'about':'Version {version} • Traitement local',
  'duration_unit':'secondes', 'interval_unit':'millisecondes',
  'pieces': ['Pion','Cavalier','Fou','Tour','Dame','Roi'],
 },
 'en': {
  'disclaimer':'Use at your own risk. The developer is not responsible for account suspensions or bans.',
  'subtitle':'LIVE  /  ANALYSIS STUDIO', 'local':'LOCAL  •  STOCKFISH', 'board':'CHESSBOARD',
  'settings':'⚙  Settings', 'board_help':'Click the board to correct an unrecognized move.',
  'undo':'↶  Undo', 'reset':'↻  New game', 'flip':'⇅  Flip',
  'best_title':'01   /   RECOMMENDED MOVE', 'config_title':'02   /   CONFIGURATION',
  'tools_title':'03   /   ANALYSIS TOOLS', 'status_title':'04   /   TRACKING STATUS',
  'engine':'Stockfish engine', 'orientation':'Orientation', 'white_bottom':'White at bottom',
  'black_bottom':'Black at bottom', 'calibrate':'⊞  Select board area',
  'start':'▶  Start tracking', 'stop':'⏸  Stop tracking',
  'fen':'Import FEN', 'pgn':'Export PGN',
  'footer':'Training and games allowing engine assistance only.',
  'turn_white':'White to move', 'turn_black':'Black to move', 'no_moves':'No moves recorded.',
  'from':'From', 'to':'To', 'evaluation':'WHITE EVALUATION', 'mate':'Mate in',
  'analyzing':'Analyzing…', 'end':'Game over', 'waiting':'RECOGNITION  •  waiting',
  'settings_title':'Settings', 'language':'Interface language',
  'analysis_time':'Stockfish analysis time', 'poll_time':'Detection interval',
  'save':'Save', 'cancel':'Cancel', 'welcome':'Welcome to Chess Coach Live',
  'choose_language':'Choose your language to get started.', 'continue':'Continue',
  'saved':'Settings saved.', 'engine_missing':'Select stockfish.exe to analyze.',
  'ready':'Select Stockfish, then calibrate the board from its starting position.',
  'single_move':'Only one best move is shown for the recognized position.',
  'language_hint':'You can change this later in Settings.',
  'settings_restart':'New settings apply to the next analysis.',
  'about':'Version {version} • Local processing',
  'duration_unit':'seconds', 'interval_unit':'milliseconds',
  'pieces': ['Pawn','Knight','Bishop','Rook','Queen','King'],
 },
 'es': {
  'disclaimer':'Úsalo bajo tu responsabilidad. El desarrollador no se responsabiliza de suspensiones ni bloqueos de cuentas.',
  'subtitle':'EN VIVO  /  ANÁLISIS', 'local':'LOCAL  •  STOCKFISH', 'board':'TABLERO',
  'settings':'⚙  Ajustes', 'board_help':'Haz clic en el tablero para corregir una jugada.',
  'undo':'↶  Deshacer', 'reset':'↻  Nueva partida', 'flip':'⇅  Girar',
  'best_title':'01   /   MEJOR JUGADA', 'config_title':'02   /   CONFIGURACIÓN',
  'tools_title':'03   /   HERRAMIENTAS', 'status_title':'04   /   ESTADO',
  'engine':'Motor Stockfish', 'orientation':'Orientación', 'white_bottom':'Blancas abajo',
  'black_bottom':'Negras abajo', 'calibrate':'⊞  Seleccionar tablero',
  'start':'▶  Iniciar seguimiento', 'stop':'⏸  Detener seguimiento',
  'fen':'Importar FEN', 'pgn':'Exportar PGN',
  'footer':'Solo entrenamiento y partidas que permiten asistencia.',
  'turn_white':'Juegan blancas', 'turn_black':'Juegan negras', 'no_moves':'Sin jugadas registradas.',
  'from':'Desde', 'to':'Hasta', 'evaluation':'EVALUACIÓN BLANCAS', 'mate':'Mate en',
  'analyzing':'Analizando…', 'end':'Partida terminada', 'waiting':'RECONOCIMIENTO  •  esperando',
  'settings_title':'Ajustes', 'language':'Idioma de la interfaz',
  'analysis_time':'Tiempo de análisis Stockfish', 'poll_time':'Intervalo de detección',
  'save':'Guardar', 'cancel':'Cancelar', 'welcome':'Bienvenido a Chess Coach Live',
  'choose_language':'Elige tu idioma para empezar.', 'continue':'Continuar',
  'saved':'Ajustes guardados.', 'engine_missing':'Selecciona stockfish.exe para analizar.',
  'ready':'Selecciona Stockfish y calibra el tablero inicial.',
  'single_move':'Solo se muestra una mejor jugada para la posición detectada.',
  'language_hint':'Puedes cambiarlo después en Ajustes.',
  'settings_restart':'Los cambios se aplican al próximo análisis.',
  'about':'Versión {version} • Procesamiento local',
  'duration_unit':'segundos', 'interval_unit':'milisegundos',
  'pieces': ['Peón','Caballo','Alfil','Torre','Dama','Rey'],
 }
}

# Additional interface languages (full translation of the main UI).
TRANSLATIONS.update({
 'it': {
  'disclaimer':'Usa il programma a tuo rischio. Lo sviluppatore non è responsabile di sospensioni o ban degli account.',
  'subtitle': 'LIVE / STUDIO DI ANALISI',
  'local': 'LOCALE • STOCKFISH',
  'board': 'SCACCHIERA',
  'settings': '⚙ Impostazioni',
  'board_help': 'Clicca sulla scacchiera per correggere una mossa non riconosciuta.',
  'undo': '↶ Annulla',
  'reset': '↻ Nuova partita',
  'flip': '⇅ Ruota',
  'best_title': '01 / MOSSA CONSIGLIATA',
  'config_title': '02 / CONFIGURAZIONE',
  'tools_title': '03 / STRUMENTI DI ANALISI',
  'status_title': '04 / STATO RILEVAMENTO',
  'engine': 'Motore Stockfish',
  'orientation': 'Orientamento',
  'white_bottom': 'Bianco in basso',
  'black_bottom': 'Nero in basso',
  'calibrate': '⊞ Seleziona scacchiera',
  'start': '▶ Avvia rilevamento',
  'stop': '⏸ Ferma rilevamento',
  'fen': 'Importa FEN',
  'pgn': 'Esporta PGN',
  'footer': 'Solo allenamento e partite che consentono assistenza esterna.',
  'turn_white': 'Muove il Bianco',
  'turn_black': 'Muove il Nero',
  'no_moves': 'Nessuna mossa registrata.',
  'from': 'Da',
  'to': 'A',
  'evaluation': 'VALUTAZIONE BIANCO',
  'mate': 'Matto in',
  'analyzing': 'Analisi…',
  'end': 'Partita terminata',
  'waiting': 'RICONOSCIMENTO • in attesa',
  'settings_title': 'Impostazioni',
  'language': 'Lingua dell’interfaccia',
  'analysis_time': 'Durata analisi Stockfish',
  'poll_time': 'Intervallo di rilevamento',
  'save': 'Salva',
  'cancel': 'Annulla',
  'welcome': 'Benvenuto in Chess Coach Live',
  'choose_language': 'Scegli la lingua per iniziare.',
  'continue': 'Continua',
  'saved': 'Impostazioni salvate.',
  'engine_missing': 'Seleziona stockfish.exe per analizzare.',
  'ready': 'Seleziona Stockfish e calibra la posizione iniziale.',
  'single_move': 'Viene mostrata una sola mossa migliore per la posizione riconosciuta.',
  'language_hint': 'Puoi cambiare lingua più tardi nelle Impostazioni.',
  'settings_restart': 'Le nuove impostazioni si applicano alla prossima analisi.',
  'about': 'Versione {version} • Elaborazione locale',
  'duration_unit': 'secondi',
  'interval_unit': 'millisecondi',
  'pieces': ['Pedone', 'Cavallo', 'Alfiere', 'Torre', 'Donna', 'Re'],
 },
 'de': {
  'disclaimer':'Nutzung auf eigene Verantwortung. Der Entwickler haftet nicht für Kontosperrungen oder Bans.',
  'subtitle': 'LIVE / ANALYSESTUDIO',
  'local': 'LOKAL • STOCKFISH',
  'board': 'SCHACHBRETT',
  'settings': '⚙ Einstellungen',
  'board_help': 'Klicke auf das Brett, um einen nicht erkannten Zug zu korrigieren.',
  'undo': '↶ Rückgängig',
  'reset': '↻ Neue Partie',
  'flip': '⇅ Drehen',
  'best_title': '01 / EMPFOHLENER ZUG',
  'config_title': '02 / KONFIGURATION',
  'tools_title': '03 / ANALYSEWERKZEUGE',
  'status_title': '04 / ERKENNUNGSSTATUS',
  'engine': 'Stockfish-Engine',
  'orientation': 'Ausrichtung',
  'white_bottom': 'Weiß unten',
  'black_bottom': 'Schwarz unten',
  'calibrate': '⊞ Brett auswählen',
  'start': '▶ Erkennung starten',
  'stop': '⏸ Erkennung stoppen',
  'fen': 'FEN importieren',
  'pgn': 'PGN exportieren',
  'footer': 'Nur für Training und Partien mit erlaubter Engine-Hilfe.',
  'turn_white': 'Weiß am Zug',
  'turn_black': 'Schwarz am Zug',
  'no_moves': 'Noch keine Züge.',
  'from': 'Von',
  'to': 'Nach',
  'evaluation': 'BEWERTUNG FÜR WEISS',
  'mate': 'Matt in',
  'analyzing': 'Analysiere…',
  'end': 'Partie beendet',
  'waiting': 'ERKENNUNG • wartet',
  'settings_title': 'Einstellungen',
  'language': 'Sprache der Oberfläche',
  'analysis_time': 'Stockfish-Analysezeit',
  'poll_time': 'Erkennungsintervall',
  'save': 'Speichern',
  'cancel': 'Abbrechen',
  'welcome': 'Willkommen bei Chess Coach Live',
  'choose_language': 'Wähle deine Sprache aus.',
  'continue': 'Weiter',
  'saved': 'Einstellungen gespeichert.',
  'engine_missing': 'Wähle stockfish.exe für die Analyse aus.',
  'ready': 'Wähle Stockfish aus und kalibriere die Startstellung.',
  'single_move': 'Für die erkannte Stellung wird nur ein bester Zug angezeigt.',
  'language_hint': 'Du kannst die Sprache später in den Einstellungen ändern.',
  'settings_restart': 'Neue Einstellungen gelten ab der nächsten Analyse.',
  'about': 'Version {version} • Lokale Verarbeitung',
  'duration_unit': 'Sekunden',
  'interval_unit': 'Millisekunden',
  'pieces': ['Bauer', 'Springer', 'Läufer', 'Turm', 'Dame', 'König'],
 },
 'pt': {
  'disclaimer':'Use por sua conta e risco. O desenvolvedor não se responsabiliza por suspensões ou banimentos de contas.',
  'subtitle': 'AO VIVO / ESTÚDIO DE ANÁLISE',
  'local': 'LOCAL • STOCKFISH',
  'board': 'TABULEIRO',
  'settings': '⚙ Definições',
  'board_help': 'Clica no tabuleiro para corrigir uma jogada não detetada.',
  'undo': '↶ Desfazer',
  'reset': '↻ Nova partida',
  'flip': '⇅ Rodar',
  'best_title': '01 / JOGADA RECOMENDADA',
  'config_title': '02 / CONFIGURAÇÃO',
  'tools_title': '03 / FERRAMENTAS DE ANÁLISE',
  'status_title': '04 / ESTADO DA DETEÇÃO',
  'engine': 'Motor Stockfish',
  'orientation': 'Orientação',
  'white_bottom': 'Brancas em baixo',
  'black_bottom': 'Pretas em baixo',
  'calibrate': '⊞ Selecionar tabuleiro',
  'start': '▶ Iniciar deteção',
  'stop': '⏸ Parar deteção',
  'fen': 'Importar FEN',
  'pgn': 'Exportar PGN',
  'footer': 'Apenas treino e partidas que permitam ajuda de motores.',
  'turn_white': 'Jogam as brancas',
  'turn_black': 'Jogam as pretas',
  'no_moves': 'Sem jogadas registadas.',
  'from': 'De',
  'to': 'Para',
  'evaluation': 'AVALIAÇÃO DAS BRANCAS',
  'mate': 'Mate em',
  'analyzing': 'A analisar…',
  'end': 'Partida terminada',
  'waiting': 'RECONHECIMENTO • à espera',
  'settings_title': 'Definições',
  'language': 'Idioma da interface',
  'analysis_time': 'Tempo de análise Stockfish',
  'poll_time': 'Intervalo de deteção',
  'save': 'Guardar',
  'cancel': 'Cancelar',
  'welcome': 'Bem-vindo ao Chess Coach Live',
  'choose_language': 'Escolhe o idioma para começar.',
  'continue': 'Continuar',
  'saved': 'Definições guardadas.',
  'engine_missing': 'Seleciona stockfish.exe para analisar.',
  'ready': 'Seleciona Stockfish e calibra a posição inicial.',
  'single_move': 'É mostrada apenas uma melhor jogada para a posição reconhecida.',
  'language_hint': 'Podes alterar o idioma mais tarde nas Definições.',
  'settings_restart': 'As novas definições aplicam-se à próxima análise.',
  'about': 'Versão {version} • Processamento local',
  'duration_unit': 'segundos',
  'interval_unit': 'milissegundos',
  'pieces': ['Peão', 'Cavalo', 'Bispo', 'Torre', 'Dama', 'Rei'],
 },
 'ru': {
  'disclaimer':'Используйте на свой риск. Разработчик не несёт ответственности за блокировки аккаунтов.',
  'subtitle': 'LIVE / СТУДИЯ АНАЛИЗА',
  'local': 'ЛОКАЛЬНО • STOCKFISH',
  'board': 'ШАХМАТНАЯ ДОСКА',
  'settings': '⚙ Настройки',
  'board_help': 'Нажмите на доску, чтобы исправить нераспознанный ход.',
  'undo': '↶ Отменить',
  'reset': '↻ Новая партия',
  'flip': '⇅ Повернуть',
  'best_title': '01 / РЕКОМЕНДУЕМЫЙ ХОД',
  'config_title': '02 / НАСТРОЙКИ',
  'tools_title': '03 / ИНСТРУМЕНТЫ АНАЛИЗА',
  'status_title': '04 / СОСТОЯНИЕ ОТСЛЕЖИВАНИЯ',
  'engine': 'Движок Stockfish',
  'orientation': 'Ориентация',
  'white_bottom': 'Белые снизу',
  'black_bottom': 'Чёрные снизу',
  'calibrate': '⊞ Выбрать область доски',
  'start': '▶ Начать отслеживание',
  'stop': '⏸ Остановить отслеживание',
  'fen': 'Импорт FEN',
  'pgn': 'Экспорт PGN',
  'footer': 'Только для обучения и партий, где разрешена помощь движка.',
  'turn_white': 'Ход белых',
  'turn_black': 'Ход чёрных',
  'no_moves': 'Ходов пока нет.',
  'from': 'Откуда',
  'to': 'Куда',
  'evaluation': 'ОЦЕНКА ЗА БЕЛЫХ',
  'mate': 'Мат через',
  'analyzing': 'Анализ…',
  'end': 'Партия окончена',
  'waiting': 'РАСПОЗНАВАНИЕ • ожидание',
  'settings_title': 'Настройки',
  'language': 'Язык интерфейса',
  'analysis_time': 'Время анализа Stockfish',
  'poll_time': 'Интервал распознавания',
  'save': 'Сохранить',
  'cancel': 'Отмена',
  'welcome': 'Добро пожаловать в Chess Coach Live',
  'choose_language': 'Выберите язык для начала.',
  'continue': 'Продолжить',
  'saved': 'Настройки сохранены.',
  'engine_missing': 'Выберите stockfish.exe для анализа.',
  'ready': 'Выберите Stockfish и откалибруйте начальную позицию.',
  'single_move': 'Для распознанной позиции показывается только один лучший ход.',
  'language_hint': 'Позже язык можно изменить в настройках.',
  'settings_restart': 'Новые настройки вступят в силу при следующем анализе.',
  'about': 'Версия {version} • Локальная обработка',
  'duration_unit': 'секунд',
  'interval_unit': 'миллисекунд',
  'pieces': ['Пешка', 'Конь', 'Слон', 'Ладья', 'Ферзь', 'Король'],
 },
 'zh': {
  'disclaimer':'使用风险由用户自行承担。开发者不对账号封禁或停用负责。',
  'subtitle': '实时 / 分析工作室',
  'local': '本地 • STOCKFISH',
  'board': '棋盘',
  'settings': '⚙ 设置',
  'board_help': '点击棋盘以修正未识别的走法。',
  'undo': '↶ 撤销',
  'reset': '↻ 新对局',
  'flip': '⇅ 翻转棋盘',
  'best_title': '01 / 推荐走法',
  'config_title': '02 / 配置',
  'tools_title': '03 / 分析工具',
  'status_title': '04 / 跟踪状态',
  'engine': 'Stockfish 引擎',
  'orientation': '棋盘方向',
  'white_bottom': '白方在下',
  'black_bottom': '黑方在下',
  'calibrate': '⊞ 选择棋盘区域',
  'start': '▶ 开始跟踪',
  'stop': '⏸ 停止跟踪',
  'fen': '导入 FEN',
  'pgn': '导出 PGN',
  'footer': '仅用于训练及允许引擎辅助的对局。',
  'turn_white': '白方走棋',
  'turn_black': '黑方走棋',
  'no_moves': '尚无走法记录。',
  'from': '起点',
  'to': '终点',
  'evaluation': '白方局面评估',
  'mate': '将在以下步数将死：',
  'analyzing': '分析中…',
  'end': '对局结束',
  'waiting': '识别 • 等待中',
  'settings_title': '设置',
  'language': '界面语言',
  'analysis_time': 'Stockfish 分析时长',
  'poll_time': '检测间隔',
  'save': '保存',
  'cancel': '取消',
  'welcome': '欢迎使用 Chess Coach Live',
  'choose_language': '请选择语言以开始。',
  'continue': '继续',
  'saved': '设置已保存。',
  'engine_missing': '请选择 stockfish.exe 进行分析。',
  'ready': '请选择 Stockfish 并校准初始棋盘。',
  'single_move': '仅显示识别局面的一个最佳走法。',
  'language_hint': '稍后可在设置中更改语言。',
  'settings_restart': '新设置将应用于下一次分析。',
  'about': '版本 {version} • 本地处理',
  'duration_unit': '秒',
  'interval_unit': '毫秒',
  'pieces': ['兵', '马', '象', '车', '后', '王'],
 },
 'ja': {
  'disclaimer':'自己責任でご利用ください。開発者はアカウントの停止・BANについて責任を負いません。',
  'subtitle': 'ライブ / 解析スタジオ',
  'local': 'ローカル • STOCKFISH',
  'board': 'チェス盤',
  'settings': '⚙ 設定',
  'board_help': '認識されなかった手は盤面をクリックして修正できます。',
  'undo': '↶ 元に戻す',
  'reset': '↻ 新しい対局',
  'flip': '⇅ 反転',
  'best_title': '01 / 推奨手',
  'config_title': '02 / 設定',
  'tools_title': '03 / 解析ツール',
  'status_title': '04 / 追跡状態',
  'engine': 'Stockfish エンジン',
  'orientation': '盤面の向き',
  'white_bottom': '白を下に表示',
  'black_bottom': '黒を下に表示',
  'calibrate': '⊞ 盤面を選択',
  'start': '▶ 追跡開始',
  'stop': '⏸ 追跡停止',
  'fen': 'FEN を読み込む',
  'pgn': 'PGN を書き出す',
  'footer': 'エンジンの使用が許可された練習・対局のみで使用してください。',
  'turn_white': '白番',
  'turn_black': '黒番',
  'no_moves': '指し手の記録はありません。',
  'from': '移動元',
  'to': '移動先',
  'evaluation': '白側の評価値',
  'mate': '詰みまで',
  'analyzing': '解析中…',
  'end': '対局終了',
  'waiting': '認識 • 待機中',
  'settings_title': '設定',
  'language': '表示言語',
  'analysis_time': 'Stockfish の解析時間',
  'poll_time': '検出間隔',
  'save': '保存',
  'cancel': 'キャンセル',
  'welcome': 'Chess Coach Live へようこそ',
  'choose_language': '最初に言語を選択してください。',
  'continue': '続行',
  'saved': '設定を保存しました。',
  'engine_missing': '解析するには stockfish.exe を選択してください。',
  'ready': 'Stockfish を選択し、初期配置で盤面を調整してください。',
  'single_move': '認識した局面の最善手を1手だけ表示します。',
  'language_hint': '言語は後から設定で変更できます。',
  'settings_restart': '新しい設定は次の解析から適用されます。',
  'about': 'バージョン {version} • ローカル処理',
  'duration_unit': '秒',
  'interval_unit': 'ミリ秒',
  'pieces': ['ポーン', 'ナイト', 'ビショップ', 'ルーク', 'クイーン', 'キング'],
 },
 'ko': {
  'disclaimer':'사용에 따른 책임은 사용자에게 있습니다. 개발자는 계정 정지나 차단에 책임지지 않습니다.',
  'subtitle': '라이브 / 분석 스튜디오',
  'local': '로컬 • STOCKFISH',
  'board': '체스판',
  'settings': '⚙ 설정',
  'board_help': '인식하지 못한 수는 체스판을 클릭하여 수정하세요.',
  'undo': '↶ 실행 취소',
  'reset': '↻ 새 게임',
  'flip': '⇅ 뒤집기',
  'best_title': '01 / 추천 수',
  'config_title': '02 / 설정',
  'tools_title': '03 / 분석 도구',
  'status_title': '04 / 추적 상태',
  'engine': 'Stockfish 엔진',
  'orientation': '방향',
  'white_bottom': '백색 아래',
  'black_bottom': '흑색 아래',
  'calibrate': '⊞ 체스판 선택',
  'start': '▶ 추적 시작',
  'stop': '⏸ 추적 중지',
  'fen': 'FEN 가져오기',
  'pgn': 'PGN 내보내기',
  'footer': '엔진 사용이 허용된 훈련 및 게임에서만 사용하세요.',
  'turn_white': '백 차례',
  'turn_black': '흑 차례',
  'no_moves': '기록된 수가 없습니다.',
  'from': '시작',
  'to': '도착',
  'evaluation': '백 기준 평가',
  'mate': '체크메이트까지',
  'analyzing': '분석 중…',
  'end': '게임 종료',
  'waiting': '인식 • 대기 중',
  'settings_title': '설정',
  'language': '인터페이스 언어',
  'analysis_time': 'Stockfish 분석 시간',
  'poll_time': '감지 간격',
  'save': '저장',
  'cancel': '취소',
  'welcome': 'Chess Coach Live에 오신 것을 환영합니다',
  'choose_language': '시작할 언어를 선택하세요.',
  'continue': '계속',
  'saved': '설정이 저장되었습니다.',
  'engine_missing': '분석하려면 stockfish.exe를 선택하세요.',
  'ready': 'Stockfish를 선택하고 시작 위치에서 체스판을 보정하세요.',
  'single_move': '인식된 위치에서 최선의 수 하나만 표시합니다.',
  'language_hint': '나중에 설정에서 언어를 변경할 수 있습니다.',
  'settings_restart': '새 설정은 다음 분석부터 적용됩니다.',
  'about': '버전 {version} • 로컬 처리',
  'duration_unit': '초',
  'interval_unit': '밀리초',
  'pieces': ['폰', '나이트', '비숍', '룩', '퀸', '킹'],
 },
})

def config_path():
    directory = os.path.join(os.environ.get('APPDATA') or os.path.expanduser('~'), 'ChessCoachLive')
    return os.path.join(directory, 'settings.json')

def load_config():
    try:
        with open(config_path(), 'r', encoding='utf-8') as file:
            cfg = json.load(file)
        if not isinstance(cfg, dict): raise ValueError('Invalid settings')
    except (OSError, ValueError, TypeError):
        return {}, False
    return cfg, True

def save_config(cfg):
    path = config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as file:
        json.dump(cfg, file, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

def bounded_number(value, lo, hi, default):
    try: return max(lo, min(hi, float(value)))
    except (TypeError, ValueError): return default


def tiles_of(image, rect, white_bottom):
    x, y, width, height = rect
    out = {}
    side = min(width, height)
    # Board rectangle is measured from top-left, with 8 equally sized squares.
    for r in range(8):
        for c in range(8):
            l = x + round(c * side / 8)
            t = y + round(r * side / 8)
            rr = x + round((c + 1) * side / 8)
            bb = y + round((r + 1) * side / 8)
            crop = image[t:bb, l:rr]
            if crop.size == 0:
                raise ValueError('Zone de capture hors écran : recalibre l’échiquier.')
            # Ignore borders, coordinates and status markers.
            h, w = crop.shape[:2]
            crop = crop[int(h*.16):int(h*.84), int(w*.16):int(w*.84)]
            crop = cv2.resize(crop, (40,40), interpolation=cv2.INTER_AREA)
            rank = 7-r if white_bottom else r
            file = c if white_bottom else 7-c
            out[chess.square(file, rank)] = crop.astype(np.float32)
    return out


def screen_bgr():
    with mss.mss() as s:
        monitor = s.monitors[0]  # all monitors (virtual desktop)
        shot = s.grab(monitor)
        rgb = np.array(shot)[:, :, :3]
        return rgb.copy(), (monitor['left'], monitor['top'])


class BoardPicker(tk.Toplevel):
    def __init__(self, owner, callback):
        super().__init__(owner)
        self.callback = callback
        pixels, offset = screen_bgr()
        self.offset = offset
        self.photo = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB)))
        self.geometry(f'{self.photo.width()}x{self.photo.height()}+{offset[0]}+{offset[1]}')
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.canvas = tk.Canvas(self, width=self.photo.width(), height=self.photo.height(), highlightthickness=0, cursor='crosshair')
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        self.canvas.create_rectangle(8, 8, 600, 46, fill='#111827', outline='')
        self.canvas.create_text(17, 28, text='Clique-glisse pour encadrer les 64 cases de l’échiquier. Échap = annuler.', anchor='w', fill='white', font=('Segoe UI', 12, 'bold'))
        self.start = None
        self.box = None
        self.canvas.bind('<ButtonPress-1>', self.down)
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<ButtonRelease-1>', self.up)
        self.bind('<Escape>', lambda e: self.destroy())
        self.focus_force()

    def down(self, e):
        self.start = (e.x, e.y)
        if self.box: self.canvas.delete(self.box)
    def drag(self, e):
        if not self.start: return
        if self.box: self.canvas.delete(self.box)
        x, y = self.start
        self.box = self.canvas.create_rectangle(x, y, e.x, e.y, outline='#22c55e', width=3)
    def up(self, e):
        if not self.start: return
        x, y = self.start
        left, top, right, bottom = min(x,e.x), min(y,e.y), max(x,e.x), max(y,e.y)
        side = min(right-left, bottom-top)
        if side < 160:
            messagebox.showwarning('Zone trop petite', 'Sélectionne un échiquier d’au moins 160 pixels.', parent=self)
            return
        self.destroy()
        self.callback((left+self.offset[0],top+self.offset[1],side,side))


class ScreenRecognizer:
    """Learns piece appearances from the standard starting position.
    This is heuristic, and should never silently claim perfect vision.
    """
    def __init__(self, tiles):
        self.model = {}
        start = chess.Board()
        # Empty-square background is estimated from central ranks.
        for parity in range(2):
            empty = [t for sq,t in tiles.items() if start.piece_at(sq) is None and ((chess.square_file(sq)+chess.square_rank(sq))%2)==parity]
            if not empty: raise ValueError('Échiquier initial non visible.')
            self.model[(None,parity)] = np.median(np.stack(empty),axis=0)
        for sq, tile in tiles.items():
            p = start.piece_at(sq)
            if p is None: continue
            key = (p.symbol(), (chess.square_file(sq)+chess.square_rank(sq))%2)
            self.model.setdefault(key, []).append(tile)
        for key, samples in list(self.model.items()):
            if isinstance(samples, list): self.model[key] = np.median(np.stack(samples),axis=0)
        # Extract piece silhouettes from captured square, so background parity can change.
        for (symbol, parity), tile in list(self.model.items()):
            if symbol is None: continue
            base = self.model[(None,parity)]
            mask = np.max(np.abs(tile-base),axis=2) > 24
            mask = cv2.dilate(mask.astype(np.uint8),np.ones((3,3),np.uint8)).astype(bool)
            self.model[(symbol,parity)] = (tile, mask)

    def predicted(self, symbol, parity):
        background = self.model[(None,parity)]
        if symbol is None: return background
        if (symbol,parity) in self.model:
            foreground, mask = self.model[(symbol,parity)]
        elif (symbol,1-parity) in self.model:
            foreground, mask = self.model[(symbol,1-parity)]
        else:
            return background
        result = background.copy()
        result[mask] = foreground[mask]
        return result

    def score_board(self, tiles, position):
        distances = []
        for sq, tile in tiles.items():
            piece = position.piece_at(sq)
            parity = (chess.square_file(sq)+chess.square_rank(sq))%2
            predicted = self.predicted(piece.symbol() if piece else None, parity)
            distances.append(float(np.mean(np.abs(tile-predicted))))
        return float(np.mean(distances))

    def _error_table(self, tiles):
        """Cache image errors once per frame, instead of reprocessing each move."""
        symbols = (None, 'P', 'N', 'B', 'R', 'Q', 'K',
                   'p', 'n', 'b', 'r', 'q', 'k')
        table = {}
        for square, tile in tiles.items():
            parity = (chess.square_file(square) + chess.square_rank(square)) % 2
            table[square] = {
                symbol: float(np.mean(np.abs(tile - self.predicted(symbol, parity))))
                for symbol in symbols
            }
        return table

    @staticmethod
    def _position_error(table, board):
        return sum(errors[board.piece_at(sq).symbol() if board.piece_at(sq) else None]
                   for sq, errors in table.items()) / max(1, len(table))

    @staticmethod
    def _affected_squares(board, move):
        """Squares that can change after a legal move, including special moves."""
        affected = {move.from_square, move.to_square}
        if board.is_en_passant(move):
            affected.add(move.to_square - 8 if board.turn else move.to_square + 8)
        if board.is_castling(move):
            rank = chess.square_rank(move.from_square)
            if board.is_kingside_castling(move):
                affected.update({chess.square(7, rank), chess.square(5, rank)})
            else:
                affected.update({chess.square(0, rank), chess.square(3, rank)})
        return affected

    def likely_transition(self, tiles, board):
        """Compare unchanged, one-move, and two-move states efficiently.

        Rather than re-scoring all 64 squares for every legal continuation,
        adjust only squares affected by each legal move. This keeps the
        application responsive in middlegame positions with many candidates.
        """
        table = self._error_table(tiles)
        original = {sq: (board.piece_at(sq).symbol()
                         if board.piece_at(sq) else None) for sq in table}
        baseline_total = sum(table[sq][symbol] for sq, symbol in original.items())
        divisor = max(1, len(table))
        baseline = baseline_total / divisor

        def changed_score(squares):
            delta = 0.0
            for sq in squares:
                if sq not in table:
                    continue
                piece = board.piece_at(sq)
                symbol = piece.symbol() if piece else None
                delta += table[sq][symbol] - table[sq][original[sq]]
            return (baseline_total + delta) / divisor

        one_ply = []
        for first in list(board.legal_moves):
            affected1 = self._affected_squares(board, first)
            board.push(first)
            score = changed_score(affected1)
            board.pop()
            one_ply.append((score, (first,)))
        one_ply.sort(key=lambda item: item[0])
        if not one_ply:
            return None, baseline, 0.0
        first_score, first_line = one_ply[0]
        runner = one_ply[1][0] if len(one_ply) > 1 else float('inf')
        if baseline - first_score > 1.5 and runner - first_score > 0.25:
            return first_line, first_score, baseline - first_score
        if baseline < 4.5:
            return None, baseline, 0.0

        # Scan two missed half-moves; score only the union of changed squares.
        best_two = []
        for first in list(board.legal_moves):
            affected1 = self._affected_squares(board, first)
            board.push(first)
            for second in list(board.legal_moves):
                affected2 = self._affected_squares(board, second)
                board.push(second)
                score = changed_score(affected1 | affected2)
                board.pop()
                best_two.append((score, (first, second)))
            board.pop()
        if not best_two:
            return None, baseline, 0.0
        best_two.sort(key=lambda item: item[0])
        score, line = best_two[0]
        runner = best_two[1][0] if len(best_two) > 1 else float('inf')
        if baseline - score > 2.5 and first_score - score > 1.2 and runner - score > 0.35:
            return line, score, baseline - score
        return None, baseline, 0.0


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(f'Chess Coach Live  |  v{APP_VERSION}')
        self.set_app_icon(self.root)
        self.root.geometry('1200x860')
        self.root.minsize(1060, 740)
        self.root.configure(bg=BG)
        self.config, self.has_config = load_config()
        self.lang = self.config.get('language', 'fr')
        if self.lang not in LANGUAGES: self.lang = 'fr'
        self.analysis_seconds = bounded_number(self.config.get('analysis_seconds', 1.5), 0.2, 10, 1.5)
        self.poll_ms = int(bounded_number(self.config.get('poll_ms', 450), 250, 2000, 450))
        self.localized_widgets = []
        self.board = chess.Board()
        self.orientation = tk.BooleanVar(value=True)
        self.stockfish = tk.StringVar(value=self.resolve_stockfish(self.config.get('stockfish_path')))
        self.status = tk.StringVar(value=self.tr('ready'))
        self.best = tk.StringVar(value='—')
        self.explain = tk.StringVar(value=self.tr('single_move'))
        self.eval_text = tk.StringVar(value='ÉVALUATION  —')
        self.history_text = tk.StringVar(value=self.tr('no_moves'))
        self.recognition_text = tk.StringVar(value=self.tr('waiting'))
        self.monitoring = False
        self.rect = None
        self.recognizer = None
        self.suggested = None
        self.selected = None
        self.messages = queue.Queue()
        self.generation = 0
        self.engine_wakeup = threading.Event()
        self.pending_analysis = None
        self.closing = False
        self.visual_synced = False
        self.confirm_move = None
        self.confirm_count = 0
        self.visual_limit = 13.0
        self.current_fen = None
        self.setup_ui()
        self.draw()
        threading.Thread(target=self.engine_loop,daemon=True).start()
        self.root.after(100,self.process_messages)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        if not self.has_config:
            self.root.after(120, self.first_run_language)

    def tr(self, key):
        return TRANSLATIONS[self.lang].get(key, TRANSLATIONS['en'].get(key, key))

    def labeled(self, widget, key):
        self.localized_widgets.append((widget, key))
        return widget

    def refresh_language(self):
        for widget, key in self.localized_widgets:
            if widget.winfo_exists(): widget.configure(text=self.tr(key))
        self.root.title(f'Chess Coach Live  |  v{APP_VERSION}')
        self.toggle_btn.configure(text=self.tr('stop' if self.monitoring else 'start'))
        self.draw()
        self.refresh_history()
        self.status.set(self.tr('ready'))
        self.explain.set(self.tr('single_move'))
        self.recognition_text.set(self.tr('waiting'))
        if self.suggested:
            piece = self.board.piece_at(self.suggested[0])
            if piece:
                self.best.set(self.tr('pieces')[piece.piece_type - 1] + ' → ' + chess.square_name(self.suggested[1]))

    def first_run_language(self):
        self.root.withdraw()
        dialog = tk.Toplevel(self.root)
        dialog.title('Chess Coach Live • Choose your language')
        self.set_app_icon(dialog)
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.geometry('530x330')
        dialog.protocol('WM_DELETE_WINDOW', self.root.destroy)
        dialog.grab_set()
        tk.Label(dialog, text='♞  CHESS COACH LIVE', fg=ACCENT, bg=BG,
                 font=('Segoe UI', 20, 'bold')).pack(pady=(27, 9))
        title = tk.Label(dialog, text='Welcome to Chess Coach Live', fg='#F6F8FF', bg=BG, font=('Segoe UI', 13, 'bold'), wraplength=490, justify='center')
        title.pack(pady=(0, 8))
        hint = tk.Label(dialog, text='Choose your language to get started.', fg='#A5B5CE', bg=BG, font=('Segoe UI', 10), wraplength=490, justify='center')
        hint.pack()
        selected = tk.StringVar(value=LANGUAGES['en'])
        choice = ttk.Combobox(dialog, textvariable=selected, values=list(LANGUAGES.values()),
                              state='readonly', width=30, font=('Segoe UI', 12))
        choice.pack(pady=22)
        note = tk.Label(dialog, text='You can change your language later in Settings.', fg='#A5B5CE', bg=BG, font=('Segoe UI', 9), wraplength=490, justify='center')
        note.pack()
        def finish():
            self.lang = next(k for k,v in LANGUAGES.items() if v == selected.get())
            self.config.update(language=self.lang, analysis_seconds=self.analysis_seconds, poll_ms=self.poll_ms)
            try: save_config(self.config)
            except OSError as exc:
                messagebox.showwarning('Chess Coach Live', str(exc), parent=dialog)
            dialog.grab_release()
            dialog.destroy()
            self.root.deiconify()
            self.refresh_language()
        accept = ttk.Button(dialog, text='Continue', command=finish, style='Accent.TButton')
        accept.pack(pady=12)
        dialog.focus_force()

    def open_settings(self):
        window = tk.Toplevel(self.root)
        window.title(self.tr('settings_title'))
        window.configure(bg=BG)
        window.geometry('520x420')
        window.resizable(False, False)
        window.transient(self.root)
        window.grab_set()
        tk.Label(window, text=self.tr('settings_title'), bg=BG, fg='#FFFFFF',
                 font=('Segoe UI', 20, 'bold')).pack(anchor='w', padx=25, pady=(23, 8))
        tk.Label(window, text=self.tr('language'), bg=BG, fg='#C9D8ED',
                 font=('Segoe UI', 11)).pack(anchor='w', padx=25, pady=(12, 4))
        language_var = tk.StringVar(value=LANGUAGES[self.lang])
        ttk.Combobox(window, textvariable=language_var, values=list(LANGUAGES.values()),
                     state='readonly', font=('Segoe UI', 11)).pack(fill='x', padx=25)
        tk.Label(window, text=self.tr('analysis_time'), bg=BG, fg='#C9D8ED',
                 font=('Segoe UI', 11)).pack(anchor='w', padx=25, pady=(15, 4))
        time_var = tk.StringVar(value=str(self.analysis_seconds))
        tk.Spinbox(window, from_=0.2, to=10.0, increment=0.1, textvariable=time_var,
                   width=12, font=('Segoe UI', 11)).pack(anchor='w', padx=25)
        tk.Label(window, text=self.tr('poll_time'), bg=BG, fg='#C9D8ED',
                 font=('Segoe UI', 11)).pack(anchor='w', padx=25, pady=(15, 4))
        poll_var = tk.StringVar(value=str(self.poll_ms))
        ttk.Combobox(window, textvariable=poll_var, values=['250', '350', '450', '600', '750', '1000', '1500', '2000'],
                     state='readonly', font=('Segoe UI', 11)).pack(anchor='w', padx=25)
        buttons = tk.Frame(window, bg=BG)
        buttons.pack(fill='x', padx=25, pady=26)
        def save():
            self.lang = next(k for k,v in LANGUAGES.items() if v == language_var.get())
            self.analysis_seconds = bounded_number(time_var.get(), 0.2, 10, 1.5)
            self.poll_ms = int(bounded_number(poll_var.get(), 250, 2000, 450))
            self.config.update(language=self.lang, analysis_seconds=self.analysis_seconds, poll_ms=self.poll_ms)
            try: save_config(self.config)
            except OSError as exc:
                messagebox.showerror('Chess Coach Live', str(exc), parent=window)
                return
            self.refresh_language()
            self.status.set(self.tr('saved'))
            window.destroy()
        ttk.Button(buttons, text=self.tr('cancel'), command=window.destroy,
                   style='Coach.TButton').pack(side='right', padx=(8,0))
        ttk.Button(buttons, text=self.tr('save'), command=save,
                   style='Accent.TButton').pack(side='right')


    @staticmethod
    def set_app_icon(window):
        # PyInstaller extracts bundled resources to sys._MEIPASS.
        resource_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(resource_dir, 'assets', 'ChessCoachLive.ico')
        if os.path.isfile(path):
            try: window.iconbitmap(path)
            except (tk.TclError, OSError): pass

    @staticmethod
    def find_stockfish():
        """Prefer the packaged engine in source or PyInstaller onefile mode."""
        resource_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        exe_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
        candidates = [
            os.path.join(resource_dir, 'stockfish', 'stockfish.exe'),
            os.path.join(exe_dir, 'stockfish', 'stockfish.exe'),
            os.path.join(exe_dir, 'stockfish.exe'),
        ]
        for folder in (resource_dir, exe_dir):
            if not os.path.isdir(folder):
                continue
            for name in os.listdir(folder):
                if name.lower().startswith('stockfish') and name.lower().endswith('.exe'):
                    candidates.append(os.path.join(folder, name))
        return next((path for path in candidates if os.path.isfile(path)), '')

    @classmethod
    def resolve_stockfish(cls, configured_path):
        # Old versions may have saved a path that no longer exists.
        if configured_path and os.path.isfile(configured_path):
            return configured_path
        return cls.find_stockfish()

    def setup_ui(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('Coach.TButton', background='#273550', foreground='#F0F4FF',
                        borderwidth=0, padding=(12, 11), font=('Segoe UI', 10, 'bold'))
        style.map('Coach.TButton', background=[('active', '#344969')])
        style.configure('Accent.TButton', background='#54D6AC', foreground='#0C1B27',
                        borderwidth=0, padding=(12, 12), font=('Segoe UI', 10, 'bold'))
        style.map('Accent.TButton', background=[('active', '#83E6C5')])
        style.configure('Coach.TEntry', fieldbackground='#0F1728', foreground='#F0F4FF',
                        bordercolor='#34445C', padding=8)
        style.configure('Coach.TRadiobutton', background=PANEL, foreground='#E3ECFB',
                        font=('Segoe UI', 10))
        style.map('Coach.TRadiobutton', background=[('active', PANEL)],
                  foreground=[('active', '#FFFFFF')])

        header = tk.Frame(self.root, bg=BG)
        header.pack(fill='x', padx=26, pady=(22, 18))
        tk.Label(header, text='♞', bg=BG, fg='#54D6AC',
                 font=('Segoe UI Symbol', 30)).pack(side='left', padx=(0, 14))
        names = tk.Frame(header, bg=BG)
        names.pack(side='left')
        tk.Label(names, text='CHESS COACH', bg=BG, fg='#F6F8FF',
                 font=('Segoe UI', 23, 'bold')).pack(anchor='w')
        self.labeled(tk.Label(names, text=self.tr('subtitle'), bg=BG, fg='#94A4BF',
                 font=('Segoe UI', 9, 'bold')), 'subtitle').pack(anchor='w')
        self.settings_btn = self.labeled(ttk.Button(header, text=self.tr('settings'), command=self.open_settings,
                    style='Coach.TButton'), 'settings')
        self.settings_btn.pack(side='right', padx=(12, 0))
        self.labeled(tk.Label(header, text=self.tr('local'), bg='#1C2B3C', fg='#A8EBD4',
                 font=('Segoe UI', 9, 'bold'), padx=14, pady=8), 'local').pack(side='right')

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill='both', expand=True, padx=26)
        left = tk.Frame(body, bg=BG)
        left.pack(side='left', anchor='n', padx=(0, 24))
        topbar = tk.Frame(left, bg=BG)
        topbar.pack(fill='x', pady=(0, 10))
        self.labeled(tk.Label(topbar, text=self.tr('board'), bg=BG, fg='#DCE6F6',
                 font=('Segoe UI', 11, 'bold')), 'board').pack(side='left')
        self.turn_label = tk.StringVar(value=self.tr('turn_white'))
        tk.Label(topbar, textvariable=self.turn_label, bg=BG, fg='#A0B4CE',
                 font=('Segoe UI', 10)).pack(side='right')
        self.canvas = tk.Canvas(left, width=536, height=536, bg='#19253B',
                                highlightthickness=0, cursor='hand2')
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.click_board)
        self.labeled(tk.Label(left, text=self.tr('board_help'),
                 bg=BG, fg='#91A3BD', font=('Segoe UI', 9)), 'board_help').pack(anchor='w', pady=(12, 9))
        controls = tk.Frame(left, bg=BG)
        controls.pack(fill='x')
        self.labeled(ttk.Button(controls, text=self.tr('undo'), command=self.undo,
                   style='Coach.TButton'), 'undo').pack(side='left', padx=(0, 8))
        self.labeled(ttk.Button(controls, text=self.tr('reset'), command=self.reset,
                   style='Coach.TButton'), 'reset').pack(side='left', padx=(0, 8))
        self.labeled(ttk.Button(controls, text=self.tr('flip'), command=self.flip,
                   style='Coach.TButton'), 'flip').pack(side='left')

        right = tk.Frame(body, bg=BG)
        right.pack(side='left', fill='both', expand=True)
        self.card_best = tk.Frame(right, bg=PANEL, padx=20, pady=18)
        self.card_best.pack(fill='x', pady=(0, 14))
        self.caption(self.card_best, 'best_title')
        tk.Label(self.card_best, textvariable=self.eval_text, bg=PANEL, fg='#A7B9D4',
                 font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(9, 0))
        tk.Label(self.card_best, textvariable=self.best, bg=PANEL, fg='#54D6AC',
                 font=('Segoe UI', 23, 'bold'), anchor='w', justify='left',
                 wraplength=350).pack(anchor='w', pady=(13, 5))
        tk.Label(self.card_best, textvariable=self.explain, bg=PANEL, fg='#C4D1E5',
                 font=('Segoe UI', 11), anchor='w', justify='left',
                 wraplength=350).pack(anchor='w', pady=(0, 4))

        card_config = tk.Frame(right, bg=PANEL, padx=20, pady=18)
        card_config.pack(fill='x', pady=(0, 14))
        self.caption(card_config, 'config_title')
        self.labeled(tk.Label(card_config, text=self.tr('engine'), bg=PANEL, fg='#C7D4E8',
                 font=('Segoe UI', 10)), 'engine').pack(anchor='w', pady=(14, 5))
        pathrow = tk.Frame(card_config, bg=PANEL)
        pathrow.pack(fill='x', pady=(0, 13))
        ttk.Entry(pathrow, textvariable=self.stockfish,
                  style='Coach.TEntry').pack(side='left', fill='x', expand=True)
        ttk.Button(pathrow, text='…', width=3, command=self.browse,
                   style='Coach.TButton').pack(side='left', padx=(8, 0))
        self.labeled(tk.Label(card_config, text=self.tr('orientation'), bg=PANEL, fg='#C7D4E8',
                 font=('Segoe UI', 10)), 'orientation').pack(anchor='w', pady=(0, 6))
        orientations = tk.Frame(card_config, bg=PANEL)
        orientations.pack(fill='x', pady=(0, 13))
        self.labeled(ttk.Radiobutton(orientations, text=self.tr('white_bottom'), variable=self.orientation,
                        value=True, command=self.change_orientation,
                        style='Coach.TRadiobutton'), 'white_bottom').pack(side='left', padx=(0, 15))
        self.labeled(ttk.Radiobutton(orientations, text=self.tr('black_bottom'), variable=self.orientation,
                        value=False, command=self.change_orientation,
                        style='Coach.TRadiobutton'), 'black_bottom').pack(side='left')
        self.labeled(ttk.Button(card_config, text=self.tr('calibrate'),
                   command=self.pick_board, style='Coach.TButton'), 'calibrate').pack(fill='x', pady=(0, 8))
        self.toggle_btn = ttk.Button(card_config, text=self.tr('start'),
                                     command=self.toggle_monitor, style='Accent.TButton')
        self.toggle_btn.pack(fill='x')

        card_tools = tk.Frame(right, bg=PANEL, padx=20, pady=14)
        card_tools.pack(fill='x', pady=(0, 12))
        self.caption(card_tools, 'tools_title')
        tools_row = tk.Frame(card_tools, bg=PANEL)
        tools_row.pack(fill='x', pady=(10, 0))
        self.labeled(ttk.Button(tools_row, text=self.tr('fen'), command=self.import_fen,
                   style='Coach.TButton'), 'fen').pack(side='left', padx=(0, 7))
        self.labeled(ttk.Button(tools_row, text=self.tr('pgn'), command=self.export_pgn,
                   style='Coach.TButton'), 'pgn').pack(side='left')
        tk.Label(card_tools, textvariable=self.history_text, bg=PANEL, fg='#A6B9D6',
                 justify='left', font=('Consolas', 9), wraplength=360).pack(anchor='w', pady=(10, 0))

        card_status = tk.Frame(right, bg=PANEL, padx=20, pady=16)
        card_status.pack(fill='x')
        self.caption(card_status, 'status_title')
        tk.Label(card_status, textvariable=self.recognition_text, bg=PANEL, fg=ACCENT,
                 font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(9, 0))
        tk.Label(card_status, textvariable=self.status, bg=PANEL, fg='#B7C7DF',
                 font=('Segoe UI', 10), wraplength=350,
                 justify='left').pack(anchor='w', pady=(12, 2))

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill='x', padx=26, pady=(14, 17))
        tk.Label(footer, text=f'CHESS COACH  /  v{APP_VERSION}', bg=BG, fg='#7185A4',
                 font=('Segoe UI', 9, 'bold')).pack(side='left')
        legal = tk.Frame(footer, bg=BG)
        legal.pack(side='right', fill='x', expand=True, padx=(16, 0))
        self.labeled(tk.Label(legal, text=self.tr('footer'),
                 bg=BG, fg='#7185A4', font=('Segoe UI', 9),
                 anchor='e', justify='right', wraplength=500), 'footer').pack(anchor='e')
        self.labeled(tk.Label(legal, text=self.tr('disclaimer'),
                 bg=BG, fg='#93A9C8', font=('Segoe UI', 9),
                 anchor='e', justify='right', wraplength=500), 'disclaimer').pack(anchor='e', pady=(3, 0))

    def caption(self, parent, text):
        self.labeled(tk.Label(parent, text=self.tr(text), bg=PANEL, fg='#93A9C8',
                 font=('Segoe UI', 9, 'bold')), text).pack(anchor='w')

    def square(self,row,col):
        return chess.square(col if self.orientation.get() else 7-col,7-row if self.orientation.get() else row)

    def draw(self):
        c=self.canvas;c.delete('all');size=67
        self.turn_label.set(self.tr('turn_white' if self.board.turn else 'turn_black'))
        for row in range(8):
            for col in range(8):
                sq=self.square(row,col)
                color='#E6EAF0' if (row+col)%2==0 else '#7994AA'
                if self.suggested and sq in self.suggested:color='#B8E8D9'
                if sq==self.selected:color='#A9C5FF'
                x,y=col*size,row*size
                c.create_rectangle(x,y,x+size,y+size,fill=color,outline=color)
                piece=self.board.piece_at(sq)
                if piece:
                    # Outline the glyph to keep white pieces readable on light squares,
                    # and black pieces readable on dark/highlighted squares.
                    glyph = GLYPHS[piece.symbol()]
                    cx, cy = x + size / 2, y + size / 2
                    font = ('Segoe UI Symbol', 38)
                    foreground = '#FFFFFF' if piece.color else '#182434'
                    outline = '#243447' if piece.color else '#F0F5FA'
                    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2),
                                   (-1, -1), (-1, 1), (1, -1), (1, 1)):
                        c.create_text(cx + dx, cy + dy, text=glyph,
                                      font=font, fill=outline)
                    c.create_text(cx, cy, text=glyph, font=font, fill=foreground)
                if row==7:
                    c.create_text(x+58,y+58,text=chess.square_name(sq)[0],font=('Segoe UI',8,'bold'),fill='#344054')
                if col==0:
                    c.create_text(x+8,y+10,text=chess.square_name(sq)[1],font=('Segoe UI',8,'bold'),fill='#344054')
        # A single clear arrow highlights the one move recommended by the engine.
        if self.suggested:
            a, b = self.suggested
            def center(sq):
                f, r = chess.square_file(sq), chess.square_rank(sq)
                col = f if self.orientation.get() else 7-f
                row = 7-r if self.orientation.get() else r
                return col*size+size/2, row*size+size/2
            x1, y1 = center(a)
            x2, y2 = center(b)
            c.create_line(x1, y1, x2, y2, fill='#136E68', width=8,
                          arrow=tk.LAST, arrowshape=(18, 22, 9), capstyle=tk.ROUND)

    def click_board(self,event):
        row,col=event.y//67,event.x//67
        if row not in range(8) or col not in range(8):return
        sq=self.square(row,col)
        if self.selected is not None:
            options=[m for m in self.board.legal_moves if m.from_square==self.selected and m.to_square==sq]
            if options:
                self.push(next((m for m in options if m.promotion==chess.QUEEN),options[0]),'Position corrigée à la main.')
                return
        p=self.board.piece_at(sq)
        self.selected=sq if p and p.color==self.board.turn else None
        self.draw()

    def browse(self):
        f=filedialog.askopenfilename(title='Sélectionner stockfish.exe',filetypes=[('EXE','*.exe'),('Tous','*')])
        if f:
            self.stockfish.set(f)
            self.config['stockfish_path'] = f
            try: save_config(self.config)
            except OSError: pass
            self.generation += 1
            self.request_analysis()
    def change_orientation(self):
        self.draw()
        if self.rect:self.stop_monitor('Orientation modifiée : recalibre la capture.')
    def flip(self):self.orientation.set(not self.orientation.get());self.change_orientation()
    def reset(self):
        self.board=chess.Board();self.changed('Nouvelle partie. Recalibre si les pièces à l’écran ont changé.')
    def undo(self):
        if self.board.move_stack:self.board.pop();self.changed('Dernier coup annulé.')
    def push(self,move,msg):self.board.push(move);self.changed(msg)
    def changed(self,msg):
        self.generation+=1
        self.selected=None;self.suggested=None;self.best.set(self.tr('analyzing'));self.explain.set('')
        self.status.set(msg)
        self.eval_text.set('ÉVALUATION  —')
        self.refresh_history()
        self.draw()
        self.request_analysis()

    def refresh_history(self):
        replay = self.board.root()
        tokens = []
        for i, move in enumerate(self.board.move_stack):
            prefix = f'{(i // 2) + 1}.' if i % 2 == 0 else ''
            tokens.append(prefix + replay.san(move))
            replay.push(move)
        self.history_text.set(' '.join(tokens[-16:]) or self.tr('no_moves'))

    def import_fen(self):
        if self.monitoring:
            self.stop_monitor('Suivi arrêté pour importer une position.')
        fen = simpledialog.askstring('Importer FEN',
            'Colle une position FEN complète (pour analyse hors suivi) :', parent=self.root)
        if not fen:
            return
        try:
            board = chess.Board(fen.strip())
            if not board.is_valid():
                raise ValueError('La position FEN est illégale ou incohérente.')
        except ValueError as exc:
            messagebox.showerror('FEN invalide', str(exc), parent=self.root)
            return
        self.board = board
        self.recognizer = None
        self.rect = None
        self.visual_synced = False
        self.recognition_text.set('RECONNAISSANCE  •  non calibrée')
        self.changed('Position FEN chargée. Recalibre depuis le début pour le suivi visuel.')

    def export_pgn(self):
        if not self.board.move_stack:
            messagebox.showinfo('Historique vide', 'Aucun coup à exporter.', parent=self.root)
            return
        filename = filedialog.asksaveasfilename(defaultextension='.pgn',
            filetypes=[('Partie PGN', '*.pgn')], title='Exporter la partie')
        if not filename:
            return
        try:
            game = chess.pgn.Game.from_board(self.board)
            game.headers['Event'] = 'Chess Coach Live analysis'
            game.headers['Site'] = 'Local'
            with open(filename, 'w', encoding='utf-8') as handle:
                print(game, file=handle)
            self.status.set('PGN exporté : ' + os.path.basename(filename))
        except OSError as exc:
            messagebox.showerror('Export impossible', str(exc), parent=self.root)

    def pick_board(self):
        self.stop_monitor('Capture arrêtée pour calibrage.')
        self.root.withdraw()
        # The root is hidden so it does not cover the board under calibration.
        self.root.after(300,lambda:BoardPicker(self.root,self.finish_pick))

    def finish_pick(self,rect):
        # Capture while the application window is still hidden.
        pixels,offset=screen_bgr()
        self.root.deiconify()
        self.rect=rect
        if self.board.fen()!=chess.Board().fen():
            if not messagebox.askyesno('Réinitialiser ?', 'Pour apprendre les pièces, la position affichée doit être la position initiale. Réinitialiser la partie ?'):
                self.status.set('Le calibrage nécessite une position initiale standard.');return
            self.board=chess.Board()
        try:
            # translate global coordinates to screenshot array coordinates
            local=(rect[0]-offset[0],rect[1]-offset[1],rect[2],rect[3])
            tiles=tiles_of(pixels,local,self.orientation.get())
            self.recognizer=ScreenRecognizer(tiles)
            reference=self.recognizer.score_board(tiles,self.board)
            self.visual_limit = max(10.0, reference + 12.0)
            self.visual_synced = True
            self.recognition_text.set('RECONNAISSANCE  •  calibrée')
            self.confirm_move = None
            self.confirm_count = 0
            self.status.set(f'Calibré ({int(rect[2])} px). Score initial {reference:.1f}. Lance le suivi.')
            self.changed(self.status.get())
        except Exception as e:
            self.recognizer=None
            messagebox.showerror('Calibrage impossible',str(e))

    def toggle_monitor(self):
        if self.monitoring:self.stop_monitor('Suivi mis en pause.')
        else:
            if not self.recognizer or not self.rect:
                messagebox.showinfo('Calibrage requis','Encadre un échiquier en position initiale avant de démarrer.')
                return
            self.monitoring=True
            self.visual_synced = False
            self.confirm_move = None
            self.confirm_count = 0
            self.best.set('Vérification de la position…')
            self.recognition_text.set('RECONNAISSANCE  •  vérification')
            self.suggested = None
            self.draw()
            self.toggle_btn.configure(text=self.tr('stop'))
            self.status.set('Suivi de l’écran activé. Laisse l’échiquier visible, sans le déplacer.')
            self.root.after(500,self.poll_screen)
            self.request_analysis()

    def stop_monitor(self,msg):
        self.monitoring=False
        self.toggle_btn.configure(text=self.tr('start'))
        self.status.set(msg)
        self.recognition_text.set('RECONNAISSANCE  •  en pause')

    def poll_screen(self):
        if not self.monitoring or self.closing:return
        try:
            pixels,offset=screen_bgr()
            rect=(self.rect[0]-offset[0],self.rect[1]-offset[1],self.rect[2],self.rect[3])
            ts=tiles_of(pixels,rect,self.orientation.get())
            # Do not display a suggestion based on a board that no longer
            # matches the actual captured board. Recognition is heuristic.
            unchanged = self.recognizer.score_board(ts, self.board)
            moves, score, improvement = self.recognizer.likely_transition(ts, self.board)
            if moves is not None and score < self.visual_limit:
                if self.confirm_move == moves:
                    self.confirm_count += 1
                else:
                    self.confirm_move = moves
                    self.confirm_count = 1
                self.visual_synced = False
                self.recognition_text.set('RECONNAISSANCE  •  confirmation')
                self.best.set('Coup détecté — confirmation…')
                self.suggested = None
                self.draw()
                if self.confirm_count >= 2:
                    notation = []
                    for detected in moves:
                        notation.append(self.board.san(detected))
                        self.board.push(detected)
                    self.confirm_move = None
                    self.confirm_count = 0
                    self.visual_synced = True
                    self.recognition_text.set('RECONNAISSANCE  •  synchronisée')
                    self.changed(f"À l’écran : {' '.join(notation)} • score visuel {score:.1f}.")
            elif unchanged <= self.visual_limit:
                self.confirm_move = None
                self.confirm_count = 0
                if not self.visual_synced:
                    self.visual_synced = True
                    self.recognition_text.set('RECONNAISSANCE  •  synchronisée')
                    self.status.set('Position à l’écran reconnue ; analyse synchronisée.')
                    self.request_analysis()
            else:
                self.confirm_move = None
                self.confirm_count = 0
                self.visual_synced = False
                self.recognition_text.set('RECONNAISSANCE  •  incertaine')
                self.suggested = None
                self.best.set('Position non synchronisée')
                self.eval_text.set('ÉVALUATION  —')
                self.explain.set('Le suivi visuel ne reconnaît pas la position. Corrige les coups sur l’échiquier local, ou recommence le calibrage depuis le début.')
                self.status.set(f'Capture incertaine (écart {unchanged:.1f}). Aucun coup conseillé pour éviter une erreur.')
                self.draw()
            if self.board.is_game_over():
                self.status.set('Partie terminée.')
        except Exception as e:
            self.stop_monitor('Erreur de capture : '+str(e)[:140]);return
        self.root.after(self.poll_ms,self.poll_screen)

    def request_analysis(self):
        self.pending_analysis=(self.generation,self.board.copy(),self.stockfish.get().strip().strip('"'))
        self.engine_wakeup.set()

    def engine_loop(self):
        engine=None;current_path=None
        try:
            while not self.closing:
                self.engine_wakeup.wait(.4)
                self.engine_wakeup.clear()
                task=self.pending_analysis
                if not task:continue
                gen,board,path=task
                if not path or not os.path.isfile(path):
                    self.messages.put(('error',gen,self.tr('engine_missing')))
                    continue
                try:
                    if engine is None or path!=current_path:
                        if engine:
                            try:engine.quit()
                            except Exception:pass
                        # Prevent the Stockfish console from appearing on Windows.
                        flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
                        engine=chess.engine.SimpleEngine.popen_uci(
                            path, timeout=8, creationflags=flags
                        )
                        current_path=path
                    if board.is_game_over():
                        self.messages.put(('result',gen,board,None));continue
                    data=engine.analyse(board,chess.engine.Limit(time=self.analysis_seconds),multipv=1)
                    self.messages.put(('result',gen,board,data[0] if isinstance(data, list) else data))
                except Exception as e:
                    self.messages.put(('error',gen,'Stockfish : '+str(e)[:150]))
                    try:
                        if engine:engine.quit()
                    except Exception:pass
                    engine=None;current_path=None
        finally:
            if engine:
                try:engine.quit()
                except Exception:pass

    def process_messages(self):
        try:
            while True:
                kind,gen,*args=self.messages.get_nowait()
                if gen!=self.generation:continue
                if self.monitoring and not self.visual_synced:continue
                if kind=='error':self.best.set('—');self.explain.set(args[0]);continue
                board,info=args
                if not info or not info.get('pv'):
                    self.best.set(self.tr('end'));self.eval_text.set('ÉVALUATION  —');self.explain.set(board.result());self.suggested=None;self.draw();continue
                # Un seul coup suggéré : première variation principale de Stockfish.
                move = info['pv'][0]
                piece = board.piece_at(move.from_square)
                self.suggested = (move.from_square, move.to_square)
                self.best.set(f'{self.tr("pieces")[piece.piece_type-1]} → {chess.square_name(move.to_square)}')
                score = info.get('score')
                if score is not None:
                    side_score = score.white()
                    if side_score.is_mate():
                        evaluation = f'{self.tr("mate")} {side_score.mate()}'
                    else:
                        cp = side_score.score()
                        evaluation = f'{cp/100:+.2f}' if cp is not None else '—'
                    self.eval_text.set(self.tr('evaluation') + '  ' + evaluation)
                self.explain.set(
                    self.tr('from') + ' : ' + chess.square_name(move.from_square)
                    + '\n' + self.tr('to') + ' : ' + chess.square_name(move.to_square)
                )
                self.draw()
        except queue.Empty:pass
        if not self.closing:self.root.after(100,self.process_messages)

    def close(self):
        self.closing=True;self.monitoring=False;self.engine_wakeup.set();self.root.destroy()


if __name__=='__main__':
    root=tk.Tk()
    App(root)
    root.mainloop()
