# ai-tell-check

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · **日本語** · [한국어](README.ko.md) · [Español](README.es.md)

ゲームやアプリのアートを素材ごとに **「AIっぽさ」** で判定するエージェントスキルです。「AIっぽさ」とは、プレイヤーに「これは生成AIで作られた絵だ」と思わせるあらゆる兆候のことです。画像ファイルと画面キャプチャだけを扱うので、エンジンを問いません（Unity・Unreal・Godot・Cocos/Axmol・Web）。

## インストール

```bash
npx skills add dlstjd0237/ai-tell-check -g
```

Claude Code・Codex・Cursor・OpenCode などにインストールされます。特定のツールだけに入れる場合は `-a claude-code` のように指定します。手動でインストールする場合は、`skills/ai-tell-check` フォルダを `~/.claude/skills/`（Claude Code）または `~/.agents/skills/`（Codex など）にコピーしてください。

計測スクリプトには Python 3.9 以上が必要です。依存パッケージは venv にインストールしてください。

```bash
python -m venv .venv
.venv/bin/pip install -r skills/ai-tell-check/scripts/requirements.txt   # Windows: .venv\Scripts\pip
```

## 使い方

```
/ai-tell-check Assets/Art/Background
```

「このフォルダの ArtQA をして、AIっぽいところがないか見て」と頼むだけでも動きます。

エージェントは次のことを行います。

1. 出どころを確認します。生成ツールのメタデータを読み、生成結果や git の過去バージョンと照合して、色だけ変えた素材や切り抜いた素材も見つけます。
2. 目に見える兆候を確認します。パースの破綻、左右対称の構図、溶けたディテール、切り抜きの縁残り、画風の衝突などです。
3. 素材ごとに **強 / 中 / 弱 / なし** のいずれかで判定します。
4. 根拠画像と修正の順番をつけたレポートを出します。

## 計測ツールだけを使う

```bash
python skills/ai-tell-check/scripts/aitell.py meta  a.png model.glb        # 生成ツールのメタデータ・文字列
python skills/ai-tell-check/scripts/aitell.py match asset.png gen1.png     # 生成結果（の一部）と同じ絵か
python skills/ai-tell-check/scripts/aitell.py sym   bg.png --bottom 0.35   # 左右の鏡像構図
python skills/ai-tell-check/scripts/aitell.py color a.png b.png            # 彩度・紫〜ピンクの割合・縁の色
python skills/ai-tell-check/scripts/aitell.py selftest
```

## 注意

- 画素だけで AI 生成かどうかを証明することはできません。判定は出どころと目に見える兆候に基づきます。
- AI 判定モデルのスコアは使いません。多くは写真で学習しており、イラストでは当てになりません。

## ライセンス

MIT
