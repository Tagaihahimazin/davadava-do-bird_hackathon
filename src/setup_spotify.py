"""Spotify API 認証セットアップスクリプト.

初回実行時にブラウザが開き、Spotify にログインして認証を完了します。
一度認証すればトークンがキャッシュされ、以降は自動で認証されます。

使い方:
    1. .env ファイルに SPOTIPY_CLIENT_ID と SPOTIPY_CLIENT_SECRET を設定
    2. python3.11 setup_spotify.py を実行
    3. ブラウザでSpotifyにログインして許可
    4. リダイレクトされたURLをターミナルに貼り付け
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

missing = []
if not os.environ.get("SPOTIPY_CLIENT_ID"):
    missing.append("SPOTIPY_CLIENT_ID")
if not os.environ.get("SPOTIPY_CLIENT_SECRET"):
    missing.append("SPOTIPY_CLIENT_SECRET")

if missing:
    print("=" * 60)
    print("Spotify API の認証情報が必要です!")
    print("=" * 60)
    print()
    print("1. https://developer.spotify.com/dashboard にアクセス")
    print("2. 「Create app」でアプリを作成")
    print("   - App name: davadava-dj")
    print("   - Redirect URI: http://localhost:8888/callback")
    print("3. 作成後、Settings から Client ID と Client Secret をコピー")
    print("4. src/.env ファイルを作成して以下を記入:")
    print()
    print("   SPOTIPY_CLIENT_ID=ここにClient ID")
    print("   SPOTIPY_CLIENT_SECRET=ここにClient Secret")
    print("   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback")
    print()
    print(f"Missing: {', '.join(missing)}")
    sys.exit(1)

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-modify-playback-state user-read-playback-state user-read-currently-playing",
    cache_path=os.path.join(os.path.dirname(__file__), ".spotify_cache"),
))

user = sp.current_user()
print(f"認証成功! ログインユーザー: {user['display_name']} ({user['id']})")
print("トークンがキャッシュされました。以降は自動認証されます。")
