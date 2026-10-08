#!/usr/bin/env python3
"""Combine local pyannote speaker diarization with whisper.cpp JSON output.

No audio is uploaded.  The pyannote pipeline is loaded from a local directory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook


def load_whisper_segments(json_path: Path) -> list[dict]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    segments = data.get("transcription", data.get("segments", []))
    parsed = []
    for item in segments:
        offsets = item.get("offsets", {})
        start = offsets.get("from")
        end = offsets.get("to")
        if start is None or end is None:
            # Alternative JSON layout used by some whisper.cpp releases.
            start = item.get("start")
            end = item.get("end")
            if isinstance(start, float):
                start = round(start * 1000)
            if isinstance(end, float):
                end = round(end * 1000)
        text = item.get("text", "").strip()
        if start is not None and end is not None and text:
            parsed.append({"start": float(start) / 1000, "end": float(end) / 1000, "text": text})
    if not parsed:
        raise ValueError("No timed segments found in the whisper.cpp JSON file.")
    return parsed


def fmt(seconds: float) -> str:
    total = round(seconds)
    return f"{total // 3600:02d}:{(total % 3600) // 60:02d}:{total % 60:02d}"


def choose_speaker(start: float, end: float, turns: list[tuple[float, float, str]]) -> str:
    overlap: dict[str, float] = {}
    midpoint = (start + end) / 2
    closest: tuple[float, str] | None = None
    for turn_start, turn_end, speaker in turns:
        duration = max(0.0, min(end, turn_end) - max(start, turn_start))
        overlap[speaker] = overlap.get(speaker, 0.0) + duration
        distance = 0.0 if turn_start <= midpoint <= turn_end else min(abs(midpoint - turn_start), abs(midpoint - turn_end))
        if closest is None or distance < closest[0]:
            closest = (distance, speaker)
    if overlap and max(overlap.values()) > 0:
        return max(overlap, key=overlap.get)
    return closest[1] if closest else "UNKNOWN"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a speaker-labelled transcript entirely locally.")
    parser.add_argument("--audio", required=True, help="16 kHz mono WAV input")
    parser.add_argument("--whisper-json", required=True, help="JSON created by whisper-cli -oj")
    parser.add_argument("--pipeline", required=True, help="Local pyannote Community-1 model folder")
    parser.add_argument("--output", required=True, help="Output text file")
    parser.add_argument("--speakers", type=int, help="Exact number of speakers, e.g. 3 or 4")
    args = parser.parse_args()

    pipeline = Pipeline.from_pretrained(args.pipeline)
    kwargs = {"num_speakers": args.speakers} if args.speakers else {}
    with ProgressHook() as hook:
        result = pipeline(args.audio, hook=hook, **kwargs)

    # Exclusive diarization assigns every moment to at most one speaker, which
    # makes joining it with Whisper segments more readable.
    annotation = getattr(result, "exclusive_speaker_diarization", None) or result.speaker_diarization
    turns = [(turn.start, turn.end, label) for turn, _, label in annotation.itertracks(yield_label=True)]
    segments = load_whisper_segments(Path(args.whisper_json))

    out = Path(args.output)
    with out.open("w", encoding="utf-8") as f:
        previous = None
        for segment in segments:
            speaker = choose_speaker(segment["start"], segment["end"], turns)
            if previous is not None and speaker != previous:
                f.write("\n")
            f.write(f"[{fmt(segment['start'])}] {speaker}: {segment['text']}\n")
            previous = speaker
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
