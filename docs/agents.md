# Агенты

Агенты — основа CAI. Агент использует большие языковые модели (LLM), настроенные инструкциями и инструментами для выполнения специализированных задач кибербезопасности. Каждый агент определён в отдельном файле `.py` в `src/cai/agents` и оптимизирован под конкретные домены безопасности.

## Доступные агенты

CAI предоставляет набор специализированных агентов для разных сценариев кибербезопасности:

| Агент | Описание | Основной сценарий использования | Ключевые инструменты |
|-------|-----------|----------------------------------|------------------------|
| **redteam_agent** | Специалист по атакующей безопасности для пентестинга | Активная эксплуатация, поиск уязвимостей | nmap, metasploit, burp |
| **blueteam_agent** | Эксперт по защитной безопасности для снижения угроз | Укрепление защиты, реагирование на инциденты | wireshark, suricata, osquery |
| **bug_bounter_agent** | Охотник за багами, оптимизированный под исследование уязвимостей | Безопасность веб-приложений, тестирование API | ffuf, sqlmap, nuclei |
| **one_tool_agent** | Минималистичный агент, ориентированный на выполнение одной команды/инструмента | Быстрые проверки, операции конкретных инструментов | Команды Generic Linux |
| **dfir_agent** | Эксперт по цифровой криминалистике и реагированию на инциденты | Анализ логов, форензика | volatility, autopsy, log2timeline |
| **reverse_engineering_agent** | Анализ бинарников и обратная разработка | Анализ вредоносного ПО, реверс прошивок | ghidra, radare2, ida |
| **memory_analysis_agent** | Специалист по анализу дампов памяти | Форензика RAM, анализ процессов | volatility, rekall |
| **network_traffic_analyzer** | Эксперт по анализу сетевых пакетов | Разбор PCAP, инспекция трафика | wireshark, tcpdump, tshark |
| **android_sast_agent** | Статический анализ безопасности Android (SAST) | Разбор APK, сканирование уязвимостей Android | jadx, apktool, mobsf |
| **wifi_security_tester** | Оценка безопасности беспроводных сетей | Пентест Wi-Fi, подбор WPA | aircrack-ng, reaver, wifite |
| **replay_attack_agent** | Специалист по выполнению replay-атак | Replay протоколов, обход аутентификации | пользовательские скрипты, burp |
| **subghz_sdr_agent** | Эксперт по анализу сигналов SDR в диапазоне Sub‑GHz | Анализ RF, тестирование IoT‑протоколов | hackrf, gqrx, urh |

### Быстрый старт с агентами

```bash
# Запустить CAI с указанным агентом
CAI_AGENT_TYPE=redteam_agent cai

# Запустить с собственной моделью
CAI_AGENT_TYPE=bug_bounter_agent CAI_MODEL=alias0 cai

# Или переключиться между агентами во время сессии
CAI>/agent redteam_agent

# Показать список доступных агентов с описаниями
CAI>/agent list

# Получить подробную информацию об агенте
CAI>/agent info redteam_agent
```

### Выбор подходящего агента

- **Для общего пентестинга**: начинайте с `redteam_agent`
- **Для веб-приложений**: используйте `bug_bounter_agent`
- **Для форензики**: используйте `dfir_agent` или `memory_analysis_agent`
- **Для IoT/встроенных устройств**: попробуйте `subghz_sdr_agent` или `reverse_engineering_agent`
- **Для сетевой безопасности**: используйте `network_traffic_analyzer` или `blueteam_agent`
- **Для мобильных приложений**: используйте `android_sast_agent`
- **Для беспроводных сетей**: используйте `wifi_security_tester`

---

## Матрица возможностей агентов

| Возможность | redteam | blueteam | bug_bounty | dfir | reverse_eng | network |
|-----------|---------|----------|------------|------|-------------|---------|
| **Тестирование веб-приложений** | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ |
| **Анализ сети** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| **Анализ бинарников** | ⭐⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| **Форензика** | ⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **IoT/встроенные устройства** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Тестирование API** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ |
| **Разработка эксплойтов** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐ |

