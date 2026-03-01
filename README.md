# Redmi Note 12 Pro+ Photo Manual

Этот репозиторий — практическое руководство по съемке на **Redmi Note 12 Pro+**.
Главная страница всегда здесь, в `README.md`. Подробности вынесены в отдельные разделы.

## Как пользоваться этим мануалом

1. Откройте быстрый старт: [guide/01_quick_start.md](guide/01_quick_start.md)
2. Выберите нужный сценарий: портрет, ночь, видео
3. Пройдите чеклист перед съемкой: [guide/99_checklists.md](guide/99_checklists.md)
4. После практики зафиксируйте заметки и примеры в `assets/`

## Оглавление

- Область и цели: [guide/00_scope.md](guide/00_scope.md)
- Быстрый старт (2 минуты): [guide/01_quick_start.md](guide/01_quick_start.md)
- Режимы камеры: [guide/02_camera_modes.md](guide/02_camera_modes.md)
- Свет и экспозиция: [guide/03_light_and_exposure.md](guide/03_light_and_exposure.md)
- Портрет: [guide/04_portrait.md](guide/04_portrait.md)
- Ночная съемка: [guide/05_night.md](guide/05_night.md)
- Видео: [guide/06_video.md](guide/06_video.md)
- Чеклисты: [guide/99_checklists.md](guide/99_checklists.md)

## Быстрые сценарии

- Хочу красивый портрет: [guide/04_portrait.md](guide/04_portrait.md)
- Хочу снять ночью без смаза: [guide/05_night.md](guide/05_night.md)
- Хочу стабильное видео для соцсетей: [guide/06_video.md](guide/06_video.md)

## Прогресс и возобновление работы

Чтобы можно было прерваться в любой момент и продолжить с любого агента:

- Текущее состояние: [workflow/CURRENT_STATE.md](workflow/CURRENT_STATE.md)
- Что еще сделать: [workflow/BACKLOG.md](workflow/BACKLOG.md)
- Передача контекста: [workflow/HANDOFF.md](workflow/HANDOFF.md)
- История сессий: [workflow/SESSION_LOG.md](workflow/SESSION_LOG.md)
- Принятые решения: [workflow/DECISIONS.md](workflow/DECISIONS.md)

## Автосовет от Claude Code

Для автоматического second opinion по планам и уже сделанным задачам:

```bash
python3 skills/claude-plan-advisor/scripts/ask_claude_plan_advice.py
```

Опционально с фокусом:

```bash
python3 skills/claude-plan-advisor/scripts/ask_claude_plan_advice.py \
  --focus "Улучшить разделы портрета и ночной съемки"
```

Результат сохраняется в `workflow/advice/claude-advice-*.md`.

## Структура репозитория

```text
guide/            Основные разделы мануала
assets/photos/    Исходные фото и тестовые кадры
assets/examples/  Иллюстрации и примеры для гайда
workflow/         Файлы состояния и handoff
AGENTS.md         Правила для Codex и других агентов
CLAUDE.md         Быстрый вход для Claude Code
```

## Правило завершения каждой сессии

Перед паузой всегда:

1. Обновить `workflow/CURRENT_STATE.md`
2. Добавить короткую запись в `workflow/SESSION_LOG.md`
3. Обновить `workflow/HANDOFF.md` (Next 3 actions)
4. Сделать commit с префиксом `checkpoint:`
