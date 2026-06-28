# Инструменты

Инструменты позволяют агентам выполнять действия: получать данные, запускать код, обращаться к внешним API и даже использовать компьютер. В агентах CAI есть три класса инструментов:

-   Размещённые (Hosted tools): выполняются на LLM-серверах вместе с моделями. CAI предлагает некоторые [tools](src/cai/tools)
-   Function calling: позволяют использовать любую Python-функцию как инструмент.
-   Агенты как инструменты: позволяют использовать агента как инструмент, чтобы агенты могли вызывать другие агенты без передачи управления (handoff).

## Размещённые инструменты (Hosted tools)

CAI предлагает несколько встроенных инструментов при использовании [`OpenAIResponsesModel`][cai.sdk.agents.models.openai_responses.OpenAIResponsesModel]. Они находятся в [tools](src/cai/tools) и сгруппированы в 6 крупных категорий, вдохновлённых security kill chain[2]:

1. Разведка и боевое применение — *reconnaissance* (crypto, listing и т.п.)
2. Эксплуатация — *exploitation*
3. Эскалация привилегий — *escalation*
4. Боковое перемещение — *lateral*
5. Экфильтрация данных — *exfiltration*
6. Командование и управление — *control*

### Инструмент C99 (C99 Tool)

CAI включает интеграцию с API C99.nl для поиска поддоменов и DNS-enumeration. Этот инструмент особенно полезен для разведки во время security assessments.

#### Конфигурация

Чтобы использовать инструмент C99, вам нужно настроить ключ API:

```bash
# В вашем .env файле
C99_API_KEY="your-c99-api-key-here"
```

