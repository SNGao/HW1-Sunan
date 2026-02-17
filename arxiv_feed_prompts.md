# arXiv Paper Feed - Copilot CLI Prompts

This document contains the prompts used with GitHub Copilot CLI to build the auto-updating arXiv paper feed.

## Plan Overview

**Goal**: Create an auto-updating arXiv paper feed that:
1. Fetches latest papers from arXiv API matching chosen keywords
2. Generates a styled HTML page with paper details
3. Auto-updates daily via GitHub Actions
4. Links from the homepage

---

## Step 1: Planning Prompt

```
@workspace I need to build an auto-updating arXiv paper feed for my coding blog website. Help me plan the architecture:

1. A Python script that fetches papers from arXiv API matching keywords like "machine learning", "large language models"
2. The script generates an HTML page with paper titles, authors, abstracts, and PDF links
3. A GitHub Actions workflow that runs at midnight daily to execute the script and commit changes
4. The page should match my existing website style in coding_blog/css/style.css

What files do I need to create and what's the recommended workflow?
```

---

## Step 2: Create the arXiv Fetcher Script

```
Create a Python script at coding_blog/scripts/fetch_arxiv.py that:
1. Uses the arXiv API to fetch the 20 latest papers matching keywords: "large language model", "machine learning", "biostatistics"
2. Parses the XML response to extract: title, authors, abstract, published date, PDF link, arXiv ID
3. Generates an HTML file at coding_blog/papers.html with:
   - A styled header matching my site theme (dark mode, pink accents)
   - Paper cards showing title, authors (truncated if >5), abstract (first 300 chars), and "Read PDF" button
   - Sort papers by date (newest first)
4. Include error handling and logging
5. Use only standard library + requests + feedparser (pip installable)
```

---

## Step 3: Create the HTML Template

```
Create a Jinja2 or string-template based HTML generator in the fetch_arxiv.py script. The output HTML should:
1. Have the same navigation bar as my coding_blog/index.html
2. Use CSS from ../css/style.css
3. Display papers in a responsive grid layout (2 columns on desktop, 1 on mobile)
4. Each paper card should have:
   - Title as a link to the arXiv abstract page
   - Authors list
   - Publication date badge
   - Collapsible abstract (show first 200 chars, expand on click)
   - "View PDF" button linking to the PDF
5. Show "Last updated: [timestamp]" at the top
6. Include a search/filter box to filter papers by keyword (client-side JavaScript)
```

---

## Step 4: Create GitHub Actions Workflow

```
Create a GitHub Actions workflow at .github/workflows/update-arxiv.yml that:
1. Runs on schedule: every day at midnight UTC (cron: '0 0 * * *')
2. Also allows manual trigger (workflow_dispatch)
3. Steps:
   - Checkout the repository
   - Set up Python 3.11
   - Install dependencies: pip install requests feedparser
   - Run the fetch script: python coding_blog/scripts/fetch_arxiv.py
   - Commit and push changes if papers.html was modified
   - Use a bot commit message like "Auto-update arXiv papers [skip ci]"
4. Use GITHUB_TOKEN for authentication
5. Configure git user as "github-actions[bot]"
```

---

## Step 5: Add Link to Homepage

```
Update coding_blog/index.html to add a link to the papers.html page:
1. Add a card in the Projects section linking to papers.html
2. Title: "arXiv Paper Feed"
3. Description: "Latest research papers on ML, LLMs, and biostatistics - auto-updated daily"
4. Add an icon or emoji (📄 or 📚)
```

---

## Step 6: Create Requirements File

```
Create coding_blog/scripts/requirements.txt with:
requests>=2.28.0
feedparser>=6.0.0
```

---

## Architecture Summary

```
coding_blog/
├── scripts/
│   ├── fetch_arxiv.py      # Fetches papers, generates HTML
│   └── requirements.txt    # Python dependencies
├── papers.html             # Generated page (auto-updated)
├── index.html              # Homepage (add link to papers)
└── css/style.css           # Existing styles

.github/
└── workflows/
    └── update-arxiv.yml    # Nightly automation
```

---

## Verification Commands

After implementing, test with:
```bash
cd coding_blog/scripts && pip install -r requirements.txt && python fetch_arxiv.py
```

Then verify:
- `papers.html` is generated with recent papers
- Page renders correctly when served locally
- GitHub Actions workflow runs successfully (check Actions tab)
