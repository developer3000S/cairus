# Handoffs

Handoffs позволяют агенту делегировать задачу другому агенту. Это особенно полезно в сценариях, где разные агенты специализируются на разных областях. Например, в приложении поддержки клиентов могут быть агенты, которые обрабатывают только статус заказа, возвраты, часто задаваемые вопросы и т.п.

Handoffs представлены как инструменты для LLM. Поэтому если происходит передача агенту с именем `Flag Discriminator`, инструмент будет называться `transfer_to_flag_discriminator`.

## Создание handoff

У всех агентов есть параметр [`handoffs`][cai.sdk.agents.agent.Agent.handoffs], который может принимать либо сам `Agent`, либо объект `Handoff`, настраивающий передачу.

Вы можете создать handoff с помощью функции [`handoff()`][cai.sdk.agents.handoffs.handoff]. Эта функция позволяет указать агента, которому будет передана задача, а также опциональные переопределения и фильтры ввода.

### Базовое использование

Вот как выглядит простое создание handoff:

```python
from cai.sdk.agents import Agent, handoff

crypto_agent = Agent(name="Cryptography Agent")
bash_agent = Agent(name="Bash Agent")

# (1)!
cybersecurity_lead = Agent(name="Cybersecurity Lead Agent", handoffs=[crypto_agent, handoff(bash_agent)])
```

1. Вы можете использовать агента напрямую (как `crypto_agent`) или использовать функцию `handoff()`.

### Настройка handoff через функцию `handoff()`

Функция [`handoff()`][cai.sdk.agents.handoffs.handoff] позволяет настраивать передачу.

-   `agent`: агент, которому будет передана задача.
-   `tool_name_override`: по умолчанию используется `Handoff.default_tool_name()`, который превращает имя агента в `transfer_to_<agent_name>`. Это можно переопределить.
-   `tool_description_override`: переопределяет описание инструмента по умолчанию, которое берётся из `Handoff.default_tool_description()`.
-   `on_handoff`: callback-функция, выполняющаяся при вызове handoff. Это полезно для запуска дополнительной загрузки данных сразу после того, как handoff вызван. Эта функция получает контекст агента и может опционально принять входные данные от LLM. Входные данные контролируются параметром `input_type`.
-   `input_type`: тип ожидаемого ввода для handoff (опционально).
-   `input_filter`: позволяет фильтровать ввод, который получит следующий агент. Подробнее ниже.

```python
from cai.sdk.agents import Agent, handoff, RunContextWrapper

def on_handoff(ctx: RunContextWrapper[None]):
    print("Handoff called")

agent = Agent(name="My agent")

handoff_obj = handoff(
    agent=agent,
    on_handoff=on_handoff,
    tool_name_override="custom_handoff_tool",
    tool_description_override="Custom description",
)
```

## Входные данные handoff

В некоторых ситуациях вы хотите, чтобы LLM передавал дополнительные данные при вызове handoff. Например, если handoff идёт на «агента эскалации», может потребоваться причина, чтобы её можно было сохранить в лог.

```python
from pydantic import BaseModel

from cai.sdk.agents import Agent, handoff, RunContextWrapper

class EscalationData(BaseModel):
    reason: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"Escalation agent called with reason: {input_data.reason}")

agent = Agent(name="Escalation agent")

handoff_obj = handoff(
    agent=agent,
    on_handoff=on_handoff,
    input_type=EscalationData,
)
```

## Фильтры ввода

Когда происходит handoff, создаётся впечатление, что новый агент принимает управление беседой и видит всю предыдущую историю. Если вы хотите изменить этот ввод, можно задать [`input_filter`][cai.sdk.agents.handoffs.Handoff.input_filter]. Фильтр ввода — это функция, которая получает текущие данные через [`HandoffInputData`][cai.sdk.agents.handoffs.HandoffInputData] и должна вернуть новый `HandoffInputData`.

Есть несколько распространённых шаблонов (например, удаление всех вызовов инструментов из истории), которые реализованы за вас в [`cai.sdk.agents.extensions.handoff_filters`][].

```python
from cai.sdk.agents import Agent, handoff
from agents.extensions import handoff_filters

network_agent = Agent(name="Network Agent")

handoff_obj = handoff(
    agent=network_agent,
    input_filter=handoff_filters.remove_all_tools, # (1)!
)
```

(1). Это автоматически удалит все инструменты из истории, когда будет вызван `Network Agent`.

## Рекомендуемые подсказки

