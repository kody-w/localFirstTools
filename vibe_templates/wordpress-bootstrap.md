# WordPress Directory Website Bootstrap Guide for AI Agents

This guide helps AI agents bootstrap complete WordPress directory websites with comprehensive research, SEO optimization, and zero 404 errors.

## ⚠️ CRITICAL REQUIREMENTS

**Every WordPress directory website MUST include:**
1. ✅ Complete research phase with exhaustive data collection
2. ✅ Full WordPress theme development with multiple templates
3. ✅ All directory entries created from JSON data
4. ✅ All taxonomy pages working (categories, locations, combinations)
5. ✅ **Playwright verification with ZERO 404 errors**
6. ✅ Review system (not comments) for directory entries
7. ✅ Complete SEO optimization for all pages
8. ✅ Docker development environment
9. ✅ Migration script for Digital Ocean deployment

## 🚨 MANDATORY: Complete One-Shot Execution

**DO NOT STOP PARTWAY. The website must be FULLY FUNCTIONAL at http://localhost before reporting back.**

## Quick Start Checklist

```markdown
☐ 1. Deep research phase - scrape ALL data for EVERY entry
☐ 2. Create comprehensive JSON datasets with rich information
☐ 3. Setup Docker WordPress environment
☐ 4. Develop custom theme with 5-7 template variations
☐ 5. Import all directory data and create pages
☐ 6. Build all taxonomy archive pages with SEO content
☐ 7. Create mega navigation with all categories/locations
☐ 8. Implement custom review system (not comments)
☐ 9. VERIFY EVERY LINK with Playwright - ZERO 404s required
☐ 10. Fix all broken links found
☐ 11. Prepare for deployment
```

## Step 1: Gather Project Information

Required information:
- **Directory type**: What are we listing? (e.g., "SaaS tools", "restaurants", "therapists")
- **Target locations**: Geographic scope (e.g., "New York", "nationwide", "global")
- **Categories/Types**: Main taxonomies (e.g., "CRM, Marketing, Analytics" or "Italian, Chinese, Mexican")
- **Number of entries**: How many items to include (minimum 20-30 for viable directory)
- **Domain name**: For branding and SEO optimization

## Step 2: Deep Research Phase (MANDATORY - DO NOT SKIP)

### Research Each Individual Entry Exhaustively

**For each directory entry, use Jina AI to gather:**

```bash
# Search for comprehensive information
curl "https://s.jina.ai/?q=COMPANY_NAME+reviews+pricing+features" \
  -H "Authorization: Bearer $JINA_API_KEY"

# Scrape the company's website
curl "https://r.jina.ai/https://company-website.com" \
  -H "Authorization: Bearer $JINA_API_KEY"

# Scrape pricing page specifically
curl "https://r.jina.ai/https://company-website.com/pricing" \
  -H "Authorization: Bearer $JINA_API_KEY"

# Find reviews and comparisons
curl "https://s.jina.ai/?q=COMPANY_NAME+vs+alternatives+comparison" \
  -H "Authorization: Bearer $JINA_API_KEY"
```

### Create Comprehensive JSON Data Structure

For EACH directory entry, create a JSON file with this structure:

```json
{
  "id": "unique-slug",
  "basics": {
    "name": "Company Name",
    "tagline": "Their main value proposition",
    "description": "500+ word comprehensive description covering what they do, who they serve, their unique approach, company history, mission, and why they matter in the industry",
    "founded": "2015",
    "headquarters": "San Francisco, CA",
    "employees": "50-100",
    "funding": "$10M Series A",
    "website": "https://example.com",
    "logo": "url-from-unsplash-or-actual"
  },
  "detailed_features": [
    {
      "name": "Advanced Analytics Dashboard",
      "description": "100+ word description of this specific feature, how it works, what problems it solves, and why it's valuable",
      "category": "Analytics",
      "importance": "critical"
    }
    // 10-20 features minimum
  ],
  "pricing": {
    "model": "subscription",
    "free_tier": true,
    "free_tier_details": "14-day trial with full features",
    "starter_price": "$29/month",
    "currency": "USD",
    "billing_options": ["monthly", "annual"],
    "tiers": [
      {
        "name": "Starter",
        "price": "$29/month",
        "annual_price": "$290/year",
        "features": [
          "Up to 1,000 contacts",
          "5 user accounts",
          "Email support",
          // 20+ features per tier
        ],
        "limits": {
          "users": 5,
          "contacts": 1000,
          "storage": "10GB"
        },
        "best_for": "Small teams just getting started"
      }
      // All pricing tiers
    ],
    "enterprise": {
      "available": true,
      "contact_sales": true,
      "minimum_seats": 50
    }
  },
  "use_cases": [
    {
      "title": "Sales Team Productivity",
      "description": "200+ word description of how sales teams use this tool, specific workflows, results they achieve, and real examples",
      "industry": "B2B Sales",
      "company_size": "10-50 employees",
      "roi": "3x increase in close rate"
    }
    // 5-10 use cases
  ],
  "pros_cons": {
    "pros": [
      {
        "title": "Intuitive Interface",
        "explanation": "50+ word explanation of why this is a strength, with specific examples"
      }
      // 5-7 pros
    ],
    "cons": [
      {
        "title": "Limited Integrations",
        "explanation": "50+ word explanation of this limitation and who it affects"
      }
      // 3-5 cons
    ]
  },
  "integrations": [
    {
      "name": "Salesforce",
      "type": "CRM",
      "description": "Two-way sync with Salesforce CRM",
      "documentation_url": "https://docs.example.com/salesforce"
    }
    // All integrations
  ],
  "alternatives": [
    {
      "name": "Competitor A",
      "comparison": "100+ word comparison explaining when to choose this vs the alternative",
      "when_to_choose": "Choose Competitor A if you need better mobile support",
      "price_difference": "20% more expensive"
    }
    // 3-5 alternatives
  ],
  "reviews": {
    "average_rating": 4.5,
    "total_reviews": 1847,
    "rating_breakdown": {
      "5": 62,
      "4": 23,
      "3": 10,
      "2": 3,
      "1": 2
    },
    "platforms": {
      "g2": { "rating": 4.6, "reviews": 523 },
      "capterra": { "rating": 4.4, "reviews": 892 },
      "trustpilot": { "rating": 4.3, "reviews": 432 }
    },
    "expert_reviews": [
      {
        "source": "TechCrunch",
        "rating": 4.5,
        "date": "2024-01",
        "summary": "200+ word expert review summary",
        "pros": ["Great UX", "Powerful features"],
        "cons": ["Expensive", "Learning curve"]
      }
    ]
  },
  "technical_specs": {
    "platforms": ["Web", "iOS", "Android"],
    "languages": ["English", "Spanish", "French"],
    "api": {
      "available": true,
      "type": "REST",
      "rate_limits": "1000 requests/hour",
      "documentation": "https://api.example.com/docs"
    },
    "security": {
      "encryption": "256-bit SSL",
      "two_factor": true,
      "sso": true,
      "compliance": ["SOC 2", "GDPR", "HIPAA"]
    }
  },
  "support": {
    "channels": ["email", "chat", "phone", "knowledge_base"],
    "response_time": {
      "email": "24 hours",
      "chat": "5 minutes",
      "phone": "immediate"
    },
    "hours": "24/7 for enterprise, business hours for others",
    "documentation_quality": "excellent",
    "community": {
      "forum": true,
      "slack": true,
      "user_groups": 15
    }
  },
  "media": {
    "logo": "https://unsplash.com/photos/...",
    "screenshots": [
      "dashboard-url",
      "feature1-url",
      "feature2-url"
      // 10+ screenshots
    ],
    "videos": [
      {
        "title": "Product Demo",
        "url": "youtube.com/...",
        "duration": "5:23"
      }
    ],
    "diagrams": ["architecture-diagram-url"]
  },
  "seo": {
    "focus_keywords": ["crm software", "sales automation"],
    "long_tail": ["best crm for small business", "affordable sales automation tool"],
    "meta_title": "CompanyName Review 2024: Features, Pricing & Alternatives",
    "meta_description": "In-depth CompanyName review covering all features, pricing tiers, pros/cons, and alternatives. See why 10,000+ companies choose CompanyName for..."
  },
  "location_specific": {
    // For local businesses only
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "phone": "(555) 123-4567",
    "hours": {
      "monday": "9am-5pm",
      "tuesday": "9am-5pm"
    },
    "service_area": ["Manhattan", "Brooklyn", "Queens"],
    "parking": "Street parking available",
    "accessibility": "Wheelchair accessible"
  }
}
```

