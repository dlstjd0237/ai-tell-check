# ai-tell-check

게임·앱 아트에서 **AI 티**를 자산마다 판정하는 에이전트 스킬입니다. AI 티는 유저가 "생성형 AI 그림이네"라고 의심하게 만드는 신호를 말합니다. 그림 파일과 화면 캡처만 다루기 때문에 엔진에 상관없이 쓸 수 있습니다(Unity·Unreal·Godot·Cocos/Axmol·웹).

## 설치

```bash
npx skills add dlstjd0237/ai-tell-check -g
```

Claude Code, Codex, Cursor, OpenCode 등에 설치됩니다. 한 도구에만 넣으려면 `-a claude-code`처럼 지정하세요. 손으로 설치할 때는 `skills/ai-tell-check` 폴더를 `~/.claude/skills/`(Claude Code)나 `~/.agents/skills/`(Codex 등)에 복사하면 됩니다.

측정 스크립트는 Python 3.9 이상이 필요합니다. 의존성은 venv에 설치하세요.

```bash
python -m venv .venv
.venv/bin/pip install -r skills/ai-tell-check/scripts/requirements.txt   # Windows: .venv\Scripts\pip
```

## 사용

```
/ai-tell-check Assets/Art/Background
```

또는 "이 폴더 ArtQA 해 줘, AI 티 나는지 봐 줘"라고 말해도 됩니다.

에이전트가 하는 일은 다음과 같습니다.

1. 출처를 확인합니다. 생성 도구 메타데이터를 보고, 생성 결과물이나 git 이전 버전과 대조해 색만 바꾼 것·오려 낸 것까지 찾습니다.
2. 보이는 신호를 확인합니다. 원근 불일치, 거울 구도, 녹은 디테일, 누끼 흔적, 화풍 충돌 등입니다.
3. 자산마다 **강함 / 중간 / 약함 / 없음** 중 하나로 판정합니다.
4. 근거 이미지와 고칠 순서를 붙여 리포트를 냅니다.

## 측정 도구만 쓰기

```bash
python skills/ai-tell-check/scripts/aitell.py meta  a.png model.glb        # 생성 도구 메타데이터·문자열
python skills/ai-tell-check/scripts/aitell.py match asset.png gen1.png     # 생성 결과물(의 일부)과 같은 그림인지
python skills/ai-tell-check/scripts/aitell.py sym   bg.png --bottom 0.35   # 좌우 거울 구도
python skills/ai-tell-check/scripts/aitell.py color a.png b.png            # 채도·보라핑크 비율·가장자리 색
python skills/ai-tell-check/scripts/aitell.py selftest
```

## 주의

- 그림만 보고 AI 여부를 확정할 수는 없습니다. 이 스킬의 판정은 출처와 보이는 신호를 근거로 한 것입니다.
- 판별 모델 점수는 쓰지 않습니다. 대부분 사진으로 학습해서 일러스트에서는 잘 틀립니다.

## 라이선스

MIT
