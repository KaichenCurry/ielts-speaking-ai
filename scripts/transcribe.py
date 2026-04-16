#!/usr/bin/env python3
"""快速语音转写脚本 - 使用PyAV + HuggingFace Whisper"""
import sys
import av
import numpy as np
import wave
import os

def convert_ogg_to_wav(ogg_path: str, wav_path: str) -> float:
    """将OGG音频转换为16kHz单声道WAV，返回时长(秒)"""
    container = av.open(ogg_path)
    stream = container.streams.audio[0]
    resampler = av.audio.resampler.AudioResampler(format='s16', layout='mono', rate=16000)
    
    all_data = []
    for frame in container.decode(stream):
        frame = resampler.resample(frame)
        if frame:
            for f in frame:
                arr = np.frombuffer(f.to_ndarray(), dtype=np.int16)
                all_data.append(arr)
    
    if not all_data:
        return 0.0
    
    audio_data = np.concatenate(all_data)
    duration = len(audio_data) / 16000.0
    
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio_data.tobytes())
    
    return duration

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: transcribe.py <input.ogg> <output.wav>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    duration = convert_ogg_to_wav(input_path, output_path)
    print(f"{duration:.2f}")