### Create Comprehensive Taxonomy Archive Content

For EACH category/type page, create rich content JSON:

```json
{
  "taxonomy": "crm-software",
  "type": "category",
  "content": {
    "title": "Best CRM Software in 2024",
    "meta_title": "Best CRM Software 2024: Top 25 Compared & Reviewed",
    "meta_description": "Compare the best CRM software of 2024. In-depth reviews, pricing analysis, and expert recommendations for businesses of all sizes.",
    "hero_content": "1000+ word comprehensive overview of CRM software...",
    "buyers_guide": "2000+ word guide on choosing CRM software...",
    "key_features": [
      {
        "feature": "Contact Management",
        "importance": "essential",
        "description": "200+ words on this feature..."
      }
    ],
    "pricing_analysis": "500+ words on CRM pricing models...",
    "comparison_methodology": "How we evaluate and compare CRM tools...",
    "faqs": [
      {
        "question": "What is CRM software?",
        "answer": "Comprehensive 200+ word answer..."
      }
      // 20-30 FAQs
    ],
    "statistics": {
      "market_size": "$58.5 billion",
      "growth_rate": "12.5% annually",
      "adoption_rate": "74% of businesses"
    },
    "glossary": [
      {
        "term": "Lead Scoring",
        "definition": "The process of..."
      }
    ]
  }
}
```

## Step 3: Setup WordPress Docker Environment

```bash
# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  wordpress:
    image: wordpress:latest
    container_name: wp-dev
    ports:
      - "80:80"
    environment:
      WORDPRESS_DB_HOST: mysql:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress_password
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - ./wp-content:/var/www/html/wp-content
      - ./wp-config.php:/var/www/html/wp-config.php
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    container_name: wp-mysql
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress_password
      MYSQL_ROOT_PASSWORD: root_password
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
EOF

# Start Docker
docker-compose up -d
```

## Step 4: Create Custom WordPress Theme

### Create Theme Structure

```bash
mkdir -p wp-content/themes/directory-theme/{css,js,templates,inc,parts}
```

### functions.php - Theme Setup

```php
<?php
// Theme setup
function directory_theme_setup() {
    // Theme supports
    add_theme_support('post-thumbnails');
    add_theme_support('menus');
    add_theme_support('title-tag');
    add_theme_support('custom-logo');
    
    // Image sizes for directory
    add_image_size('directory-thumb', 400, 300, true);
    add_image_size('directory-hero', 1920, 600, true);
    add_image_size('company-logo', 200, 100, false);
    
    // Register menus
    register_nav_menus(array(
        'primary' => 'Primary Menu',
        'footer' => 'Footer Menu',
        'categories' => 'Categories Menu',
        'locations' => 'Locations Menu'
    ));
}
add_action('after_setup_theme', 'directory_theme_setup');

// Register Custom Post Type for Directory
function register_directory_post_type() {
    register_post_type('directory', array(
        'labels' => array(
            'name' => 'Directory Entries',
            'singular_name' => 'Directory Entry'
        ),
        'public' => true,
        'has_archive' => true,
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
        'menu_icon' => 'dashicons-building',
        'show_in_rest' => true,
        'rewrite' => array('slug' => 'companies')
    ));
}
add_action('init', 'register_directory_post_type');

// Register Taxonomies
function register_directory_taxonomies() {
    // Categories (e.g., CRM, Marketing, Analytics)
    register_taxonomy('directory_category', 'directory', array(
        'labels' => array(
            'name' => 'Categories',
            'singular_name' => 'Category'
        ),
        'hierarchical' => true,
        'public' => true,
        'show_in_rest' => true,
        'rewrite' => array('slug' => 'categories')
    ));
    
    // Locations
    register_taxonomy('directory_location', 'directory', array(
        'labels' => array(
            'name' => 'Locations',
            'singular_name' => 'Location'
        ),
        'hierarchical' => true,
        'public' => true,
        'show_in_rest' => true,
        'rewrite' => array('slug' => 'locations')
    ));
    
    // Tags
    register_taxonomy('directory_tag', 'directory', array(
        'labels' => array(
            'name' => 'Tags',
            'singular_name' => 'Tag'
        ),
        'hierarchical' => false,
        'public' => true,
        'show_in_rest' => true,
        'rewrite' => array('slug' => 'tags')
    ));
}
add_action('init', 'register_directory_taxonomies');

// Custom Review System (NOT comments)
function register_review_post_type() {
    register_post_type('directory_review', array(
        'labels' => array(
            'name' => 'Reviews',
            'singular_name' => 'Review'
        ),
        'public' => false,
        'show_ui' => true,
        'supports' => array('title', 'editor', 'author'),
        'menu_icon' => 'dashicons-star-filled'
    ));
}
add_action('init', 'register_review_post_type');
```

### style.css - Comprehensive Styles

