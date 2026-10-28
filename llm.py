import requests
import os
from openai import OpenAI

# ================= 1. 本地引擎 =================
class LocalEngine:
    def __init__(self, model=None):
        self.model = model or os.getenv("LOCAL_MODEL", "qwen2.5:0.5b")
        self.session = requests.Session()
        self.session.trust_env = False # 解决机房/校园网代理问题

    def ask(self, prompt, **kwargs):
        r = self.session.post("http://localhost:11434/api/chat", json={
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }, timeout=60) 
        
        r.raise_for_status() # 报错要暴露，不能静默失败
        return r.json()["message"]["content"]

# ================= 2. 云端引擎 =================
class APIEngine:
    def __init__(self):
        self.client = None # 延迟初始化，防止没配环境变量直接崩溃
        
    def ensure_client(self):
        if self.client is None:
            self.client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"), # 注意：需要在环境变量里配好
                base_url="https://api.deepseek.com/v1"
            )

    def ask(self, prompt, **kwargs):
        self.ensure_client()
        r = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        return r.choices[0].message.content

# ================= 3. 统一入口与双向回退 =================
class LLM:
    def __init__(self):
        self.local = LocalEngine()
        self.api = APIEngine()

    def ask(self, prompt, prefer="local"):
        # 选择首选和备选
        first, second = (self.local, self.api) if prefer == "local" else (self.api, self.local)
        
        try:
            return first.ask(prompt)
        except Exception as e:
            # 讲义要求：必须打印切换原因
            print(f"[首选引擎失败，自动切换!] 报错信息: {e}")
            try:
                return second.ask(prompt)
            except Exception as e2:
                print(f"[备用引擎也失败了] 报错信息: {e2}")
                return "双引擎均失效，请检查网络或服务。"

# ================= 测试代码 =================
if __name__ == "__main__":
    llm = LLM()
    
    # 测试1：正常本地
    print("--- 测试1：首选本地 (Ollama需开启) ---")
    print(llm.ask("你好，你是谁？", prefer="local"))
    
    # 测试2：本地挂，切云端 (你可以手动关掉Ollama试试)
    # print("--- 测试2：首选本地 (手动关掉Ollama) ---")
    # print(llm.ask("你好，你是谁？", prefer="local"))