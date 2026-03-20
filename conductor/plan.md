# Interactive Textual Selection for 'list' Command

## Objective
Enhance the existing `nexus list` command to display a full-screen interactive Terminal User Interface (TUI) using `Textual`. The user will be able to navigate the hierarchical PARA tree of their notes using arrow keys and press `o` to open or `e` to edit the currently selected note.

## Key Files & Context
- `pyproject.toml`: Needs to be updated to include `textual` in the dependencies.
- `nexus_cli/main.py`: The `list` command needs to be refactored to launch the Textual app instead of printing a Rich tree. The `edit` and `open_note` commands are already present and can be reused.
- `nexus_cli/tui.py` (New File): A dedicated file to house the Textual application class to keep `main.py` clean.

## Implementation Steps

### 1. Update Dependencies
- Add `"textual>=0.50.0"` to the `dependencies` list in `pyproject.toml`.

### 2. Create the Textual Interface (`nexus_cli/tui.py`)
- Import necessary Textual widgets (`App`, `ComposeResult`, `Tree`).
- Define a `NexusListApp` that extends `App`.
- **Bindings**: Add class-level bindings for `o` (action: open), `e` (action: edit), `m` (action: move), and `q` (action: quit).
- **UI Composition**: Use a `Tree` widget to display the PARA categories and their corresponding notes. Attach note IDs to the `data` attribute of the tree nodes.
- **Actions**:
  - Implement `action_open`, `action_edit`, and `action_move`.
  - In these methods, retrieve the currently highlighted node in the tree.
  - If the node represents a note (has a note ID in its data):
    - For `open`: call `self.exit(("open", note_id))`.
    - For `edit`: call `self.exit(("edit", note_id))`.
    - For `move`: 
      - Launch a `SelectionList` or a simple `Select` overlay within Textual to pick the target PARA category.
      - Upon selection, call `self.exit(("move", note_id, target_category))`.
  - Implement `action_quit` to exit without an action.

### 3. Refactor `list` Command (`nexus_cli/main.py`)
- In the `list_notes` function, replace the Rich `Tree` printing logic with launching the `NexusListApp`.
- Pass the fetched `results` (from `get_filtered_notes`) into the `NexusListApp` upon initialization.
- Await/capture the result of `NexusListApp().run()`.
- If the app returns a result tuple:
  - If `action == "open"`, call `open_note(note_id)`.
  - If `action == "edit"`, call `edit(note_id)`.
  - If `action == "move"`, call `move(note_id, to=target_category)`.

## Verification & Testing
- Run `nexus list` and ensure it launches a full-screen TUI instead of static text.
- Verify the arrow keys correctly navigate through the PARA categories and individual notes.
- Hover over a note and press `e`. Verify the TUI closes and the note opens in the editor.
- Hover over a note and press `o`. Verify the TUI closes and the note is opened in read-only mode.
- Hover over a note and press `m`. Verify an overlay appears to select a new PARA category. Select one and verify the note is moved.
- Verify that pressing `o`, `e`, or `m` on a category node (not a note node) does nothing or gracefully handles it without errors.
- Verify that filtering with `nexus list --para Project` still works and only populates the selected notes into the TUI.