import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import threading
import sys
import json
import pygame

# 创建一个语音识别对象
recognizer = sr.Recognizer()
# 创建一个麦克风对象
mic = sr.Microphone()

# 设置一个退出关键词
exit_keyword = "停止"

# 用于控制录音线程的标志
recording = False

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

# 录音函数
def record():
    global recording
    recording = True
    print("开始录音...")

    try:
        while recording:
            with mic as source:
                # 调整环境噪音水平
                recognizer.adjust_for_ambient_noise(source)
                print("Listening...")

                # 设置没有超时限制，但通过 `phrase_time_limit` 限制每次语音输入的长度
                audio = recognizer.listen(source, phrase_time_limit=5)

            try:
                # 使用 Google Speech Recognition API 识别语音
                output = recognizer.recognize_google(audio, language="zh-CN")
                print(f"你说的是：{output}")

                # 检查是否说出了退出关键词
                if exit_keyword in output:
                    recording = False
                    play_audio(exit_keyword)  # 播放退出关键词对应的音频
                else:
                    # 如果识别到关键词，播放对应的音频
                    play_audio(output)

            except sr.UnknownValueError:
                print("无法识别语音，请再说一次。")
            except sr.RequestError as e:
                print(f"请求失败； {e}")
            except sr.WaitTimeoutError:
                # 超时错误不应导致录音停止，继续监听
                continue
    finally:
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
