---
inclusion: fileMatch
fileMatchPattern: ['**/logging.py', '**/log*.py', 'LOGGING.md', '**/LOGGING.*']
---

# Logging Guidelines for LLM Agents (Elastic Stack / ELK)

This document defines best practices for configuring Python application logging using the Elastic Stack (ELK) for centralized observability. It standardizes on structured JSON logging via `dictConfig`, contextual enrichment, and multiple handlers to support console output, file persistence, and Elasticsearch ingestion.

## Core Components

### 1. Logger and Log Levels

- Use module-specific loggers via `logging.getLogger(__name__)` to avoid the root logger.  
- Control verbosity with levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

### 2. Handlers

- **ConsoleHandler** (`logging.StreamHandler`) for real-time logs to `stdout`.  
- **FileHandler** (`logging.FileHandler`) for local persistence; manage rotation externally (e.g., `logrotate`).  
- **ElasticHandler** (from `python-elasticsearch-logging`) for HTTP ingestion into Elasticsearch indices.

### 3. Formatters

- Use `python-json-logger`'s `JsonFormatter` to emit ECS-compatible JSON.  
- Rename fields for consistency:
  - `asctime` → `time`
  - `levelname` → `level`

### 4. Filters

- **NoHealthChecksFilter**: drop any record containing `"/health"`.  
- **ContextFilter**: inject metadata (e.g., `hostname`, `process_id`) into each record.

## Example `logging_agent.mdc` Configuration

```yaml
version: 1
disable_existing_loggers: false

formatters:
  json_formatter:
    (): pythonjsonlogger.jsonlogger.JsonFormatter
    format: "%(asctime)s %(name)s %(levelname)s %(message)s"
    rename_fields:
      asctime: time
      levelname: level

filters:
  no_health:
    (): logging.Filter
    filter: "lambda record: '/health' not in record.getMessage()"
  context:
    (): log_context.ContextFilter

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: json_formatter
    stream: ext://sys.stdout

  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: json_formatter
    filename: app.log

  elastic:
    class: elasticsearch_logging.ElasticHandler
    level: INFO
    host: "https://elastic:changeme@localhost:9200"
    index: "llm-agent-logs-%Y.%m.%d"
    buffer_size: 5000
    use_ssl: false

loggers:
  llm_agent:
    level: DEBUG
    handlers: [console, file, elastic]
    filters: [no_health, context]
    propagate: false

root:
  level: WARNING
  handlers: [console, elastic]
