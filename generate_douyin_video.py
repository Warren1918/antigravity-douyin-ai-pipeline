import os
import sys

# 适配 Windows 控制台 UTF-8 输出
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import asyncio
import requests
from urllib.parse import quote
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 3段式抖音短视频脚本（爆款科技认知流）
SCENES = [
    {
        "id": 1,
        "text": "很多人以为人工智能只是聊天工具，但真相正在颠覆你的认知。",
        "prompt": "futuristic artificial intelligence glowing core, complex cybernetic data streams, vertical ratio, 8k cinematic lighting, sci-fi concept art",
    },
    {
        "id": 2,
        "text": "全球顶级实验室正在加速突破脑机与具身智能，现实与虚拟的界限正被彻底打破。",
        "prompt": "surreal cybernetic human silhouette merging with luminous holographic matrix, neon cyberpunk, vertical ratio, photorealistic masterpiece, 8k",
    },
    {
        "id": 3,
        "text": "未来的竞争，从来不是人和机器的竞争，而是用不用超级工具的降维打击。",
        "prompt": "epic futuristic skyline, glowing golden sunrise over high-tech metropolis, cinematic perspective, inspirational sci-fi atmosphere, vertical ratio",
    }
]

async def generate_speech(text, audio_path):
    import edge_tts
    # 使用抖音最经典的解说音色：微软云希
    communicate = edge_tts.Communicate(text, "zh-CN-YunxiNeural", rate="+15%")
    await communicate.save(audio_path)

def download_image(prompt, image_path):
    encoded_prompt = quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=720&height=1280&nologo=true&seed=42"
    resp = requests.get(url, timeout=60)
    if resp.status_code == 200:
        with open(image_path, "wb") as f:
            f.write(resp.content)
    else:
        raise Exception(f"Failed to download image from Pollinations: HTTP {resp.status_code}")

def main():
    print("=" * 60)
    print("🍵 [Antigravity AI Video Pipeline] 开始执行短视频自动化任务...")
    print("=" * 60)
    
    clips = []
    
    for scene in SCENES:
        s_id = scene["id"]
        audio_path = os.path.join(OUTPUT_DIR, f"audio_scene_{s_id}.mp3")
        image_path = os.path.join(OUTPUT_DIR, f"image_scene_{s_id}.jpg")
        
        # 1. 生成配音
        print(f"🪻 [分镜 {s_id}] 正在生成微软云希专业配音...")
        asyncio.run(generate_speech(scene["text"], audio_path))
        
        # 2. 生成免费高清配图
        print(f"🌊 [分镜 {s_id}] 正在从开源图像引擎下载 9:16 竖屏高清画面...")
        download_image(scene["prompt"], image_path)
        
        # 3. 装配音画片段
        print(f"🍊 [分镜 {s_id}] 正在对齐音频与图像时间轴...")
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        # 创建画面 clip，并设置与音频一致的持续时间
        img_clip = ImageClip(image_path).with_duration(duration).with_audio(audio_clip)
        clips.append(img_clip)
        print(f"   ✓ 分镜 {s_id} 就绪 (时长: {duration:.2f} 秒)")
    
    # 4. 拼接成完整抖音竖屏视频
    print("\n🍵 正在将所有分镜缝合为抖音 1080x1920 竖屏成片...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    output_mp4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "douyin_ai_demo.mp4")
    
    # 导出 MP4 文件
    final_video.write_videofile(
        output_mp4,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        logger=None
    )
    
    # 清理释放资源
    for clip in clips:
        clip.close()
    final_video.close()
    
    print("\n" + "=" * 60)
    print(f"🎉 视频生成圆满完成！输出文件路径:")
    print(f"👉 {output_mp4}")
    print("=" * 60)

if __name__ == "__main__":
    main()
