# Model context protocol (MCP)

[Model context protocol](https://modelcontextprotocol.io/introduction) (или MCP) — это способ предоставить инструменты и контекст LLM. Из документации MCP:

> MCP — это открытый протокол, стандартизирующий способ предоставления контекста LLM. Представьте MCP как USB-C для AI-приложений. Точно так же, как USB-C обеспечивает стандартное подключение устройств к периферии, MCP предоставляет стандартный способ подключения моделей к различным источникам данных и инструментам.

MCP позволяет использовать широкий спектр MCP-серверов для предоставления инструментов вашим агентам.

## MCP-серверы

В настоящее время спецификация MCP определяет два типа серверов в зависимости от используемого транспорта:

1. **stdio** серверы запускаются как подпроцесс вашего приложения. Можно считать, что они работают «локально».
2. **HTTP over SSE** серверы работают удалённо. Вы подключаетесь к ним по URL.

Вы можете использовать классы [`MCPServerStdio`][cai.sdk.agents.mcp.server.MCPServerStdio] и [`MCPServerSse`][cai.sdk.agents.mcp.server.MCPServerSse] для подключения к таким серверам.

Например, так можно использовать [официальный MCP файловый сервер](https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem).

```python
async with MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
    }
) as server:
    tools = await server.list_tools()
```

## Использование MCP-серверов

MCP-серверы можно добавлять к агентам. Во время запуска агент собирает инструменты с каждого сервера (через `list_tools()`), чтобы модель могла их вызвать; каждый вызов использует `call_tool()` сервера.

```python
from cai.sdk.agents import Agent

# mcp_server_1 и mcp_server_2 — это подключённые экземпляры MCPServerStdio / MCPServerSse.
cybersecurity_lead = Agent(
    name="Cybersecurity Lead Agent",
    instructions="Use the tools to solve the task.",
    mcp_servers=[mcp_server_1, mcp_server_2],
)
```

## Кэширование

Каждый раз при запуске агента вызывается `list_tools()` на MCP-сервере. Это может добавлять задержку, особенно если сервер удалённый. Чтобы автоматически кэшировать список инструментов, можно передать `cache_tools_list=True` как в [`MCPServerStdio`][cai.sdk.agents.mcp.server.MCPServerStdio], так и в [`MCPServerSse`][cai.sdk.agents.mcp.server.MCPServerSse]. Делайте это только если уверены, что список инструментов не будет меняться.

Если вы хотите сбросить кэш, вызовите `invalidate_tools_cache()` на сервере.

## End-to-end examples

Смотрите директорию `examples/mcp/` в репозитории CAI для runnable-скриптов (стиль stdio и SSE).


## Трейсинг   
[Tracing](./tracing.md) автоматически записывает MCP-операции, включая:

1. Вызовы MCP-сервера для получения списка инструментов
2. MCP-данные в информации о вызовах функций
![MCP Tracing Screenshot](./assets/images/mcp-tracing.jpg)