**Легенда**: ⭐ Ограничено | ⭐⭐⭐ Средне | ⭐⭐⭐⭐⭐ Отлично

---

## Общие рабочие сценарии агентов

### Сценарий 1: полный пентест веб-приложения

```bash
# 1. Начать с разведки
CAI>/agent bug_bounter_agent
CAI> Scan https://target.com for vulnerabilities

# 2. Переключиться на эксплуатацию
CAI>/agent redteam_agent  
CAI> Exploit the SQL injection found at /login

# 3. Анализ пост-эксплуатации
CAI>/agent dfir_agent
CAI> Analyze the logs to understand the attack surface
```

### Сценарий 2: оценка безопасности IoT-устройства

```bash
# 1. Анализ радиосигналов
CAI>/agent subghz_sdr_agent
CAI> Analyze the 433MHz signals from the device

# 2. Анализ прошивки
CAI>/agent reverse_engineering_agent
CAI> Extract and analyze the firmware from dump.bin

# 3. Анализ памяти, если устройство было захвачено
CAI>/agent memory_analysis_agent
CAI> Analyze the memory dump for secrets
```

### Сценарий 3: реагирование на сетевой инцидент

```bash
# 1. Анализ сетевого трафика
CAI>/agent network_traffic_analyzer
CAI> Analyze capture.pcap for suspicious activity

# 2. Форензика
CAI>/agent dfir_agent
CAI> Investigate the compromised host logs

# 3. Защитные рекомендации
CAI>/agent blueteam_agent
CAI> Provide mitigation strategies based on findings
```

---

## Базовая конфигурация

Ключевые свойства агента включают:

-   `name`: имя агента (например, имя `one_tool_agent` — «CTF Agent»)
-   `instructions`: системный prompt, задающий поведение агента
-   `model`: какая LLM используется, с опциональными `model_settings` для настройки параметров, таких как temperature, top_p и т.д.
-   `tools`: инструменты, которыми агент может пользоваться для выполнения задач
-   `handoffs`: позволяет агенту делегировать задачи другому агенту

## Пример: `one_tool_agent.py`

```python
from cai.sdk.agents import Agent, OpenAIChatCompletionsModel
from cai.tools.reconnaissance.generic_linux_command import generic_linux_command 
from openai import AsyncOpenAI

one_tool_agent = Agent(
    name="CTF agent",
    description="Агент, сосредоточенный на решении задач по безопасности с помощью generic linux команд",
    instructions="Вы эксперт по кибербезопасности, решающий задачу CTF.",
    tools=[
        generic_linux_command,
    ],
    model=OpenAIChatCompletionsModel(
        model="qwen2.5:14b",
        openai_client=AsyncOpenAI(),
    )
)
```


## Контекст

Существует два основных типа контекста. Подробнее см. [context](context.md).

Агенты параметризуются типом `context`. Контекст — это инструмент внедрения зависимостей: это объект, который вы создаёте и передаёте в `Runner.run()`. Он передаётся каждому агенту, инструменту, handoff и служит контейнером зависимостей и состояния для запуска агента. Вы можете передать любой Python-объект в качестве контекста.

```python
@dataclass
class SecurityContext:
  target_system: str
  is_compromised: bool

  async def get_exploits() -> list[Exploits]:
     return ...

agent = Agent[SecurityContext](
    ...,
)
```

## Типы выходных данных

