# 第六周测试记录 (week06_test_log.md)

| 测试条件 | 实际走的引擎 | 耗时与答案质量点评 | 是否符合预期/怎么改的 |
| :--- | :--- | :--- | :--- |
| 正常本地：Ollama开，prefer="local" | 本地 (qwen2.5:0.5b) | 约 0.5s，准确回答身份（阿里Qwen） | 符合 |
| 本地挂->切云端：关Ollama，prefer="local" | 云端失败->本地拒绝 | 瞬间捕捉连接错误，并自动尝试切换 | 符合，回退日志成功打印 |

## 回退日志原文（核心证据）
[首选引擎失败，自动切换!] 报错信息: HTTPConnectionPool(host='localhost', port=11434): Max retries exceeded with url: /api/chat (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x...>: Failed to establish a new connection: [WinError 10061] 由于目标计算机积极拒绝，无法连接。'))
[备用引擎也失败了] 报错信息: Missing credentials. Please pass an `api_key`, `workload_identity`, `admin_api_key`, or set the `OPENAI_API_KEY` or `OPENAI_ADMIN_KEY` environment variable.
双引擎均失效，请检查网络或服务。