```css
/*
Theme Name: Directory Theme
Description: Professional directory website theme
Version: 1.0
*/

/* Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    /* Color System */
    --primary: #2563eb;
    --primary-dark: #1e40af;
    --secondary: #10b981;
    --accent: #f59e0b;
    --text-primary: #1f2937;
    --text-secondary: #6b7280;
    --bg-primary: #ffffff;
    --bg-secondary: #f3f4f6;
    --border: #e5e7eb;
    
    /* Spacing Scale */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;
    --space-2xl: 3rem;
    --space-3xl: 4rem;
    
    /* Typography Scale */
    --text-xs: 0.75rem;
    --text-sm: 0.875rem;
    --text-base: 1rem;
    --text-lg: 1.125rem;
    --text-xl: 1.25rem;
    --text-2xl: 1.5rem;
    --text-3xl: 1.875rem;
    --text-4xl: 2.25rem;
    --text-5xl: 3rem;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
    
    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-base: 250ms ease;
    --transition-slow: 350ms ease;
    
    /* Border Radius */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 1rem;
    --radius-full: 9999px;
}

/* Typography */
body {
    font-family: system-ui, -apple-system, sans-serif;
    font-size: var(--text-base);
    line-height: 1.6;
    color: var(--text-primary);
    background: var(--bg-primary);
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: var(--space-md);
}

h1 { font-size: var(--text-4xl); }
h2 { font-size: var(--text-3xl); }
h3 { font-size: var(--text-2xl); }
h4 { font-size: var(--text-xl); }
h5 { font-size: var(--text-lg); }
h6 { font-size: var(--text-base); }

/* Container */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--space-lg);
}

/* Header with Mega Menu */
.site-header {
    background: var(--bg-primary);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: var(--shadow-sm);
}

.header-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-md) 0;
}

.site-logo {
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--primary);
    text-decoration: none;
    transition: color var(--transition-base);
}

.site-logo:hover {
    color: var(--primary-dark);
}

/* Navigation Menu */
.primary-nav ul {
    display: flex;
    list-style: none;
    gap: var(--space-xl);
}

.primary-nav a {
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    padding: var(--space-sm) 0;
    position: relative;
    transition: color var(--transition-base);
}

.primary-nav a::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--primary);
    transition: width var(--transition-base);
}

.primary-nav a:hover {
    color: var(--primary);
}

.primary-nav a:hover::after {
    width: 100%;
}

/* Mega Menu Dropdown */
.has-mega-menu {
    position: relative;
}

.mega-menu {
    position: absolute;
    top: 100%;
    left: -100px;
    width: 800px;
    background: var(--bg-primary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-xl);
    padding: var(--space-xl);
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all var(--transition-base);
}

.has-mega-menu:hover .mega-menu {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

.mega-menu-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-xl);
}

.mega-menu-column h4 {
    color: var(--primary);
    margin-bottom: var(--space-md);
    font-size: var(--text-sm);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.mega-menu-column ul {
    list-style: none;
}

.mega-menu-column a {
    display: block;
    padding: var(--space-xs) 0;
    color: var(--text-secondary);
    transition: color var(--transition-fast);
}

.mega-menu-column a:hover {
    color: var(--primary);
}

/* Directory Grid Layouts */

/* Layout 1: Card Grid */
.directory-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: var(--space-xl);
    margin: var(--space-2xl) 0;
}

.directory-card {
    background: var(--bg-primary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: all var(--transition-base);
    position: relative;
}

.directory-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary);
}

.directory-card-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.directory-card-content {
    padding: var(--space-lg);
}

.directory-card-title {
    font-size: var(--text-xl);
    margin-bottom: var(--space-sm);
    color: var(--text-primary);
}

.directory-card-meta {
    display: flex;
    gap: var(--space-md);
    margin-bottom: var(--space-md);
    font-size: var(--text-sm);
    color: var(--text-secondary);
}

.directory-card-rating {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
}

.star-rating {
    color: var(--accent);
}

.directory-card-description {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: var(--space-md);
}

.directory-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: var(--space-md);
    border-top: 1px solid var(--border);
}

.directory-card-price {
    font-size: var(--text-lg);
    font-weight: 700;
    color: var(--primary);
}

.directory-card-cta {
    background: var(--primary);
    color: white;
    padding: var(--space-sm) var(--space-lg);
    border-radius: var(--radius-md);
    text-decoration: none;
    transition: background var(--transition-base);
}

.directory-card-cta:hover {
    background: var(--primary-dark);
}

/* Layout 2: List View */
.directory-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-lg);
}

.directory-list-item {
    display: flex;
    gap: var(--space-xl);
    padding: var(--space-xl);
    background: var(--bg-primary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    transition: all var(--transition-base);
}

.directory-list-item:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--primary);
}

.directory-list-image {
    width: 200px;
    height: 150px;
    object-fit: cover;
    border-radius: var(--radius-md);
    flex-shrink: 0;
}

.directory-list-content {
    flex: 1;
}

.directory-list-header {
    display: flex;
    justify-content: space-between;
    align-items: start;
    margin-bottom: var(--space-md);
}

.directory-list-title {
    font-size: var(--text-2xl);
    color: var(--text-primary);
}

.directory-list-badges {
    display: flex;
    gap: var(--space-sm);
}

.badge {
    padding: var(--space-xs) var(--space-sm);
    background: var(--bg-secondary);
    border-radius: var(--radius-full);
    font-size: var(--text-xs);
    font-weight: 600;
    text-transform: uppercase;
}

.badge.featured {
    background: var(--accent);
    color: white;
}

.badge.verified {
    background: var(--secondary);
    color: white;
}

/* Layout 3: Comparison Table */
.comparison-table {
    width: 100%;
    background: var(--bg-primary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.comparison-table thead {
    background: var(--bg-secondary);
}

.comparison-table th {
    padding: var(--space-md);
    text-align: left;
    font-weight: 600;
    color: var(--text-primary);
    border-bottom: 2px solid var(--border);
}

.comparison-table td {
    padding: var(--space-md);
    border-bottom: 1px solid var(--border);
}

.comparison-table tbody tr:hover {
    background: var(--bg-secondary);
}

.comparison-table .feature-check {
    color: var(--secondary);
    font-size: var(--text-xl);
}

.comparison-table .feature-cross {
    color: #ef4444;
    font-size: var(--text-xl);
}

/* Layout 4: Masonry Grid */
.directory-masonry {
    column-count: 3;
    column-gap: var(--space-xl);
}

.masonry-item {
    break-inside: avoid;
    margin-bottom: var(--space-xl);
    background: var(--bg-primary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: all var(--transition-base);
}

.masonry-item:hover {
    transform: scale(1.02);
    box-shadow: var(--shadow-lg);
}

/* Layout 5: Map View Container */
.directory-map-view {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: var(--space-xl);
    height: 600px;
}

.map-sidebar {
    overflow-y: auto;
    padding: var(--space-lg);
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
}

.map-container {
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
    position: relative;
}

/* Single Directory Entry Page */
.directory-single {
    margin: var(--space-3xl) 0;
}

.directory-hero {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: var(--space-2xl);
    margin-bottom: var(--space-3xl);
}

.directory-hero-image {
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.directory-hero-content h1 {
    font-size: var(--text-5xl);
    margin-bottom: var(--space-lg);
}

.directory-meta-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-lg);
    margin: var(--space-xl) 0;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.meta-icon {
    width: 24px;
    height: 24px;
    color: var(--primary);
}

/* Tabs Component */
.tabs {
    margin: var(--space-2xl) 0;
}

.tab-list {
    display: flex;
    border-bottom: 2px solid var(--border);
    margin-bottom: var(--space-xl);
}

.tab-button {
    padding: var(--space-md) var(--space-xl);
    background: none;
    border: none;
    font-size: var(--text-lg);
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    position: relative;
    transition: color var(--transition-base);
}

.tab-button:hover {
    color: var(--text-primary);
}

.tab-button.active {
    color: var(--primary);
}

.tab-button.active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--primary);
}

.tab-content {
    padding: var(--space-xl);
}

/* Review System Styles */
.review-section {
    margin: var(--space-3xl) 0;
}

.review-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-xl);
}

.review-summary {
    display: flex;
    align-items: center;
    gap: var(--space-xl);
}

.review-average {
    font-size: var(--text-5xl);
    font-weight: 700;
    color: var(--text-primary);
}

.review-stars {
    display: flex;
    gap: var(--space-xs);
}

.review-count {
    color: var(--text-secondary);
}

.write-review-btn {
    background: var(--primary);
    color: white;
    padding: var(--space-md) var(--space-xl);
    border-radius: var(--radius-md);
    border: none;
    font-size: var(--text-base);
    font-weight: 600;
    cursor: pointer;
    transition: background var(--transition-base);
}

.write-review-btn:hover {
    background: var(--primary-dark);
}

/* Review Form */
.review-form {
    background: var(--bg-secondary);
    padding: var(--space-2xl);
    border-radius: var(--radius-lg);
    margin-bottom: var(--space-2xl);
}

.review-form-group {
    margin-bottom: var(--space-xl);
}

.review-form label {
    display: block;
    font-weight: 600;
    margin-bottom: var(--space-sm);
}

.review-form input,
.review-form textarea,
.review-form select {
    width: 100%;
    padding: var(--space-md);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    font-size: var(--text-base);
    transition: border-color var(--transition-base);
}

.review-form input:focus,
.review-form textarea:focus,
.review-form select:focus {
    outline: none;
    border-color: var(--primary);
}

.star-rating-input {
    display: flex;
    gap: var(--space-sm);
    font-size: var(--text-2xl);
}

.star-rating-input button {
    background: none;
    border: none;
    color: #d1d5db;
    cursor: pointer;
    transition: color var(--transition-fast);
}

.star-rating-input button:hover,
.star-rating-input button.active {
    color: var(--accent);
}

/* Individual Reviews */
.reviews-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-xl);
}

.review-item {
    padding: var(--space-xl);
    background: var(--bg-primary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
}

.review-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--space-md);
}

.review-author {
    display: flex;
    align-items: center;
    gap: var(--space-md);
}

.review-avatar {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-full);
    background: var(--bg-secondary);
}

.review-author-name {
    font-weight: 600;
}

.review-date {
    color: var(--text-secondary);
    font-size: var(--text-sm);
}

.review-rating {
    display: flex;
    gap: var(--space-xs);
    color: var(--accent);
}

.review-content {
    line-height: 1.8;
    color: var(--text-primary);
    margin-bottom: var(--space-md);
}

.review-helpful {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding-top: var(--space-md);
    border-top: 1px solid var(--border);
}

.review-helpful button {
    background: none;
    border: 1px solid var(--border);
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-base);
}

.review-helpful button:hover {
    background: var(--bg-secondary);
    border-color: var(--primary);
}

/* Filters and Sorting */
.filters-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-lg);
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
    margin-bottom: var(--space-2xl);
}

.filter-group {
    display: flex;
    gap: var(--space-md);
}

.filter-select {
    padding: var(--space-sm) var(--space-md);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    background: var(--bg-primary);
    cursor: pointer;
}

.filter-tag {
    padding: var(--space-sm) var(--space-md);
    background: var(--bg-primary);
    border: 1px solid var(--border);
    border-radius: var(--radius-full);
    font-size: var(--text-sm);
    cursor: pointer;
    transition: all var(--transition-base);
}

.filter-tag:hover {
    border-color: var(--primary);
    color: var(--primary);
}

.filter-tag.active {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

/* Pagination */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--space-sm);
    margin: var(--space-3xl) 0;
}

.pagination a,
.pagination span {
    padding: var(--space-sm) var(--space-md);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    text-decoration: none;
    transition: all var(--transition-base);
}

.pagination a:hover {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

.pagination .current {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

/* Footer */
.site-footer {
    background: var(--text-primary);
    color: white;
    padding: var(--space-3xl) 0;
    margin-top: var(--space-3xl);
}

.footer-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: var(--space-2xl);
    margin-bottom: var(--space-2xl);
}

.footer-column h3 {
    color: white;
    margin-bottom: var(--space-lg);
}

.footer-column ul {
    list-style: none;
}

.footer-column a {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    display: block;
    padding: var(--space-xs) 0;
    transition: color var(--transition-base);
}

.footer-column a:hover {
    color: white;
}

.footer-bottom {
    padding-top: var(--space-xl);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Responsive Design */
@media (max-width: 1024px) {
    .directory-grid {
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    }
    
    .directory-masonry {
        column-count: 2;
    }
    
    .mega-menu {
        width: 600px;
    }
    
    .mega-menu-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .primary-nav {
        display: none;
    }
    
    .mobile-menu-toggle {
        display: block;
    }
    
    .directory-grid {
        grid-template-columns: 1fr;
    }
    
    .directory-masonry {
        column-count: 1;
    }
    
    .directory-hero {
        grid-template-columns: 1fr;
    }
    
    .directory-map-view {
        grid-template-columns: 1fr;
    }
    
    .footer-grid {
        grid-template-columns: 1fr;
        gap: var(--space-xl);
    }
    
    .filters-bar {
        flex-direction: column;
        gap: var(--space-md);
    }
}

@media (max-width: 480px) {
    :root {
        --text-5xl: 2rem;
        --text-4xl: 1.75rem;
        --text-3xl: 1.5rem;
    }
    
    .container {
        padding: 0 var(--space-md);
    }
    
    .directory-list-item {
        flex-direction: column;
    }
    
    .directory-list-image {
        width: 100%;
    }
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn var(--transition-slow) ease-out;
}

@keyframes slideIn {
    from {
        transform: translateX(-100%);
    }
    to {
        transform: translateX(0);
    }
}

.slide-in {
    animation: slideIn var(--transition-slow) ease-out;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

.pulse {
    animation: pulse 2s infinite;
}

/* Loading States */
.skeleton {
    background: linear-gradient(90deg, var(--bg-secondary) 25%, var(--border) 50%, var(--bg-secondary) 75%);
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}

/* Accessibility */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* Focus Styles */
*:focus-visible {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}

/* Print Styles */
@media print {
    .site-header,
    .site-footer,
    .filters-bar,
    .pagination,
    .write-review-btn {
        display: none;
    }
    
    body {
        font-size: 12pt;
        line-height: 1.5;
        color: black;
    }
    
    a {
        color: black;
        text-decoration: underline;
    }
}
```

