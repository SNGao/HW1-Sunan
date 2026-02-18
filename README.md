# Homework 1: Code with AI

BST 236: Computing I | Harvard University

## 🌐 Coding Blog Website


**[Visit the HW1 website](https://sngao.github.io/HW1-Sunan/)**

### Website Pages

| Page | Description |
|------|-------------|
| [Coding Blog Homepage](coding_blog/index.html) | Main landing page with project overview |
| [Valentine's Pac-Man](coding_blog/games/pacman_build/index.html) | Play the Valentine-themed Pac-Man game |
| [arXiv Papers](coding_blog/papers.html) | Auto-updating research paper feed |

---

## Case Study: Using AI Copilot for Coding

This README serves as a case-study tutorial documenting how I used AI coding assistants to complete three problems. Below, I describe the AI tools used, how I designed and adjusted prompts through iterative debugging, and the lessons learned from each problem.

### AI Tools Used

| Tool | Usage |
|------|-------|
| **GitHub Copilot (VSCode)** | Primary coding assistant, code generation, debugging |
| **Claude AI (Opus 4.5)** | Complex problem-solving, architecture decisions, multi-file refactoring, planning |

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

### Prompt Design Process

**Note**: I actually started with Problem 2 (the game), then moved to Problem 1. After completing the game, I needed to integrate it into a website.

**Main Prompt**:
```
Following the illustrations in Guide.md, I need Create a homepage for a website for my coding blog. The website should be hosted on GitHub Pages. You can design the homepage by yourself in any proper style you like. You may need to make the design expandable to add more content from our  future assignments. The link to the homepage should be added to the README.md of your homework repository so that anyone can access the homepage and the following two webpages from the Internet using this link. And we already develop the game: Pac_Man, saved in the Pac_Man folder
```

**Key Design Decision**: I let the AI choose the design style ("You can design the homepage by yourself in any proper style you like") while specifying the requirement for expandability for future assignments.

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

### Detailed Prompt Engineering & Iterative Debugging Process

This section documents the complete workflow showing how I used AI assistants and adjusted prompts iteratively.

#### Step 1: Initial Planning with Claude Opus 4.5

I started by using the `plan` mode to get AI guidance on the task:

```
Following the illustrations in Guide.md, I first need to develop a game named 
Pac-Man(Valentine's Special), which corresponds to the Problem 2. For this game, 
the user can play this game on a browser by opening html. I want to use Python to code. 
Please give me a detailed prompt on the instruction of this task.
```

Then I asked the AI to:
```
Save this prompt into a markdown file, and then please do the task and write the code.
```

#### Step 2: First Bug - Ghost Movement Issues

**Problem Observed**: The game runs normally, but ghosts appear at the start of the game, go to the same spot one by one, and then stop instead of chasing Pac-Man.

**My Prompt**:
```
The game runs normally, but the issues still exist. Ghosts appear at the start of the 
game, but instead of chasing Pac-Man, they go to the same spot one by one and then stop. 
The ghost is expected to move and chase Pac-Man rather than staying in the same place.
```

#### Step 3: Web Deployment Issues with pygbag

After building with pygbag, I faced deployment issues. My debugging prompts:

**Prompt 1**:
```
I have built the Pac-Man game using 'pygbag --build main.py', and generated the file 
saved in Pac_Man/build folder. And following the instructions, I copy the contents in 
Pac_Man/build/web and paste them in coding_blog/games/pacman_build. But I faced issues 
to open the game after clicking index.html, and it returned "Loading, please wait", 
but no more changes.
```

**Prompt 2** (after partial fix):
```
It shows loading first, and then changes to "ready to start, please click/touch page", 
but after clicking, I still fail to play the game.
```

**Prompt 3** (problem persisted):
```
The problem persists. After clicking the "Ready to start, please click/touch the page" 
message, the page turns gray. Additionally, I cannot load the game interface from 
'Pac_Man/build/web/index.html'.
```

#### Step 4: Pivoting to JavaScript

After multiple failed attempts with pygbag, I decided to change technology:

```
Change to JavaScript. How to open the coding blog website and run the Pac-Man game?
```

**New issue with JS version**:
```
I can open the website but fail to start the game as the game window in the page is 
completely black, even though I have pressed start button.
```

**Follow-up**:
```
I can play the game through 'python main.py' in the folder Pac_Man, but I fail to play 
the game in the html you show me. And the game window is always black. Could you solve this issue?
```

#### Step 5: Ghost AI Debugging (Multiple Iterations)

Once the game loaded, I discovered ghost AI issues. Here's my iterative debugging:

**Iteration 1**:
```
I can start the game now, but the ghosts seem to have some problems moving. When I move 
Pac-Man, the ghosts can't catch me; they don't seem to understand the structure of the 
obstacles in the maze, and even when they can move, they can't leave the area where they appear.
```

**Iteration 2** (after a fix):
```
The movement of ghost still have several issues. After my Pac-Man meets with the ghost 
and dies, some ghosts will stop chasing Pac-Man. I remember in the original Pac-Man game, 
this issue didn't appear. Could you check why it happens and solve it?
```

**Iteration 3** (comparing with working version):
```
Similar issues as before. When I move Pac-Man, the ghosts can't catch me; they don't seem 
to understand the structure of the obstacles in the maze, and even when they can move, 
they can't leave the area where they appear. And when they leave the birth region and 
begin to chase me, some of them will stop chasing me. Also, the game before we build website 
seems to work well. That is to say, these issues do not exist when running 'Pac_Man % python main.py'.
```

**Key Insight**: Comparing the working Python version with the broken JavaScript version helped identify that the pathfinding logic wasn't properly ported.

#### Step 6: Final Tuning

**Balance adjustment**:
```
Everything is great, but the ghost is much faster than Pac-Man, could you make it a little slower?
```

### Lessons Learned from Problem 2

1. **Technology Pivot**: When pygbag CDN failed, switching to pure JavaScript was the right call
2. **Specific Bug Reports**: Describing exactly what ghosts were doing wrong (stopping, not understanding maze) was more effective than saying "ghosts don't work"
3. **Reference Comparison**: Pointing out that "python main.py works but HTML doesn't" helped AI identify porting issues
4. **Iterative Refinement**: Multiple rounds of testing and feedback were necessary to get ghost AI working correctly

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

### Prompt Design Process with Copilot CLI

Following the agentic programming paradigm taught in class, I used a "plan first, then implement" approach.

**Initial Planning Prompt**:
```
In this part, I plan to build an auto-updating arXiv paper feed in my website. 
I plan to break the task into agent-friendly steps, prompt the agent effectively, 
and wire everything together. Could you show me the prompt that can help Copilot CLI to code. 

Here are several requirements: Add a new page to your website that displays the latest 
arXiv papers. The page must include:
1. **Paper Listing**: The latest arXiv papers matching keywords of your choice. Design the layout as you see fit.
2. **Paper Details**: Each entry must show the paper title, authors, abstract, and a direct link to the PDF.
3. **Auto-Update**: The paper list must refresh automatically every midnight via a GitHub Actions workflow.
4. **Homepage Link**: A link to this page must appear on your homepage from Problem 1.
5. **Page Design**: Style the page in any way you think readers would appreciate.

And detailed illustrations can be found in Guide.md
```

**Implementation Prompts** (used sequentially with Copilot CLI):

```
1. "Create a Python script that fetches papers from arXiv API using keywords 
   'large language model', 'machine learning', 'biostatistics', 'deep learning'"

2. "Generate an HTML page from the fetched papers with title, authors, abstract, 
   and PDF link"

3. "Create a GitHub Actions workflow that runs the script daily at midnight UTC"

4. "Add search/filter functionality to the papers page"

5. "Make keywords configurable via a JSON config file"
```

**Follow-up Refinement**:
```
Nice, there are something I want to further check: 
(1) Could I change the keywords, and then the paper shown will be changed correspondingly? 
    The keywords now seem fixed.
```

This led to the implementation of `config.json` for configurable keywords.

### Iteration Notes

- Added configurable keywords via `config.json`
- Improved font colors for better visibility
- Added interactive keyword editor with multiple CORS proxy fallbacks
- Added visual indicator showing auto-update schedule

See `arxiv_feed_prompts.md` for the complete list of prompts used.

---

## Summary: Lessons Learned

1. **Pygbag CDN Issues**: External dependencies can fail unexpectedly. Having a fallback (JavaScript) saved the project.

2. **Iterative Debugging**: AI assistants work best with specific, incremental problem descriptions rather than vague complaints.

3. **CORS Limitations**: Browser-based API calls require CORS proxies; server-side fetching (GitHub Actions) is more reliable.

4. **Prompt Engineering**: Being specific about requirements (e.g., "ghosts should chase Pac-Man and understand maze walls") produces better results.

5. **Planning First**: Using the "plan first" approach before implementing helped break down complex tasks into manageable agent-friendly steps.

6. **Reference Comparison**: When debugging, comparing working code (Python main.py) with broken code (JavaScript port) helps AI identify issues faster.

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
