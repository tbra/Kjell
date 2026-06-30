# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Kjell is a Telegram group bot written in Python. It uses the `python-telegram-bot` library and integrates with Google Calendar. The bot is written primarily in Swedish.

## Running the bot

```bash
pip install -r requirements.txt
python main.py
```

There is no test suite. The bot must be run live against the Telegram API to verify behavior.

## Required secrets

`utils/secret.py` is gitignored and must be created manually with:
- `API_TOKEN` — Telegram bot token
- `CHAT_ID` — the primary group chat ID
- `DEBUG_CHAT_ID` — where error tracebacks are sent
- `CALENDAR_ID` — Google Calendar ID

Google Calendar also requires `service.json` (service account credentials file) in the project root.

## Architecture

### Handler registration via decorators

Commands register themselves at import time using decorators from `bot/register_handlers.py`:

- `@command_handler(command, description, admin_only)` — registers a `/command` handler. If `description` is provided it appears in the Telegram command list. Pass any truthy third argument to make it admin-only.
- `@message_handler(filter)` — registers a handler triggered by message content (not a slash command).
- `@conversation_handler(commands_dict, states, fallbacks)` — registers a multi-step `ConversationHandler`.

`commands/__init__.py` imports every command module, which triggers all decorator registrations. `main.py` then imports `commands` to load everything before starting the bot.

### Adding a new command

1. Create `commands/mycommand.py` with an `async def` function decorated with `@command_handler`.
2. Add `import commands.mycommand` to `commands/__init__.py`.

### Bot startup sequence

`main.py` → imports `bot` and `commands` (handlers register) → adds error handler → schedules `alive()` job (10s delay, registers command list and announces startup) → schedules `sync_calendar` repeating job (every 30s) → starts polling.

### Calendar sync

`calendar_client/sync_events.py` polls Google Calendar every 30 seconds using an incremental sync token stored in `sync_token.pickle`. New, updated, or cancelled events are sent as formatted messages to `CHAT_ID`.

### Logging and errors

`utils/debug.py` configures stdlib logging at the level set in `utils/constants.py` (`LOG_LEVEL = 'INFO'`). The `error` handler catches all unhandled exceptions, stores the latest traceback in a module-level variable (retrievable with `/error`), and forwards the full traceback to `DEBUG_CHAT_ID`.

## Weather location

`utils/constants.py` contains `WEATHER_LAT` and `WEATHER_LON` (default: Stockholm). Change these to match your group's location. The `/vader` command uses SMHI's free open-data API, which only covers Sweden.
