# Справочник переменных окружения

Это исчерпывающее руководство описывает все переменные окружения, доступные в CAI: их назначение, значения по умолчанию и примеры использования.

---

## 🔎 Поиск переменных в REPL

В текущих релизах CAI вы можете исследовать переменные окружения прямо **внутри интерактивного CLI**, не выходя из сессии:

| Что нужно | Команда |
| --- | --- |
| **Нумерованный список с текущими значениями** (что установлено *сейчас*) | `/env` или `/env list` для расширенного списка переменных |
| **Полные справочные таблицы** (значения по умолчанию, допустимые значения, когда применяются, доп. параметры) | `/help` — пролистайте быстрый гид до таблиц (`/help topics` выводит команды только по категориям, без env-таблиц) |
| **Развёрнутая помощь по одной переменной** (примеры, индекс `/env list`, примечания) | `/help var VARIABLE_NAME` (например, `/help var CAI_MODEL`) |

Псевдонимы вроде `/h` для `/help` работают аналогично. Эта страница остаётся **канонической веб-справкой**; вывод REPL отражает версию, которую вы установили.

---

## 📋 Полная справочная таблица

| Переменная | Описание | Значение по умолчанию |
| --- | --- | --- |
| CTF_NAME | Имя CTF-челленджа для запуска (например, "picoctf_static_flag") | - |
| CTF_CHALLENGE | Конкретное название челленджа внутри CTF для тестирования | - |
| CTF_SUBNET | Сетевая подсеть для контейнера с CTF | 192.168.3.0/24 |
| CTF_IP | IP-адрес для контейнера с CTF | 192.168.3.100 |
| CTF_INSIDE | Нужно ли "захватывать" CTF изнутри контейнера | true |
| CAI_MODEL | Модель для агентов | alias1 |
| CAI_DEBUG | Уровень отладочного вывода (0: только вывод инструментов, 1: подробный debug, 2: debug для CLI) | 1 |
| CAI_BRIEF | Включить/выключить краткий режим вывода | false |
| CAI_MAX_TURNS | Максимальное число "ходов" для взаимодействий агентов | inf |
| CAI_ORCHESTRATION_WORKER_MAX_TURNS | Максимум ходов `Runner` для каждого specialist worker, создаваемого инструментами `orchestration_agent` | 6 |
| CAI_ORCHESTRATION_MAS_HINT | Когда `true`, `orchestration_agent` может получить синтетический nudge для многофронтовых задач | true |
| CAI_MAX_INTERACTIONS | Максимум взаимодействий (вызовы инструментов, действия агентов и т.п.) за сессию | inf |
| CAI_PRICE_LIMIT | Лимит стоимости разговора в долларах | 1 |
| CAI_TRACING | Включить/выключить трассировку OpenTelemetry | true |
| CAI_AGENT_TYPE | Ключ зарегистрированного агента | orchestration_agent |
| CAI_STATE | Включить/выключить stateful-режим | false |
| CAI_COMPACTED_MEMORY | Добавляет в system prompt краткие сводки из `/compact` | false |
| CAI_ENV_CONTEXT | Добавляет контекст окружения в контекст LLM | true |
| CAI_SUPPORT_MODEL | Модель для агента поддержки | o3-mini |
| CAI_SUPPORT_INTERVAL | Число ходов между запусками агента поддержки | 5 |
| CAI_STREAM | Включить/выключить стриминг вывода для LLM-инференса | false |
| CAI_TOOL_STREAM | Включить/выключить стриминг вывода инструментов | true |
| CAI_DEBUG_TOOLS_VIZ | Включить отладочный вывод для визуализации инструментов | false |
| CAI_SHOW_CACHE | Показать информацию о кэше и список истории сообщений | false |
| CAI_TELEMETRY | Включить/выключить телеметрию | true |
| CAI_PARALLEL | Число параллельных экземпляров агента | 1 |
| CAI_GUARDRAILS | Включить/выключить security guardrails для агентов | false |
| CAI_GCTR_NITERATIONS | Число взаимодействий до запуска GCTR анализа в `bug_bounter_gctr` | 5 |
| CAI_ACTIVE_CONTAINER | ID Docker-контейнера для выполнения команд | - |
| C99_API_KEY | API-ключ для сервиса discovery C99.nl subdomain | - |
| CAI_TOOL_TIMEOUT | Переопределить таймаут для выполнения команд инструментов (в секундах) | varies |
| CAI_IDLE_TIMEOUT | Максимум секунд без вывода до остановки команды | 100 |
| CAI_CTX_TRUNC | Включить усечение контекста для больших выводов инструментов | false |
| CAI_DISPLAY_MAX_OUTPUT | Показывать полный вывод инструментов без усечения | false |

