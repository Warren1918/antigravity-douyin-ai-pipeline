# 🍵 Antigravity · Douyin AI Video & Voice Cloning Pipeline
> 全自动跨模态短视频生成与本地 RTX 4060 声音克隆流水线 (Zero-Cost & Local Private Architecture)

基于 **Antigravity** 编排驱动的抖音 9:16 短视频全自动生产线。支持**零成本云端多模态流**与**本地 RTX 4060 GPU 私有声音克隆**，彻底消除传统 AI 营销号的塑料机械味。

---

## 🌟 核心特性 (Key Features)

- 🎙️ **原声采集与声音种子提取**：内置倒计时提示音驱动录音终端，支持实时去燥 (`noisereduce`) 与 200Hz 胸腔共鸣增益。
- ⚡ **本地 RTX 4060 私有克隆**：利用 8GB 显存与 CUDA 加速，实现本地纯离线 Zero-Shot 音色复刻。
- 🎨 **去 AI 化美学画质**：结合 35mm 柯达胶片色彩流（Kodak Portra）与微颗粒质感，告别廉价荧光塑料感。
- 🎬 **抖音爆款排版安全区**：自动在 Y:200 绘制金黄爆款胶囊徽章，在 Y:980-1080 绘制高对比度黑金字幕衬板。
- 🛠️ **双模剪辑引擎**：支持直接无水印导出 720x1280 竖屏 MP4，或一键写入本地剪映电脑版工程草稿 (`pyJianYingDraft`)。

---

## 📁 目录结构 (Repository Structure)

```text
├── build_douyin_video.py        # 全自动 3 段式抖音短视频生成主程序
├── record_cli.py                # 麦克风倒计时录音终端
├── record_with_audio_cues.py    # 提示音驱动的盲操录音引擎
├── 双击我开始录音.bat           # Windows 一键无脑双击录音批处理脚本
├── requirements.txt             # Python 依赖清单
└── README.md                    # 项目说明文档
```

---

## 🚀 极速上手 (Quickstart)

### 1. 安装核心依赖
```bash
pip install -r requirements.txt
```

### 2. 采集你的专属原声音频
在文件夹中双击运行 `双击我开始录音.bat`，或在命令行中运行：
```bash
python record_cli.py
```
录音结束后将自动进行声学降噪与电平标准化，保存为 `my_voice_studio_master.wav`。

### 3. 一键渲染抖音短视频
```bash
python build_douyin_video.py
```
渲染完成后将自动输出符合抖音规格的竖屏短视频 `douyin_ai_masterpiece.mp4`。

---

## 🔒 隐私与安全声明 (Privacy)
本项目默认运行于本地环境。录制的声音样本及推理过程 100% 留存在本地显卡与硬盘中，绝不上传至未经许可的外部第三方服务器。
