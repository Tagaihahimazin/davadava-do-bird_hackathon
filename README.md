# davadava

VoiceOS + MCP で動く音声 DJ アプリ。タスク・モチベーション・ドライブの目的地に応じて Spotify の曲を推薦・再生する。

## できること

### ドライブモード
- 目的地に応じた選曲 (ビーチ、山、都市、高速、田舎道、夜ドライブ、デート)
- 気分 + 時間帯を加味したスマート推薦
- ハンズフリーで音声操作

### タスク・モチベーションモード
- 作業内容に応じた BGM (集中、運動、リラックス、クリエイティブ)
- モチベーションレベルに合わせた曲調の調整

### 基本操作
- 再生 / 一時停止 / スキップ / 前の曲
- 音量調整 & スムーズフェード
- シャッフル / リピート
- 曲の検索・直接再生

## セットアップ

```bash
pip install -r requirements.txt
```

Google Mapsのルート計算を使う場合は API キーを設定:

```bash
export GOOGLE_MAPS_API_KEY="YOUR_API_KEY"
```

必要API: `Directions API`

Anthropicで移動時間推定を使う場合:

```bash
export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY"
# 任意
export ANTHROPIC_MODEL="claude-3-5-sonnet-latest"
```

Spotify Web APIで検索を使う場合:

```bash
export SPOTIFY_CLIENT_ID="YOUR_SPOTIFY_CLIENT_ID"
export SPOTIFY_CLIENT_SECRET="YOUR_SPOTIFY_CLIENT_SECRET"
```

## VoiceOS への接続

1. VoiceOS を開く
2. **設定 → 連携 → カスタム連携** に移動
3. **追加** → 名前: `davadava-dj` → 起動コマンド:

```bash
python3 /path/to/davadava/src/dj_server.py
```

## 音声コマンド例

| 話しかけ方 | 実行される機能 |
|-----------|--------------|
| 「海に向かうからいい曲かけて」 | ビーチドライブ向け選曲 |
| 「渋谷から横浜までドライブセッション開始して」 | Spotify起動 + Googleマップ起動 + ルート時間連動で再生 |
| 「渋谷から横浜までの時間を見て、合う曲を流して」 | ルート距離/時間を取得して最適プレイリスト再生 |
| 「渋谷から箱根まで80kmくらい。時間を予測して合う曲かけて」 | Anthropicで所要時間を推定して最適プレイリスト再生 |
| 「夜のドライブに合う曲」 | 夜ドライブ向けの lo-fi / R&B |
| 「集中したいから作業用BGM流して」 | 集中向け lo-fi / ambient |
| 「テンション上げたい」 | ハイエネルギーな曲 |
| 「プレイリスト Chill Hits を流して」 | ライブラリ内のプレイリスト名で直接再生 |
| 「ずっと真夜中でいいのに。のプレイリスト探して流して」 | Spotify検索 + Anthropic選定で再生 |
| 「次の曲」 | スキップ |
| 「音量下げて」 | 音量調整 |
| 「今なんの曲?」 | 曲情報を返答 |

## ドキュメント

- [VoiceOS MCP できること一覧](docs/voiceos-mcp-overview.md)

## Anthropic向け時間予測プロンプト（実装済み）

`anthropic_eta_prompt(origin, destination, distance_km, departure_context)` で確認可能。

要点:
- 出発地 / 目的地 / 距離(km) / 補足コンテキストを渡す
- 都市部・郊外推定、渋滞ゆらぎ込みでレンジ予測
- 返却形式を厳密JSONに固定

期待するJSON:
```json
{
  "minutes_low": 55,
  "minutes_mid": 75,
  "minutes_high": 105,
  "confidence": "medium",
  "rationale": "夕方の都心流入で混雑しやすく、平均速度が落ちるため"
}
```
