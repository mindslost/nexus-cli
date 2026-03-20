# Nexus CLI Quickstart Guide

Get up and running with Nexus CLI, your terminal-based personal knowledge base enforcing the PARA method.

## 1. Installation

Install Nexus CLI in editable mode from the project root:

```bash
pip install -e .
```

Ensure your `$EDITOR` environment variable is set (defaults to `vim`):

```bash
export EDITOR=nano  # or vim, code, etc.
```

## 2. Create Your First Note

Nexus uses the PARA method (Projects, Areas, Resources, Archives). Create a new note by specifying a title and a category:

```bash
nexus add "Launch Nexus CLI" --para Project
```

This will open your editor with pre-filled YAML frontmatter. Add your content below the `---` separators and save.

## 3. List Your Notes

View your PARA tree to see how your knowledge is organized:

```bash
nexus list
```

For an interactive experience to open, edit, or move notes, use:

```bash
nexus list --interactive
```

## 4. Search Your Knowledge

Use powerful full-text search to find specific information across all notes:

```bash
nexus search "launch"
```

## 5. Manage Notes

### Edit a Note
Use the unique 8-character ID or the full Title:
```bash
nexus edit [ID|Title]
```

### Move a Note
Quickly change a note's PARA category:
```bash
nexus move [ID|Title] --to Area
```

### Delete a Note
Permanently remove a note (requires confirmation):
```bash
nexus delete [ID|Title]
```

## 6. AI Integration (MCP)

If you use AI agents that support the Model Context Protocol (MCP), start the server:

```bash
nexus mcp-start
```
