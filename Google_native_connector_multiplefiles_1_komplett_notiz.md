# Google native connector (multiple files) — 完整原文学习笔记

> 来源：根据你刚才提供的 `Google_native_connector_multiplefiles_1.py` 截图逐段转写。
> 
> 安全处理：真实 API key 已删除并替换为 `<YOUR_API_KEY>`；其余代码结构、顺序和逻辑保持原样。说明文字只用于学习，不是原脚本的一部分。

## 1. 导入与日志配置

作用：准备 HTTP 请求、JSON、日志、本地文件读取和 Base64 编码。

```python
import requests
import json
import logging
import os
import base64


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
```

## 2. 连接器初始化

作用：建立 `BoschLLMConnector`；它保存模型名、API key、请求地址和最近一次 token 用量。它本身不是 Gemini 模型。

```python
class BoschLLMConnector:
    def __init__(self, model_name, api_key, base_url):
        self.model_name = model_name
        self.api_key = api_key

        self.base_url = base_url.rstrip("/")
        self.url = f"{self.base_url}/publishers/google/models/{self.model_name}:generateContent"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        self.last_usage = None
```

## 3. 底层请求函数

作用：将已准备好的 JSON 发给 Bosch LLM Farm，取回模型的文字回答，并保存 token 用量。

```python
    def _send_request(self, payload: dict, generation_config: dict = None):
        try:
            if generation_config:
                payload["generationConfig"] = generation_config

            logging.info(f"Sende Anfrage an Modell: {self.model_name}")
            response = requests.post(self.url, headers=self.headers, json=payload)

            response.raise_for_status()
            result = response.json()

            self.last_usage = result.get("usageMetadata", {})

            candidates = result.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                text_parts = [part["text"] for part in parts if "text" in part]
                if text_parts:
                    return "".join(text_parts)

            logging.warning("Keine Textantwort in der Modellantwort gefunden.")
            return ""

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP-Fehler: {e}")
            return f"HTTP-Fehler: {e}"
        except requests.exceptions.RequestException as e:
            logging.error(f"Anfragefehler: {e}")
            return f"Anfragefehler: {e}"
        except (ValueError, KeyError, IndexError) as e:
            logging.error(f"Fehler beim Verarbeiten der Antwort: {e}")
            return f"Antwortverarbeitungsfehler: {e}"
```

## 4. 纯文本提问

作用：`llm.ask("...")` 时，将文字包装成 Gemini API 需要的格式，再调用上面的请求函数。

```python
    def ask(self, prompt: str):
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ]
        }
        return self._send_request(payload)
```

## 5. 多文件分析

作用：将一个问题和多个 PDF / PNG / JPG / JPEG 文件合并为同一次请求；每个文件先读成二进制，再 Base64 编码。

```python
    def analyze_documents(
        self,
        file_paths: list,
        user_prompt: str,
        system_prompt: str = None,
        generation_config: dict = None,
    ):
        logging.info(f"Analysiere {len(file_paths)} Dokument(e) für die Anfrage...")

        user_parts = [{"text": user_prompt}]

        for file_path in file_paths:
            if not os.path.exists(file_path):
                logging.error(f"Datei nicht gefunden: {file_path}")
                continue

            try:
                with open(file_path, "rb") as f:
                    file_bytes = f.read()

                base64_data = base64.b64encode(file_bytes).decode("utf-8")

                ext = os.path.splitext(file_path)[1].lower()
                mime_map = {
                    ".pdf": "application/pdf",
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                }

                if ext not in mime_map:
                    logging.warning(f"Nicht unterstützter Dateityp übersprungen: {file_path}")
                    continue

                user_parts.append(
                    {
                        "inline_data": {
                            "mime_type": mime_map[ext],
                            "data": base64_data,
                        }
                    }
                )
                logging.info(f"Datei hinzugefügt: {file_path}")

            except Exception as e:
                logging.error(f"Fehler beim Lesen von {file_path}: {e}")

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": user_parts,
                }
            ]
        }

        if system_prompt:
            payload["system_instruction"] = {
                "parts": [{"text": system_prompt}]
            }

        return self._send_request(payload, generation_config)
```

## 6. 方便的多文件入口与 token 用量

作用：主分类脚本通常调用 `ask_about_files()`；它只是把参数转交给 `analyze_documents()`。`get_last_token_usage()` 取回最近一次的统计信息。

```python
    def ask_about_files(
        self,
        file_paths: list,
        question: str,
        system_prompt: str = None,
        generation_config: dict = None,
    ):
        return self.analyze_documents(
            file_paths=file_paths,
            user_prompt=question,
            system_prompt=system_prompt,
            generation_config=generation_config,
        )

    def get_last_token_usage(self):
        return self.last_usage
```

## 7. 直接运行时的测试区

作用：只有直接运行这个 connector 文件时才执行；如果其他脚本用 `import BoschLLMConnector` 导入它，这一段不会执行。

```python
if __name__ == "__main__":
    BOSCH_FARM_API_KEY = "<YOUR_API_KEY>"
    MODEL_NAME = "gemini-2.5-pro"
    BASE_URL = "HIER_BOSCH_LLM_FARM_BASE_URL_EINTRAGEN"

    llm = BoschLLMConnector(
        model_name=MODEL_NAME,
        api_key=BOSCH_FARM_API_KEY,
        base_url=BASE_URL,
    )

    print("Test 1 - Textanfrage:")
    print(llm.ask("Welches Modell bist du?"))
    print("Token usage:", llm.get_last_token_usage())

    test_files = [
        "test.pdf",
        "test.png",
    ]
    existing_files = [path for path in test_files if os.path.exists(path)]

    if existing_files:
        print("\\nTest 2 - Anfrage mit Dateien:")
        print(
            llm.ask_about_files(
                file_paths=existing_files,
                question="Beschreibe die bereitgestellten Dokumente kurz.",
            )
        )
        print("Token usage:", llm.get_last_token_usage())
    else:
        print("\\nTest 2 übersprungen: Keine Testdateien gefunden.")
```

## 一句话流程

```text
主分类脚本 → BoschLLMConnector → 打包文字 + PDF/图片 → Bosch LLM Farm / Gemini → 返回文本类别
```
