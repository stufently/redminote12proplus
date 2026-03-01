# PROCESS

Процессный файл для агентов. Не дублируется в пользовательских разделах мануала.

## Прогресс и возобновление

- Текущее состояние: [CURRENT_STATE.md](CURRENT_STATE.md)
- Что еще сделать: [BACKLOG.md](BACKLOG.md)
- Передача контекста: [HANDOFF.md](HANDOFF.md)
- История сессий: [SESSION_LOG.md](SESSION_LOG.md)
- Принятые решения: [DECISIONS.md](DECISIONS.md)

## Skill проверки

- Используется глобальный skill Codex `claude-plan-advisor`
- Локальная папка `skills/` в репозитории не используется
- Skill должен покрывать:
  - проверку планов;
  - проверку выполнения;
  - проверку результата перед завершением.

## Структура репозитория

```text
guide/            Основные разделы мануала
assets/photos/    Исходные фото и тестовые кадры
assets/examples/  Иллюстрации и примеры для гайда
workflow/         Файлы состояния и handoff
AGENTS.md         Правила для Codex и других агентов
CLAUDE.md         Быстрый вход для Claude Code
```

Правила примеров: [../assets/examples/README.md](../assets/examples/README.md)

## Правило завершения сессии

1. Обновить `CURRENT_STATE.md`
2. Добавить запись в `SESSION_LOG.md`
3. Обновить `HANDOFF.md` (Next 3 actions)
4. Зафиксировать `checkpoint` commit и отправить в удаленный репозиторий
