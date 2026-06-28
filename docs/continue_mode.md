# Режим продолжения CAI

## Обзор

Флаг `--continue` позволяет агентам CAI работать автономно: система автоматически генерирует интеллектуальные подсказки для продолжения, когда агент обычно останавливается и ждёт ввода пользователя. Эта функция использует анализ с помощью ИИ, чтобы предоставлять контекстные рекомендации на основе истории диалога — благодаря этому агенты могут выполнять сложные задачи без ручного вмешательства.

## Быстрый старт

```bash
# Рассказываем шутки непрерывно
cai --continue --prompt "tell me a joke about security"

# Анализируем код автономно
cai --continue --prompt "find all SQL injection vulnerabilities in this codebase"

# Выполняем проверку безопасности
cai --continue --prompt "perform a comprehensive security audit"
```

## Пример: шутки про безопасность в режиме продолжения

Вот что происходит, когда вы запускаете `cai --continue --prompt "tell me a joke about security"`:

```bash
$ cai --continue --prompt "tell me a joke about security"

🤖 Processing initial prompt: tell me a joke about security

Agent: Why did the hacker break up with their password? 
       Because it wasn't strong enough! 💔🔐

🤖 Auto-continuing with: Tell another cybersecurity joke or pun.

Agent: Why don't cybersecurity experts tell secrets at parties?
       Because they're afraid of social engineering! 🎉🕵️

🤖 Auto-continuing with: Tell another cybersecurity joke or pun.

Agent: What's a hacker's favorite season?
       Phishing season! 🎣💻

[Continues until interrupted with Ctrl+C]
```

## Как это работает

### 1. Интеллектуальный анализ контекста

Когда агент завершает ход, система продолжения анализирует:
- **Исходный запрос**: первоначальную задачу или подсказку пользователя
- **Историю беседы**: последние сообщения и ответы
- **Использование инструментов**: какие инструменты были задействованы и их результаты
- **Состояние ошибок**: любые встреченные ошибки и их типы
- **Прогресс задачи**: текущую степень выполнения задачи

### 2. Генерация продолжения на базе ИИ

Система использует настроенную модель ИИ (по умолчанию: alias1) для генерации контекстных подсказок продолжения:

```python
# Система создаёт подробное резюме контекста
context_summary = """
ORIGINAL TASK: Tell me a joke about security
CONVERSATION FLOW:
User: Tell me a joke about security
Agent: Why did the hacker break up with their password? Because it wasn't strong enough!

CURRENT STATUS:
- Last action: Told a cybersecurity joke
- Tools used: None
- Errors: No

Generate a specific continuation prompt...
"""
```

### 3. Умная система резервного продолжения

Когда модель ИИ недоступна, система предоставляет интеллектуальные резервные варианты на основе контекста:

| Ситуация | Резервное продолжение |
|----------|----------------------|
| Рассказывается шутка про безопасность | "Tell another cybersecurity joke or pun." |
| Файл не найден | "Search for the correct file path or create the missing resource." |
| Поиск завершён | "Examine the search results in detail and investigate the most relevant findings." |
| Анализ безопасности | "Analyze the code for security vulnerabilities like injection flaws or authentication issues." |
| Доступ запрещён | "Check permissions and try accessing the resource with appropriate credentials." |

## Частые сценарии использования

### 1. Автоматические проверки безопасности
```bash
cai --continue --prompt "perform a security audit of the authentication system"
```
Агент будет:
- Искать файлы, связанные с аутентификацией
- Анализировать код на наличие уязвимостей
- Проверять распространённые проблемы безопасности
- Формировать подробный отчёт

### 2. Непрерывный поиск багов
```bash
cai --continue --prompt "find and document all XSS vulnerabilities"
```
Агент будет:
- Искать код, обрабатывающий пользовательский ввод
- Определять потенциальные XSS-векторы
- Документировать находки
- Предлагать исправления

### 3. Расширенный анализ кода
```bash
cai --continue --prompt "analyze this codebase for OWASP Top 10 vulnerabilities"
```
Агент будет:
- Системно проверять каждый тип уязвимости
- Давать подробные результаты
- Продолжать до покрытия всех категорий

### 4. Развлекательный режим
```bash
cai --continue --prompt "tell me cybersecurity jokes and fun facts"
```
Агент будет:
- Рассказывать шутки по теме безопасности
- Делить интересными фактами о безопасности
- Продолжать развлекать до остановки

## Настройка

### Переменные окружения

```bash
# Использовать другую модель для генерации продолжений
export CAI_MODEL=gpt-4
cai --continue --prompt "analyze this code"

# Указать запасную модель, если основная не сработает
export CAI_CONTINUATION_FALLBACK_MODEL=gpt-3.5-turbo
cai --continue --prompt "test application security"

# Настроить API-ключи для пользовательских моделей
export ALIAS_API_KEY=your-api-key
cai --continue --prompt "perform penetration testing"
```

### Совместное использование с другими функциями CAI

```bash
# Использовать конкретного агента с режимом continue
CAI_AGENT_TYPE=bug_bounter_agent cai --continue --prompt "test example.com"

# Установить рабочую область для операций с файлами
CAI_WORKSPACE=project1 cai --continue --prompt "audit all Python files"

# Включить потоковый вывод для реального времени
CAI_STREAM=true cai --continue --prompt "monitor security events"
```

## Продвинутые функции

### Логика принятия решения о продолжении

Система решает, продолжать ли работу, исходя из:
1. **Индикаторов завершения**: останавливается, если агент говорит «completed», «finished», «done»
2. **Обнаружения активной работы**: продолжает, если используются инструменты
3. **Восстановления после ошибок**: пытается автоматически исправить ошибки
4. **Прогресса задачи**: оценивает, достигнута ли исходная цель

