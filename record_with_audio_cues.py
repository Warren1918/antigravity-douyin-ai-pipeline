import os
import sys
import time
import winsound
import sounddevice as sd
import soundfile as sf
import numpy as np

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_voice.wav")
SAMPLE_RATE = 24000
DURATION = 8  # 8 秒

def play_countdown():
    # 3 次低音倒计时提示
    for i in range(3):
        winsound.Beep(600, 250)
        time.sleep(0.75)
    # 高音开录提示
    winsound.Beep(1200, 500)

def play_finish():
    winsound.Beep(1000, 200)
    time.sleep(0.1)
    winsound.Beep(1200, 300)

def main():
    print("准备开始倒计时提示音...")
    play_countdown()
    
    print("正在录音中...")
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    
    sf.write(OUTPUT_PATH, recording, SAMPLE_RATE)
    print(f"录音已保存至: {OUTPUT_PATH}")
    
    play_finish()

if __name__ == "__main__":
    main()