## Step 5: Create Multiple Page Templates

### Template 1: archive-directory.php (Main Directory Grid)

```php
<?php get_header(); ?>

<main class="site-main">
    <div class="container">
        <div class="page-header">
            <h1>Browse All Companies</h1>
            <p>Discover the best solutions for your business</p>
        </div>
        
        <!-- Filters Bar -->
        <div class="filters-bar">
            <div class="filter-group">
                <select class="filter-select" id="category-filter">
                    <option value="">All Categories</option>
                    <?php
                    $categories = get_terms('directory_category');
                    foreach ($categories as $category) {
                        echo '<option value="' . $category->slug . '">' . $category->name . '</option>';
                    }
                    ?>
                </select>
                
                <select class="filter-select" id="location-filter">
                    <option value="">All Locations</option>
                    <?php
                    $locations = get_terms('directory_location');
                    foreach ($locations as $location) {
                        echo '<option value="' . $location->slug . '">' . $location->name . '</option>';
                    }
                    ?>
                </select>
                
                <select class="filter-select" id="sort-filter">
                    <option value="newest">Newest First</option>
                    <option value="rating">Highest Rated</option>
                    <option value="popular">Most Popular</option>
                    <option value="price-low">Price: Low to High</option>
                    <option value="price-high">Price: High to Low</option>
                </select>
            </div>
            
            <div class="results-count">
                <?php echo $wp_query->found_posts; ?> companies found
            </div>
        </div>
        
        <!-- Directory Grid -->
        <div class="directory-grid">
            <?php
            if (have_posts()) :
                while (have_posts()) : the_post();
                    get_template_part('parts/directory-card');
                endwhile;
            endif;
            ?>
        </div>
        
        <!-- Pagination -->
        <div class="pagination">
            <?php
            echo paginate_links(array(
                'prev_text' => '← Previous',
                'next_text' => 'Next →'
            ));
            ?>
        </div>
    </div>
</main>

<?php get_footer(); ?>
```

### Template 2: taxonomy-directory_category.php (Category Archive)

