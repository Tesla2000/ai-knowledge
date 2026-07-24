#!/usr/bin/env python3
import json
import math
import re
import struct
import subprocess
import sys
from pathlib import Path


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
    def _agent_transcript_is_complete(cls, subagents_dir: Path, agent_id: str) -> bool:
        agent_file = subagents_dir / f"agent-{agent_id}.jsonl"
        try:
            with open(agent_file, encoding="utf-8") as handle:
                lines = handle.readlines()
        except OSError:
            return False
        for raw_line in reversed(lines):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                entry = json.loads(stripped)
            except json.JSONDecodeError:
                return False
            message = entry.get("message")
            if not isinstance(message, dict):
                return False
            return entry.get("type") == "assistant" and message.get("stop_reason") is not None
        return False

    @classmethod
    def _pending_background_task_ids(cls, transcript_path: str) -> set[str]:
        try:
            with open(transcript_path, encoding="utf-8") as handle:
                lines = handle.readlines()
        except OSError:
            return set()
        agent_ids: set[str] = set()
        background_task_ids: set[str] = set()
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
            if not isinstance(result, dict):
                continue
            agent_id = result.get("agentId")
            if isinstance(agent_id, str):
                agent_ids.add(agent_id)
                continue
            background_task_id = result.get("backgroundTaskId")
            if isinstance(background_task_id, str):
                background_task_ids.add(background_task_id)

        # Agent-tool launches get their own sidechain transcript
        # (<session>/subagents/agent-<id>.jsonl) that's independent of this
        # transcript and survives /compact, so completion is checked there
        # directly instead of relying on notification text surviving in
        # this (possibly-compacted) transcript. Other background tasks
        # (e.g. Bash run_in_background) have no equivalent file, so they
        # still rely on the notification-text match.
        subagents_dir = (
            Path(transcript_path).parent / Path(transcript_path).stem / "subagents"
        )
        pending_agents = {
            agent_id
            for agent_id in agent_ids
            if not cls._agent_transcript_is_complete(subagents_dir, agent_id)
        }
        pending_background_tasks = background_task_ids - resolved
        return pending_agents | pending_background_tasks

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
