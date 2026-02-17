#!/usr/bin/env python3
"""
arXiv Paper Fetcher
Fetches latest papers from arXiv API and generates an HTML page.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import html
import sys
import json

# Configuration - load from config.json if available
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

def load_config():
    """Load configuration from config.json file."""
    default_config = {
        "keywords": ["large language model", "machine learning", "biostatistics", "deep learning"],
        "max_results": 20
    }
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return {
                    "keywords": config.get("keywords", default_config["keywords"]),
                    "max_results": config.get("max_results", default_config["max_results"])
                }
        except Exception as e:
            print(f"Warning: Could not load config.json: {e}")
            print("Using default configuration.")
    
    return default_config

# Load configuration
config = load_config()
KEYWORDS = config["keywords"]
MAX_RESULTS = config["max_results"]
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "..", "papers.html")

# arXiv API endpoint
ARXIV_API_URL = "http://export.arxiv.org/api/query"

def fetch_papers(keywords, max_results=20):
    """Fetch papers from arXiv API matching the given keywords."""
    # Build search query (OR between keywords)
    search_query = " OR ".join([f'all:"{kw}"' for kw in keywords])
    
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"
    print(f"Fetching papers from: {url}")
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            xml_data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return []
    
    return parse_arxiv_response(xml_data)

def parse_arxiv_response(xml_data):
    """Parse arXiv API XML response and extract paper details."""
    papers = []
    
    # Define namespaces
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []
    
    for entry in root.findall('atom:entry', namespaces):
        try:
            paper = {}
            
            # Title
            title_elem = entry.find('atom:title', namespaces)
            paper['title'] = ' '.join(title_elem.text.split()) if title_elem is not None and title_elem.text else "No title"
            
            # Authors
            authors = []
            for author in entry.findall('atom:author', namespaces):
                name_elem = author.find('atom:name', namespaces)
                if name_elem is not None and name_elem.text:
                    authors.append(name_elem.text)
            paper['authors'] = authors
            
            # Abstract
            summary_elem = entry.find('atom:summary', namespaces)
            paper['abstract'] = ' '.join(summary_elem.text.split()) if summary_elem is not None and summary_elem.text else "No abstract available"
            
            # Published date
            published_elem = entry.find('atom:published', namespaces)
            if published_elem is not None and published_elem.text:
                try:
                    pub_date = datetime.fromisoformat(published_elem.text.replace('Z', '+00:00'))
                    paper['published'] = pub_date.strftime('%Y-%m-%d')
                except:
                    paper['published'] = published_elem.text[:10]
            else:
                paper['published'] = "Unknown"
            
            # Links (abstract page and PDF)
            paper['arxiv_url'] = ""
            paper['pdf_url'] = ""
            
            for link in entry.findall('atom:link', namespaces):
                href = link.get('href', '')
                link_type = link.get('type', '')
                link_title = link.get('title', '')
                
                if link_title == 'pdf' or 'pdf' in href:
                    paper['pdf_url'] = href
                elif link_type == 'text/html' or '/abs/' in href:
                    paper['arxiv_url'] = href
            
            # arXiv ID
            id_elem = entry.find('atom:id', namespaces)
            if id_elem is not None and id_elem.text:
                paper['arxiv_id'] = id_elem.text.split('/abs/')[-1]
                if not paper['arxiv_url']:
                    paper['arxiv_url'] = id_elem.text
                if not paper['pdf_url']:
                    paper['pdf_url'] = id_elem.text.replace('/abs/', '/pdf/') + '.pdf'
            else:
                paper['arxiv_id'] = "Unknown"
            
            # Categories
            categories = []
            for category in entry.findall('atom:category', namespaces):
                term = category.get('term', '')
                if term:
                    categories.append(term)
            paper['categories'] = categories[:3]  # Limit to 3 categories
            
            papers.append(paper)
            
        except Exception as e:
            print(f"Error parsing entry: {e}")
            continue
    
    print(f"Parsed {len(papers)} papers")
    return papers

def truncate_text(text, max_length=300):
    """Truncate text to max_length and add ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'