---

## 🎯 Быстрая справка по сценариям использования

### 🚀 Старт для новичков (самое важное)

Для первых пользователей — это переменные, которые нужно настроить в первую очередь:

```bash
# Требуется: выбор модели
CAI_MODEL="alias1"                    # или gpt-4o, claude-sonnet-4.5, ollama/qwen2.5:72b

# Рекомендуется: тип агента (по умолчанию CLI entry — orchestration_agent)
CAI_AGENT_TYPE="orchestration_agent" # breadth-first + specialist инструменты; selection_agent = только handoffs

# Опционально, но полезно: контроль стоимости
CAI_PRICE_LIMIT="1"                   # Максимальные затраты в долларах
```

### 🏴 CTF-челленджи

Для запуска Capture The Flag в контейнеризованных средах:

```bash
# Выбор челленджа
CTF_NAME="picoctf_static_flag"        # Имя CTF челленджа
CTF_CHALLENGE="web_exploitation_1"    # Конкретный под-челлендж

# Сетевая конфигурация
CTF_SUBNET="192.168.3.0/24"          # Подсеть контейнера
CTF_IP="192.168.3.100"               # IP контейнера

# Режим выполнения
CTF_INSIDE="true"                     # Запуск агента внутри контейнера
```

### 🔍 Разведка (Recon) и OSINT

Для задач разведки с использованием внешних инструментов:

```bash
# C99.nl: discovery поддоменов
C99_API_KEY="your-c99-api-key"        # Включить инструмент разведки C99

# Конфигурация агента для recon
CAI_AGENT_TYPE="redteam_agent"        # Или создать собственный recon-агент
```

### 🧠 Уплотнённая память и state

Для переноса кратко-обобщённого контекста после `/compact`:

```bash
# Отслеживание состояния
CAI_STATE="true"                      # Включить tracking состояния сети

# Внедрять сводки /compact в system prompt новых агентов
CAI_COMPACTED_MEMORY="true"
```

### 🛡️ Безопасность и контроль рисков

Для включения security guardrails и контроля поведения агентов:

```bash
# Security guardrails
CAI_GUARDRAILS="true"                 # Предотвратить опасные команды
CAI_PRICE_LIMIT="1"                   # Лимит стоимости в долларах
CAI_MAX_INTERACTIONS="inf"            # Максимум разрешённых взаимодействий

# Отладка и мониторинг
CAI_DEBUG="1"                         # 0: минимально, 1: подробный, 2: debug CLI
CAI_TRACING="true"                    # Включить трассировку OpenTelemetry
```

### ⚡ Оптимизация производительности

Для оптимизации вывода, скорости выполнения и расхода ресурсов:

```bash
# Управление выводом
CAI_BRIEF="true"                      # Краткий режим вывода
CAI_STREAM="false"                    # Отключить стриминг inference для LLM (по умолчанию: false)
CAI_TOOL_STREAM="true"                # Включить стриминг вывода инструментов (по умолчанию: true)

# Оптимизация контекста
CAI_ENV_CONTEXT="true"                # Добавлять окружение в контекст
CAI_MAX_TURNS="50"                    # Ограничить число ходов разговора
CAI_CTX_TRUNC="true"                  # Усекать большие выводы, чтобы экономить контекст
CAI_DISPLAY_MAX_OUTPUT="false"        # Показывать полный вывод (установите true, чтобы отключить усечение)

# Таймаут выполнения команд
CAI_TOOL_TIMEOUT="60"                 # Переопределить таймаут команд (в секундах)
CAI_IDLE_TIMEOUT="100"                # Максимум секунд без вывода до остановки (по умолчанию: 100)
```

### 🔧 Продвинутая конфигурация агентов

