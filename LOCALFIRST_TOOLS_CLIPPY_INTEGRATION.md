# LocalFirst Tools + Clippy AI Integration Guide

## Overview
This guide shows how to integrate an AI-powered Local First Tools browser into windows95-emulator.html with full Clippy assistance.

## Key Features to Implement

### 1. **AI-Powered Tool Discovery**
- Clippy can search for tools on behalf of users
- Intelligent recommendations based on user needs
- Natural language tool search
- Category and complexity filtering

### 2. **Clippy Methods for Tool Discovery**

Add these methods to your `MorphingClippy` class (around line 11,250):

```javascript
// =====================================================
// CLIPPY TOOL DISCOVERY METHODS
// =====================================================

// Search tools by natural language query
async searchToolsForUser(query) {
    if (!window.emulator.toolsBrowserState) {
        this.show('Please open the LocalFirst Tools Browser first! I can help you find tools there.', 'organizer');
        return null;
    }

    const state = window.emulator.toolsBrowserState;

    // Use AI to understand the query and find matching tools
    if (this.aiManager && this.aiManager.hasAPIKey()) {
        try {
            const context = {
                program: 'LocalFirst Tools',
                action: 'search_tools',
                query: query,
                availableCategories: Array.from(state.categories.keys()),
                toolCount: state.allTools.length
            };

            const prompt = `You are Clippy helping a user find tools.
Available categories: ${context.availableCategories.join(', ')}
Total tools: ${context.toolCount}

User query: "${query}"

Based on this query, suggest:
1. Best search keywords
2. Relevant category
3. Recommended complexity level
4. Brief explanation of why

Respond in JSON format:
{
    "keywords": ["word1", "word2"],
    "category": "category_name",
    "complexity": "simple|intermediate|advanced",
    "explanation": "why these tools match"
}`;

            const response = await this.aiManager.getClippyResponse(context, prompt);

            // Parse AI response and apply filters
            try {
                const suggestions = JSON.parse(response.tip);
                this.applyToolFilters(suggestions);
                this.show(`🔍 ${suggestions.explanation}`, 'organizer');
                return suggestions;
            } catch (e) {
                // Fallback to simple search
                this.simpleToolSearch(query);
            }
        } catch (error) {
            console.error('AI search failed:', error);
            this.simpleToolSearch(query);
        }
    } else {
        // Offline search
        this.simpleToolSearch(query);
    }
}

// Simple keyword-based search (fallback)
simpleToolSearch(query) {
    const searchInput = document.getElementById('tools-search-input');
    if (searchInput) {
        searchInput.value = query;
        searchInput.dispatchEvent(new Event('input', { bubbles: true }));
        this.show(`🔍 Searching for "${query}"...`, 'organizer');
    }
}

// Apply filters to tool browser
applyToolFilters(filters) {
    const categorySelect = document.getElementById('tools-category-select');
    const complexitySelect = document.getElementById('tools-complexity-select');
    const searchInput = document.getElementById('tools-search-input');

    if (filters.category && categorySelect) {
        categorySelect.value = filters.category;
        categorySelect.dispatchEvent(new Event('change'));
    }

    if (filters.complexity && complexitySelect) {
        complexitySelect.value = filters.complexity;
        complexitySelect.dispatchEvent(new Event('change'));
    }

    if (filters.keywords && searchInput) {
        searchInput.value = filters.keywords.join(' ');
        searchInput.dispatchEvent(new Event('input'));
    }
}

// Get AI-powered tool recommendations
async recommendToolsForUser(userNeed) {
    if (!window.emulator.toolsBrowserState) {
        this.show('Open LocalFirst Tools Browser for recommendations!', 'organizer');
        return;
    }

    this.show('🤔 Let me think about what would help you...', 'thinking', { thinking: true });

    const state = window.emulator.toolsBrowserState;

    if (this.aiManager && this.aiManager.hasAPIKey()) {
        try {
            const categories = Array.from(state.categories.entries()).map(([key, data]) => ({
                key, name: data.name, description: data.description || ''
            }));

            const sampleTools = state.allTools.slice(0, 10).map(t => ({
                title: t.title,
                category: t.categoryName,
                tags: t.tags?.slice(0, 3) || []
            }));

            const prompt = `You are Clippy recommending tools to a user.

User need: "${userNeed || 'general productivity'}"

Available categories: ${JSON.stringify(categories)}

