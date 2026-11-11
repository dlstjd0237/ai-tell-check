---
name: ai-tell-check
description: Use when doing ArtQA on game or app art (backgrounds, props, icons, characters, 3D models, UI, logos) for a commercial release, or when someone asks whether assets look AI-generated — "AI slop", "looks AI-made", "AI 티", "AI感", "AIっぽい". Engine-agnostic (Unity, Unreal, Godot, Cocos/Axmol, web).
---

# AI-tell check (ArtQA)

**An AI tell is anything that makes a player think "this was made by generative AI".** Pixels alone cannot prove that an image is AI-generated, so judge each asset on its **provenance** and its **visible signals**. Do not use AI-detector model scores as evidence: most are trained on photos and are unreliable on illustration.

## 1. Collect the targets (any engine)

Look at both: the **source image files** and the **real screen** (a capture at the game's actual resolution, or a composite built from the layout coordinates).

| Engine | Where source images live |
|---|---|
| Unity | `Assets/**` png/psd/tga; look at source sprites, not packed atlases |
| Unreal | `.uasset` is binary: find the source-art folder or export from the editor |
| Godot | `res://**` png; ignore `.godot/imported` |
| Cocos / Axmol / others | `Resources/`, `Content/`, `assets/`; for plist/atlas/FairyGUI/Spine atlases, find the individual source images |
| 3D | glb/fbx/obj and their textures |

## 2. Provenance — first, for every asset

Provenance is the strongest evidence. A clean-looking asset can still be a crop or a recolor of a generated image. The measuring tool is `scripts/aitell.py` in this skill's folder; its dependencies are in `scripts/requirements.txt`. Install them into a venv, never into a shared or conda environment. Self-check: `python scripts/aitell.py selftest`.

1. **Metadata and strings**: `aitell.py meta <files...>`. It finds ComfyUI/A1111 prompt chunks and 3D-generator markers (tripo, meshy, rodin, hunyuan, …).
2. **Compare with generated outputs**: `aitell.py match <asset> <candidates...>`. Find candidates in:
   - generation scripts in the repo (ComfyUI API calls, `prompt`, workflow JSON) and their output folders
   - ComfyUI `output/`, and `ComfyUI_*` / `exec-*` files in the downloads folder
   - **earlier git versions of the same asset**: `git log -- <path>`, then `git show <commit>:<path>`. Cut-out props usually come from an earlier single-piece image.
   - if none are found, ask the user where generated outputs are kept.
3. **Reading the numbers**:
   - `corr ≥ 0.95` means it is the same picture.
   - A high `same_px` as well means it was used as-is.
   - A high `corr` with a low `same_px` means it was only recolored.
   - In a crop search, a high value near `scale` 1.0 means it was cut out.

Record provenance as one of: `generated (evidence)` / `suspected generated` / `drawn by code` / `hand-made` / `unknown`.

## 3. Visible signals

Inspect each asset at 2–6× zoom, and note separately whether each signal is also visible at game size.

| Signal | How to check |
|---|---|
| Broken perspective or structure | vanishing points disagree, side faces show on the wrong side, floor-ellipse ratios differ per asset, walls or pillars stop mid-air |
| Mirror layout / duplication | in scenes and backgrounds, `aitell.py sym [--bottom 0.35]` ≥ 0.85 (skip objects that are symmetric by design); twin props; the same arrangement in every slot |
| Meaningless filler | scattered dots and pebbles, pipes or ornaments with no function, fine blotches on flat areas |
| Melted detail | fingers, paws, lettering, or pattern edges melting; checks or grids bending |
| Fake effects | bokeh, bloom, light rays, glow, depth of field |
| Stock generative recipe | thick uniform outline + airbrushed gradients + fine blotches; the same gloss on every object |
| Style clash | outline/shading rules differ between assets on one screen (e.g. lined cel sprites over a lineless painted background) |
| Palette | `aitell.py color` for purple–pink share and chroma (C); if there is a reference art style, compare it with the same metrics |
| Upscaled | true resolution is lower than display size (barely changes when downscaled and scaled back up) |
| Cut-out traces | white halos and background bleed (`edge_rgb` from `color`), leftover background bits, color left in transparent pixels |
| Stand-ins | emoji icons, template logos (font + stacked strokes + gradient), shared face parts and expression presets |

## 4. Verdict — exactly one of four

- **Strong**: a signal is visible at game size — one is enough if provenance is `generated`, otherwise two or more.
- **Medium**: several signals visible only when zoomed, or provenance is `generated` and signals show only when zoomed.
- **Weak**: provenance is `generated` but signals are barely visible, or there is a single zoom-only signal.
- **None**: provenance is not `generated` and there are no signals.

Recoloring, filtering, flipping, and cropping do not change provenance. Label such fixes "reduces visibility only".

## 5. Report format

Write in the user's language, in this order:

1. One-line summary: the asset with the strongest AI tell, and why
2. A per-asset table with **one row for every image asset** (a set made the same way may share a row)

   | Asset | Provenance | AI tell | Evidence (where, what, numbers) | Fix |
   |---|---|---|---|---|

3. Evidence images: at least one game-size screen, plus a zoomed crop for each signal
4. Fix order, with the size of each fix and whether code can do it or it needs an artist
5. Method and limits: what was compared, which candidates were not found, and that pixels alone cannot prove AI origin

## Fix principles

- When the cause is a generated image, the root fix is a **redraw or overpaint** by an artist. Keep it separate from code fixes that only reduce visibility.
- Cut-out halos, bleed, and transparent-pixel color are quick code fixes.
- If the user or the project has locked a design (a character, say), do not propose changing it; adjust the surroundings (background, UI, effects) to fit it.
