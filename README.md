# ai-tell-check

**English** · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

An agent skill that rates the **AI tell** of every asset in game and app art. An AI tell is anything that makes a player think "this was made by generative AI". The skill works on image files and screen captures, so it does not depend on the engine (Unity, Unreal, Godot, Cocos/Axmol, web).

## Install

```bash
npx skills add dlstjd0237/ai-tell-check -g
```

This installs the skill for Claude Code, Codex, Cursor, OpenCode, and others. To install for a single tool, add a flag such as `-a claude-code`. To install by hand, copy the `skills/ai-tell-check` folder into `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (Codex and others).

The measuring script needs Python 3.9 or later. Install its dependencies into a venv:

```bash
python -m venv .venv
.venv/bin/pip install -r skills/ai-tell-check/scripts/requirements.txt   # Windows: .venv\Scripts\pip
```

## Usage

```
/ai-tell-check Assets/Art/Background
```

Or just ask: "Run ArtQA on this folder. Does anything look AI-generated?"

The agent:

1. Checks provenance. It reads generator metadata and compares assets with generated outputs and earlier git versions, which also catches recolors and cut-outs.
2. Checks visible signals: broken perspective, mirrored layouts, melted detail, cut-out halos, style clashes, and more.
3. Gives each asset exactly one verdict: **Strong / Medium / Weak / None**.
4. Writes a report with evidence images and a fix order.

## Using the measuring tool alone

```bash
python skills/ai-tell-check/scripts/aitell.py meta  a.png model.glb        # generator metadata and strings
python skills/ai-tell-check/scripts/aitell.py match asset.png gen1.png     # same image as (part of) a generated output?
python skills/ai-tell-check/scripts/aitell.py sym   bg.png --bottom 0.35   # left-right mirror layout
python skills/ai-tell-check/scripts/aitell.py color a.png b.png            # chroma, purple-pink share, edge color
python skills/ai-tell-check/scripts/aitell.py selftest
```

## Notes

- Pixels alone cannot prove that an image is AI-generated. Verdicts rest on provenance and visible signals.
- AI-detector model scores are not used. Most are trained on photos and are unreliable on illustration.

## License

MIT
