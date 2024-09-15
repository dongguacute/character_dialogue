import tkinter as tk
import threading
import sys
import json
import pygame
import os
import pyaudio
from vosk import Model, KaldiRecognizer

# 初始化pygame用于播放音频
pygame.mixer.init()

# 从 JSON 文件中加载关键词和音频的对应关系
with open('keywords_audio.json', 'r', encoding='utf-8') as f:
    keywords_audio = json.load(f)

# 播放音频函数
def play_audio(keyword):
    if keyword in keywords_audio:
        audio_file = keywords_audio[keyword]
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
    else:
        print(f"没有找到关键词 '{keyword}' 的音频文件。")

# 用于控制录音线程的标志
recording = False

# 初始化Vosk模型
model_path = "你的Vosk中文模型路径"  # 下载中文模型并解压在此路径
if not os.path.exists(model_path):
    print("请下载Vosk中文模型并放到指定路径")
    exit(1)

model = Model(model_path)

# 初始化PyAudio用于麦克风输入
mic = pyaudio.PyAudio()
recognizer = KaldiRecognizer(model, 16000)

# 录音函数，使用Vosk进行本地语音识别
def record():
    global recording
    recording = True

    # 打开麦克风流
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print("开始录音...")

    try:
        while recording:
            data = stream.read(4000)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result)["text"]
                print(f"识别结果: {text}")

                # 检查是否说出了关键词
                if "停止" in text:
                    recording = False
                    play_audio("停止")  # 播放退出关键词对应的音频
                else:
                    play_audio(text)  # 播放识别到的关键词对应的音频
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        print("结束录音。")
        sys.exit()  # 结束整个程序

# 开始按钮的点击事件处理函数
def start_recording():
    global recording_thread
    if not recording:
        recording_thread = threading.Thread(target=record)
        recording_thread.start()

# 停止按钮的点击事件处理函数
def stop_recording():
    global recording
    recording = False
    print("录音已停止。")

# 主窗口类
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("语音识别程序")
        self.geometry("300x150")

        # 创建开始按钮
        self.start_button = tk.Button(self, text="开始", command=start_recording)
        self.start_button.pack(pady=10)

        # 创建停止按钮
        self.stop_button = tk.Button(self, text="停止", command=stop_recording)
        self.stop_button.pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
