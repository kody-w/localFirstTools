# The "Art House" Transformation Plan
## *Reorganizing LocalFirstTools into a Digital Museum*

### 🏛️ Philosophy: "Curated Chaos"
The goal is to transform the repository from a "cluttered workshop" into a "high-end gallery" without losing the raw, experimental energy of the tools. We will treat every HTML file not just as code, but as an **Exhibit**.

The repository will function like a physical museum:
1.  **The Grand Halls (Directories):** Clean, thematic spaces for finished works.
2.  **The Workshop (Staging):** A messy space for active development.
3.  **The Archives (Storage):** A preserved history of previous iterations.

---

### 🏗️ Phase 1: The Physical Renovation (Directory Structure)

Currently, the root directory is overcrowded. We will move files into "Wings" based on the existing categories in `vibe_gallery_config.json`.

**Proposed Structure:**

```text
localFirstTools/
├── index.html                  # The Museum Entrance (Lobby)
├── vibe_gallery_config.json    # The Exhibition Catalog
├── assets/                     # Shared resources (icons, global styles)
├── scripts/                    # The Museum Staff (Automation)
│
├── Exhibition_Halls/           # The Main Galleries (Moved from root)
│   ├── Visual_Arts/            # Canvas, SVG, Generative Art
│   ├── Simulation_Lab/         # Physics, Particles, Math
│   ├── The_Arcade/             # Games, Puzzles
│   ├── Sound_Studio/           # Audio, Music, Synesthesia
│   ├── Productivity_Suite/     # Tools, Utilities, Text
│   └── AI_Research/            # Neural Nets, Agents, LLM tools
│
├── The_Workshop/               # (New) "Mad Science" Zone
│   ├── _prototypes/            # Half-finished ideas
│   └── _incoming/              # New drops before categorization
│
└── The_Archives/               # (New) Historical Preservation
    ├── v1_classics/            # Old versions of tools
    └── deprecated/             # Broken or superseded experiments
```

**Action Items:**
- [ ] Create the `Exhibition_Halls` directory structure.
- [ ] Run a "Migration Script" (to be written) that moves HTML files based on their current category in `vibe_gallery_config.json`.
- [ ] **Crucial:** The migration script must auto-update relative links (e.g., `<a href="index.html">` becomes `<a href="../../index.html">`) inside the HTML files to prevent breaking navigation.

---

### 🖼️ Phase 2: The "Plaque" System (Metadata Standardization)

In a museum, every piece has a plaque. Currently, we scrape messy HTML tags. We will standardize metadata to treat code as art.

**The Standard:**
Every HTML file will include a standardized JSON-LD block in its `<head>`.

```html
<script type="application/ld+json" id="gallery-metadata">
{
  "title": "Particle Life Simulator",
  "artist": "Claude & User",
  "curator_note": "A study in emergent behavior using simple rules.",
  "year": 2024,
  "medium": ["Canvas", "JavaScript", "Physics"],
  "category": "Simulation_Lab",
  "complexity": "Advanced",
  "controls": ["Mouse", "Touch"]
}
</script>
```

**Action Items:**
- [ ] Update `vibe_gallery_updater.py` to prioritize this JSON block over regex scraping.
- [ ] Create a "Librarian Script" that auto-injects this template into existing files (populating what it can) for the user to fill out later.

---

### 🎨 Phase 3: The Gallery Experience (UI Overhaul)

The `index.html` is the lobby. It needs to feel like one.

1.  **The Map View:**
    *   Replace the long list with a visual "Museum Map" (SVG/Canvas).
    *   Clicking a "Wing" (e.g., "The Arcade") zooms into that section.
    *   *Why:* It handles scale better than a list of 200 items.

2.  **"Curator's Choice" (Featured Rotations):**
    *   Instead of static "Featured" items, implement a weekly rotation based on the `lastUpdated` date or random selection from the "High Complexity" tier.

3.  **The "White Cube" Mode:**
    *   When a tool is opened, it currently just opens.
    *   **New Feature:** Wrap opened tools in a subtle "Museum Frame" UI (optional iframe wrapper) that provides a "Back to Gallery" button, the "Plaque" info, and a "Like/Vote" button, keeping the user immersed in the ecosystem.

---

### 🤖 Phase 4: The Curator Agent (Automation)

We need an automated curator to maintain order as the repo scales to 1000+ tools.

**New Scripts:**
*   `curator.py`:
    *   **Intake:** Scans `The_Workshop/_incoming`.
    *   **Analysis:** Analyzes code content to suggest a "Wing" (Category).
    *   **Accession:** Moves the file to the correct `Exhibition_Hall`, adds the JSON plaque, and updates the config.
    *   **Preservation:** If a file is being overwritten, automatically moves the old version to `The_Archives` with a timestamp.

---

### 🚀 Execution Strategy (How to do this safely)

1.  **Freeze:** Stop adding new tools for 1 hour.
2.  **Backup:** `cp -r localFirstTools localFirstTools_BACKUP`.
3.  **Scripted Move:** Do *not* move files manually. Write a python script `scripts/maintenance/organize_museum.py` to handle the move + link updating simultaneously.
4.  **Verify:** Run the `tests/test_gallery_updater.py` (updated for new paths) to ensure the gallery still builds.
5.  **Launch:** Push the new structure.

This plan transforms the repo from a "folder of files" into a **Self-Curating Digital Institution**.
