# **语音识别回复音频**

## 概述

关于我为什么要来写这个软件，原因如下：

![](https://pic.imgdb.cn/item/66e6b1f7d9c307b7e996cf17.jpg)

她的意思是要我写一个对话软件就是，可以和自己喜欢的人物对话，所以我就灵机一动写了这个软件

## **开发者指南**

### **线上识别版**

内地的小伙伴们可能访问不了，因为使用的是Google的API

**对应文件是`main.py`**

#### 需要安装以下库

**Portaudio**

Win

```bash
conda install -c conda-forge portaudio
```

Mac

```bash
brew install portaudio
```

**Speech_recognition**

```bash
pip install SpeechRecognition
```

**其它**

```bash
pip install pygame
pip install playsound
pip install PyAudio
```

#### JSON格式指南

示例：

```json
{
  "你好": "audio/hello.mp3",
  "再见": "audio/goodbye.mp3",
  "停止": "audio/stop.mp3"
}

```

请把所有音频放在`audio`文件夹内，并且在文件名前面加入`audio/`

### 本地版

与在线版基本一致，但是加入了本地语音识别模型功能

**对应文件是`main_local.py`**

#### 额外库安装

```bash
pip install vosk
```

#### 语音识别模型下载

```bash
https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip        41.87 M
https://alphacephei.com/vosk/models/vosk-model-cn-0.15.zip               1.67 G
```

请把模型文件放在`model`文件夹内

## 版权

本项目采用MIT版权协议