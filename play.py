# /// script
# dependencies = [
#     "requests",
# ]
# ///
import requests
import time  # 导入时间库用来生成时间戳
import os

url = "http://localhost:5050/v1/tts"

# 在这里自由调整你的参数！
payload = {
    "filename": "云希变声测试",    # 自定义的文件名前缀
    "text": "哈哈，你瞧！我现在说话不仅速度变快了，而且声音听起来是不是有点像动画片里的小松鼠？",
    "voice": "zh-CN-YunxiNeural",  # 云希
    "rate": "+30%",                # 语速加快 30%（适合做快节奏短视频）
    "pitch": "+12Hz",              # 音调调高 12Hz（声音会变尖、变年轻或变喜感）
    "volume": "+0%"                # 音量保持不变
}

print("正在发送带有多参数的请求到本地 TTS 服务器...")
try:
    response = requests.post(url, json=payload, timeout=15)
    if response.status_code == 200:
        
        # 1. 定义你的目标文件夹名称
        output_dir = "voice_list"
        
        # 2. 如果当前目录下没有这个文件夹，Python 会自动帮你创建它
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"【提示】检测到未创建目标文件夹，已自动新建：{output_dir}/")
        
        # 3. 提取名称并生成时间戳
        name_prefix = payload.get("filename", "output")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # 4. 核心修改：将路径与文件名拼接在一起 (例如：voice_list/名称_时间戳.mp3)
        final_filename = os.path.join(output_dir, f"{name_prefix}_{timestamp}.mp3")
        
        # 5. 保存文件到指定目录
        with open(final_filename, "wb") as f:
            f.write(response.content)
            
        print(f"【成功】音频已生成！已安全保存至：{final_filename}")
    else:
        print(f"【失败】服务器返回错误: {response.status_code}, 原因: {response.text}")
except Exception as e:
    print(f"【错误】{e}")