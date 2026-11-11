# ai-tell-check

[English](README.md) · [简体中文](README.zh-CN.md) · **繁體中文** · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

一個為遊戲與應用程式美術逐一資源判定 **「AI 感」** 的代理技能。「AI 感」指任何會讓玩家覺得「這是生成式 AI 畫的」的跡象。它只處理圖片檔與螢幕截圖，因此與引擎無關（Unity、Unreal、Godot、Cocos/Axmol、Web）。

## 安裝

```bash
npx skills add dlstjd0237/ai-tell-check -g
```

可安裝到 Claude Code、Codex、Cursor、OpenCode 等。只想裝到某一個工具時，加上 `-a claude-code` 之類的參數。手動安裝時，把 `skills/ai-tell-check` 資料夾複製到 `~/.claude/skills/`（Claude Code）或 `~/.agents/skills/`（Codex 等）。

測量腳本需要 Python 3.9 以上。請把相依套件安裝到 venv 中：

```bash
python -m venv .venv
.venv/bin/pip install -r skills/ai-tell-check/scripts/requirements.txt   # Windows: .venv\Scripts\pip
```

## 用法

```
/ai-tell-check Assets/Art/Background
```

也可以直接說：「對這個資料夾做 ArtQA，看看有沒有 AI 感。」

代理會：

1. 查核來源。讀取生成工具的中繼資料，並與生成結果和 git 歷史版本比對，連只改了顏色或去背切出來的資源也能找出。
2. 檢查可見跡象：透視錯誤、鏡像構圖、融化的細節、去背殘邊、畫風衝突等。
3. 給每個資源一個判定：**強 / 中 / 弱 / 無**。
4. 輸出附有證據圖與修改順序的報告。

## 單獨使用測量工具

```bash
python skills/ai-tell-check/scripts/aitell.py meta  a.png model.glb        # 生成工具中繼資料與字串
python skills/ai-tell-check/scripts/aitell.py match asset.png gen1.png     # 是否與生成結果（的一部分）為同一張圖
python skills/ai-tell-check/scripts/aitell.py sym   bg.png --bottom 0.35   # 左右鏡像構圖
python skills/ai-tell-check/scripts/aitell.py color a.png b.png            # 彩度、紫粉比例、邊緣顏色
python skills/ai-tell-check/scripts/aitell.py selftest
```

## 注意

- 僅憑像素無法證明一張圖是 AI 生成的。判定依據是來源與可見跡象。
- 不使用 AI 偵測模型的分數。它們大多以照片訓練，對插畫不可靠。

## 授權

MIT
