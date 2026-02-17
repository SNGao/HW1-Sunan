# Homework 1: Code with AI

BST 236: Computing I | Harvard University

## 🌐 Coding Blog Website

**[Visit the Coding Blog Homepage](https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPO_NAME/coding_blog/)**

> **Note**: Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name after deploying to GitHub Pages.

### Website Pages

| Page | Description |
|------|-------------|
| [Homepage](coding_blog/index.html) | Main landing page with project overview |
| [Valentine's Pac-Man](coding_blog/games/pacman_build/index.html) | Play the Valentine-themed Pac-Man game |
| [arXiv Papers](coding_blog/papers.html) | Auto-updating research paper feed |

---

## Problem 1: GitHub Website for Your Coding Blog

Created a homepage for the coding blog website hosted on GitHub Pages. The design features:

- Modern, dark-themed UI with responsive design
- Navigation with smooth scrolling
- Projects section showcasing the Pac-Man game and arXiv Paper Feed
- Papers section for the arXiv feed
- About section describing the blog purpose
- Expandable structure for future assignments

### Files Created

- `coding_blog/index.html` - Main homepage
- `coding_blog/papers.html` - arXiv papers page (auto-generated)
- `coding_blog/games/pacman_build/index.html` - Pac-Man game
- `coding_blog/css/style.css` - Stylesheet
- `coding_blog/js/main.js` - JavaScript functionality

### Prompt Used
```
Following the illustrations in Guide.md, I need Create a homepage for a website for my coding blog. 
The website should be hosted on GitHub Pages. You can design the homepage by yourself in any 
proper style you like. You may need to make the design expandable to add more content from our 
future assignments.
```

---

## Problem 2: Game Coding - Pac-Man (Valentine's Special 💘)

Developed a Valentine-themed Pac-Man game with the following features:

### Core Features

1. **Classic Pac-Man Mechanics**
   - 28x31 grid maze with walls and dots
   - Pac-Man controlled by arrow keys
   - 4 ghosts with different AI behaviors (chase, scatter, random)

2. **Valentine's Power-Up — Rose 🌹**
   - Roses randomly appear on the maze every few seconds
   - Collecting a rose activates powered-up state for ~5 seconds
   - Visual indicator when powered up

3. **Heart Projectiles 💕**
   - When powered up, Pac-Man automatically shoots hearts
   - Hearts travel in the facing direction through the maze
   - Hearts eliminate ghosts on contact (ghosts respawn)

### Technology Stack

**Initial Attempt**: Python/Pygame with pygbag for WebAssembly compilation
- Encountered issue: pygbag CDN (pygame-web.github.io) returning 404 errors for WebAssembly runtime files

**Final Solution**: Pure JavaScript/HTML5 Canvas implementation
- No external dependencies
- Works directly in browser without server compilation
- Full game functionality preserved

### Game Files

Web version in `coding_blog/games/pacman_build/`:
- `index.html` - Complete game (~850 lines of JavaScript)

Original Python version in `Pac_Man/` folder (for reference):
- `main.py`, `game.py`, `pacman.py`, `ghost.py`, `maze.py`, `projectile.py`, `powerup.py`, `config.py`

### Prompts and Iterations

Initial prompt:
```
Following the illustrations in Guide.md, I first need to develop a game named Pac-Man 
(Valentine's Special). The user can play this game on a browser by opening html. 
Please give me a detailed prompt on the instruction of this task.
```

Debugging prompts (iterative fixes):
```
- "The ghosts can't catch me; they don't seem to understand the structure of the obstacles in the maze"
- "When they leave the birth region and begin to chase me, some of them will stop chasing me"
- "The ghost is much faster than Pac-Man, could make it a little slower?"
```

---

## Problem 3: Data Scaffolding from the Internet

Built an auto-updating arXiv paper feed using Copilot CLI (GitHub Copilot in VSCode).

### Deliverables Completed

1. **Paper Listing** ✅
   - Fetches 20 latest papers matching configurable keywords
   - Keywords: "large language model", "machine learning", "biostatistics", "deep learning"
   - Keywords configurable via `scripts/config.json`

2. **Paper Details** ✅
   - Paper title (linked to arXiv page)
   - Authors (with "show more" for many authors)
   - Abstract (expandable)
   - Direct PDF link
   - arXiv categories

3. **Auto-Update** ✅
   - GitHub Actions workflow runs at midnight UTC daily
   - Also triggers on push to main branch
   - Workflow file: `.github/workflows/update-arxiv.yml`

4. **Homepage Link** ✅
   - Papers section on homepage with "View Papers" button
   - Project card for arXiv Paper Feed in Projects section

5. **Page Design** ✅
   - Dark theme matching homepage
   - Search/filter functionality
   - Interactive keyword editor (live fetch with CORS proxy fallback)
   - Responsive grid layout

### Files Created

- `coding_blog/scripts/fetch_arxiv.py` - Python script to fetch papers and generate HTML
- `coding_blog/scripts/config.json` - Configurable keywords
- `coding_blog/scripts/requirements.txt` - Python dependencies
- `coding_blog/papers.html` - Generated papers page
- `.github/workflows/update-arxiv.yml` - GitHub Actions workflow

### Prompts Used with Copilot CLI

See `arxiv_feed_prompts.md` for detailed prompts. Key prompts:

```
1. "Create a Python script that fetches papers from arXiv API using keywords 
   'large language model', 'machine learning', 'biostatistics', 'deep learning'"

2. "Generate an HTML page from the fetched papers with title, authors, abstract, 
   and PDF link"

3. "Create a GitHub Actions workflow that runs the script daily at midnight UTC"

4. "Add search/filter functionality to the papers page"

5. "Make keywords configurable via a JSON config file"
```

### Iteration Notes

- Added configurable keywords via `config.json`
- Improved font colors for better visibility
- Added interactive keyword editor with multiple CORS proxy fallbacks
- Added visual indicator showing auto-update schedule

---

## AI Tools Used

| Tool | Usage |
|------|-------|
| **GitHub Copilot (VSCode)** | Primary coding assistant, code generation, debugging |
| **Claude AI (Opus 4.5)** | Complex problem-solving, architecture decisions, multi-file refactoring |

## Lessons Learned

1. **Pygbag CDN Issues**: External dependencies can fail unexpectedly. Having a fallback (JavaScript) saved the project.

2. **Iterative Debugging**: AI assistants work best with specific, incremental problem descriptions rather than vague complaints.

3. **CORS Limitations**: Browser-based API calls require CORS proxies; server-side fetching (GitHub Actions) is more reliable.

4. **Prompt Engineering**: Being specific about requirements (e.g., "ghosts should chase Pac-Man and understand maze walls") produces better results.

---

## How to Deploy

1. Push this repository to GitHub
2. Go to repository Settings → Pages
3. Configure GitHub Pages to deploy from the main branch
4. The website will be available at `https://YOUR_USERNAME.github.io/REPO_NAME/coding_blog/`

## Local Development

```bash
# Run local server
cd coding_blog
python -m http.server 8000
# Visit http://localhost:8000

# Regenerate arXiv papers
cd coding_blog/scripts
python fetch_arxiv.py
```

## Repository Structure

```
HW1-byme/
├── .github/
│   └── workflows/
│       └── update-arxiv.yml    # Daily auto-update workflow
├── coding_blog/
│   ├── css/style.css           # Stylesheet
│   ├── js/main.js              # JavaScript
│   ├── games/pacman_build/     # Pac-Man game
│   │   └── index.html
│   ├── scripts/
│   │   ├── fetch_arxiv.py      # arXiv fetcher
│   │   ├── config.json         # Keywords config
│   │   └── requirements.txt
│   ├── index.html              # Homepage
│   └── papers.html             # arXiv papers (auto-generated)
├── Pac_Man/                    # Original Python game (reference)
├── Guide.md                    # Assignment instructions
├── track_records.md            # Prompt history
├── arxiv_feed_prompts.md       # Copilot CLI prompts
└── README.md                   # This file
```