Ключ API можно получить, зарегистрировавшись на [C99.nl](https://c99.nl).

#### Пример использования

```python
from cai.sdk.agents import Agent, Runner, OpenAIChatCompletionsModel
from cai.tools.reconnaissance.c99_tool import c99_subdomain_finder
from openai import AsyncOpenAI

recon_agent = Agent(
    name="Recon Agent",
    description="Агент, специализирующийся на поиске поддоменов",
    instructions="Вы — эксперт по разведке, сфокусированный на DNS-enumeration.",
    tools=[
        c99_subdomain_finder,
    ],
    model=OpenAIChatCompletionsModel(
        model="qwen2.5:14b",
        openai_client=AsyncOpenAI(),
    )
)

async def main():
    result = await Runner.run(recon_agent, "Find all subdomains for example.com")
    print(result.final_output)
```

Инструмент C99 даёт широкие возможности по перечислению поддоменов, поэтому он особенно ценен на фазе разведки security assessment.

```python
from cai.sdk.agents import Agent, Runner, OpenAIChatCompletionsModel
from cai.tools.reconnaissance.generic_linux_command import generic_linux_command 
from openai import AsyncOpenAI

one_tool_agent = Agent(
    name="CTF agent",
    description="Агент, сфокусированный на перечислении директорий",
    instructions="Вы — эксперт по кибербезопасности, ведущий игрок, перед которым стоит CTF.",
    tools=[
        generic_linux_command,
    ],
    model=OpenAIChatCompletionsModel(
        model="qwen2.5:14b",
        openai_client=AsyncOpenAI(),
    )
)
async def main():
    result = await Runner.run(one_tool_agent, "List all directories")
    print(result.final_output)
```

## Function tools

Вы можете использовать любую Python-функцию как инструмент. CAI автоматически настроит инструмент:

-   Имя инструмента будет именем Python-функции (или вы можете указать другое имя)
-   Описание инструмента берётся из docstring функции (или вы можете указать описание)
-   Схема входных параметров автоматически создаётся по аргументам функции
-   Описания для каждого входного параметра берутся из docstring функции, если это не отключено

Мы используем модуль Python `inspect`, чтобы извлечь сигнатуру функции, вместе с [`griffe`](https://mkdocstrings.github.io/griffe/) для парсинга docstring и `pydantic` для построения схемы.

```python
import json
from typing_extensions import TypedDict, Any
from cai.sdk.agents import Agent, FunctionTool, RunContextWrapper, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

class IPAddress(TypedDict):
    ip: str


@function_tool
async def check_ip_reputation(ip_data: IPAddress) -> str:
    """Проверить, есть ли у IP-адреса плохая репутация.

    Args:
        ip_data: Словарь с IP-адресом для проверки.
    """
    # In a real system, this would query an IP reputation API
    return "malicious" if ip_data["ip"].startswith("192.168") else "clean"


@function_tool(name_override="read_log_file")
def read_log_file(ctx: RunContextWrapper[Any], path: str, directory: str | None = None) -> str:
    """Прочитать содержимое файла логов.

    Args:
        path: Путь к файлу логов.
        directory: Необязательная директория для поиска.
    """
    # In a real system, this would read from the filesystem logs
    return "<log file contents: suspicious activity found>"


# Создаём кибербезопасностного агента
agent = Agent(
    name="CyberSecBot",
    tools=[check_ip_reputation, read_log_file],
    model=OpenAIChatCompletionsModel(
        model="qwen2.5:14b",
        openai_client=AsyncOpenAI(),
    )
)

# Отображение метаданных для каждого доступного инструмента
for tool in agent.tools:
    if isinstance(tool, FunctionTool):
        print(tool.name)
        print(tool.description)
        print(json.dumps(tool.params_json_schema, indent=2))
        print()
```

1.  Вы можете использовать любые Python-типы в аргументах функций, а функция может быть как синхронной, так и асинхронной.
2.  Docstring’и (если они есть) используются для извлечения описаний и описаний аргументов
3.  Функции могут опционально принимать `context` (он должен быть первым аргументом). Также можно задавать override’ы: имя инструмента, описание, стиль docstring и т.д.
4.  Декорированные функции можно передавать в список `tools`.

??? note "Раскрыть, чтобы увидеть вывод"

    ```
    check_ip_reputation
    Check if an IP address has a bad reputation.
    {
      "$defs": {
        "IPAddress": {
          "properties": {
            "ip": {
              "title": "Ip",
              "type": "string"
            }
          },
          "required": [
            "ip"
          ],
          "title": "IPAddress",
          "type": "object",
          "additionalProperties": false
        }
      },
      "properties": {
        "ip_data": {
          "description": "A dictionary with the IP address to check.",
          "properties": {
            "ip": {
              "title": "Ip",
              "type": "string"
            }
          },
          "required": [
            "ip"
          ],
          "title": "IPAddress",
          "type": "object",
          "additionalProperties": false
        }
      },
      "required": [
        "ip_data"
      ],
      "title": "check_ip_reputation_args",
      "type": "object",
      "additionalProperties": false
    }

    read_log_file
    Read the contents of a log file.
    {
      "properties": {
        "path": {
          "description": "The path to the log file.",
          "title": "Path",
          "type": "string"
        },
        "directory": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "description": "The optional directory to search in.",
          "title": "Directory"
        }
      },
      "required": [
        "path",
        "directory"
      ],
      "title": "read_log_file_args",
      "type": "object",
      "additionalProperties": false
    }
    ```

### Пользовательские function tools

Иногда вы не хотите использовать Python-функцию как инструмент. В этом случае вы можете напрямую создать [`FunctionTool`][cai.sdk.agents.tool.FunctionTool] — если вам удобнее такой подход. Вам потребуется:

-   `name`
-   `description`
-   `params_json_schema` — JSON-схема аргументов
-   `on_invoke_tool` — асинхронная функция, которая получает context и аргументы в виде JSON-строки и должна вернуть output инструмента строкой

```python
from typing import Any
from pydantic import BaseModel
from cai.sdk.agents import RunContextWrapper, FunctionTool


def do_some_work(data: str) -> str:
    return "done"

class FunctionArgs(BaseModel):
    username: str
    age: int


async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return do_some_work(data=f"{parsed.username} is {parsed.age} years old")


tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function,
)
```

### Автоматический парсинг аргументов и docstring

Как было сказано выше, мы автоматически парсим сигнатуру функции, чтобы извлечь схему для инструмента, а также парсим docstring для получения описаний инструмента и его отдельных аргументов. Несколько заметок:

1.  Парсинг сигнатуры выполняется через модуль `inspect`. Мы используем type annotations, чтобы понять типы аргументов, и динамически строим Pydantic-модель, которая представляет общую схему. Поддерживается большинство типов, включая базовые типы Python, модели Pydantic, `TypedDict` и др.
2.  Мы используем `griffe` для парсинга docstring. Поддерживаемые форматы docstring: `google`, `sphinx` и `numpy`. Мы пробуем автоматически определить формат, но это best-effort; при необходимости вы можете явно указать формат при вызове `function_tool`. Также можно отключить парсинг docstring, установив `use_docstring_info` в `False`.

Код извлечения схемы находится в [`cai.sdk.agents.function_schema`][].

## Агенты как инструменты

В некоторых сценариях вам может понадобиться центральный агент, который оркестрирует сеть специализированных агентов — вместо передачи управления (handoff). Это можно сделать, моделируя агентов как инструменты.

```python
from cai.sdk.agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import asyncio

# Агент, который имитирует сканирование IP на наличие угроз
ip_scanner_agent = Agent(
    name="IP Scanner",
    instructions="Вы предоставляете IP-адрес, а агент отвечает со статусом угроз (например, malicious или clean).",
)

# Агент, который имитирует анализ лог-файла
log_analyzer_agent = Agent(
    name="Log Analyzer",
    instructions="Вы получаете путь к лог-файлу и отвечаете с любыми подозрительными находками из логов.",
    model=OpenAIChatCompletionsModel(
        model="qwen2.5:14b",
        openai_client=AsyncOpenAI(),
    )
)

# Оркестратор-агент, который маршрутизирует задачи к нужному инструменту
cyber_orchestrator_agent = Agent(
    name="Cyber Orchestrator",
    instructions=(
        "You are a cybersecurity assistant. Based on the user's request, you decide whether to scan an IP or analyze a log. "
        "Use the appropriate tool for each task."
    ),
    tools=[
        ip_scanner_agent.as_tool(
            tool_name="scan_ip",
            tool_description="Сканирует IP-адрес на наличие возможных угроз",
        ),
        log_analyzer_agent.as_tool(
            tool_name="analyze_log",
            tool_description="Анализирует системный log-файл на предмет подозрительной активности",
        ),
    ],
    model=OpenAIChatCompletionsModel(
        model="qwen2.5:14b",
        openai_client=AsyncOpenAI(),
    )
)

# Основная функция: просим оркестратор-агента просканировать IP
async def main():
    # Пример входных данных
    result = await Runner.run(cyber_orchestrator_agent, input="Scan the IP address 192.168.0.10 for threats.")
    print(result.final_output)

# Запуск асинхронной main-функции
if __name__ == "__main__":
    asyncio.run(main())
```

## Обработка ошибок в function tools

При создании function tool через `@function_tool` вы можете передать `failure_error_function`. Это функция, которая формирует ответ об ошибке для LLM в случае, если вызов инструмента падает.

-   По умолчанию (если вы ничего не передаёте) запускается `default_tool_error_function`, которая сообщает LLM, что произошла ошибка.
-   Если вы передаёте свою error-функцию, будет использоваться она, и её ответ отправится в LLM.
-   Если явно передать `None`, ошибки вызовов инструмента будут пробрасываться дальше — например, как `ModelBehaviorError` (если модель сгенерировала некорректный JSON) или `UserError` (если упала ваша логика).

Если вы вручную создаёте объект `FunctionTool`, то вам нужно обрабатывать ошибки внутри `on_invoke_tool`.

---

[1] Arguably, the Chain-of-Thought agentic pattern is a special case of the Hierarchical agentic pattern.
[2] Kamhoua, C. A., Leslie, N. O., & Weisman, M. J. (2018). Game theoretic modeling of advanced persistent threat in internet of things. Journal of Cyber Security and Information Systems.
[3] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023, January). React: Synergizing reasoning and acting in language models. In International Conference on Learning Representations (ICLR).