```php
<?php get_header(); ?>

<main class="site-main">
    <div class="container">
        <?php
        $term = get_queried_object();
        $term_meta = get_term_meta($term->term_id);
        ?>
        
        <div class="taxonomy-hero">
            <h1>Best <?php echo $term->name; ?> Software in 2024</h1>
            <div class="taxonomy-description">
                <?php echo term_description(); ?>
            </div>
        </div>
        
        <!-- Buyer's Guide Section -->
        <section class="buyers-guide">
            <h2>Complete <?php echo $term->name; ?> Buyer's Guide</h2>
            <div class="guide-content">
                <!-- This would be populated from term meta or custom fields -->
                <p>Comprehensive guide content about choosing <?php echo $term->name; ?>...</p>
            </div>
        </section>
        
        <!-- Top 10 Comparison Table -->
        <section class="top-comparison">
            <h2>Top 10 <?php echo $term->name; ?> Compared</h2>
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Company</th>
                        <th>Rating</th>
                        <th>Starting Price</th>
                        <th>Free Trial</th>
                        <th>Key Features</th>
                        <th>Best For</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    $top_query = new WP_Query(array(
                        'post_type' => 'directory',
                        'posts_per_page' => 10,
                        'tax_query' => array(
                            array(
                                'taxonomy' => 'directory_category',
                                'field' => 'term_id',
                                'terms' => $term->term_id
                            )
                        ),
                        'meta_key' => 'rating',
                        'orderby' => 'meta_value_num',
                        'order' => 'DESC'
                    ));
                    
                    while ($top_query->have_posts()) : $top_query->the_post();
                    ?>
                    <tr>
                        <td>
                            <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                        </td>
                        <td>
                            <div class="star-rating">
                                <?php echo get_post_meta(get_the_ID(), 'rating', true); ?>/5
                            </div>
                        </td>
                        <td><?php echo get_post_meta(get_the_ID(), 'starting_price', true); ?></td>
                        <td><?php echo get_post_meta(get_the_ID(), 'free_trial', true) ? '✓' : '✗'; ?></td>
                        <td><?php echo get_post_meta(get_the_ID(), 'key_features', true); ?></td>
                        <td><?php echo get_post_meta(get_the_ID(), 'best_for', true); ?></td>
                    </tr>
                    <?php
                    endwhile;
                    wp_reset_postdata();
                    ?>
                </tbody>
            </table>
        </section>
        
        <!-- All Entries in Category -->
        <section class="category-entries">
            <h2>All <?php echo $term->name; ?> Companies</h2>
            <div class="directory-grid">
                <?php
                if (have_posts()) :
                    while (have_posts()) : the_post();
                        get_template_part('parts/directory-card');
                    endwhile;
                endif;
                ?>
            </div>
        </section>
        
        <!-- FAQs -->
        <section class="faqs">
            <h2>Frequently Asked Questions about <?php echo $term->name; ?></h2>
            <div class="faq-list">
                <!-- FAQs would be populated from term meta -->
            </div>
        </section>
    </div>
</main>

<?php get_footer(); ?>
```

## Step 6: Import Directory Data from JSON

### Create Import Script

```php
<?php
// wp-content/themes/directory-theme/import-directory.php

function import_directory_from_json() {
    $json_files = glob(get_template_directory() . '/data/*.json');
    
    foreach ($json_files as $file) {
        $data = json_decode(file_get_contents($file), true);
        
        // Check if entry already exists
        $existing = get_page_by_path($data['id'], OBJECT, 'directory');
        if ($existing) {
            $post_id = $existing->ID;
            // Update existing
            wp_update_post(array(
                'ID' => $post_id,
                'post_title' => $data['basics']['name'],
                'post_content' => $data['basics']['description'],
                'post_excerpt' => $data['basics']['tagline']
            ));
        } else {
            // Create new entry
            $post_id = wp_insert_post(array(
                'post_type' => 'directory',
                'post_title' => $data['basics']['name'],
                'post_name' => $data['id'],
                'post_content' => $data['basics']['description'],
                'post_excerpt' => $data['basics']['tagline'],
                'post_status' => 'publish'
            ));
        }
        
        // Update all meta fields
        update_post_meta($post_id, 'company_data', $data);
        update_post_meta($post_id, 'rating', $data['reviews']['average_rating']);
        update_post_meta($post_id, 'starting_price', $data['pricing']['starter_price']);
        update_post_meta($post_id, 'free_trial', $data['pricing']['free_tier']);
        update_post_meta($post_id, 'founded', $data['basics']['founded']);
        update_post_meta($post_id, 'employees', $data['basics']['employees']);
        
        // Set categories
        if (!empty($data['categories'])) {
            wp_set_object_terms($post_id, $data['categories'], 'directory_category');
        }
        
        // Set locations
        if (!empty($data['locations'])) {
            wp_set_object_terms($post_id, $data['locations'], 'directory_location');
        }
        
        // Set tags
        if (!empty($data['tags'])) {
            wp_set_object_terms($post_id, $data['tags'], 'directory_tag');
        }
        
        // Set featured image from URL
        if (!empty($data['media']['logo'])) {
            // Download and attach image
            $image_id = media_sideload_image($data['media']['logo'], $post_id, $data['basics']['name'], 'id');
            if (!is_wp_error($image_id)) {
                set_post_thumbnail($post_id, $image_id);
            }
        }
    }
}

// Run import
add_action('init', function() {
    if (isset($_GET['import_directory']) && current_user_can('manage_options')) {
        import_directory_from_json();
        wp_die('Import complete!');
    }
});
```

## Step 7: Implement Review System

### Create Review Form Handler

```php
// In functions.php
function handle_directory_review_submission() {
    if (!isset($_POST['review_nonce']) || !wp_verify_nonce($_POST['review_nonce'], 'submit_review')) {
        return;
    }
    
    $directory_id = intval($_POST['directory_id']);
    $rating = intval($_POST['rating']);
    $review_title = sanitize_text_field($_POST['review_title']);
    $review_content = sanitize_textarea_field($_POST['review_content']);
    $categories = array(
        'quality' => intval($_POST['rating_quality']),
        'service' => intval($_POST['rating_service']),
        'value' => intval($_POST['rating_value'])
    );
    
    // Create review post
    $review_id = wp_insert_post(array(
        'post_type' => 'directory_review',
        'post_title' => $review_title,
        'post_content' => $review_content,
        'post_status' => 'pending', // Moderate reviews
        'meta_input' => array(
            'directory_id' => $directory_id,
            'overall_rating' => $rating,
            'category_ratings' => $categories,
            'author_name' => sanitize_text_field($_POST['author_name']),
            'author_email' => sanitize_email($_POST['author_email']),
            'would_recommend' => isset($_POST['would_recommend']) ? 'yes' : 'no'
        )
    ));
    
    // Update directory average rating
    update_directory_rating($directory_id);
    
    wp_redirect(get_permalink($directory_id) . '?review=submitted');
    exit;
}
add_action('init', 'handle_directory_review_submission');
```

## Step 8: Playwright Verification (MANDATORY)

### Complete Link Verification Process

```javascript
// Use Playwright MCP to run this verification

// Step 1: Test ALL Header Links
const headerLinks = await page.$$eval('header a[href]', links => 
    links.map(link => ({
        text: link.textContent.trim(),
        href: link.href
    }))
);

console.log(`Found ${headerLinks.length} header links to test`);

for (const link of headerLinks) {
    const response = await page.goto(link.href);
    if (response.status() === 404) {
        console.error(`❌ 404 ERROR: ${link.text} - ${link.href}`);
        // FIX IT NOW - Create the missing page or fix the link
    } else {
        console.log(`✓ OK: ${link.text}`);
    }
}

// Step 2: Test ALL Footer Links
await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
const footerLinks = await page.$$eval('footer a[href]', links => 
    links.map(link => ({
        text: link.textContent.trim(),
        href: link.href
    }))
);

console.log(`Found ${footerLinks.length} footer links to test`);

for (const link of footerLinks) {
    const response = await page.goto(link.href);
    if (response.status() === 404) {
        console.error(`❌ 404 ERROR: ${link.text} - ${link.href}`);
        // FIX IT NOW
    }
}

// Step 3: Test ALL Directory Entries
const directoryLinks = await page.$$eval('a[href*="/companies/"]', links => 
    links.map(link => link.href)
);

console.log(`Found ${directoryLinks.length} directory entries to test`);

for (const link of directoryLinks) {
    const response = await page.goto(link);
    if (response.status() === 404) {
        console.error(`❌ 404 ERROR: Directory entry - ${link}`);
    }
}

// Step 4: Test ALL Category Pages
const categoryLinks = await page.$$eval('a[href*="/categories/"]', links => 
    links.map(link => link.href)
);

console.log(`Found ${categoryLinks.length} category pages to test`);

for (const link of categoryLinks) {
    const response = await page.goto(link);
    if (response.status() === 404) {
        console.error(`❌ 404 ERROR: Category - ${link}`);
    }
}

// Step 5: Test ALL Location Pages
const locationLinks = await page.$$eval('a[href*="/locations/"]', links => 
    links.map(link => link.href)
);

console.log(`Found ${locationLinks.length} location pages to test`);

for (const link of locationLinks) {
    const response = await page.goto(link);
    if (response.status() === 404) {
        console.error(`❌ 404 ERROR: Location - ${link}`);
    }
}

// Final Report
console.log(`
============================
FINAL VERIFICATION REPORT
============================
Header Links Tested: ${headerLinks.length}
Footer Links Tested: ${footerLinks.length}
Directory Entries Tested: ${directoryLinks.length}
Category Pages Tested: ${categoryLinks.length}
Location Pages Tested: ${locationLinks.length}
----------------------------
TOTAL LINKS TESTED: ${headerLinks.length + footerLinks.length + directoryLinks.length + categoryLinks.length + locationLinks.length}
404 ERRORS FOUND: [MUST BE ZERO]
============================
`);
```