### Контекстно-зависимые подсказки

Подсказки продолжения адаптируются в зависимости от:
- **Типа задачи**: анализ безопасности, тестирование, ревью кода и т.д.
- **Текущего состояния**: ошибки, находки, прогресс
- **Использования инструментов**: разные подсказки для разных инструментов
- **Потока разговора**: поддерживают логичное развитие задачи

## Лучшие практики

### 1. Чёткие начальные подсказки
```bash
# Хорошо — конкретно и действенно
cai --continue --prompt "find SQL injection vulnerabilities in user.py"

# Менее эффективно — слишком расплывчато
cai --continue --prompt "check security"
```

### 2. Отслеживайте прогресс
- Проверяйте вывод периодически, чтобы убедиться, что направление верное
- Используйте Ctrl+C, чтобы остановить при необходимости
- Просматривайте логи для подробной истории выполнения

### 3. Устанавливайте разумные лимиты
```python
# В коде используйте max_turns
run_cai_cli(
    starting_agent=agent,
    initial_prompt="analyze security",
    continue_mode=True,
    max_turns=10  # Ограничение до 10 ходов
)
```

### 4. Обработка ошибок
Система автоматически:
- повторяет неудачные операции другими способами
- ищет альтернативы, когда файлы отсутствуют
- корректирует стратегию в зависимости от типа ошибки

## Поиск и исправление проблем

### Проблема: общие сообщения продолжения
**Симптом**: всегда появляется «Continue working on the task based on your previous findings»

**Решение**:
- Проверьте, что конфигурация модели корректна
- Убедитесь, что API-ключи действительны
- Просмотрите отладочные логи на предмет ошибок API

### Проблема: продолжение не запускается
**Симптом**: агент останавливается после завершения задачи

**Возможные причины**:
- агент явно сказал, что задача «completed» или «done»
- не обнаружено недавнего использования инструментов
- ошибка в модуле продолжения

**Решение**:
- используйте более открытые начальные подсказки
- проверьте логи на индикаторы завершения
- убедитесь, что флаг --continue установлен правильно

### Проблема: бесконечные циклы
**Симптом**: агент продолжает делать одно и то же

**Решение**:
- задайте ограничение max_turns
- используйте более конкретные начальные подсказки
- прервите Ctrl+C и уточните задачу

## Техническая реализация

### Основные компоненты

1. **`src/cai/continuation.py`**: основная логика продолжения
   - `generate_continuation_advice()`: создаёт подсказки на базе ИИ
   - `should_continue_automatically()`: решает, продолжать ли

2. **`src/cai/cli.py`**: точка интеграции
   - обработка флага `--continue`
   - реализация цикла продолжения

3. **Анализ контекста**:
   - извлекает историю беседы
   - определяет шаблоны использования инструментов
   - обнаруживает условия ошибок

### Интеграция с API

The continuation system uses LiteLLM for model calls:
```python
response = await litellm.acompletion(
    model=model_name,
    messages=[{"role": "user", "content": context_summary}],
    temperature=0.3,  # Low temperature for focused responses
    max_tokens=150
)
```

## Examples Gallery

### Security Audit Continuation
```
Original: "Audit the login system"
→ "Search for authentication-related files in the codebase."
→ "Analyze the login function for SQL injection vulnerabilities."
→ "Check password hashing implementation for security best practices."
→ "Review session management for potential security issues."
```

### Bug Bounty Continuation
```
Original: "Test example.com for vulnerabilities"
→ "Perform initial reconnaissance to gather information about the target."
→ "Scan for exposed endpoints and services."
→ "Test authentication endpoints for common vulnerabilities."
→ "Check for information disclosure in error messages."
```

### Code Review Continuation
```
Original: "Review api.py for security issues"
→ "Analyze input validation in API endpoints."
→ "Check for proper authentication and authorization."
→ "Review error handling for information leakage."
→ "Examine data serialization for injection vulnerabilities."
```

## Example Scripts

Explore working examples in the `examples/` directory:

### Security Jokes Example
```python
# examples/continue_mode_jokes.py
# Demonstrates continuous joke telling with --continue flag
python examples/continue_mode_jokes.py
```

### Security Audit Example
```python
# examples/continue_mode_security_audit.py
# Shows autonomous vulnerability scanning with --continue
python examples/continue_mode_security_audit.py
```

These examples demonstrate:
- How to use --continue flag programmatically
- Handling continuous output
- Graceful interruption with Ctrl+C
- Practical security use cases

## Combining with Session Resume

The `--continue` flag works seamlessly with `--resume` to continue interrupted sessions autonomously:

```bash
# Resume last session and continue working autonomously
cai --resume --continue

# Resume specific session and continue
cai --resume abc12345 --continue

# Resume from interactive selector and continue
cai --resume list --continue
```

This powerful combination:
1. **Restores your previous session** with full conversation history
2. **Automatically generates a continuation prompt** based on where you left off
3. **Continues working autonomously** without waiting for user input

For more details on session resume capabilities, see the [Session Resume](session_resume.md) documentation.

## Summary

The `--continue` flag transforms CAI into an autonomous cybersecurity assistant capable of:
- Working independently on complex tasks
- Recovering from errors intelligently
- Maintaining context across multiple operations
- Resuming and continuing interrupted sessions with `--resume --continue`
- Providing entertainment with continuous jokes

Whether you're conducting security audits, hunting for bugs, or just want some cybersecurity humor, continue mode keeps your agent working until the job is done.