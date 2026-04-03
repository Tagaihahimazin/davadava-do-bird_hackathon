# VoiceOS MCP 統合 - できることの整理

## MCP (Model Context Protocol) とは

MCPサーバーを構築し、VoiceOSに接続することで、音声コマンドによるカスタム機能を実現するプロトコル。
VoiceOSがMCPクライアントとして動作し、MCPサーバーが提供するツールを音声経由で呼び出す。

## アーキテクチャ

```
ユーザー (音声) → VoiceOS → MCP Client → (Stdio転送) → MCP Server → 各種ツール実行
```

## できること一覧

### 1. スマートホーム制御
- Apple HomeKit デバイスの制御 (Apple Shortcuts 経由)
- 照明の ON/OFF、調光
- 温度調整 (エアコン、サーモスタット)
- 「電気を消して」などの自然言語命令に対応

### 2. Spotify 音楽操作
- AppleScript 経由で Spotify を制御
- 再生 / 一時停止
- 曲のスキップ (次へ/前へ)
- 現在再生中の楽曲情報の取得

### 3. macOS システム操作
- 音量の調整
- フォーカスモードの切り替え
- アプリケーションの起動
- バッテリー残量の確認

### 4. カスタムツール (自作可能)
- MCPサーバーを自作することで、任意の機能を音声で呼び出せる
- Python / TypeScript どちらでも実装可能

## 技術スタック

| 項目 | 選択肢 |
|------|--------|
| サーバー言語 | Python (`mcp` パッケージ) / TypeScript (`@modelcontextprotocol/sdk`) |
| バリデーション | Zod (TypeScript) |
| 通信方式 | Stdio 転送 |
| 実行形式 | 非同期対応 |

## セットアップ手順

### 1. 依存パッケージのインストール

**Python:**
```bash
pip install mcp
```

**TypeScript:**
```bash
npm install @modelcontextprotocol/sdk zod
```

### 2. MCPサーバーの作成

ツールを定義し、MCPサーバーとして公開する。

**Python 例:**
```python
from mcp import tool

@mcp.tool()
async def my_tool(param: str) -> str:
    """ツールの説明"""
    return "結果"
```

**TypeScript 例:**
```typescript
server.tool("my_tool", { param: z.string() }, async ({ param }) => {
  return "結果";
});
```

### 3. VoiceOS への接続

1. VoiceOS を開く
2. **設定 → 連携 → カスタム連携** に移動
3. **追加** をクリックし、名前と起動コマンドを設定

起動コマンド例:
```bash
# Python
python3 /path/to/my_mcp_server.py

# TypeScript
npx tsx /path/to/my-mcp-server.ts
```

## 提供テンプレート

| テンプレート | 用途 | 概要 |
|-------------|------|------|
| クイックスタート | 学習用 | 単一ツールの最小構成 |
| スマートホーム | HomeKit制御 | Apple Shortcuts 経由のデバイス制御 |
| Spotify | 音楽操作 | AppleScript による Spotify 制御 |
| システム操作 | macOS制御 | 音量・アプリ・バッテリーなどの操作 |