def format_authors(authors, max_display=5):
    """Format author list, truncating if too many."""
    if len(authors) <= max_display:
        return ', '.join(authors)
    return ', '.join(authors[:max_display]) + f' <em>(+{len(authors) - max_display} more)</em>'

def generate_html(papers):
    """Generate the HTML page with paper listings."""
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    keywords_str = ', '.join(KEYWORDS)
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>arXiv Paper Feed | Coding Blog</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>
        .papers-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 100px 20px 40px;
        }}
        .papers-header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .papers-header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .update-info {{
            color: #cbd5e1;
            font-size: 0.9rem;
            margin-bottom: 8px;
        }}
        .auto-update-info {{
            color: #22c55e;
            font-size: 0.85rem;
            margin-bottom: 15px;
        }}
        .config-hint {{
            color: #94a3b8;
            font-size: 0.8rem;
            margin-bottom: 10px;
        }}
        .config-hint code {{
            background: #334155;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: var(--font-code);
            color: #f472b6;
        }}
        .search-box {{
            max-width: 500px;
            margin: 20px auto;
        }}
        .search-box input {{
            width: 100%;
            padding: 12px 20px;
            border: 2px solid var(--border);
            border-radius: 25px;
            background: var(--card-bg);
            color: var(--text-primary);
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }}
        .search-box input:focus {{
            border-color: var(--primary);
        }}
        .search-box input::placeholder {{
            color: var(--text-muted);
        }}
        .papers-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }}
        .paper-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 25px;
            transition: all 0.3s ease;
        }}
        .paper-card:hover {{
            border-color: var(--primary);
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(236, 72, 153, 0.15);
        }}
        .paper-card.hidden {{
            display: none;
        }}
        .paper-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        .paper-title a {{
            color: inherit;
            text-decoration: none;
            transition: color 0.3s;
        }}
        .paper-title a:hover {{
            color: var(--primary);
        }}
        .paper-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 12px;
        }}
        .paper-date {{
            background: var(--primary);
            color: white;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 500;
        }}
        .paper-category {{
            background: #334155;
            color: #e2e8f0;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.75rem;
        }}
        .paper-authors {{
            color: #cbd5e1;
            font-size: 0.9rem;
            margin-bottom: 12px;
            line-height: 1.5;
        }}
        .paper-abstract {{
            color: #94a3b8;
            font-size: 0.9rem;
            line-height: 1.7;
            margin-bottom: 15px;
        }}
        .paper-abstract.expanded {{
            max-height: none;
        }}
        .expand-btn {{
            background: none;
            border: none;
            color: var(--primary);
            cursor: pointer;
            font-size: 0.85rem;
            padding: 0;
            margin-bottom: 15px;
        }}
        .expand-btn:hover {{
            text-decoration: underline;
        }}
        .paper-actions {{
            display: flex;
            gap: 10px;
        }}
        .pdf-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            text-decoration: none;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.3s;
        }}
        .pdf-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(236, 72, 153, 0.3);
        }}
        .arxiv-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            background: var(--surface);
            color: var(--text-primary);
            text-decoration: none;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            border: 1px solid var(--border);
            transition: all 0.3s;
        }}
        .arxiv-btn:hover {{
            border-color: var(--primary);
            color: var(--primary);
        }}
        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: var(--text-muted);
        }}
        .no-results h3 {{
            font-size: 1.5rem;
            margin-bottom: 10px;
            color: var(--text-secondary);
        }}
        .keywords-info {{
            background: #1e293b;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            text-align: center;
            border: 1px solid #334155;
        }}
        .keywords-info > span {{
            color: #e2e8f0;
            font-size: 0.95rem;
            font-weight: 500;
        }}
        .keyword-tag {{
            display: inline-block;
            background: linear-gradient(135deg, #6366f1, #ec4899);
            color: #ffffff;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 4px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }}
        .keyword-editor {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #334155;
        }}
        .keyword-input-group {{
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 10px;
        }}
        .keyword-input {{
            padding: 10px 16px;
            border: 2px solid #334155;
            border-radius: 25px;
            background: #0f172a;
            color: #f8fafc;
            font-size: 0.9rem;
            width: 250px;
            outline: none;
            transition: border-color 0.3s;
        }}
        .keyword-input:focus {{
            border-color: #6366f1;
        }}
        .keyword-input::placeholder {{
            color: #64748b;
        }}
        .fetch-btn {{
            padding: 10px 24px;
            background: linear-gradient(135deg, #6366f1, #ec4899);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .fetch-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(99, 102, 241, 0.4);
        }}
        .fetch-btn:disabled {{
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }}
        .editor-hint {{
            color: #94a3b8;
            font-size: 0.8rem;
            margin-top: 8px;
        }}
        @media (max-width: 768px) {{
            .papers-grid {{
                grid-template-columns: 1fr;
            }}
            .papers-header h1 {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="index.html" class="nav-logo">
                <span class="logo-icon">💻</span>
                <span class="logo-text">Coding Blog</span>
            </a>
            <ul class="nav-menu">
                <li><a href="index.html" class="nav-link">Home</a></li>
                <li><a href="index.html#projects" class="nav-link">Projects</a></li>
                <li><a href="papers.html" class="nav-link active">Papers</a></li>
                <li><a href="index.html#about" class="nav-link">About</a></li>
            </ul>
            <button class="nav-toggle" aria-label="Toggle navigation">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </nav>

    <div class="papers-container">
        <div class="papers-header">
            <h1>📚 arXiv Paper Feed</h1>
            <p class="update-info">Last updated: {update_time}</p>
            <p class="auto-update-info">⏰ Auto-updates daily at midnight UTC via GitHub Actions</p>
            <div class="keywords-info">
                <span>Current keywords: </span>
                <div id="currentKeywords">
                    {''.join([f'<span class="keyword-tag">{kw}</span>' for kw in KEYWORDS])}
                </div>
                <div class="keyword-editor">
                    <p class="editor-hint">🔄 Try different keywords (fetches live from arXiv):</p>
                    <div class="keyword-input-group">
                        <input type="text" id="customKeywords" class="keyword-input" 
                               placeholder="e.g., reinforcement learning, NLP" 
                               value="{', '.join(KEYWORDS)}">
                        <button onclick="fetchCustomPapers()" class="fetch-btn" id="fetchBtn">
                            Fetch Papers
                        </button>
                    </div>
                    <p class="editor-hint">Separate multiple keywords with commas</p>
                </div>
            </div>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Filter papers by title, author, or abstract..." oninput="filterPapers()">
            </div>
        </div>

        <div class="papers-grid" id="papersGrid">
'''
    
    if not papers:
        html_content += '''
            <div class="no-results" style="grid-column: 1 / -1;">
                <h3>No papers found</h3>
                <p>Try again later or check the keywords configuration.</p>
            </div>
'''
    else:
        for i, paper in enumerate(papers):
            title_escaped = html.escape(paper['title'])
            authors_formatted = format_authors(paper['authors'])
            abstract_short = html.escape(truncate_text(paper['abstract'], 200))
            abstract_full = html.escape(paper['abstract'])
            
            # Escape single quotes for JavaScript (avoiding backslash in f-string)
            abstract_full_js = abstract_full.replace("'", "\\'")
            abstract_short_js = abstract_short.replace("'", "\\'")
            
            categories_html = ''.join([f'<span class="paper-category">{cat}</span>' for cat in paper['categories']])
            
            html_content += f'''
            <article class="paper-card" data-search="{html.escape(paper['title'].lower())} {html.escape(' '.join(paper['authors']).lower())} {html.escape(paper['abstract'].lower())}">
                <h2 class="paper-title">
                    <a href="{paper['arxiv_url']}" target="_blank" rel="noopener">{title_escaped}</a>
                </h2>
                <div class="paper-meta">
                    <span class="paper-date">📅 {paper['published']}</span>
                    {categories_html}
                </div>
                <p class="paper-authors">{authors_formatted}</p>
                <p class="paper-abstract" id="abstract-{i}">{abstract_short}</p>
                <button class="expand-btn" onclick="toggleAbstract({i}, '{abstract_full_js}', '{abstract_short_js}')" id="expand-btn-{i}">Show more ▼</button>
                <div class="paper-actions">
                    <a href="{paper['pdf_url']}" class="pdf-btn" target="_blank" rel="noopener">📄 View PDF</a>
                    <a href="{paper['arxiv_url']}" class="arxiv-btn" target="_blank" rel="noopener">🔗 arXiv</a>
                </div>
            </article>
'''
    
    html_content += '''
        </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Coding Blog | BST 236 Computing I | Harvard University</p>
            <p class="footer-links">
                <a href="https://github.com">GitHub</a>
            </p>
        </div>
    </footer>

    <script src="js/main.js"></script>
    <script>
        function filterPapers() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.paper-card');
            
            cards.forEach(card => {
                const searchText = card.getAttribute('data-search');
                if (searchText.includes(query)) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        }
        
        function toggleAbstract(index, fullText, shortText) {
            const abstractEl = document.getElementById('abstract-' + index);
            const btnEl = document.getElementById('expand-btn-' + index);
            
            if (abstractEl.classList.contains('expanded')) {
                abstractEl.textContent = shortText;
                abstractEl.classList.remove('expanded');
                btnEl.textContent = 'Show more ▼';
            } else {
                abstractEl.textContent = fullText;
                abstractEl.classList.add('expanded');
                btnEl.textContent = 'Show less ▲';
            }
        }
        
        // Client-side arXiv fetching for custom keywords
        // CORS proxies to try in order
        const corsProxies = [
            url => `https://corsproxy.io/?${encodeURIComponent(url)}`,
            url => `https://api.codetabs.com/v1/proxy?quest=${encodeURIComponent(url)}`,
            url => `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`
        ];
        
        async function tryFetchWithProxies(url, proxies) {
            for (let i = 0; i < proxies.length; i++) {
                const proxyUrl = proxies[i](url);
                try {
                    const response = await fetch(proxyUrl, { timeout: 10000 });
                    if (response.ok) {
                        return await response.text();
                    }
                } catch (e) {
                    console.log(`Proxy ${i + 1} failed:`, e.message);
                }
            }
            throw new Error('All CORS proxies failed. Please try again later or edit scripts/config.json directly.');
        }
        
        async function fetchCustomPapers() {
            const input = document.getElementById('customKeywords').value.trim();
            const btn = document.getElementById('fetchBtn');
            const grid = document.getElementById('papersGrid');
            const keywordsDisplay = document.getElementById('currentKeywords');
            
            if (!input) {
                alert('Please enter at least one keyword');
                return;
            }
            
            const keywords = input.split(',').map(k => k.trim()).filter(k => k);
            
            btn.disabled = true;
            btn.textContent = 'Fetching...';
            
            // Update displayed keywords
            keywordsDisplay.innerHTML = keywords.map(kw => 
                `<span class="keyword-tag">${escapeHtml(kw)}</span>`
            ).join('');
            
            // Build arXiv query
            const searchQuery = keywords.map(kw => `all:"${kw}"`).join(' OR ');
            const url = `https://export.arxiv.org/api/query?search_query=${encodeURIComponent(searchQuery)}&start=0&max_results=20&sortBy=submittedDate&sortOrder=descending`;
            
            try {
                const xmlText = await tryFetchWithProxies(url, corsProxies);
                
                // Parse XML
                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
                const entries = xmlDoc.querySelectorAll('entry');
                
                if (entries.length === 0) {
                    grid.innerHTML = `
                        <div class="no-results" style="grid-column: 1 / -1;">
                            <h3>No papers found</h3>
                            <p>Try different keywords.</p>
                        </div>
                    `;
                } else {
                    let html = '';
                    entries.forEach((entry, i) => {
                        const title = entry.querySelector('title')?.textContent?.replace(/\\s+/g, ' ').trim() || 'Untitled';
                        const abstract = entry.querySelector('summary')?.textContent?.replace(/\\s+/g, ' ').trim() || 'No abstract';
                        const published = entry.querySelector('published')?.textContent?.substring(0, 10) || 'Unknown';
                        const id = entry.querySelector('id')?.textContent || '';
                        const pdfUrl = id.replace('/abs/', '/pdf/') + '.pdf';
                        
                        const authors = [];
                        entry.querySelectorAll('author name').forEach(n => authors.push(n.textContent));
                        const authorsStr = authors.length > 5 
                            ? authors.slice(0, 5).join(', ') + ` <em>(+${authors.length - 5} more)</em>`
                            : authors.join(', ');
                        
                        const categories = [];
                        entry.querySelectorAll('category').forEach(c => {
                            const term = c.getAttribute('term');
                            if (term && categories.length < 3) categories.push(term);
                        });
                        
                        const abstractShort = abstract.length > 200 
                            ? abstract.substring(0, 200).replace(/\\s+\\S*$/, '') + '...'
                            : abstract;
                        
                        html += `
                            <article class="paper-card" data-search="${escapeHtml(title.toLowerCase())} ${escapeHtml(authors.join(' ').toLowerCase())} ${escapeHtml(abstract.toLowerCase())}">
                                <h2 class="paper-title">
                                    <a href="${escapeHtml(id)}" target="_blank" rel="noopener">${escapeHtml(title)}</a>
                                </h2>
                                <div class="paper-meta">
                                    <span class="paper-date">📅 ${escapeHtml(published)}</span>
                                    ${categories.map(c => `<span class="paper-category">${escapeHtml(c)}</span>`).join('')}
                                </div>
                                <p class="paper-authors">${authorsStr}</p>
                                <p class="paper-abstract" id="abstract-dyn-${i}">${escapeHtml(abstractShort)}</p>
                                <button class="expand-btn" onclick="toggleAbstract('dyn-${i}', '${escapeHtml(abstract).replace(/'/g, "\\\\'")}', '${escapeHtml(abstractShort).replace(/'/g, "\\\\'")}')">Show more ▼</button>
                                <div class="paper-actions">
                                    <a href="${escapeHtml(pdfUrl)}" class="pdf-btn" target="_blank" rel="noopener">📄 View PDF</a>
                                    <a href="${escapeHtml(id)}" class="arxiv-btn" target="_blank" rel="noopener">🔗 arXiv</a>
                                </div>
                            </article>
                        `;
                    });
                    grid.innerHTML = html;
                }
                
                // Update timestamp
                const now = new Date().toISOString().replace('T', ' ').substring(0, 19) + ' (live fetch)';
                document.querySelector('.update-info').textContent = 'Last updated: ' + now;
                
            } catch (error) {
                console.error('Fetch error:', error);
                grid.innerHTML = `
                    <div class="no-results" style="grid-column: 1 / -1;">
                        <h3>Error fetching papers</h3>
                        <p>${escapeHtml(error.message)}</p>
                        <p style="margin-top: 15px; font-size: 0.9rem;">
                            <strong>Alternative:</strong> Edit <code style="background: #334155; padding: 2px 6px; border-radius: 4px;">scripts/config.json</code> 
                            and run <code style="background: #334155; padding: 2px 6px; border-radius: 4px;">python scripts/fetch_arxiv.py</code> locally, 
                            or push to GitHub to trigger the auto-update.
                        </p>
                    </div>
                `;
            }
            
            btn.disabled = false;
            btn.textContent = 'Fetch Papers';
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Allow Enter key to trigger fetch
        document.getElementById('customKeywords').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') fetchCustomPapers();
        });
    </script>
</body>
</html>
'''
    
    return html_content

def main():
    """Main function to fetch papers and generate HTML."""
    print("=" * 50)
    print("arXiv Paper Fetcher")
    print("=" * 50)
    print(f"Keywords: {KEYWORDS}")
    print(f"Max results: {MAX_RESULTS}")
    print()
    
    # Fetch papers
    papers = fetch_papers(KEYWORDS, MAX_RESULTS)
    
    if not papers:
        print("Warning: No papers fetched. Generating empty page.")
    
    # Generate HTML
    html_content = generate_html(papers)
    
    # Write to file
    output_path = os.path.abspath(OUTPUT_FILE)
    print(f"\nWriting HTML to: {output_path}")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Successfully generated papers.html with {len(papers)} papers!")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