## Step 9: Fix Any Issues Found

For EVERY 404 found, you MUST:

1. **Create missing pages**:
```php
// Create About page if missing
wp_insert_post(array(
    'post_type' => 'page',
    'post_title' => 'About Us',
    'post_name' => 'about',
    'post_content' => 'Comprehensive about content...',
    'post_status' => 'publish'
));
```

2. **Fix incorrect links**:
```php
// Update menu items with correct URLs
wp_update_nav_menu_item($menu_id, $item_id, array(
    'menu-item-url' => home_url('/correct-url/')
));
```

3. **Create missing taxonomy pages**:
```php
// Ensure all taxonomy terms exist
wp_insert_term('New York', 'directory_location', array(
    'slug' => 'new-york',
    'description' => 'Comprehensive description of New York market...'
));
```

## Step 10: Deployment Preparation

```bash
# Only after ZERO 404s confirmed

# Create migration package
tar -czf wordpress-site.tar.gz wp-content/

# Prepare deployment script
cat > deploy.sh << 'EOF'
#!/bin/bash
# Deploy to Digital Ocean
echo "Ready for deployment"
echo "Site verified with zero 404 errors"
echo "All ${TOTAL_PAGES} pages working correctly"
EOF

chmod +x deploy.sh
```

## Verification Checklist

✅ **Website is ONLY complete when:**
- All directory entries imported and accessible
- All category pages have comprehensive content (1000+ words)
- All location pages have local market analysis
- All combination pages work (category + location)
- Navigation menus fully populated
- Review system implemented (not comments)
- Contact form working
- Playwright verified EVERY link - ZERO 404s
- All broken links fixed and re-verified
- SEO meta titles/descriptions on all pages
- Mobile responsive design verified
- Loading performance optimized

## Common Issues & Fixes

### Missing Privacy/Terms Pages
```php
// Create required legal pages
$pages = array(
    'Privacy Policy' => 'privacy-policy',
    'Terms of Service' => 'terms',
    'Cookie Policy' => 'cookies',
    'Sitemap' => 'sitemap'
);

foreach ($pages as $title => $slug) {
    wp_insert_post(array(
        'post_type' => 'page',
        'post_title' => $title,
        'post_name' => $slug,
        'post_content' => 'Page content here...',
        'post_status' => 'publish'
    ));
}
```

### Broken Category Links
```bash
# Flush rewrite rules after creating taxonomies
wp rewrite flush
```

### Missing Featured Images
```php
// Set default featured image for entries without one
$entries = get_posts(array('post_type' => 'directory', 'posts_per_page' => -1));
foreach ($entries as $entry) {
    if (!has_post_thumbnail($entry->ID)) {
        // Set a default image
        set_post_thumbnail($entry->ID, $default_image_id);
    }
}
```

## Success Criteria

✅ **Project is COMPLETE when:**
- Research gathered comprehensive data for all entries
- WordPress site running at http://localhost
- All directory entries created with rich data
- All taxonomy pages populated with SEO content
- Navigation menus working with zero broken links
- Review system functional (not using comments)
- Contact form operational
- **Playwright verified EVERY SINGLE link works (ZERO 404s)**
- All templates created and styled
- Mobile responsive verified
- Ready for deployment with ./migrate_now.sh

**Missing any of these means the bootstrap is INCOMPLETE!**

## Deployment Phase (After Local Completion)

### Step 1: Setup Digital Ocean Environment

```bash
# Create .env file with credentials
cat > .env << 'EOF'
DO_API_TOKEN=your_digital_ocean_api_token
JINA_API_KEY=your_jina_api_key
DOMAIN_NAME=yourdomain.com
EOF

# Install Python dependencies
pip3 install python-dotenv requests
```

### Step 2: Create Droplet with WordPress

```python
# create_droplet_with_ssh.py
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv('DO_API_TOKEN')
domain_name = os.getenv('DOMAIN_NAME')

headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
}

# Create droplet with WordPress pre-installed
droplet_data = {
    'name': f'{domain_name}-wordpress',
    'region': 'nyc3',
    'size': 's-1vcpu-1gb',
    'image': 'ubuntu-22-04-x64',
    'ssh_keys': [],
    'user_data': '''#!/bin/bash
    apt-get update
    apt-get install -y apache2 mysql-server php php-mysql libapache2-mod-php
    
    # Install WordPress
    cd /var/www/html
    wget https://wordpress.org/latest.tar.gz
    tar -xzf latest.tar.gz
    mv wordpress/* .
    rm -rf wordpress latest.tar.gz
    
    # Configure Apache
    a2enmod rewrite
    systemctl restart apache2
    
    # Install WP-CLI
    curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
    chmod +x wp-cli.phar
    mv wp-cli.phar /usr/local/bin/wp
    
    # Set permalinks
    wp --allow-root rewrite structure "/%postname%/"
    wp --allow-root rewrite flush
    '''
}

response = requests.post(
    'https://api.digitalocean.com/v2/droplets',
    headers=headers,
    json=droplet_data
)

if response.status_code == 202:
    droplet_info = response.json()['droplet']
    with open('.droplet_info', 'w') as f:
        json.dump({
            'droplet_id': droplet_info['id'],
            'ip_address': None  # Will be assigned
        }, f)
    print(f"Droplet created: {droplet_info['id']}")
```

### Step 3: Migration Script

