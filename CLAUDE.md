# CLAUDE.md

## プロジェクト概要
davadava - VoiceOS MCP 音声 DJ アプリ。
タスク・モチベーション・ドライブの目的地に応じて Spotify の曲を推薦・再生する。

## 技術スタック
- Python 3
- `mcp` (FastMCP) - MCP サーバーフレームワーク
- AppleScript (osascript) - Spotify / macOS 制御

## ディレクトリ構成
```
src/
  dj_server.py    - MCPサーバー (エントリポイント)
  spotify.py      - Spotify操作ヘルパー (AppleScript)
  recommender.py  - 曲推薦エンジン (タスク/モチベ/ドライブ)
docs/
  voiceos-mcp-overview.md - VoiceOS MCP 機能一覧
```

## 開発コマンド
```bash
pip install -r requirements.txt    # 依存関係
python3 src/dj_server.py           # MCPサーバー起動
```

## 設計方針
- VoiceOS の AI がツールの description を読んで音声→ツールのマッピングを行う
- description は英語で書く（VoiceOS の AI が解釈しやすいため）
- 推薦ロジックは recommender.py に集約し、dj_server.py はMCPツール定義に専念
- Spotify操作は spotify.py に集約し、AppleScript の詳細を隠蔽
