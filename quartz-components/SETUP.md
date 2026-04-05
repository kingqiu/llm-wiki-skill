# Bilingual Component Setup Guide

This directory contains the Quartz components needed for the Chinese translation toggle feature.

## Files

- `Bilingual.tsx` — Quartz component that renders the "中" toggle button
- `scripts/bilingual.inline.ts` — Client-side JS for toggle behavior and localStorage persistence

## Installation Steps

### Step 1: Copy files

```bash
WIKI_DIR=/path/to/your/wiki  # your Quartz installation

cp Bilingual.tsx $WIKI_DIR/quartz/components/
cp scripts/bilingual.inline.ts $WIKI_DIR/quartz/components/scripts/
```

### Step 2: Register the component

Edit `$WIKI_DIR/quartz/components/index.ts` — add two lines:

```typescript
// Add this import near the top
import Bilingual from "./Bilingual"

// Add to the export block
export {
  // ... existing exports ...
  Bilingual,
}
```

### Step 3: Add to layout

Edit `$WIKI_DIR/quartz.layout.ts` — add Bilingual to the Flex group alongside Darkmode and ReaderMode:

```typescript
Component.Flex({
  components: [
    { Component: Component.Search(), grow: true },
    { Component: Component.Darkmode() },
    { Component: Component.ReaderMode() },
    { Component: Component.Bilingual() },   // ← add this line
  ],
}),
```

### Step 4: Add CSS

Append the following to `$WIKI_DIR/quartz/styles/custom.scss`:

```scss
// ── Bilingual Toggle Button ──────────────────────────────────────────────────
.bilingual-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1.5px solid var(--gray);
  border-radius: 50%;
  cursor: pointer;
  color: var(--darkgray);
  width: 1.65rem;
  height: 1.65rem;
  font-size: 0.8rem;
  font-weight: 700;
  font-family: var(--cjkBodyFont, sans-serif);
  padding: 0;
  transition: color 0.2s, border-color 0.2s;

  &:hover {
    border-color: var(--secondary);
    color: var(--secondary);
  }

  &.active {
    border-color: var(--secondary);
    color: var(--secondary);
  }
}

// ── Chinese Translation Paragraphs ───────────────────────────────────────────
.zh-trans {
  display: none;
  margin-top: 0.2rem;
  margin-bottom: 0.8rem;
  padding: 0.4rem 0.75rem;
  border-left: 3px solid var(--lightgray);
  color: var(--gray);
  font-size: 0.92em;
  line-height: 1.65;
}
```

### Step 5: Rebuild

```bash
cd $WIKI_DIR
npx quartz build
```

## Adding translations to your content

Use the `translate_wiki.py` script in the root of this skill to add `<div class="zh-trans">` blocks to your markdown files. See the main README for instructions.