```bash
#!/bin/bash
# migrate_now.sh

# Read droplet IP
DROPLET_IP=$(python3 -c "import json; print(json.load(open('.droplet_info'))['ip_address'])")

echo "Migrating WordPress to $DROPLET_IP..."

# Export local database
docker exec wp-mysql mysqldump -u wordpress -pwordpress_password wordpress > wordpress_backup.sql

# Copy files to droplet
scp -r wp-content/* root@$DROPLET_IP:/var/www/html/wp-content/
scp wordpress_backup.sql root@$DROPLET_IP:/tmp/

# Import database on droplet
ssh root@$DROPLET_IP << 'EOF'
mysql -u root -e "CREATE DATABASE IF NOT EXISTS wordpress;"
mysql -u root wordpress < /tmp/wordpress_backup.sql

# Update wp-config.php
cat > /var/www/html/wp-config.php << 'CONFIG'
<?php
define('DB_NAME', 'wordpress');
define('DB_USER', 'root');
define('DB_PASSWORD', '');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

$table_prefix = 'wp_';

define('WP_DEBUG', false);
define('WP_HOME', 'http://$DROPLET_IP');
define('WP_SITEURL', 'http://$DROPLET_IP');

define('AUTH_KEY',         'generate-new-salt');
define('SECURE_AUTH_KEY',  'generate-new-salt');
define('LOGGED_IN_KEY',    'generate-new-salt');
define('NONCE_KEY',        'generate-new-salt');
define('AUTH_SALT',        'generate-new-salt');
define('SECURE_AUTH_SALT', 'generate-new-salt');
define('LOGGED_IN_SALT',   'generate-new-salt');
define('NONCE_SALT',       'generate-new-salt');

if ( ! defined( 'ABSPATH' ) ) {
    define( 'ABSPATH', __DIR__ . '/' );
}

require_once ABSPATH . 'wp-settings.php';
CONFIG

# Set permissions
chown -R www-data:www-data /var/www/html
chmod -R 755 /var/www/html

# Restart Apache
systemctl restart apache2

# Flush permalinks
wp --allow-root rewrite structure '/%postname%/'
wp --allow-root rewrite flush
EOF

echo "Migration complete! Site available at http://$DROPLET_IP"
```

## Template Variables Reference

| Placeholder | Description | Example |
|------------|-------------|---------|
| `{directory_type}` | Type of directory | `SaaS tools`, `restaurants`, `therapists` |
| `{location}` | Geographic scope | `New York`, `California`, `nationwide` |
| `{category}` | Main categories | `CRM`, `Italian`, `Anxiety` |
| `{domain_name}` | Your domain | `best-saas-tools.com` |

## Critical Final Checks

### Pre-Deployment Checklist

```bash
# 1. Verify all pages exist
wp post list --post_type=page --fields=ID,post_title,post_name
wp post list --post_type=directory --fields=ID,post_title --format=count
# Should show all expected pages and directory entries

# 2. Check all taxonomies populated
wp term list directory_category --fields=term_id,name,slug,count
wp term list directory_location --fields=term_id,name,slug,count
# All terms should have count > 0

# 3. Verify menus have items
wp menu item list main-menu
wp menu item list footer-menu
# Should show all menu items

# 4. Test database integrity
wp db check
wp db optimize

# 5. Verify no broken images
wp media regenerate --yes

# 6. Check theme is active
wp theme list --status=active
# Should show directory-theme as active

# 7. Permalinks are correct
wp rewrite list --format=csv
# Should show custom post type rules

# 8. No PHP errors
tail -f debug.log
# Should be empty or minimal warnings only
```

### Performance Optimization

```php
// Add to functions.php for production

// Enable caching headers
function add_cache_headers() {
    if (!is_admin()) {
        header('Cache-Control: max-age=3600, public');
        header('Expires: ' . gmdate('D, d M Y H:i:s', time() + 3600) . ' GMT');
    }
}
add_action('send_headers', 'add_cache_headers');

// Optimize images on upload
add_filter('wp_handle_upload_prefilter', function($file) {
    $image_types = array('image/jpeg', 'image/png', 'image/gif');
    if (in_array($file['type'], $image_types)) {
        // Compress image
        $image = wp_get_image_editor($file['tmp_name']);
        if (!is_wp_error($image)) {
            $image->set_quality(85);
            $image->save($file['tmp_name']);
        }
    }
    return $file;
});

// Lazy load images
add_filter('wp_lazy_loading_enabled', '__return_true');

// Minify HTML output
function minify_html($buffer) {
    $search = array('/\>[^\S ]+/s', '/[^\S ]+\</s', '/(\s)+/s');
    $replace = array('>', '<', '\\1');
    $buffer = preg_replace($search, $replace, $buffer);
    return $buffer;
}
ob_start('minify_html');
```

### Security Hardening

```php
// Add to wp-config.php for production

// Security headers
header('X-Frame-Options: SAMEORIGIN');
header('X-Content-Type-Options: nosniff');
header('X-XSS-Protection: 1; mode=block');
header('Referrer-Policy: strict-origin-when-cross-origin');

// Disable file editing
define('DISALLOW_FILE_EDIT', true);

// Limit login attempts
function limit_login_attempts() {
    // Implementation here
}

// Hide WordPress version
remove_action('wp_head', 'wp_generator');

// Disable XML-RPC
add_filter('xmlrpc_enabled', '__return_false');

// Secure uploads directory
$htaccess_content = 'Options -Indexes';
file_put_contents(ABSPATH . 'wp-content/uploads/.htaccess', $htaccess_content);
```

## Troubleshooting Guide

### Common Bootstrap Failures and Solutions

#### Research Phase Issues

**Problem**: Jina AI scraping fails or returns incomplete data
```bash
# Solution: Retry with different approach
curl "https://s.jina.ai/?q=COMPANY_NAME+site:g2.com" \
  -H "Authorization: Bearer $JINA_API_KEY"

# Or use alternative sources
curl "https://s.jina.ai/?q=COMPANY_NAME+site:capterra.com" \
  -H "Authorization: Bearer $JINA_API_KEY"
```

**Problem**: Can't find enough information for directory entries
```bash
# Solution: Use multiple search queries
searches=("features" "pricing" "reviews" "alternatives" "integrations")
for term in "${searches[@]}"; do
  curl "https://s.jina.ai/?q=COMPANY_NAME+$term" \
    -H "Authorization: Bearer $JINA_API_KEY"
done
```

#### WordPress Development Issues

**Problem**: Custom post type pages return 404
```php
// Solution: Flush rewrite rules after registering
function fix_directory_permalinks() {
    register_directory_post_type();
    flush_rewrite_rules();
}
add_action('after_switch_theme', 'fix_directory_permalinks');
```

**Problem**: Taxonomy archive pages not showing content
```php
// Solution: Ensure proper query modification
function include_directory_in_archives($query) {
    if (!is_admin() && $query->is_main_query()) {
        if (is_tax('directory_category') || is_tax('directory_location')) {
            $query->set('post_type', 'directory');
            $query->set('posts_per_page', 20);
        }
    }
}
add_action('pre_get_posts', 'include_directory_in_archives');
```

**Problem**: Images not importing from JSON
```php
// Solution: Use proper image sideloading
function import_image_from_url($url, $post_id, $desc) {
    require_once(ABSPATH . 'wp-admin/includes/media.php');
    require_once(ABSPATH . 'wp-admin/includes/file.php');
    require_once(ABSPATH . 'wp-admin/includes/image.php');
    
    $image = media_sideload_image($url, $post_id, $desc, 'id');
    
    if (is_wp_error($image)) {
        // Try alternative method
        $tmp = download_url($url);
        if (!is_wp_error($tmp)) {
            $file_array = array(
                'name' => basename($url),
                'tmp_name' => $tmp
            );
            $image = media_handle_sideload($file_array, $post_id);
            @unlink($tmp);
        }
    }
    
    return $image;
}
```

#### Playwright Verification Issues

**Problem**: Playwright can't connect to localhost
```javascript
// Solution: Use correct URL and wait for load
const browser = await playwright.chromium.launch();
const page = await browser.newPage();

// Ensure WordPress is running
await page.goto('http://localhost', { 
    waitUntil: 'networkidle',
    timeout: 30000 
});

// If using Docker, might need container IP
await page.goto('http://127.0.0.1', { 
    waitUntil: 'networkidle' 
});
```

