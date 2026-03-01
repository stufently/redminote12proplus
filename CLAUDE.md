# CLAUDE QUICK START

Если вы подхватываете этот проект после другого агента:

1. Прочитайте `README.md` (главная страница мануала)
2. Прочитайте `workflow/HANDOFF.md` (что делать прямо сейчас)
3. Проверьте `workflow/CURRENT_STATE.md` и `workflow/BACKLOG.md`
4. Выполните ближайшие 1-3 шага из handoff
5. В конце обновите `CURRENT_STATE.md`, `SESSION_LOG.md`, `HANDOFF.md`

## Принципы

- `README.md` всегда остается центральной точкой входа
- Детали и длинные инструкции живут в `guide/`
- Любая новая секция должна быть добавлена в оглавление `README.md`

## Автосовет по плану

При необходимости внешнего second opinion запускайте:

```bash
python3 skills/claude-plan-advisor/scripts/ask_claude_plan_advice.py
```

С фокусом:

```bash
python3 skills/claude-plan-advisor/scripts/ask_claude_plan_advice.py --focus "..."
```

## Минимальный handoff перед выходом

- Что завершено
- Что в работе
- Следующие 3 действия
- Открытые вопросы и риски
