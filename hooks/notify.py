#!/usr/bin/env python3
import json
import math
import re
import struct
import subprocess
import sys


class Notification:
    RATE: int = 44100
    VOL: float = 0.35
    FADE: float = 0.015
    TASK_NOTIFICATION_PATTERN: re.Pattern[str] = re.compile(
        r"<task-notification>.*?<task-id>([^<]+)</task-id>.*?</task-notification>",
        re.DOTALL,
    )

    @classmethod
    def _tone(cls, freq: float, dur: float) -> list[int]:
        n = int(cls.RATE * dur)
        fade_n = int(cls.RATE * cls.FADE)
        out: list[int] = []
        for i in range(n):
            v = math.sin(2 * math.pi * freq * i / cls.RATE)
            if i < fade_n:
                v *= i / fade_n
            elif i > n - fade_n:
                v *= (n - i) / fade_n
            out.append(int(v * cls.VOL * 32767))
        return out

    @classmethod
    def _note(cls, freq: float, gap: float) -> list[int]:
        note_dur = gap * 0.82
        rest_dur = gap - note_dur
        return cls._tone(freq, note_dur) + [0] * int(cls.RATE * rest_dur)

    @classmethod
    def _pending_background_task_ids(cls, transcript_path: str) -> set[str]:
        try:
            with open(transcript_path, encoding="utf-8") as handle:
                lines = handle.readlines()
        except OSError:
            return set()
        launched: set[str] = set()
        resolved: set[str] = set()
        for raw_line in lines:
            stripped = raw_line.strip()
            if not stripped:
                continue
            resolved.update(cls.TASK_NOTIFICATION_PATTERN.findall(stripped))
            try:
                entry = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            result = entry.get("toolUseResult")
            if isinstance(result, dict):
                task_id = result.get("agentId") or result.get("backgroundTaskId")
                if isinstance(task_id, str):
                    launched.add(task_id)
        return launched - resolved

    @classmethod
    def should_play(cls) -> bool:
        try:
            hook_input = json.load(sys.stdin)
        except (json.JSONDecodeError, ValueError):
            return True
        if not isinstance(hook_input, dict):
            return True
        transcript_path = hook_input.get("transcript_path")
        if not isinstance(transcript_path, str) or not transcript_path:
            return True
        return not cls._pending_background_task_ids(transcript_path)

    @classmethod
    def play(cls) -> None:
        score: list[tuple[float, float]] = [
            (523.3, 0.15),
            (659.3, 0.15),
            (784.0, 0.40),
        ]
        samples: list[int] = []
        for freq, gap in score:
            samples.extend(cls._note(freq, gap))
        data = struct.pack(f"<{len(samples)}h", *samples)
        proc = subprocess.Popen(
            ["pacat", "--rate", str(cls.RATE), "--channels", "1", "--format", "s16le"],
            stdin=subprocess.PIPE,
        )
        assert proc.stdin is not None
        proc.stdin.write(data)
        proc.stdin.close()
        proc.wait()


if __name__ == "__main__":
    if Notification.should_play():
        Notification.play()