Для специализированных агентов и сложных сценариев:

```bash
# Поддерживающий агент (meta-reasoning)
CAI_SUPPORT_MODEL="o3-mini"          # Модель для агента поддержки
CAI_SUPPORT_INTERVAL="5"             # Интервал (в ходах) между запусками поддержки

# Параллельное выполнение
CAI_PARALLEL="3"                      # Запуск 3 экземпляров агента параллельно
```

### 🐳 Контейнеры и виртуализация

Для выполнения команд внутри Docker-контейнеров:

```bash
# Целевой контейнер
CAI_ACTIVE_CONTAINER="a1b2c3d4e5f6"  # Docker container ID

# Автоматически с CTF
CTF_INSIDE="true"                     # Auto-set CAI_ACTIVE_CONTAINER при старте CTF
```

### 🖥️ Конфигурация, специфичная для TUI

Для терминального пользовательского интерфейса и сценариев работы:

```bash
# Отображение TUI
CAI_STREAM="true"                     # Включить стриминг inference LLM в панелях TUI
CAI_TOOL_STREAM="true"                # Включить стриминг вывода инструментов (по умолчанию)
CAI_BRIEF="false"                     # Полный вывод для интерактивных сессий
```

### 🐛 Отладка и разработка

Для отладки внутренних компонентов CAI и разработки:

```bash
# Debug уровни
CAI_DEBUG="1"                         # 0: минимально, 1: подробный, 2: debug CLI

# Debug визуализации инструментов
CAI_DEBUG_TOOLS_VIZ="true"            # Отладка отрисовки панелей инструментов и дедупликации

# Debug кэша и сообщений
CAI_SHOW_CACHE="true"                 # Показать статистику кэша и полный список истории сообщений
```

---

## 💡 Примеры типовой конфигурации

### Пример 1: Локальная разработка с Ollama

```bash
CAI_MODEL="ollama/qwen2.5:72b"
CAI_AGENT_TYPE="redteam_agent"
CAI_PRICE_LIMIT="0"
CAI_DEBUG="1"
CAI_GUARDRAILS="false"
```

### Пример 2: Решение Production CTF

```bash
CTF_NAME="hackthebox_challenge"
CTF_INSIDE="true"
CAI_MODEL="alias1"
CAI_STATE="true"
CAI_COMPACTED_MEMORY="true"
CAI_GUARDRAILS="true"
CAI_PRICE_LIMIT="5"
```

### Пример 3: Pentest с контролем стоимости

```bash
CAI_MODEL="gpt-4o"
CAI_AGENT_TYPE="redteam_agent"
CAI_PRICE_LIMIT="2"
CAI_MAX_INTERACTIONS="100"
CAI_GUARDRAILS="true"
CAI_BRIEF="false"
```

### Пример 4: Параллельные тесты (не TUI)

```bash
CAI_MODEL="alias0-fast"
CAI_PARALLEL="5"
CAI_BRIEF="true"
CAI_MAX_TURNS="20"
CAI_STREAM="false"
CAI_TOOL_STREAM="false"
```

---

## ⚠️ Важные замечания

### API-ключи

CAI **не предоставляет API-ключи** ни для одной модели по умолчанию. Настраивайте свои ключи в файле `.env`:

```bash
OPENAI_API_KEY="sk-..."              # требуется (можно использовать "sk-123" как заглушку)
ANTHROPIC_API_KEY="sk-ant-..."       # для Claude-моделей
ALIAS_API_KEY="sk-..."               # для alias1 (CAI PRO)
OLLAMA_API_BASE="http://localhost:11434/v1"  # для локальных моделей
C99_API_KEY="your-api-key"           # для C99.nl subdomain discovery
```

### Настройка переменных

Есть три способа задать переменные окружения:

**1. Файл `.env` (рекомендуется)**

```bash
# Добавьте в .env файл
CAI_MODEL="alias1"
CAI_PRICE_LIMIT="1"
```

**2. Командная строка**

```bash
CAI_MODEL="gpt-4o" CAI_PRICE_LIMIT="2" cai
```

**3. Настройка во время выполнения**

Используйте slash-команды внутри сессии: `/env list`, `/env set …`, а также встроенную справку выше (`/help`, `/help var …`).
