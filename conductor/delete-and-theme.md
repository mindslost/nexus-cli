# Add Delete and Theme Persistence to Ostraca CLI

## Objective
1.  Add an interactive "Delete" (key binding `d`) to the TUI with a confirmation modal.
2.  Implement theme persistence (e.g., saving "light" or "dark" mode) so it's remembered across sessions.

## Key Files & Context
- `ostraca_cli/main.py`: Update the `list` command handler to support the `delete` action returned by the TUI.
- `ostraca_cli/tui.py`: 
    - Add `DeleteConfirmationScreen`.
    - Add `d` key binding and `action_delete_note`.
    - Add a key binding (e.g., `t`) to toggle themes.
    - Load and save theme settings.
- `ostraca_cli/config.py` (New File): A simple utility to load and save JSON configuration from `~/.ost_config.json`.

## Implementation Steps

### 1. Configuration Utility (`ostraca_cli/config.py`)
- Create a `load_config` and `save_config` function.
- Default theme should be "dark" (or based on system preference).

### 2. Update TUI (`ostraca_cli/tui.py`)
- **Delete Functionality**:
    - Add `DeleteConfirmationScreen` modal.
    - Add `d` key binding for `action_delete_note`.
    - Upon confirmation, exit with `("delete", note_id)`.
- **Theme Toggling**:
    - Add `t` key binding to toggle between "light" and "dark" themes.
    - On toggle, call `save_config` to persist the setting.
    - In `OstracaListApp.__init__`, load the theme and set `self.theme`.

### 3. Update main.py
- In `list_notes`, add a handler for `elif action == "delete": delete(data)`.

## Verification & Testing
- Run `ost list`, select a note, press `d`, confirm, and ensure the note is deleted.
- Run `ost list`, press `t` to change the theme, exit, and re-run to verify the theme is remembered.
