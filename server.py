# /// script
# dependencies = [
#     "flask",
#     "edge-tts",
# ]
# ///

from flask import Flask, request, send_file
import asyncio
import edge_tts
import io

app = Flask(__name__)

@app.route('/v1/tts', methods=['POST'])
def tts():
    data = request.json or {}
    
    # 获取参数，并设置默认值
    text = data.get("text", "请输入文本")
    voice = data.get("voice", "zh-CN-YunxiNeural")
    rate = data.get("rate", "+0%")      # 默认语速正常
    pitch = data.get("pitch", "+0Hz")    # 默认音调正常
    volume = data.get("volume", "+0%")  # 默认音量正常
    
    async def amain():
        # 将 rate, pitch, volume 参数传给 Communicate
        communicate = edge_tts.Communicate(
            text=text, 
            voice=voice,
            rate=rate,
            pitch=pitch,
            volume=volume
        )
        audio_stream = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])
        audio_stream.seek(0)
        return audio_stream

    try:
        mp3_file = asyncio.run(amain())
        return send_file(mp3_file, mimetype="audio/mpeg", as_attachment=True, download_name="speech.mp3")
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    # 保持你之前调通的 0.0.0.0 完美配置
    app.run(host='0.0.0.0', port=5050)
