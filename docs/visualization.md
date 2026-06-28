# Визуализация агентов

Визуализация агентов позволяет сгенерировать структурное графическое представление агентов и их связей с помощью **Graphviz**. Это помогает понять, как агенты, инструменты и handoff взаимодействуют в приложении.

## Установка

Установите дополнительную группу зависимостей `viz`:

```bash
pip install "openai-agents[viz]"
```

## Генерация графа

Вы можете создать визуализацию агента с помощью функции `draw_graph`. Эта функция строит ориентированный граф, в котором:

- **Агенты** отображаются жёлтыми прямоугольниками.
- **Инструменты** отображаются зелёными эллипсами.
- **Handoffs** отображаются направленными ребрами от одного агента к другому.

### Пример использования

```python
from agents import Agent, function_tool
from agents.extensions.visualization import draw_graph

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
    tools=[get_weather],
)

draw_graph(triage_agent)
```

![Agent Graph](./assets/images/graph.png)

Это создаёт граф, который визуально показывает структуру **triage agent** и его связи с дочерними агентами и инструментами.

## Понимание визуализации

Сгенерированный граф включает:

- **стартовую вершину** (`__start__`), обозначающую точку входа.
- Агенты, представленные в виде **прямоугольников** с жёлтым фоном.
- Инструменты, представленные в виде **эллипсов** с зелёным фоном.
- Направленные рёбра, показывающие взаимодействия:
  - **Сплошные стрелки** для handoff между агентами.
  - **Пунктирные стрелки** для вызова инструментов.
- **концевую вершину** (`__end__`), обозначающую место завершения выполнения.

## Настройка графа

### Отображение графа
По умолчанию `draw_graph` отображает граф встроено. Чтобы показать его в отдельном окне, используйте:

```python
draw_graph(triage_agent).view()
```

### Сохранение графа
По умолчанию `draw_graph` отображает граф встроено. Чтобы сохранить его в файл, укажите имя файла:

```python
draw_graph(triage_agent, filename="agent_graph.png")
```

Это создаст файл `agent_graph.png` в рабочем каталоге.


