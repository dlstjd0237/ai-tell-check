"""Measurements for AI-tell checks. A person or agent makes the verdict; this only prints evidence numbers."""
import argparse, json, re, sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

GEN_MARKERS = rb"tripo|meshy|rodin|hunyuan|trellis|comfyui|stable.?diffusion|midjourney|dall.?e|firefly|flux|qwen|z-image|sdxl|novelai|c2pa"


def load(path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im)
    return a[..., :3], a[..., 3]


def meta(paths):
    for p in paths:
        p = Path(p)
        found = {}
        if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            info = Image.open(p).info
            found = {k: str(v)[:200] for k, v in info.items() if k.lower() in ("prompt", "workflow", "parameters", "comment", "description", "software", "xml:com.adobe.xmp", "exif")}
        hits = sorted({m.decode(errors="ignore").lower() for m in re.findall(GEN_MARKERS, p.read_bytes(), re.I)})
        print(json.dumps({"file": p.name, "meta": found, "markers": hits}, ensure_ascii=False))


def match(asset, candidates):
    """Is the asset the same image as a candidate (generated output), or a crop of one?"""
    rgb, alpha = load(asset)
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    mask = (alpha > 128).astype(np.float32)
    h, w = g.shape
    for c in candidates:
        crgb, _ = load(c)
        cg = cv2.cvtColor(crgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
        H, W = cg.shape
        best = (-1.0, 1.0, (0, 0))
        top = min(H / h, W / w)
        for s in np.unique(np.r_[np.geomspace(max(top * 0.15, 8 / min(h, w)), top, 40), top, 1.0]):
            th, tw = int(h * s), int(w * s)
            if th < 8 or tw < 8 or th > H or tw > W:
                continue
            t = cv2.resize(g, (tw, th), interpolation=cv2.INTER_AREA)
            m = cv2.resize(mask, (tw, th), interpolation=cv2.INTER_NEAREST)
            r = cv2.matchTemplate(cg, t, cv2.TM_CCOEFF_NORMED, mask=m)
            r[~np.isfinite(r)] = -1
            _, v, _, loc = cv2.minMaxLoc(r)
            if v > best[0]:
                best = (v, s, loc)
        v, s, (x, y) = best
        th, tw = int(h * s), int(w * s)
        t = cv2.resize(rgb, (tw, th), interpolation=cv2.INTER_AREA).astype(int)
        m = cv2.resize(alpha, (tw, th), interpolation=cv2.INTER_NEAREST) > 128
        same = (np.abs(t - crgb[y:y + th, x:x + tw].astype(int)).max(-1) <= 12)[m].mean()
        print(json.dumps({"asset": Path(asset).name, "candidate": Path(c).name, "corr": round(float(v), 3),
                          "same_px": round(float(same), 3), "scale": round(float(s), 3), "at": [int(x), int(y)]}, ensure_ascii=False))


def sym(paths, bottom):
    """Left-right mirror symmetry (flip correlation). 0.85 or more suggests a mirrored layout."""
    for p in paths:
        rgb, alpha = load(p)
        g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
        g[alpha < 128] = g[alpha >= 128].mean() if (alpha >= 128).any() else 0
        if bottom:
            g = g[int(g.shape[0] * (1 - bottom)):]
        print(json.dumps({"file": Path(p).name, "mirror_corr": round(float(np.corrcoef(g.ravel(), g[:, ::-1].ravel())[0, 1]), 3)}))


def color(paths):
    """Median Lab lightness/chroma of opaque pixels, purple-pink share, dark share, and edge color."""
    for p in paths:
        rgb, alpha = load(p)
        op = alpha >= 250
        lab = cv2.cvtColor((rgb[op][None] / 255.0).astype(np.float32), cv2.COLOR_RGB2LAB)[0]
        C = np.hypot(lab[:, 1], lab[:, 2])
        hsv = cv2.cvtColor(rgb[op][None], cv2.COLOR_RGB2HSV_FULL)[0].astype(float)
        hue, sat, val = hsv[:, 0] * 360 / 255, hsv[:, 1] / 255, hsv[:, 2] / 255
        colored = (sat > 0.2) & (val > 0.15)
        edge = (alpha > 0) & (alpha < 250)
        out = {"file": Path(p).name, "L": round(float(np.median(lab[:, 0])), 1), "C": round(float(np.median(C)), 1),
               "b": round(float(np.median(lab[:, 2])), 1), "C_p90": round(float(np.percentile(C, 90)), 1),
               "purple_pink": round(float(((hue >= 260) & (hue <= 345) & colored).sum() / max(colored.sum(), 1)), 2),
               "dark": round(float((lab[:, 0] < 25).mean()), 2)}
        if edge.any():
            out["edge_rgb"] = [int(v) for v in np.median(rgb[edge], 0)]
            out["edge_px"] = int(edge.sum())
        print(json.dumps(out, ensure_ascii=False))


def selftest():
    import tempfile
    from PIL import PngImagePlugin
    d = Path(tempfile.mkdtemp())
    rng = np.random.default_rng(0)
    big = cv2.GaussianBlur(rng.integers(0, 255, (300, 400, 3), dtype=np.uint8), (0, 0), 3)
    Image.fromarray(big).save(d / "gen.png")
    Image.fromarray(np.dstack([big[50:150, 100:220], np.full((100, 120), 255, np.uint8)])).resize((60, 50)).save(d / "cut.png")
    half = rng.integers(0, 255, (64, 32, 3), dtype=np.uint8)
    Image.fromarray(np.hstack([half, half[:, ::-1]])).save(d / "mirror.png")
    pi = PngImagePlugin.PngInfo(); pi.add_text("prompt", '{"3": {"class_type": "KSampler"}}')
    Image.fromarray(half).save(d / "meta.png", pnginfo=pi)
    import contextlib, io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        match(d / "cut.png", [d / "gen.png"]); sym([d / "mirror.png"], 0); meta([d / "meta.png"]); color([d / "gen.png"])
    rows = [json.loads(x) for x in buf.getvalue().splitlines()]
    assert rows[0]["corr"] > 0.9 and abs(rows[0]["at"][0] - 100) <= 3, rows[0]
    assert rows[1]["mirror_corr"] > 0.99, rows[1]
    assert "prompt" in rows[2]["meta"] and "comfyui" not in rows[2]["markers"], rows[2]
    assert 0 <= rows[3]["purple_pink"] <= 1, rows[3]
    print("selftest ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("meta", help="generator metadata and string markers").add_argument("files", nargs="+")
    m = sub.add_parser("match", help="same image as (part of) a generated output?"); m.add_argument("asset"); m.add_argument("candidates", nargs="+")
    s = sub.add_parser("sym", help="left-right mirror symmetry"); s.add_argument("files", nargs="+"); s.add_argument("--bottom", type=float, default=0, help="only the bottom fraction, e.g. 0.35")
    sub.add_parser("color", help="Lab lightness/chroma, purple-pink and dark share, edge color").add_argument("files", nargs="+")
    sub.add_parser("selftest")
    a = ap.parse_args()
    {"meta": lambda: meta(a.files), "match": lambda: match(a.asset, a.candidates), "sym": lambda: sym(a.files, a.bottom),
     "color": lambda: color(a.files), "selftest": selftest}[a.cmd]()