Чтобы LLM корректно понимало handoffs, мы рекомендуем включать информацию о handoff в промпты агентов. У нас есть предложенный префикс в [`cai.sdk.agents.extensions.handoff_prompt.RECOMMENDED_PROMPT_PREFIX`][]. Либо вы можете вызвать [`cai.sdk.agents.extensions.handoff_prompt.prompt_with_handoff_instructions`][], чтобы автоматически добавить рекомендуемые инструкции к промпту.

```python
from cai.sdk.agents import Agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

billing_agent = Agent(
    name="Phising Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    <Fill in the rest of your prompt here>.""",
)
```

## Пример «всё в одном»

```
Мы покажем следующий рабочий процесс. Вы можете сделать его проще или сложнее, в зависимости от ваших потребностей.

                     ┌───────────────────┐
                     │ Cybersecurity     │
User Request ───────►│ Lead Agent        │
                     └───────┬───────────┘
              ┌──────────────┴──────────────┐
              │                             │
    ┌─────────▼────────┐         ┌─────────▼────────┐
    │ Bash Agent       │         │ Crypto Agent     │
    └─────────┬────────┘         └──────────────────┘
              │
    ┌─────────▼────────┐
    │ Flag             │
    │ Discriminator    │
    └──────────────────┘
```


```python
from cai.sdk.agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from cai.sdk.agents import handoff, function_tool, trace
from cai.sdk.agents import Runner
from cai.tools.common import run_command
from cai.sdk.agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
import os
import asyncio


@function_tool
def execute_cli_command(command: str) -> str:
    """Выполняет команду командной строки и возвращает её вывод."""
    return run_command(command)


# Создаём агент Flag Discriminator (терминальный агент в цепочке)
flag_discriminator = Agent(
    name="Flag Discriminator Agent",
    description="Агент, специализирующийся на проверке, соответствует ли контент ожидаемому формату флага в CTF.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    Вы эксперт по распознаванию CTF-флагов. Финальный флаг — это первый файл из вывода команды -ls. Вы возвращаете флаг в формате flag{{filename}}""",
    handoff_description="Специализированный агент для определения, соответствует ли контент флагу CTF.",
    handoffs=[],
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CAI_MODEL', "qwen2.5:72b"),
        openai_client=AsyncOpenAI(),
    )
)

# Создаём Bash Agent (может передавать задачу агенту Flag Discriminator)
bash_agent = Agent(
    name="Bash Agent",
    description="Агент, специализирующийся на bash-командах и операциях Linux.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    Вы эксперт по Bash и Linux. Используйте свои знания, чтобы перемещаться по файловой системе и выполнять команды.
    Финальный флаг — это первый элемент, указанный в директории.
    Когда вы найдёте имя файла, передайте задачу агенту Flag Discriminator для проверки.""",
    tools=[execute_cli_command],
    handoffs=[handoff(flag_discriminator)],
    handoff_description="Специализированный агент по bash-командам и операциям Linux.",
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CAI_MODEL', "qwen2.5:14b"),
        openai_client=AsyncOpenAI(),
    )
)

# Создаём Crypto Agent
crypto_agent = Agent(
    name="Cryptography Agent",
    description="Агент, специализирующийся на криптографии, шифрах и кодировании/декодировании.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    Вы эксперт по криптографии. Помогайте расшифровывать и декодировать зашифрованные сообщения или файлы.""",
    tools=[execute_cli_command],
    handoffs=[],
    handoff_description="Специализированный агент по криптографии и взлому кода.",
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CAI_MODEL', "qwen2.5:14b"),
        openai_client=AsyncOpenAI(),
    )
)

# Создаём Cybersecurity Lead Agent (может передать задачу и Bash, и Crypto)
cybersecurity_lead = Agent(
    name="Cybersecurity Lead Agent",
    description="Ведущий агент, сосредоточенный на решении задач безопасности с делегированием специализированным агентам.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    Вы эксперт по кибербезопасности, решающий задачи в области безопасности.
    - Передавайте задачу Bash Agent, когда нужно выполнить Linux-команды или перемещаться по файловой системе.
    - Передавайте задачу Cryptography Agent, когда вы сталкиваетесь с зашифрованными данными или кодами, которые нужно расшифровать.""",
    tools=[execute_cli_command],
    handoffs=[
        handoff(bash_agent),
        handoff(crypto_agent)
    ],
    handoff_description="Ведущий агент по операциям кибербезопасности.",
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CAI_MODEL', "qwen2.5:14b"),
        openai_client=AsyncOpenAI(),
    )
)


async def main():
    # Trace the entire run as a single workflow
    with trace(workflow_name="CTF Workflow"):
        # Run with cybersecurity_lead directly
        result = await Runner.run(cybersecurity_lead, "List directories to find the flag")

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```
