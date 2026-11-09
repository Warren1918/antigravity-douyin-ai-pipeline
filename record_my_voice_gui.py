import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import sounddevice as sd
import soundfile as sf
import numpy as np

# 适配编码
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_voice.wav")
SAMPLE_RATE = 24000  # 顶级 TTS 声音克隆标准采样率

class VoiceRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Antigravity · 原声声音采集录音室")
        self.root.geometry("520x380")
        self.root.resizable(False, False)
        self.root.configure(bg="#F8F9FA")
        
        # 居中置顶显示
        self.root.attributes("-topmost", True)
        self.center_window()
        
        self.is_recording = False
        self.recorded_frames = []
        self.start_time = 0
        
        self.setup_ui()
        
    def center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def setup_ui(self):
        # 顶部标题栏
        header = tk.Frame(self.root, bg="#2D7A5B", height=60)
        header.pack(fill="x")
        
        title_lbl = tk.Label(
            header,
            text="🍵 Antigravity 原声采集终端",
            font=("Microsoft YaHei UI", 16, "bold"),
            fg="#FFFFFF",
            bg="#2D7A5B"
        )
        title_lbl.pack(pady=12)
        
        # 内容区域
        body = tk.Frame(self.root, bg="#F8F9FA", padx=30, pady=20)
        body.pack(fill="both", expand=True)
        
        self.status_lbl = tk.Label(
            body,
            text="🌿 状态：麦克风已就绪\n请点击下方按钮，自然说 5-10 秒生活化的话语即可",
            font=("Microsoft YaHei UI", 12),
            fg="#2D3748",
            bg="#F8F9FA",
            justify="center"
        )
        self.status_lbl.pack(pady=10)
        
        # 计时器
        self.timer_lbl = tk.Label(
            body,
            text="00:00",
            font=("Consolas", 28, "bold"),
            fg="#718096",
            bg="#F8F9FA"
        )
        self.timer_lbl.pack(pady=10)
        
        # 提示语
        self.tip_lbl = tk.Label(
            body,
            text="💡 推荐例句：「其实生活就像一部电影，按自己的节奏慢慢走，挺好的。」",
            font=("Microsoft YaHei UI", 10),
            fg="#4A5568",
            bg="#F8F9FA",
            wraplength=440,
            justify="center"
        )
        self.tip_lbl.pack(pady=5)
        
        # 按钮区
        btn_frame = tk.Frame(body, bg="#F8F9FA")
        btn_frame.pack(pady=15)
        
        self.action_btn = tk.Button(
            btn_frame,
            text="🎙️ 开始录音",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg="#2D7A5B",
            fg="#FFFFFF",
            activebackground="#236047",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=25,
            pady=8,
            cursor="hand2",
            command=self.toggle_recording
        )
        self.action_btn.pack()

    def toggle_recording(self):
        if not self.is_recording:
            self.start_record()
        else:
            self.stop_record()

    def start_record(self):
        self.is_recording = True
        self.recorded_frames = []
        self.start_time = time.time()
        
        # 界面更新
        self.action_btn.config(text="⏹️ 录制完毕 · 点击保存", bg="#D45A75", activebackground="#B83A55")
        self.status_lbl.config(text="🔴 正在录制您的真实声音...\n请对着麦克风自然说话（建议说 5-10 秒）", fg="#D45A75")
        self.timer_lbl.config(fg="#D45A75")
        
        # 启动后台录音线程
        threading.Thread(target=self.record_thread, daemon=True).start()
        # 启动计时刷新
        self.update_timer()

    def record_thread(self):
        def callback(indata, frames, time_info, status):
            if self.is_recording:
                self.recorded_frames.append(indata.copy())

        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", callback=callback):
            while self.is_recording:
                sd.sleep(50)
                # 最长 15 秒自动停止保存
                if time.time() - self.start_time >= 15:
                    self.root.after(0, self.stop_record)
                    break

    def update_timer(self):
        if self.is_recording:
            elapsed = int(time.time() - self.start_time)
            self.timer_lbl.config(text=f"00:{elapsed:02d}")
            self.root.after(200, self.update_timer)

    def stop_record(self):
        if not self.is_recording:
            return
        self.is_recording = False
        
        self.status_lbl.config(text="🍵 正在处理并保存音频...", fg="#2D7A5B")
        self.action_btn.config(state="disabled", text="⏳ 正在保存...")
        self.root.update()
        
        if self.recorded_frames:
            audio_data = np.concatenate(self.recorded_frames, axis=0)
            sf.write(OUTPUT_PATH, audio_data, SAMPLE_RATE)
            print(f"[SUCCESS] 录音已保存至: {OUTPUT_PATH}")
            
            self.status_lbl.config(
                text="🎉 录音成功完成并自动就绪！\n窗口即将自动关闭，Antigravity 正在接管...",
                fg="#2D7A5B"
            )
            self.timer_lbl.config(fg="#2D7A5B")
            self.root.after(1500, self.root.destroy)
        else:
            messagebox.showwarning("提示", "未检测到有效声音输入，请重试。")
            self.reset_ui()

    def reset_ui(self):
        self.action_btn.config(state="normal", text="🎙️ 开始录音", bg="#2D7A5B")
        self.status_lbl.config(text="🌿 状态：麦克风已就绪\n请点击下方按钮开始录音", fg="#2D3748")
        self.timer_lbl.config(text="00:00", fg="#718096")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
