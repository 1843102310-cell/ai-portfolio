import requests

# 关闭系统代理，防止被拦截
s = requests.Session()
s.trust_env = False 

print("正在连接本地 Ollama，请稍候...")

try:
    resp = s.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "qwen2.5:0.5b",
            "messages": [{"role": "user", "content": "给《愚公移山》出一道HSK4阅读题"}],
            "stream": False
        },
        timeout=120
    )
    resp.raise_for_status()
    print("\n--- 模型回答 ---")
    print(resp.json()["message"]["content"])
    
except Exception as e:
    print("\n请求失败，报错信息如下：")
    print(e)