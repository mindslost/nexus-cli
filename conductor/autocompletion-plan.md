# Autocompletion for Ostraca CLI

## Objective
Enable shell autocompletion for note IDs and Titles across commands that require them (`edit`, `open`, `move`, `delete`).

## Key Files & Context
- `ostraca_cli/main.py`: Update the Typer initialization to enable completions. Create an `autocompletion` callback function and apply it to the `identifier` arguments of the relevant commands.

## Implementation Steps

### 1. Enable Completions
- In `ostraca_cli/main.py`, change `add_completion=False` to `add_completion=True` in the `typer.Typer` instantiation.

### 2. Create Completion Function
- Create a function `complete_note_identifier(incomplete: str) -> List[str]`:
    - Connect to the DB and query `SELECT id, title FROM notes`.
    - Yield/return matches where either the `id` starts with `incomplete` or the `title` contains `incomplete` (case-insensitive).
    - Typer expects this to return a list or generator of strings. Returning the `id` or `title` works, but returning just the `title` (or both) might be easier for the user to read. For safety and precision, Typer's completion can yield `CompletionItem(id, help=title)`.

### 3. Apply Completion to Commands
- For `edit`, `open_note`, `move`, and `delete`, update the `identifier` argument to use the autocompletion function:
  ```python
  identifier: str = typer.Argument(..., autocompletion=complete_note_identifier, help="ID or Title of the note...")
  ```

## Verification & Testing
- Note that Typer completions must be installed in the shell (e.g., `ost --install-completion zsh`).
- Mock testing: We will test by verifying the code structure. The user can then test it in their shell environment.
