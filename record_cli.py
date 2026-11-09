import os
import sys
import time
import sounddevice as sd
import soundfile as sf
import numpy as np

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_voice.wav")
SAMPLE_RATE = 24000
DURATION = 8  # 默认录制 8 秒

def main():
    print("=" * 60)
    print("🍵 [Antigravity 原声采集] 启动麦克风直接录音...")
    print("=" * 60)
    print("准备就绪！请在听到提示后，对着麦克风自然说 5-8 秒日常对话。")
    print("例如：「其实很多事情真没必要那么焦虑，按自己的节奏慢慢走，挺好的。」\n")
    
    # 倒计时 3 秒
    for i in range(3, 0, -1):
        print(f"⏱ 倒计时: {i} 秒后开始说话...")
        time.sleep(1)
        
    print("\n🔴 【正在录音中... 请开口说话！】(持续 8 秒)")
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    
    for sec in range(1, DURATION + 1):
        time.sleep(1)
        print(f"   🎙️ 已录制 {sec} / {DURATION} 秒...")
        
    sd.wait()
    sf.write(OUTPUT_PATH, recording, SAMPLE_RATE)
    
    print("\n" + "=" * 60)
    print(f"🎉 录制圆满结束！音频已自动保存至:")
    print(f"👉 {OUTPUT_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    main()
