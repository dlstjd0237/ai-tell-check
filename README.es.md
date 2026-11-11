# ai-tell-check

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Español**

Una skill para agentes que califica el **aspecto de IA** de cada recurso en el arte de juegos y apps. El aspecto de IA es cualquier señal que haga pensar a un jugador "esto lo hizo una IA generativa". La skill trabaja con archivos de imagen y capturas de pantalla, así que no depende del motor (Unity, Unreal, Godot, Cocos/Axmol, web).

## Instalación

```bash
npx skills add dlstjd0237/ai-tell-check -g
```

Se instala en Claude Code, Codex, Cursor, OpenCode y otros. Para instalarla en una sola herramienta, añade una opción como `-a claude-code`. Para instalarla a mano, copia la carpeta `skills/ai-tell-check` en `~/.claude/skills/` (Claude Code) o en `~/.agents/skills/` (Codex y otros).

El script de medición necesita Python 3.9 o posterior. Instala sus dependencias en un venv:

```bash
python -m venv .venv
.venv/bin/pip install -r skills/ai-tell-check/scripts/requirements.txt   # Windows: .venv\Scripts\pip
```

## Uso

```
/ai-tell-check Assets/Art/Background
```

O simplemente pide: "Haz ArtQA de esta carpeta. ¿Algo parece hecho con IA?"

El agente:

1. Comprueba el origen. Lee los metadatos del generador y compara los recursos con las salidas generadas y con versiones anteriores en git, lo que también detecta recursos solo recoloreados o recortados.
2. Comprueba las señales visibles: perspectiva rota, composiciones en espejo, detalles derretidos, halos de recorte, choques de estilo y más.
3. Da a cada recurso un solo veredicto: **Fuerte / Medio / Débil / Ninguno**.
4. Entrega un informe con imágenes de evidencia y un orden de corrección.

## Usar solo la herramienta de medición

```bash
python skills/ai-tell-check/scripts/aitell.py meta  a.png model.glb        # metadatos y cadenas del generador
python skills/ai-tell-check/scripts/aitell.py match asset.png gen1.png     # ¿misma imagen que (parte de) una salida generada?
python skills/ai-tell-check/scripts/aitell.py sym   bg.png --bottom 0.35   # composición en espejo izquierda-derecha
python skills/ai-tell-check/scripts/aitell.py color a.png b.png            # croma, proporción morado-rosa, color de borde
python skills/ai-tell-check/scripts/aitell.py selftest
```

## Notas

- Los píxeles por sí solos no prueban que una imagen sea generada por IA. Los veredictos se basan en el origen y en las señales visibles.
- No se usan puntuaciones de modelos detectores de IA. La mayoría se entrenaron con fotos y no son fiables con ilustraciones.

## Licencia

MIT