**Problem**: Too many links timing out during verification
```javascript
// Solution: Batch testing with retry logic
async function testLinksWithRetry(links, maxRetries = 3) {
    const results = [];
    
    for (const link of links) {
        let retries = 0;
        let success = false;
        
        while (retries < maxRetries && !success) {
            try {
                const response = await page.goto(link, {
                    waitUntil: 'domcontentloaded',
                    timeout: 10000
                });
                
                results.push({
                    url: link,
                    status: response.status(),
                    success: response.status() !== 404
                });
                
                success = true;
            } catch (error) {
                retries++;
                if (retries === maxRetries) {
                    results.push({
                        url: link,
                        status: 'error',
                        success: false,
                        error: error.message
                    });
                }
                await page.waitForTimeout(1000); // Wait before retry
            }
        }
    }
    
    return results;
}
```

#### Deployment Issues

**Problem**: Migration script fails to connect
```bash
# Solution: Check SSH key and IP
# Verify SSH key exists
ls -la ~/.ssh/wordpress_deploy

# Get correct IP
curl -X GET "https://api.digitalocean.com/v2/droplets" \
  -H "Authorization: Bearer $DO_API_TOKEN" | \
  python3 -m json.tool | grep ip_address

# Test connection
ssh -i ~/.ssh/wordpress_deploy root@YOUR_IP "echo 'Connected'"
```

**Problem**: Database import fails on production
```bash
# Solution: Fix MySQL permissions
ssh root@$DROPLET_IP << 'EOF'
# Create user with proper permissions
mysql -u root << 'SQL'
CREATE USER 'wordpress'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpress'@'localhost';
FLUSH PRIVILEGES;
SQL

# Import with new credentials
mysql -u wordpress -psecure_password wordpress < /tmp/wordpress_backup.sql
EOF
```

## Advanced Features

### Add Search Functionality

```php
// Enhanced search for directory entries
function enhance_directory_search($query) {
    if (!is_admin() && $query->is_search() && $query->is_main_query()) {
        $query->set('post_type', array('directory', 'post', 'page'));
        
        // Search in meta fields too
        add_filter('posts_search', function($search, $wp_query) {
            global $wpdb;
            
            if (empty($search)) return $search;
            
            $search_terms = $wp_query->get('s');
            
            $search .= " OR EXISTS (
                SELECT * FROM {$wpdb->postmeta}
                WHERE {$wpdb->postmeta}.post_id = {$wpdb->posts}.ID
                AND {$wpdb->postmeta}.meta_value LIKE '%{$search_terms}%'
            )";
            
            return $search;
        }, 10, 2);
    }
}
add_action('pre_get_posts', 'enhance_directory_search');
```

### Add AJAX Filtering

```javascript
// Add to theme's JavaScript file
jQuery(document).ready(function($) {
    $('.filter-select').on('change', function() {
        const category = $('#category-filter').val();
        const location = $('#location-filter').val();
        const sort = $('#sort-filter').val();
        
        $.ajax({
            url: ajax_object.ajax_url,
            type: 'POST',
            data: {
                action: 'filter_directory',
                category: category,
                location: location,
                sort: sort,
                nonce: ajax_object.nonce
            },
            success: function(response) {
                $('.directory-grid').html(response);
            }
        });
    });
});
```

```php
// Add to functions.php
function handle_directory_filter() {
    check_ajax_referer('filter_nonce', 'nonce');
    
    $args = array(
        'post_type' => 'directory',
        'posts_per_page' => 20
    );
    
    // Add tax query if filters selected
    $tax_query = array();
    
    if (!empty($_POST['category'])) {
        $tax_query[] = array(
            'taxonomy' => 'directory_category',
            'field' => 'slug',
            'terms' => sanitize_text_field($_POST['category'])
        );
    }
    
    if (!empty($_POST['location'])) {
        $tax_query[] = array(
            'taxonomy' => 'directory_location',
            'field' => 'slug',
            'terms' => sanitize_text_field($_POST['location'])
        );
    }
    
    if (!empty($tax_query)) {
        $args['tax_query'] = $tax_query;
    }
    
    // Add sorting
    switch($_POST['sort']) {
        case 'rating':
            $args['meta_key'] = 'rating';
            $args['orderby'] = 'meta_value_num';
            $args['order'] = 'DESC';
            break;
        case 'newest':
            $args['orderby'] = 'date';
            $args['order'] = 'DESC';
            break;
    }
    
    $query = new WP_Query($args);
    
    if ($query->have_posts()) {
        while ($query->have_posts()) {
            $query->the_post();
            get_template_part('parts/directory-card');
        }
    }
    
    wp_die();
}
add_action('wp_ajax_filter_directory', 'handle_directory_filter');
add_action('wp_ajax_nopriv_filter_directory', 'handle_directory_filter');
```

## Final Quality Assurance

### SEO Validation

```php
// Verify all SEO elements are present
function validate_seo_elements() {
    $pages = get_posts(array(
        'post_type' => array('directory', 'page'),
        'posts_per_page' => -1
    ));
    
    $missing_seo = array();
    
    foreach ($pages as $page) {
        $title = get_post_meta($page->ID, '_yoast_wpseo_title', true);
        $desc = get_post_meta($page->ID, '_yoast_wpseo_metadesc', true);
        
        if (empty($title) || strlen($title) < 30) {
            $missing_seo[] = array(
                'page' => $page->post_title,
                'issue' => 'Missing or short meta title'
            );
        }
        
        if (empty($desc) || strlen($desc) < 120) {
            $missing_seo[] = array(
                'page' => $page->post_title,
                'issue' => 'Missing or short meta description'
            );
        }
    }
    
    return $missing_seo;
}
```

### Content Completeness Check

```php
// Ensure all directory entries have complete data
function check_directory_completeness() {
    $required_fields = array(
        'rating', 'starting_price', 'company_data',
        'features', 'pros_cons', 'alternatives'
    );
    
    $incomplete = array();
    
    $entries = get_posts(array(
        'post_type' => 'directory',
        'posts_per_page' => -1
    ));
    
    foreach ($entries as $entry) {
        $missing = array();
        
        foreach ($required_fields as $field) {
            $value = get_post_meta($entry->ID, $field, true);
            if (empty($value)) {
                $missing[] = $field;
            }
        }
        
        if (!empty($missing)) {
            $incomplete[$entry->post_title] = $missing;
        }
    }
    
    return $incomplete;
}
```

## 🎯 Complete Workflow Summary

1. **Research Phase** → Exhaust all data sources with Jina AI
2. **Data Structure** → Create comprehensive JSON for every entry
3. **WordPress Setup** → Docker environment with custom theme
4. **Import Data** → All directory entries and taxonomies
5. **Create Pages** → All archive, category, location pages
6. **Build Navigation** → Mega menus with all links
7. **Review System** → Custom reviews, not comments
8. **Style Everything** → Complex CSS with multiple layouts
9. **Playwright Testing** → EVERY SINGLE LINK VERIFIED
10. **Fix All Issues** → ZERO 404s before proceeding
11. **Deploy** → Only after complete local verification
12. **Live** → Production WordPress directory site!

## 💡 Key Success Factors

- **Zero 404 Policy** - Not a single broken link is acceptable
- **Comprehensive Research** - Every entry needs 2000+ words of content
- **Complete Testing** - Test everything, not just samples
- **Rich Content** - Every page needs substantial, valuable content
- **Full SEO** - Every page optimized for search engines
- **Professional Quality** - This is a production website, not a demo

## 🚨 Important Notes

- Never deliver partial work - complete the entire website
- Always verify with Playwright - every single link must work
- Research phase is mandatory - don't skip data collection
- Review system must be custom - don't use WordPress comments
- All taxonomy pages need rich content - not just listings
- The website must be ready for immediate deployment
- Bootstrap is only complete when ready for `./migrate_now.sh`

**This bootstrap creates a complete, production-ready WordPress directory website that can immediately serve real users and rank in search engines.**