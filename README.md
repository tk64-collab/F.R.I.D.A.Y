# F.R.I.D.A.Y.

**F.R.I.D.A.Y.**（Female Replacement Intelligent Digital Assistant Youth）は、Python で構築された日本語対応の AI 音声アシスタントです。キーワードで起動し、天気・ニュース・スケジュール管理・自由会話など多様なタスクに音声で応答します。

---

## 目次

1. [機能一覧](#機能一覧)
2. [システム構成](#システム構成)
3. [ファイル構成](#ファイル構成)
4. [必要環境](#必要環境)
5. [セットアップ](#セットアップ)
6. [使い方](#使い方)
7. [環境変数](#環境変数)
8. [現在の実装状況と今後の課題](#現在の実装状況と今後の課題)

---

## 機能一覧

| 機能 | 概要 |
|------|------|
| **キーワード起動** | 「friday」という単語をマイクが拾うと自動でアシスタントが起動 |
| **音声認識** | Google Speech Recognition を使用した日本語音声入力 |
| **AI 会話** | OpenAI GPT（gpt-3.5-turbo / gpt-4o）による自然言語応答 |
| **天気情報** | OpenWeatherMap API から現在の天気・気温を取得（日本語地名対応）|
| **ニュース取得** | NewsAPI から日本の最新ニュースのトップ 5 件を取得 |
| **スケジュール管理** | 予定の記録・当日の予定確認（JSON ファイルに保存）|
| **音声合成（TTS）** | OpenAI TTS API（`tts-1` モデル・`nova` ボイス）でアシスタントの返答を音声再生 |
| **GUI** | PyQt5 ベースのシンプルなデスクトップ UI |

---

## システム構成

```
┌─────────────────────────────────────────────┐
│              PyQt5 GUI (main.py)            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ TextEdit │  │ ComboBox │  │  Button  │  │
│  │(会話履歴) │  │(モデル選択)│  │(Listen) │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└──────────────────────┬──────────────────────┘
                       │
          ┌────────────▼────────────┐
          │   KeywordListener       │
          │  (Vosk オフライン認識)   │ ← 常時マイク監視
          └────────────┬────────────┘
                       │ "friday" 検出時
          ┌────────────▼────────────┐
          │  SpeechRecognition      │
          │ (Google Speech API)     │ ← 日本語音声→テキスト
          └────────────┬────────────┘
                       │
          ┌────────────▼────────────┐
          │      ルーティング        │
          ├─────────┬───────┬───────┤
          │  天気   │ニュース│予定   │ その他→GPT
          └────┬────┴───┬───┴───┬───┘
               │        │       │
          OpenWeather  NewsAPI schedule.json
               │        │       │
          └────┴────────┴───────┘
                       │
          ┌────────────▼────────────┐
          │  OpenAI TTS (nova)      │ ← テキスト→音声
          └────────────┬────────────┘
                       │
                  afplay / macOS
```

---

## ファイル構成

```
F.R.I.D.A.Y/
├── main.py                        # エントリーポイント・PyQt5 GUI アプリ
├── keyword_listener.py            # Vosk によるキーワード常時監視
├── speech_recognition_module.py   # Google Speech Recognition による音声入力
├── gpt_response.py                # OpenAI GPT による会話応答生成
├── weather.py                     # OpenWeatherMap による天気情報取得
├── news.py                        # NewsAPI による日本語ニュース取得
├── schedule.py                    # スケジュールの保存・参照（schedule.json）
├── text_to_speech.py              # OpenAI TTS による音声合成・再生
├── city_translation.py            # 日本語都市名→英語変換テーブル
├── handle_listen_and_respond.py   # 音声応答ハンドラ（開発用スタブ含む）
├── debug.py                       # デバッグ用モジュール
├── requirements.txt               # Python 依存パッケージ一覧
├── schedule.json                  # スケジュールデータ（実行時生成）
├── city.list.json                 # OpenWeatherMap 都市 ID データ
├── vosk-model-small-en-us-0.15/   # Vosk オフライン音声モデル（英語）
└── 起動音.mp3                      # キーワード検出時の通知音
```

---

## 必要環境

- **OS**: macOS（音声再生に `afplay` を使用）
- **Python**: 3.9 以上推奨
- **マイク**: 音声入力デバイスが必要
- **インターネット接続**: Google Speech Recognition・各種 API 呼び出しに必要

---

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/tk64-collab/F.R.I.D.A.Y.git
cd F.R.I.D.A.Y
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

> PyAudio のインストールに失敗する場合は、先に `portaudio` を導入してください。
> ```bash
> brew install portaudio
> pip install pyaudio
> ```

### 3. Vosk モデルの配置

`vosk-model-small-en-us-0.15` ディレクトリがリポジトリルートに存在することを確認してください。  
なければ [Vosk Models](https://alphacephei.com/vosk/models) からダウンロードして配置してください。

### 4. 環境変数の設定

```bash
export OPENAI_API_KEY="your_openai_api_key"
export OPENWEATHER_API_KEY="your_openweathermap_api_key"
export NEWS_API_KEY="your_newsapi_key"
```

---

## 使い方

```bash
python main.py
```

### 起動後の操作

| 操作方法 | 説明 |
|----------|------|
| **キーワード起動** | 「friday」と発話するとアシスタントが自動起動 |
| **Listen ボタン** | ボタンクリックで手動で音声入力を開始 |
| **モデル選択** | ドロップダウンで `gpt-3.5-turbo` または `gpt-4o` を選択 |

### 対応コマンド例

| 発話例 | 動作 |
|--------|------|
| `東京の天気` | 東京の現在の天気・気温を返答 |
| `ニュースを教えて` | 日本の最新ニュース 5 件を読み上げ |
| `予定を記録して 14時 会議` | 当日の予定を `schedule.json` に保存 |
| `予定を確認して` | 当日に登録された予定を一覧表示 |
| その他の発話 | GPT モデルが自由に回答 |

---

## 環境変数

| 変数名 | 用途 | 取得先 |
|--------|------|--------|
| `OPENAI_API_KEY` | GPT 応答・音声合成（TTS）| [OpenAI Platform](https://platform.openai.com/) |
| `OPENWEATHER_API_KEY` | 天気情報取得 | [OpenWeatherMap](https://openweathermap.org/api) |
| `NEWS_API_KEY` | 日本語ニュース取得 | [NewsAPI](https://newsapi.org/) |

---

## 現在の実装状況と今後の課題

### ✅ 実装済み

- [x] PyQt5 GUI（テキスト表示・モデル選択・Listen ボタン）
- [x] Vosk によるオフラインキーワード検出（"friday"）
- [x] Google Speech Recognition による日本語音声入力
- [x] OpenAI GPT（gpt-3.5-turbo / gpt-4o）による会話応答
- [x] OpenWeatherMap による天気情報取得（日本語都市名→英語変換対応）
- [x] NewsAPI による日本語ニュース取得（トップ 5 件）
- [x] JSON ベースのスケジュール保存・当日予定確認
- [x] OpenAI TTS（nova ボイス）による音声合成・再生

### ⚠️ 既知の課題・制限事項

- **macOS 専用**: `text_to_speech.py` の音声再生に `afplay`（macOS 標準）を使用しているため、Windows・Linux では動作しない
- **Vosk モデルが英語のみ**: キーワード検出に使用している Vosk モデルは英語専用（`vosk-model-small-en-us-0.15`）。日本語キーワードには対応していない
- **都市変換テーブルが限定的**: `city_translation.py` に登録されていない都市名は天気検索に失敗する
- **音声認識がオンライン依存**: 音声入力（Google Speech Recognition）はインターネット接続が必須
- **`handle_listen_and_respond.py` にスタブコードが残存**: `debug.py` と `handle_listen_and_respond.py` に開発途中のデバッグ用コードが含まれている
- **スケジュール機能の解析が単純**: キーワードマッチングによる処理のため、複雑な自然言語での予定入力には対応できない

### 🔲 今後の改善案

- [ ] Windows・Linux への対応（クロスプラットフォームな音声再生ライブラリへの移行）
- [ ] 日本語キーワード検出対応（日本語 Vosk モデルの導入）
- [ ] 都市変換テーブルの拡充
- [ ] スケジュール管理機能の強化（時刻指定・編集・削除など）
- [ ] GUI のデザイン改善
- [ ] テストコードの整備
