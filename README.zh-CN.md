# ai-tell-check

[English](README.md) · **简体中文** · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

一个为游戏和应用美术逐个资源判定 **"AI 感"** 的智能体技能。"AI 感"指任何会让玩家觉得"这是生成式 AI 画的"的迹象。它只处理图片文件和屏幕截图，因此与引擎无关（Unity、Unreal、Godot、Cocos/Axmol、Web）。

## 安装

```bash
npx skills add dlstjd0237/ai-tell-check -g
```

可安装到 Claude Code、Codex、Cursor、OpenCode 等。只想装到某一个工具时，加上 `-a claude-code` 之类的参数。手动安装时，把 `skills/ai-tell-check` 文件夹复制到 `~/.claude/skills/`（Claude Code）或 `~/.agents/skills/`（Codex 等）。

测量脚本需要 Python 3.9 及以上。请把依赖安装到 venv 中：

```bash
python -m venv .venv
.venv/bin/pip install -r skills/ai-tell-check/scripts/requirements.txt   # Windows: .venv\Scripts\pip
```

## 用法

```
/ai-tell-check Assets/Art/Background
```

也可以直接说："对这个文件夹做 ArtQA，看看有没有 AI 感。"

智能体会：

1. 核查来源。读取生成工具的元数据，并与生成结果和 git 历史版本比对，连只改了颜色或抠出来的资源也能找出。
2. 检查可见迹象：透视错误、镜像构图、融化的细节、抠图残边、画风冲突等。
3. 给每个资源一个判定：**强 / 中 / 弱 / 无**。
4. 输出附带证据图和修改顺序的报告。

## 单独使用测量工具

```bash
python skills/ai-tell-check/scripts/aitell.py meta  a.png model.glb        # 生成工具元数据与字符串
python skills/ai-tell-check/scripts/aitell.py match asset.png gen1.png     # 是否与生成结果（的一部分）为同一张图
python skills/ai-tell-check/scripts/aitell.py sym   bg.png --bottom 0.35   # 左右镜像构图
python skills/ai-tell-check/scripts/aitell.py color a.png b.png            # 彩度、紫粉占比、边缘颜色
python skills/ai-tell-check/scripts/aitell.py selftest
```

## 注意

- 仅凭像素无法证明一张图是 AI 生成的。判定依据是来源和可见迹象。
- 不使用 AI 检测模型的分数。它们大多用照片训练，对插画不可靠。

## 许可证

MIT
