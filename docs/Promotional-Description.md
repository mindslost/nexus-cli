# Nexus CLI: Promotional Description & Static Website Concept

This document outlines the marketing positioning and website design strategy for Nexus CLI.

---

## 📢 Promotional Description

### **The Command-Line Brain for the AI Era**
Nexus CLI is a blazing-fast, terminal-based personal knowledge base (PKB) designed for developers and power users who demand zero-friction capture and high-performance retrieval. Built on the proven **PARA method** (Projects, Areas, Resources, Archives), Nexus transforms your terminal into a structured second brain that is as easy for humans to write as it is for AI to read.

#### **Why Nexus CLI?**
*   **📂 Structured by Design:** Forget the "unorganized pile of notes." Nexus natively enforces the PARA organization method, ensuring every piece of information has a clear home and a defined lifecycle.
*   **⚡ Instant Search, Zero Latency:** Powered by SQLite’s FTS5 engine, Nexus provides sub-millisecond full-text search across your entire knowledge base. Find what you need with highlighted context snippets, even as your library grows to thousands of notes.
*   **✍️ Use Your Own Tools:** Don't learn a new editor. Nexus opens your native `$EDITOR` (Vim, Neovim, Emacs, or Nano) to capture ideas in standard Markdown, keeping your workflow seamless and your data portable.
*   **🤖 AI-Native Context:** Nexus isn't just for you; it's for your agents. With a built-in **Model Context Protocol (MCP)** server and machine-optimized XML output, Nexus serves as a high-fidelity context provider for LLMs like Claude, allowing them to autonomously search and retrieve your notes.
*   **🔒 Privacy-First & Local:** Your data stays on your machine in a single-file SQLite database. No clouds, no subscriptions, no vendor lock-in. Just your thoughts, indexed and ready.

---

## 🌐 Static Website Concept: `nexus.cli`

A static website for Nexus should reflect its core identity: **minimalist, high-performance, and terminal-centric.**

### **1. Visual Aesthetic: "The Hacker’s Dashboard"**
*   **Color Palette:** Deep charcoal background (`#121212`), "Matrix" green or "Terminal" cyan accents (`#00FF41` or `#00D1FF`), and crisp white monospace typography.
*   **Typography:** High-quality coding fonts like *JetBrains Mono* or *Fira Code* for all headers and UI elements.

### **2. Page Structure (Single Page Scroll)**
*   **Hero Section:** 
    *   **Headline:** `nexus search "the future of notes"`
    *   **Sub-headline:** "A PARA-method PKB that speaks the language of both humans and AI."
    *   **CTA:** A copy-to-clipboard block: `pip install nexus-cli`
    *   **Background:** A subtle, slow-moving ASCII particle field or a terminal-style grid.
*   **The "Live" Demo:**
    *   An embedded **Asciinema** player or a high-quality SVG animation showing a user adding a note, searching with FTS5, and the MCP server responding to a query.
*   **Feature Grid (The PARA Advantage):**
    *   Four clean cards representing **Projects, Areas, Resources, and Archives**. 
    *   Hovering over a card reveals how Nexus handles that specific category with its built-in commands.
*   **AI & MCP Section:**
    *   A side-by-side comparison: On the left, a human-readable `nexus search` result. On the right, the raw XML context provided to an AI agent via MCP.
    *   **Heading:** "Bridge the Gap Between You and Your AI."
*   **Code-First Documentation:**
    *   A "Quick Start" section with tabs for different use cases (e.g., "Standard Use," "AI Integration," "Customization").
*   **Footer:**
    *   Links to GitHub, MIT License, and a "Built with Typer & Rich" badge.

### **3. Interactive Elements**
*   **Command Simulator:** A small interactive terminal widget where users can type `nexus --help` or `nexus list` to see simulated `rich` output right in the browser.
*   **Dark Mode Toggle:** A "Power" switch that toggles between "High Contrast" and "OLED Black" modes.
