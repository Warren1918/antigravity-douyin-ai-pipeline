import os
import sys
import time
import asyncio
import requests
from urllib.parse import quote
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

# 1. 确保 Windows 控制台字符编码正常
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(BASE_DIR, "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

# 2. 爆款抖音 9:16 短视频分镜脚本（3 段式高完播率结构）
SCENES = [
    {
        "id": 1,
        "title": "⚡ 认知颠覆",
        "text": "很多人以为AI只是聊天工具，但真相正在颠覆所有人的认知。",
        "prompt": "futuristic artificial intelligence glowing core, cybernetic data streams, vertical ratio, 8k cinematic lighting, sci-fi concept art",
    },
    {
        "id": 2,
        "title": "🌐 时代奇点",
        "text": "全球顶级实验室正在加速突破具身智能，现实与虚拟的界限已被彻底打破。",
        "prompt": "surreal cybernetic human silhouette merging with luminous holographic matrix, neon cyberpunk, vertical ratio, photorealistic 8k",
    },
    {
        "id": 3,
        "title": "🚀 降维生存",
        "text": "未来的竞争从来不是人与机器的竞争，而是掌握超级工具者的降维打击！",
        "prompt": "epic futuristic skyline, glowing golden sunrise over high-tech metropolis, cinematic perspective, inspirational sci-fi atmosphere, vertical ratio",
    }
]

FONT_PATH = "C:\\Windows\\Fonts\\msyh.ttc"  # 微软雅黑
FALLBACK_FONT_PATH = "C:\\Windows\\Fonts\\simhei.ttf"

def get_font(size):
    if os.path.exists(FONT_PATH):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception:
            pass
    if os.path.exists(FALLBACK_FONT_PATH):
        try:
            return ImageFont.truetype(FALLBACK_FONT_PATH, size)
        except Exception:
            pass
    return ImageFont.load_default()

async def generate_speech(text, audio_path):
    """使用微软 Edge-TTS 免费生成抖音解说顶流音色（云希）"""
    import edge_tts
    communicate = edge_tts.Communicate(text, "zh-CN-YunxiNeural", rate="+15%")
    await communicate.save(audio_path)

def download_image_with_fallback(prompt, image_path):
    """优先使用 Pollinations flux/turbo 免费生成，若遇网络波动则自动降级兜底"""
    models = ["flux", "turbo"]
    for model in models:
        try:
            encoded_prompt = quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model={model}&width=720&height=1280&nologo=true"
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200 and len(resp.content) > 1000:
                with open(image_path, "wb") as f:
                    f.write(resp.content)
                return True
        except Exception as e:
            print(f"      [重试警告] 模型 {model} 响应异常: {e}，尝试备用线路...")
            time.sleep(1)
            
    # 若网络完全阻断，则用 Pillow 自动绘制渐变科技底图作为保底
    print("      [备用方案] 启动本地高质感科幻海报引擎生成底图...")
    img = Image.new("RGB", (720, 1280), (12, 16, 28))
    draw = ImageDraw.Draw(img)
    # 绘制科技感线条网格
    for y in range(0, 1280, 40):
        draw.line([(0, y), (720, y)], fill=(20, 30, 50), width=1)
    for x in range(0, 720, 40):
        draw.line([(x, 0), (x, 1280)], fill=(20, 30, 50), width=1)
    img.save(image_path)
    return True

def add_douyin_overlay(raw_img_path, output_img_path, title, subtitle_text):
    """
    为画面添加标准的抖音竖屏安全区排版：
    1. 顶部爆款微胶囊标签
    2. 底部高对比度黑金醒目字幕条
    """
    img = Image.open(raw_img_path).convert("RGBA")
    img = img.resize((720, 1280), Image.Resampling.LANCZOS)
    
    # 创建文字透明图层
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    font_badge = get_font(32)
    font_sub = get_font(36)
    
    # 1. 顶部胶囊标签 (Y: 220 避开顶部关注区)
    badge_text = f"🔥 {title} · 深度思考"
    bbox_b = draw.textbbox((0, 0), badge_text, font=font_badge)
    b_w = bbox_b[2] - bbox_b[0]
    b_x = (720 - b_w) // 2
    b_y = 220
    # 胶囊底色
    draw.rounded_rectangle([b_x - 20, b_y - 8, b_x + b_w + 20, b_y + 44], radius=20, fill=(0, 0, 0, 180))
    draw.text((b_x, b_y), badge_text, fill=(255, 215, 0, 255), font=font_badge)
    
    # 2. 底部字幕 (Y: 980-1080 抖音经典安全区)
    # 按字数换行拆分（每行约14-16字）
    max_chars = 15
    lines = []
    for i in range(0, len(subtitle_text), max_chars):
        lines.append(subtitle_text[i:i + max_chars])
    
    start_y = 1000 - (len(lines) * 55) // 2
    for idx, line in enumerate(lines):
        bbox_s = draw.textbbox((0, 0), line, font=font_sub)
        s_w = bbox_s[2] - bbox_s[0]
        s_x = (720 - s_w) // 2
        cur_y = start_y + idx * 58
        
        # 字幕黑底衬板
        draw.rounded_rectangle([s_x - 16, cur_y - 6, s_x + s_w + 16, cur_y + 46], radius=12, fill=(0, 0, 0, 200))
        # 金白双色字
        draw.text((s_x, cur_y), line, fill=(255, 255, 255, 255), font=font_sub)
        
    # 合成保存
    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    final_img.save(output_img_path, quality=95)

def main():
    print("=" * 65)
    print("🍵 [Antigravity AI Video Engine] 启动全自动零成本抖音视频制作流水线...")
    print("=" * 65)
    
    clips = []
    
    for scene in SCENES:
        s_id = scene["id"]
        raw_img_path = os.path.join(WORKSPACE_DIR, f"raw_scene_{s_id}.jpg")
        framed_img_path = os.path.join(WORKSPACE_DIR, f"framed_scene_{s_id}.jpg")
        audio_path = os.path.join(WORKSPACE_DIR, f"audio_scene_{s_id}.mp3")
        
        # 1. 微软云希专业配音
        print(f"🪻 [分镜 0{s_id}/03] 正在生成抖音标配【微软云希】高清拟真解说音...")
        asyncio.run(generate_speech(scene["text"], audio_path))
        
        # 2. 免费开源 AI 生图
        print(f"🌊 [分镜 0{s_id}/03] 正在调用 Flux 引擎下载 9:16 竖屏高清科幻素材...")
        download_image_with_fallback(scene["prompt"], raw_img_path)
        
        # 3. 智能排版与字幕合成
        print(f"🍊 [分镜 0{s_id}/03] 正在为画面贴附安全区爆款胶囊与动态字幕...")
        add_douyin_overlay(raw_img_path, framed_img_path, scene["title"], scene["text"])
        
        # 4. 音画对齐
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        # 画面时长严格与语音对齐，并绑定音轨
        img_clip = ImageClip(framed_img_path).with_duration(duration).with_audio(audio_clip)
        clips.append(img_clip)
        print(f"   ✓ 分镜 0{s_id} 制作完成 (精准对齐时长: {duration:.2f} 秒)\n")
        
    # 5. 缝合拼接完整抖音成片
    print("🍵 正在将各分镜自动化混剪为完整竖屏 MP4 视频...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    final_output_path = os.path.join(BASE_DIR, "douyin_ai_masterpiece.mp4")
    
    final_video.write_videofile(
        final_output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        logger=None
    )
    
    # 释放资源
    for clip in clips:
        clip.close()
    final_video.close()
    
    print("=" * 65)
    print("🎉 恭喜！抖音 AI 短视频全流程自动化制作圆满完成！")
    print(f"📁 成片保存路径: {final_output_path}")
    print(f"⏱ 视频总时长: {sum([c.duration for c in clips]):.1f} 秒 | 分辨率: 720x1280 (抖音标准竖屏)")
    print("=" * 65)

if __name__ == "__main__":
    main()