По умолчанию агенты возвращают обычный текст (т.е. `str`). Если вы хотите, чтобы агент выдавал определённый тип данных, вы можете использовать параметр `output_type`. Частый выбор — использовать объекты [Pydantic](https://docs.pydantic.dev/), но мы поддерживаем любой тип, который можно обернуть в Pydantic [TypeAdapter](https://docs.pydantic.dev/latest/api/type_adapter/) — dataclass, список, TypedDict и т.д.

```python
from pydantic import BaseModel
from cai.sdk.agents import Agent

class SecurityVulnerability(BaseModel):
    name: str
    severity: str
    affected_files: list[str]
    description: str

agent = Agent(
    name="Vulnerability scanner",
    instructions="Проанализируйте вывод системы и определите уязвимости безопасности",
    output_type=SecurityVulnerability,
)
```

 cd /Users/system/Documents/mybuild/cairus && cat > docs/agents.md <<'EOF'
# Агенты

Агенты — основа CAI. Агент использует большие языковые модели (LLM), настроенные инструкциями и инструментами для выполнения специализированных задач кибербезопасности. Каждый агент определён в отдельном файле `.py` в `src/cai/agents` и оптимизирован под конкретные домены безопасности.

## Доступные агенты

CAI предоставляет набор специализированных агентов для разных сценариев кибербезопасности:

| Агент | Описание | Основной сценарий использования | Ключевые инструменты |
|-------|-----------|----------------------------------|------------------------|
| **redteam_agent** | Специалист по атакующей безопасности для пентестинга | Активная эксплуатация, поиск уязвимостей | nmap, metasploit, burp |
| **blueteam_agent** | Эксперт по защитной безопасности для снижения угроз | Укрепление защиты, реагирование на инциденты | wireshark, suricata, osquery |
| **bug_bounter_agent** | Охотник за багами, оптимизированный под исследование уязвимостей | Безопасность веб-приложений, тестирование API | ffuf, sqlmap, nuclei |
| **one_tool_agent** | Минималистичный агент, ориентированный на выполнение одной команды/инструмента | Быстрые проверки, операции конкретных инструментов | Команды Generic Linux |
| **dfir_agent** | Эксперт по цифровой криминалистике и реагированию на инциденты | Анализ логов, форензика | volatility, autopsy, log2timeline |
| **reverse_engineering_agent** | Анализ бинарников и обратная разработка | Анализ вредоносного ПО, реверс прошивок | ghidra, radare2, ida |
| **memory_analysis_agent** | Специалист по анализу дампов памяти | Форензика RAM, анализ процессов | volatility, rekall |
| **network_traffic_analyzer** | Эксперт по анализу сетевых пакетов | Разбор PCAP, инспекция трафика | wireshark, tcpdump, tshark |
| **android_sast_agent** | Статический анализ безопасности Android (SAST) | Разбор APK, сканирование уязвимостей Android | jadx, apktool, mobsf |
| **wifi_security_tester** | Оценка безопасности беспроводных сетей | Пентест Wi-Fi, подбор WPA | aircrack-ng, reaver, wifite |
| **replay_attack_agent** | Специалист по выполнению replay-атак | Replay протоколов, обход аутентификации | пользовательские скрипты, burp |
| **subghz_sdr_agent** | Эксперт по анализу сигналов SDR в диапазоне Sub‑GHz | Анализ RF, тестирование IoT‑прототоколов | hackrf, gqrx, urh |

### Быстрый старт с агентами

```bash
# Запустить CAI с указанным агентом
CAI_AGENT_TYPE=redteam_agent cai

# Запустить с собственной моделью
CAI_AGENT_TYPE=bug_bounter_agent CAI_MODEL=alias0 cai

# Или переключиться между агентами во время сессии
CAI>/agent redteam_agent

# Показать список доступных агентов с описаниями
CAI>/agent list

# Получить подробную информацию об агенте
CAI>/agent info redteam_agent
```

### Выбор подходящего агента

- **Для общего пентестинга**: начинайте с `redteam_agent`
- **Для веб-приложений**: используйте `bug_bounter_agent`
- **Для форензики**: используйте `dfir_agent` или `memory_analysis_agent`
- **Для IoT/встроенных устройств**: попробуйте `subghz_sdr_agent` или `reverse_engineering_agent`
- **Для сетевой безопасности**: используйте `network_traffic_analyzer` или `blueteam_agent`
- **Для мобильных приложений**: используйте `android_sast_agent`
- **Для беспроводных сетей**: используйте `wifi_security_tester`

---

## Матрица возможностей агентов

| Возможность | redteam | blueteam | bug_bounty | dfir | reverse_eng | network |
|-----------|---------|----------|------------|------|-------------|---------|
| **Тестирование веб-приложений** | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ |
| **Анализ сети** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| **Анализ бинарников** | ⭐⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| **Форензика** | ⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **IoT/встроенные устройства** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Тестирование API** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ |
| **Разработка эксплойтов** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐ |

**Легенда**: ⭐ Ограничено | ⭐⭐⭐ Средне | ⭐⭐⭐⭐⭐ Отлично

---

## Общие рабочие сценарии агентов

### Сценарий 1: полный пентест веб-приложения

```bash
# 1. Начать с разведки
CAI>/agent bug_bounter_agent
CAI> Scan https://target.com for vulnerabilities

# 2. Переключиться на эксплуатацию
CAI>/agent redteam_agent  
CAI> Exploit the SQL injection found at /login

# 3. Анализ пост-эксплуатации
CAI>/agent dfir_agent
CAI> Analyze the logs to understand the attack surface
```

### Сценарий 2: оценка безопасности IoT-устройства

```bash
# 1. Анализ радиосигналов
CAI>/agent subghz_sdr_agent
CAI> Analyze the 433MHz signals from the device

# 2. Анализ прошивки
CAI>/agent reverse_engineering_agent
CAI> Extract and analyze the firmware from dump.bin

# 3. Анализ памяти, если устройство было захвачено
CAI>/agent memory_analysis_agent
CAI> Analyze the memory dump for secrets
```

### Сценарий 3: реагирование на сетевой инцидент

```bash
# 1. Анализ сетевого трафика
CAI>/agent network_traffic_analyzer
CAI> Analyze capture.pcap for suspicious activity

# 2. Форензика
CAI>/agent dfir_agent
CAI> Investigate the compromised host logs

# 3. Защитные рекомендации
CAI>/agent blueteam_agent
CAI> Provide mitigation strategies based on findings
```

---

## Базовая конфигурация

Ключевые свойства агента включают:

-   `name`: имя агента (например, имя `one_tool_agent` — «CTF Agent»)
-   `instructions`: системный prompt, задающий поведение агента
-   `model`: какая LLM используется, с опциональными `model_settings` для настройки параметров, таких как temperature, top_p и т.д.
-   `tools`: инструменты, которыми агент может пользоваться для выполнения задач
-   `handoffs`: позволяет агенту делегировать задачи другому агенту

## Пример: `one_tool_agent.py`

```python
from cai.sdk.agents import Agent, OpenAIChatCompletionsModel
from cai.tools.reconnaissance.generic_linux_command import generic_linux_command 
from openai import AsyncOpenAI

one_tool_agent = Agent(
    name="CTF agent",
    description="Агент, сосредоточенный на решении задач по безопасности с помощью generic linux команд",
    instructions="Вы эксперт по кибербезопасности, решающий задачу CTF.",
    tools=[
        generic_linux_command,
    ],
    model=OpenAIChatCompletionsModel(
        model="qwen2.5:14b",
        openai_client=AsyncOpenAI(),
    )
)
```

## Контекст

Существует два основных типа контекста. Подробнее см. [context](context.md).

Агенты параметризуются типом `context`. Контекст — это инструмент внедрения зависимостей: это объект, который вы создаёте и передаёте в `Runner.run()`. Он передаётся каждому агенту, инструменту, handoff и служит контейнером зависимостей и состояния для запуска агента. Вы можете передать любой Python-объект в качестве контекста.

```python
@dataclass
class SecurityContext:
  target_system: str
  is_compromised: bool

  async def get_exploits() -> list[Exploits]:
     return ...

agent = Agent[SecurityContext](
    ...,
)
```

## Типы выходных данных

По умолчанию агенты возвращают обычный текст (т.е. `str`). Если вы хотите, чтобы агент выдавал определённый тип данных, вы можете использовать параметр `output_type`. Частый выбор — использовать объекты [Pydantic](https://docs.pydantic.dev/), но мы поддерживаем любой тип, который можно обернуть в Pydantic [TypeAdapter](https://docs.pydantic.dev/latest/api/type_adapter/) — dataclass, список, TypedDict и т.д.

```python
from pydantic import BaseModel
from cai.sdk.agents import Agent

class SecurityVulnerability(BaseModel):
    name: str
    severity: str
    affected_files: list[str]
    description: str

agent = Agent(
    name="Vulnerability scanner",
    instructions="Проанализируйте вывод системы и определите уязвимости безопасности",
    output_type=SecurityVulnerability,
)
```

 cd /Users/system/Documents/mybuild/cairus && python3 - <<'PY'
import pathlib, re
root = pathlib.Path('.').resolve()
eng = re.compile(r"(This|Use|Example|Guide|API|Documentation|Learn|Run|warning|success|Important|Note|Notes|Requirements|Install|Configure|Setup)", re.I)
files=[]
for p in sorted(root.rglob('*.md')):
    text=p.read_text(encoding='utf-8', errors='ignore')
    if eng.search(text):
        files.append(str(p.relative_to(root)))
with open(root / 'md_english_files.txt','w',encoding='utf-8') as f:
    f.write('
'.join(files))
print(len(files))
PY! note
   Если вы задаёте `output_type`, это сообщает модели, что нужно использовать структурированный вывод вместо обычного текстового ответа.

## Handoffs

Handoffs — это суб-агенты, которым основной агент может делегировать задачи. Вы указываете список `handoffs`, и агент может выбрать делегирование им, если это уместно. Это мощный паттерн, позволяющий оркестрировать модульные, специализированные агенты, каждый из которых отлично справляется со своей задачей. Подробнее см. документацию по [handoffs](handoffs.md).

```python
from cai.sdk.agents import Agent

crypto_agent = Agent(
    name="Cryptography agent",
    description="Агент, специализирующийся на решении криптографических задач и расшифровке зашифрованных сообщений",
    instructions="Анализируйте зашифрованные данные и применяйте криптографические методы для их расшифровки.",
    tools=[
        execute_cli_command,
    ],
    handoff_description="Специализированный агент по криптографии и взлому шифров",
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CAI_MODEL', "qwen2.5:14b"),
        openai_client=AsyncOpenAI(),
    )
)
network_agent = Agent(
    name="Network Agent",
    description="Агент, специализирующийся на сетевом анализе, инспекции пакетов и оценке сетевой безопасности",
    instructions="Анализируйте сетевой трафик, выявляйте подозрительные паттерны и помогайте с задачами CTF, связанными с сетью",
    handoff_description="Специализированный агент по сетевой безопасности, анализу трафика и пониманию протоколов",
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CAI_MODEL', "qwen2.5:72b"),
        openai_client=AsyncOpenAI(),
    )
)
lead_agent = Agent(
    name="Cybersecurity Lead Agent",
    instructions=(
        "Вы ведущий эксперт по кибербезопасности, координирующий операции по безопасности. "
        "Если пользователю нужен сетевой анализ или инспекция трафика, передавайте задачу сети. "
        "Если пользователю нужны криптографические решения или взлом шифров, передавайте задачу криптоагенту."
    ),
    handoffs=[network_agent, crypto_agent],
    model="qwen2.5:72b"
)
```

## Динамические инструкции

В большинстве случаев инструкции задаются при создании агента. Однако вы также можете передавать динамические инструкции через функцию. Функция получает агента и контекст и должна вернуть prompt. Принимаются как обычные, так и `async` функции.

```python
def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    security_level = "high" if context.context.is_admin else "standard"
    return f"Вы помогаете {context.context.name} с операциями по кибербезопасности. Уровень допуска: {security_level}. Постройте рекомендации в соответствии с уровнем и сосредоточьтесь на текущих проблемах безопасности."

agent = Agent[UserContext](
    name="Cybersecurity Triage Agent",
    instructions=dynamic_instructions,
)
```

### Запуск

```bash
cai
```

### Оптимизация производительности

**1. Используйте стриминг для более быстрой реакции:**
```bash
CAI_STREAM=true cai
```
**2. Включите трассировку для отладки:**
```bash
CAI_TRACING=true cai
```

---

## Лучшие практики работы с агентами

### 1. Начинайте с правильного агента

Не используйте специализированного агента для общих задач. Соответствуйте агент задаче:

```bash
# ✅ Хорошо: агент bug bounty для веб-тестирования
CAI_AGENT_TYPE=bug_bounter_agent cai
CAI> Test https://target.com for vulnerabilities

# ❌ Плохо: агент reverse engineering для веб-тестирования
CAI_AGENT_TYPE=reverse_engineering_agent cai
CAI> Test https://target.com for vulnerabilities
```

### 2. Переключайтесь между агентами по мере необходимости

Не бойтесь менять агента в середине сессии:

```bash
CAI>/agent bug_bounter_agent
CAI> Find vulnerabilities in the web app
# ... агент находит SQL-инъекцию ...

CAI>/agent redteam_agent
CAI> Exploit the SQL injection to gain access
# ... успешная эксплуатация ...

CAI>/agent dfir_agent
CAI> Analyze what data was exposed during the test
```

### 3. Отслеживайте использование ресурсов

Следите за затратами и производительностью:

```bash
# Во время сессии проверьте затраты
CAI>/cost

# Установите лимиты перед запуском
CAI_PRICE_LIMIT="5.00" CAI_MAX_TURNS=50 cai
```

### 4. Сохраняйте успешные сессии

Используйте `/load`, чтобы повторно применить удачные подходы:

```bash
# В следующей сессии
CAI>/load logs/logname.jsonl
```

---

## Следующие шаги

- **Запуск агентов**: см. документацию [running_agents](running_agents.md) для деталей запуска
- **Понимание результатов**: см. [results](results.md) для интерпретации выводов
- **Инструменты агента**: см. документацию [tools](tools.md) для доступных инструментов
- **Handoffs**: см. документацию [handoffs](handoffs.md) для координации агентов
- **Интеграция MCP**: см. документацию [mcp](mcp.md) для подключения внешних инструментов
- **Мультиагентные паттерны**: см. документацию [multi_agent](multi_agent.md) для паттернов оркестрации
EOF! note
   Если вы задаёте `output_type`, это сообщает модели, что нужно использовать структурированный вывод вместо обычного текстового ответа.

## Handoffs

Handoffs — это суб-агенты, которым основной агент может делегировать задачи. Вы указываете список `handoffs`, и агент может выбрать делегирование им, если это уместно. Это мощный паттерн, позволяющий оркестрировать модульные, специализированные агенты, каждый из которых отлично справляется со своей задачей. Подробнее см. документацию по [handoffs](handoffs.md).

```python
from cai.sdk.agents import Agent

crypto_agent = Agent(
    name="Cryptography agent",
    description="Агент, специализирующийся на решении криптографических задач и расшифровке зашифрованных сообщений",
    instructions="Анализируйте зашифрованные данные и применяйте криптографические методы для их расшифровки.",
    tools=[
        execute_cli_command,
    ],
    handoff_description="Специализированный агент по криптографии и взлому шифров",
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CAI_MODEL', "qwen2.5:14b"),
        openai_client=AsyncOpenAI(),
    )
)
network_agent = Agent(
    name="Network Agent",
    description="Агент, специализирующийся на сетевом анализе, инспекции пакетов и оценке сетевой безопасности",
    instructions="Анализируйте сетевой трафик, выявляйте подозрительные паттерны и помогайте с задачами CTF, связанными с сетью",
    handoff_description="Специализированный агент по сетевой безопасности, анализу трафика и пониманию протоколов",
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CAI_MODEL', "qwen2.5:72b"),
        openai_client=AsyncOpenAI(),
    )
)
lead_agent = Agent(
    name="Cybersecurity Lead Agent",
    instructions=(
        "Вы ведущий эксперт по кибербезопасности, координирующий операции по безопасности. "
        "Если пользователю нужен сетевой анализ или инспекция трафика, передавайте задачу сети. "
        "Если пользователю нужны криптографические решения или взлом шифров, передавайте задачу криптоагенту."
    ),
    handoffs=[network_agent, crypto_agent],
    model="qwen2.5:72b"
)
```

## Динамические инструкции

В большинстве случаев инструкции задаются при создании агента. Однако вы также можете передавать динамические инструкции через функцию. Функция получает агента и контекст и должна вернуть prompt. Принимаются как обычные, так и `async` функции.

```python
def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    security_level = "high" if context.context.is_admin else "standard"
    return f"Вы помогаете {context.context.name} с операциями по кибербезопасности. Уровень допуска: {security_level}. Постройте рекомендации в соответствии с уровнем и сосредоточьтесь на текущих проблемах безопасности."

agent = Agent[UserContext](
    name="Cybersecurity Triage Agent",
    instructions=dynamic_instructions,
)
```

### Запуск

```bash
cai
```

### Оптимизация производительности

**1. Используйте стриминг для более быстрой реакции:**
```bash
CAI_STREAM=true cai
```
**2. Включите трассировку для отладки:**
```bash
CAI_TRACING=true cai
```

---

## Лучшие практики работы с агентами

### 1. Начинайте с правильного агента

Не используйте специализированного агента для общих задач. Соответствуйте агент задаче:

```bash
# ✅ Хорошо: агент bug bounty для веб-тестирования
CAI_AGENT_TYPE=bug_bounter_agent cai
CAI> Test https://target.com for vulnerabilities

# ❌ Плохо: агент reverse engineering для веб-тестирования
CAI_AGENT_TYPE=reverse_engineering_agent cai
CAI> Test https://target.com for vulnerabilities
```

### 2. Переключайтесь между агентами по мере необходимости

Не бойтесь менять агента в середине сессии:

```bash
CAI>/agent bug_bounter_agent
CAI> Find vulnerabilities in the web app
# ... агент находит SQL-инъекцию ...

CAI>/agent redteam_agent
CAI> Exploit the SQL injection to gain access
# ... успешная эксплуатация ...

CAI>/agent dfir_agent
CAI> Analyze what data was exposed during the test
```

### 3. Отслеживайте использование ресурсов

Следите за затратами и производительностью:

```bash
# Во время сессии проверьте затраты
CAI>/cost

# Установите лимиты перед запуском
CAI_PRICE_LIMIT="5.00" CAI_MAX_TURNS=50 cai
```

### 4. Сохраняйте успешные сессии

Используйте `/load`, чтобы повторно применить удачные подходы:

```bash
# В следующей сессии
CAI>/load logs/logname.jsonl
```

---

## Следующие шаги

- **Запуск агентов**: см. документацию [running_agents](running_agents.md) для деталей запуска
- **Понимание результатов**: см. [results](results.md) для интерпретации выводов
- **Инструменты агента**: см. документацию [tools](tools.md) для доступных инструментов
- **Handoffs**: см. документацию [handoffs](handoffs.md) для координации агентов
- **Интеграция MCP**: см. документацию [mcp](mcp.md) для подключения внешних инструментов
- **Мультиагентные паттерны**: см. документацию [multi_agent](multi_agent.md) для паттернов оркестрации