Sample tools: ${JSON.stringify(sampleTools)}

Recommend 3 tools that would help. For each, explain why in one sentence.
Respond in JSON format:
{
    "recommendations": [
        {"toolName": "name", "reason": "why it helps"},
        ...
    ],
    "generalAdvice": "brief tip"
}`;

            const response = await this.aiManager.getClippyResponse({ program: 'LocalFirst Tools', action: 'recommend' }, prompt);

            try {
                const result = JSON.parse(response.tip);
                let message = '✨ Here are my recommendations:\n\n';
                result.recommendations.forEach((rec, i) => {
                    message += `${i + 1}. ${rec.toolName}: ${rec.reason}\n`;
                });
                if (result.generalAdvice) {
                    message += `\n💡 ${result.generalAdvice}`;
                }
                this.show(message, 'organizer');
            } catch (e) {
                this.showFallbackRecommendations();
            }
        } catch (error) {
            console.error('AI recommendation failed:', error);
            this.showFallbackRecommendations();
        }
    } else {
        this.showFallbackRecommendations();
    }
}

// Fallback recommendations without AI
showFallbackRecommendations() {
    const state = window.emulator.toolsBrowserState;
    if (!state) return;

    const popular = ['visual_art', 'games_puzzles', 'creative_tools'];
    const category = popular[Math.floor(Math.random() * popular.length)];

    this.applyToolFilters({ category });
    this.show('📋 Check out these popular tools! I filtered by a great category for you.', 'organizer');
}

// Show tool category info
explainCategory(categoryKey) {
    const state = window.emulator.toolsBrowserState;
    if (!state || !state.categories.has(categoryKey)) return;

    const category = state.categories.get(categoryKey);
    const toolCount = state.allTools.filter(t => t.category === categoryKey).length;

    this.show(
        `📂 ${category.name}: ${category.description || 'Various tools and applications'}\n` +
        `Total tools: ${toolCount}`,
        'organizer'
    );
}

// Random tool suggestion
showRandomTool() {
    const state = window.emulator.toolsBrowserState;
    if (!state || state.allTools.length === 0) return;

    const randomTool = state.allTools[Math.floor(Math.random() * state.allTools.length)];

    this.show(
        `🎲 How about "${randomTool.title}"?\n` +
        `${randomTool.description || 'Check it out!'}\n` +
        `Category: ${randomTool.categoryName}`,
        'helper'
    );

    // Open the tool
    setTimeout(() => {
        if (confirm('Want to open this tool?')) {
            window.emulator.openToolInWindow(randomTool);
        }
    }, 500);
}

// Guide user through tool discovery
async startToolDiscoveryTour() {
    const messages = [
        { text: '👋 Welcome to LocalFirst Tools! I\'m here to help you discover amazing tools.', mood: 'friendly', delay: 0 },
        { text: '🔍 You can search by keywords, or ask me to find tools for you!', mood: 'helpful', delay: 3000 },
        { text: '✨ Try saying "find me a drawing tool" or "show me games"!', mood: 'excited', delay: 6000 },
        { text: '📊 I can also recommend tools based on what you\'re working on!', mood: 'organizer', delay: 9000 }
    ];

    for (const msg of messages) {
        await new Promise(resolve => setTimeout(resolve, msg.delay));
        this.show(msg.text, msg.mood);
    }
}
```

### 3. **Enhanced Tool Browser Implementation**

Replace the `openLocalFirstBrowser()` method (line 7915-7980) with:

```javascript
// LocalFirst Tools Browser - AI-Enhanced Edition
openLocalFirstBrowser() {
    const content = document.createElement('div');
    content.className = 'tools-browser-container';
    content.style.cssText = 'display: flex; flex-direction: column; height: 100%; background: white;';

    // Create header with AI-assisted search
    const header = document.createElement('div');
    header.className = 'tools-browser-header';
    header.style.cssText = 'padding: 12px; border-bottom: 2px solid var(--button-shadow); background: var(--button-face);';

    const title = document.createElement('div');
    title.style.cssText = 'font-weight: bold; margin-bottom: 10px; font-size: 14px; display: flex; align-items: center; gap: 8px;';
    title.innerHTML = '🌐 LocalFirst Tools Gallery <span style="background: #06ffa5; color: black; padding: 2px 6px; border-radius: 8px; font-size: 10px;">AI POWERED</span>';
    header.appendChild(title);

    // Search row with Clippy assist button
    const searchRow = document.createElement('div');
    searchRow.className = 'tools-search-row';
    searchRow.style.cssText = 'display: flex; gap: 6px; margin-bottom: 8px;';

    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.className = 'tools-search-input';
    searchInput.placeholder = 'Search tools or ask Clippy for help...';
    searchInput.id = 'tools-search-input';
    searchInput.style.cssText = 'flex: 1; padding: 6px; border: 1px solid var(--button-shadow); box-shadow: inset -1px -1px 0 var(--button-highlight);';

    // Enter key triggers Clippy AI search
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && window.clippy) {
            window.clippy.searchToolsForUser(e.target.value);
        }
    });

    searchRow.appendChild(searchInput);

    const clippyAssistBtn = document.createElement('button');
    clippyAssistBtn.className = 'btn';
    clippyAssistBtn.innerHTML = '📎 Ask Clippy';
    clippyAssistBtn.title = 'Let Clippy help you find the perfect tool';
    clippyAssistBtn.onclick = () => {
        const query = searchInput.value || 'general productivity tools';
        if (window.clippy) {
            window.clippy.searchToolsForUser(query);
        }
    };
    searchRow.appendChild(clippyAssistBtn);

    header.appendChild(searchRow);

    // Filter row
    const filterRow = document.createElement('div');
    filterRow.style.cssText = 'display: flex; gap: 6px; margin-bottom: 8px; flex-wrap: wrap;';

    const categorySelect = document.createElement('select');
    categorySelect.className = 'tools-category-select';
    categorySelect.id = 'tools-category-select';
    categorySelect.style.cssText = 'padding: 4px; border: 1px solid var(--button-shadow); background: white; flex: 1; min-width: 150px;';
    categorySelect.innerHTML = '<option value="">All Categories</option>';
    filterRow.appendChild(categorySelect);

    const complexitySelect = document.createElement('select');
    complexitySelect.id = 'tools-complexity-select';
    complexitySelect.style.cssText = 'padding: 4px; border: 1px solid var(--button-shadow); background: white; flex: 1; min-width: 120px;';
    complexitySelect.innerHTML = `
        <option value="">Any Level</option>
        <option value="simple">Simple</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
    `;
    complexitySelect.addEventListener('change', (e) => {
        if (this.toolsBrowserState) {
            this.toolsBrowserState.currentComplexity = e.target.value;
            this.filterAndDisplayTools();
        }
    });
    filterRow.appendChild(complexitySelect);

    const recommendBtn = document.createElement('button');
    recommendBtn.className = 'btn';
    recommendBtn.innerHTML = '✨ Recommend';
    recommendBtn.title = 'Get AI-powered recommendations';
    recommendBtn.onclick = () => {
        if (window.clippy) {
            window.clippy.recommendToolsForUser();
        }
    };
    filterRow.appendChild(recommendBtn);

    const randomBtn = document.createElement('button');
    randomBtn.className = 'btn';
    randomBtn.innerHTML = '🎲 Random';
    randomBtn.title = 'Show me something random!';
    randomBtn.onclick = () => {
        if (window.clippy) {
            window.clippy.showRandomTool();
        }
    };
    filterRow.appendChild(randomBtn);

    header.appendChild(filterRow);

    // Results counter and stats
    const statsRow = document.createElement('div');
    statsRow.style.cssText = 'display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: var(--text-color);';

    const resultsCounter = document.createElement('div');
    resultsCounter.id = 'tools-results-counter';
    resultsCounter.textContent = 'Loading tools...';
    statsRow.appendChild(resultsCounter);

    const quickStats = document.createElement('div');
    quickStats.id = 'tools-quick-stats';
    quickStats.style.cssText = 'display: flex; gap: 12px;';
    statsRow.appendChild(quickStats);

    header.appendChild(statsRow);
    content.appendChild(header);

    // Create tools grid container with scroll
    const scrollContainer = document.createElement('div');
    scrollContainer.style.cssText = 'flex: 1; overflow-y: auto; padding: 12px; background: white;';

    const toolsGrid = document.createElement('div');
    toolsGrid.className = 'tools-grid';
    toolsGrid.id = 'tools-grid';
    toolsGrid.style.cssText = 'display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 12px;';

    // Show loading state with Clippy message
    toolsGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 40px;">
            <div class="tools-loading-spinner" style="margin: 0 auto 12px;"></div>
            <div style="font-size: 14px;">📎 Clippy is discovering your tools...</div>
            <div style="font-size: 11px; color: #808080; margin-top: 8px;">Loading from local gallery</div>
        </div>
    `;

    scrollContainer.appendChild(toolsGrid);
    content.appendChild(scrollContainer);

    // Create status bar
    const statusBar = document.createElement('div');
    statusBar.className = 'tools-status-bar';
    statusBar.id = 'tools-status-bar';
    statusBar.style.cssText = 'padding: 6px 12px; border-top: 1px solid var(--button-shadow); background: var(--button-face); font-size: 10px;';
    statusBar.textContent = '📎 Clippy is ready to help you discover tools!';
    content.appendChild(statusBar);

    this.windowManager.createWindow('LocalFirst Tools Gallery', content, { width: 900, height: 650 });

    // Fetch and display tools
    this.fetchAndDisplayTools();

    // Start Clippy tour after 2 seconds
    setTimeout(() => {
        if (window.clippy) {
            window.clippy.startToolDiscoveryTour();
        }
    }, 2000);
}
```

### 4. **Update fetchAndDisplayTools() Method**

Replace lines 7982-8081 to load from LOCAL vibe_gallery_config.json:

```javascript
async fetchAndDisplayTools() {
    // CHANGED: Load from local file instead of GitHub
    const CONFIG_URL = './vibe_gallery_config.json';
    const BASE_URL = './'; // Tools are in same directory

    const toolsGrid = document.getElementById('tools-grid');
    const statusBar = document.getElementById('tools-status-bar');
    const resultsCounter = document.getElementById('tools-results-counter');
    const categorySelect = document.getElementById('tools-category-select');
    const searchInput = document.getElementById('tools-search-input');
    const quickStats = document.getElementById('tools-quick-stats');

    if (!toolsGrid || !statusBar) return;

    try {
        statusBar.textContent = '📂 Loading from local gallery...';

        const response = await fetch(CONFIG_URL);
        if (!response.ok) {
            throw new Error(`Failed to load: ${response.status}`);
        }

        const config = await response.json();

        // Extract all tools from vibeGallery structure
        const allTools = [];
        const categories = new Map();

        if (config.vibeGallery && config.vibeGallery.categories) {
            for (const [categoryKey, categoryData] of Object.entries(config.vibeGallery.categories)) {
                categories.set(categoryKey, categoryData);

                if (categoryData.apps && Array.isArray(categoryData.apps)) {
                    categoryData.apps.forEach(app => {
                        allTools.push({
                            ...app,
                            category: categoryKey,
                            categoryName: categoryData.title,
                            categoryColor: categoryData.color,
                            description: app.description || categoryData.description || ''
                        });
                    });
                }
            }
        }

        // Store for filtering
        this.toolsBrowserState = {
            allTools: allTools,
            categories: categories,
            baseUrl: BASE_URL,
            currentSearch: '',
            currentCategory: '',
            currentComplexity: ''
        };

        // Populate category dropdown
        const sortedCategories = Array.from(categories.entries()).sort((a, b) =>
            a[1].title.localeCompare(b[1].title)
        );

        sortedCategories.forEach(([key, data]) => {
            const option = document.createElement('option');
            option.value = key;
            option.textContent = `${data.emoji || ''} ${data.title}`.trim();
            categorySelect.appendChild(option);
        });

        // Set up search with debounce
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.toolsBrowserState.currentSearch = e.target.value.toLowerCase();
                this.filterAndDisplayTools();
            }, 250);
        });

        // Set up category filter
        categorySelect.addEventListener('change', (e) => {
            this.toolsBrowserState.currentCategory = e.target.value;
            this.filterAndDisplayTools();

            // Let Clippy explain the category
            if (e.target.value && window.clippy) {
                window.clippy.explainCategory(e.target.value);
            }
        });

        // Update quick stats
        if (quickStats) {
            quickStats.innerHTML = `
                <span>📊 ${allTools.length} tools</span>
                <span>📁 ${categories.size} categories</span>
                <span>📎 AI ready</span>
            `;
        }

        // Initial display
        this.filterAndDisplayTools();

        statusBar.textContent = `✅ Loaded ${allTools.length} tools • Ask Clippy for help!`;

    } catch (error) {
        console.error('Failed to fetch tools:', error);
        toolsGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 40px;">
                <div style="font-size: 48px; margin-bottom: 12px;">⚠️</div>
                <div style="font-weight: bold; margin-bottom: 8px; font-size: 14px;">Failed to Load Tools</div>
                <div style="margin-bottom: 12px; font-size: 11px; color: #808080;">${error.message}</div>
                <div style="margin-bottom: 12px; font-size: 11px;">Make sure vibe_gallery_config.json exists!</div>
                <button class="btn" onclick="emulator.fetchAndDisplayTools()">
                    🔄 Retry
                </button>
            </div>
        `;
        statusBar.textContent = '❌ Error: Could not load gallery config';
        if (resultsCounter) {
            resultsCounter.textContent = 'Failed to load';
        }
    }
}
```

### 5. **Enhanced filterAndDisplayTools()**

Update to support complexity filter:

```javascript
filterAndDisplayTools() {
    const state = this.toolsBrowserState;
    if (!state) return;

    const toolsGrid = document.getElementById('tools-grid');
    const resultsCounter = document.getElementById('tools-results-counter');
    if (!toolsGrid) return;

    // Filter tools
    let filteredTools = state.allTools;

    // Apply category filter
    if (state.currentCategory) {
        filteredTools = filteredTools.filter(tool => tool.category === state.currentCategory);
    }

    // Apply complexity filter
    if (state.currentComplexity) {
        filteredTools = filteredTools.filter(tool => tool.complexity === state.currentComplexity);
    }

    // Apply search filter
    if (state.currentSearch) {
        filteredTools = filteredTools.filter(tool => {
            const searchStr = state.currentSearch;
            return (
                (tool.title || '').toLowerCase().includes(searchStr) ||
                (tool.description || '').toLowerCase().includes(searchStr) ||
                (tool.path || '').toLowerCase().includes(searchStr) ||
                (tool.tags || []).some(tag => tag.toLowerCase().includes(searchStr))
            );
        });
    }

    // Update counter
    if (resultsCounter) {
        const totalTools = state.allTools.length;
        resultsCounter.innerHTML = `
            Showing <strong>${filteredTools.length}</strong> of ${totalTools} tools
            ${state.currentSearch ? `(matching "${state.currentSearch}")` : ''}
        `;
    }

    // Display tools
    if (filteredTools.length === 0) {
        toolsGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 40px;">
                <div style="font-size: 48px; margin-bottom: 12px;">📭</div>
                <div style="font-weight: bold; margin-bottom: 8px;">No Tools Found</div>
                <div style="font-size: 11px; color: #808080;">Try adjusting your search or ask Clippy for help!</div>
                <button class="btn" style="margin-top: 12px;" onclick="if(window.clippy) window.clippy.recommendToolsForUser()">
                    📎 Ask Clippy for Suggestions
                </button>
            </div>
        `;
        return;
    }

    toolsGrid.innerHTML = '';

    filteredTools.forEach(tool => {
        const card = this.createToolCard(tool);
        toolsGrid.appendChild(card);
    });
}
```

## Usage Examples

Once integrated, users can:

1. **Natural Language Search**:
   - Type "drawing tools" and press Enter
   - Clippy uses AI to find the best matches

2. **Get Recommendations**:
   - Click "Recommend" button
   - Clippy analyzes needs and suggests tools

3. **Category Guidance**:
   - Select a category
   - Clippy explains what's in it

4. **Random Discovery**:
   - Click "Random" button
   - Clippy shows a surprise tool

5. **Voice Queries** (if implemented):
   - "Clippy, find me a game"
   - "Show me creative tools"

## Testing Checklist

- [ ] LocalFirst Tools opens successfully
- [ ] Tools load from local vibe_gallery_config.json
- [ ] Search works with keywords
- [ ] Category filter works
- [ ] Complexity filter works
- [ ] Clippy can search for tools
- [ ] Clippy can recommend tools
- [ ] Clippy explains categories
- [ ] Random tool button works
- [ ] Tools open in windows successfully

## Benefits

✅ **AI-Powered Discovery**: Clippy understands user intent
✅ **Natural Language**: Users can describe what they need
✅ **Intelligent Filtering**: AI suggests best filters
✅ **Guided Experience**: Clippy tours and explains
✅ **Local-First**: All tools load locally, AI optional
✅ **Privacy**: Everything stays in the browser

---

*This integration makes Clippy a true assistant for tool discovery, not just a passive helper!*
