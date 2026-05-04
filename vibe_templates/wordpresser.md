# WordPress Claude Code Wizard - Complete Workflow & Development Guide

 ## 🚨 MANDATORY: ONE-SHOT COMPLETE EXECUTION
 
 **YOU MUST COMPLETE THE ENTIRE WORKFLOW IN ONE SHOT. DO NOT STOP PARTWAY.**
 **DO NOT deliver partial work. DO NOT stop after Phase 1. DO NOT skip steps.**
 **COMPLETE MEANS: Research → Build Website → Test with Playwright → Fix ALL issues → DONE**
 **The website must be FULLY FUNCTIONAL at http://localhost before you stop.**
 
 **DO NOT REPORT BACK TO THE USER OR ASK THEM ANYTHING UNTIL YOU HAVE:**
 - A fully built website running at http://localhost
 - All directory entries created and populated
 - All taxonomy pages working
 - Navigation menus fully populated
 - ZERO 404 errors verified by Playwright
 - Ready to run ./migrate_now.sh
 
 **The user hired you to BUILD A WEBSITE, not to show research or ask questions.**

 ## ⚠️ CRITICAL REQUIREMENT: ZERO 404 ERRORS
 
 **EVERY website you build MUST have ZERO 404 errors. Use Playwright MCP to verify EVERY SINGLE link.**
 **Headers and footers ALWAYS have broken links if you don't check them systematically.**
 **Do not deliver a website until Playwright confirms every link works.**

 ## 🎯 Main Workflow Process - COMPLETE ALL PHASES

 When building a directory website, you MUST complete ALL phases in one continuous workflow:

 ### Phase 1: Deep Research & Comprehensive Data Collection
 
 **GOAL: Create pages so information-rich that visitors never need to leave your site**
 
 1. **Research each individual entry exhaustively using Jina AI**
    - Scrape the company's main website completely
    - Find and scrape their pricing pages, feature lists, documentation
    - Search for reviews, comparisons, alternatives
    - Gather technical specifications, integrations, use cases
    - Find case studies, success stories, testimonials
    - Collect founder information, company history, funding details
    - Get support options, contact methods, social media links
    - Retry any failed scrapes until you have EVERYTHING
 
 2. **Build massive JSON datasets for each entry**
    Each individual page JSON should contain:
    ```json
    {
      "basics": {
        "name", "tagline", "description" (500+ words),
        "founded", "headquarters", "employees", "funding"
      },
      "detailed_features": [
        {"name", "description" (100+ words), "category", "importance"}
      ],
      "pricing": {
        "model", "free_tier", "starter_price", "tiers": [
          {"name", "price", "features" (20+), "limits", "best_for"}
        ]
      },
      "use_cases": [
        {"title", "description" (200+ words), "industry", "company_size"}
      ],
      "pros_cons": {
        "pros": [{"title", "explanation" (50+ words)}],
        "cons": [{"title", "explanation" (50+ words)}]
      },
      "integrations": [
        {"name", "type", "description", "documentation_url"}
      ],
      "alternatives": [
        {"name", "comparison" (100+ words), "when_to_choose"}
      ],
      "reviews": {
        "average_rating", "total_reviews",
        "rating_breakdown": {"5": %, "4": %, "3": %, "2": %, "1": %},
        "expert_reviews": [{"source", "rating", "summary" (200+ words)}]
      },
      "technical_specs": {
        "platforms", "languages", "api", "security", "compliance"
      },
      "support": {
        "channels", "response_time", "documentation_quality", "community"
      },
      "media": {
        "logo", "screenshots" (10+), "videos", "diagrams"
      }
    }
    ```
 
 3. **Create comprehensive taxonomy archive pages**
    
    **For Category/Type taxonomy pages (e.g., /categories/crm-software/, /types/italian-restaurants/, /specialties/anxiety-therapy/):**
    - Comprehensive overview of the category (1000+ words)
    - Complete buyer's/selection guide
    - Key features to look for
    - Common use cases and who needs this
    - Price range analysis and what affects cost
    - Industry trends and future outlook
    - Comparison methodology explanation
    - Top 10-20 entries with detailed previews
    - Quick comparison table
    - 20-30 FAQs about this category
    - Related categories and how they differ
    - Expert opinions and industry insights
    - Glossary of category-specific terms
    - Statistics and market data
    - ALL entries in this category listed below with rich cards
    
    **For Location pages (e.g., /locations/new-york/):**
    - Complete local market analysis (1000+ words)
    - Local regulations and requirements
    - Average prices in this area vs national
    - Transportation and parking information
    - Neighborhood-by-neighborhood breakdown
    - Local insurance providers accepted
    - Emergency services in the area
    - Community resources and support groups
    - Local statistics and demographics
    - ALL providers in this location with detailed cards
    - Nearby locations for comparison
    - Local events and workshops
    
    **For Combined taxonomy pages (e.g., /crm-software-for-startups/, /italian-restaurants-manhattan/, /anxiety-therapists-new-york/):**
    - Everything from both individual taxonomies combined
    - Specific local/niche context 
    - Why this combination matters (e.g., "Why startups need different CRM")
    - Unique considerations for this intersection
    - Price analysis for this specific combination
    - Top 10 detailed comparisons with scoring methodology
    - Map visualization (if location-based)
    - Availability/wait times analysis
    - Quick filter and sort options
    - ALL matching entries with rich information cards
 
 4. **Collect extensive imagery**
    - Product screenshots (10+ per entry)
    - Logo variations
    - Feature demonstration images
    - Comparison charts and infographics
    - Industry-relevant stock photos from Unsplash
    - Create custom diagrams where needed

 ### Phase 2: Website Development (THIS IS NOT OPTIONAL - YOU MUST BUILD THE WEBSITE)
 
 **DO NOT STOP AFTER RESEARCH. BUILD THE ACTUAL WEBSITE NOW.**
 
 1. **Start with local WordPress Docker environment**
    - Run `docker-compose up -d`
    - Access at http://localhost
 
 2. **Build the custom theme with FULL SEO optimization**
    - Create detailed, complex CSS (not simple/short)
    - Modern, clean, modular design
    - Implement all directory pages from JSON data
    - Add comprehensive animations and interactions
    - Ensure responsive design with multiple breakpoints
 
 3. **Generate ALL ranking pages with maximized SEO**
    - Create "Best X in Y" pages for every location/category combination - THIS IS ESSENTIAL ON LOCATION PAGES
    - Maximize meta titles (60 chars) for each page - use words like Best X in Y or something else to help rank for those keywords
    - Maximize meta descriptions (160 chars) for each page
    - Create unique, comprehensive H1 titles
    - Write detailed, SEO-optimized descriptions for every page
    - Build internal linking structure between related pages
 
 4. **Create 5-7 horizontal template variations**
    - Grid layout with filters
    - Card-based design with hover effects  
    - List view with detailed information
    - Comparison table layout
    - Map-based directory view
    - Featured/spotlight layout
    - Masonry/Pinterest style layout
 
 5. **Build mega header navigation**
    - Multi-level dropdown menus
    - Search functionality
    - Category quick links
    - Location selector
    - Sticky header on scroll
    - Mobile-optimized hamburger menu
 
 6. **Implement review system (not basic comments)**
    - Custom review form for each directory entry
    - Frame as "Leave a Review" for product/service
    - Star rating system
    - Review categories (quality, service, value, etc.)
    - Review moderation queue
    - Display average ratings
    - Sort reviews by helpful/recent/rating
 
 7. **Add contact form**
    - Professional contact form with validation
    - Multiple contact reasons dropdown
    - File upload capability
    - Anti-spam measures
    - Email notification system
 
 8. **Import directory data from JSON**
    - Create custom post types for directory entries
    - Import JSON data into WordPress
    - Set up taxonomy/category structure
    - Generate all location/category pages automatically
 
 9. **Test thoroughly locally**
    - Check all pages and permalinks
    - Verify images load correctly
    - Test responsive design
    - Validate all SEO elements
    - Test review submission
    - Test contact form

 ### Phase 2.5: MANDATORY Playwright Verification - CHECK EVERY SINGLE LINK
 
 **⛔ STOP! DO NOT SKIP THIS! YOU MUST CHECK EVERY SINGLE LINK WITH PLAYWRIGHT!**
 
 **THE WEBSITE IS NOT COMPLETE UNTIL PLAYWRIGHT VERIFIES ZERO 404s**
 
 Use the pre-configured Playwright MCP to verify EVERY link works. Do not just check "a few" links.
 Do not just check "some" pages. CHECK THEM ALL. The header and footer ALWAYS have broken links
 if you don't verify them properly!
 
 1. **MANDATORY: Extract and Test EVERY Header Link**
    ```
    Use playwright mcp to:
    1. Navigate to http://localhost
    2. Extract ALL href attributes from the header navigation
    3. Create a list of EVERY SINGLE link found
    4. Visit EACH link one by one
    5. Verify EACH loads without 404
    6. If ANY link returns 404, FIX IT IMMEDIATELY
    
    Example: If header has Home, About, Services, Blog, Contact, Categories dropdown with 
    10 categories, Location dropdown with 20 locations - that's 35 links to check. 
    CHECK ALL 35. Not 5. Not 10. ALL 35.
    ```
 
 2. **MANDATORY: Extract and Test EVERY Footer Link**
    ```
    Use playwright mcp to:
    1. Scroll to footer
    2. Extract ALL href attributes from the footer
    3. Visit EVERY SINGLE footer link
    4. Do not assume they work - TEST THEM
    5. Common broken footer links: Privacy Policy, Terms, Sitemap
    6. CREATE these pages if they don't exist
    ```
 
 3. **MANDATORY: Test EVERY Directory Entry**
    ```
    DO NOT test "a few examples" - test EVERY SINGLE ONE:
    - Get the full list of all directory entries
    - Visit each one: /companies/company-1/, /companies/company-2/, etc.
    - If you have 50 entries, test all 50
    - Each must load with proper content, not 404
    ```
 
 4. **MANDATORY: Test EVERY Taxonomy Page**
    ```
    Test EVERY SINGLE taxonomy page that should exist:
    - EVERY category: /categories/[slug]/ for each category
    - EVERY location: /locations/[slug]/ for each location  
    - EVERY tag: /tags/[slug]/ for each tag
    - EVERY combination page if they exist
    - Do not test "some" - test EVERY SINGLE ONE
    ```
 
 5. **MANDATORY: Systematic Link Extraction and Testing**
    ```
    Use playwright mcp to run this systematic check:
    
    // Extract ALL links from the site
    const allLinks = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('a[href]'))
        .map(a => a.href)
        .filter(href => href.startsWith('http://localhost'));
    });
    
    // Test EVERY SINGLE link
    for (const link of allLinks) {
      await page.goto(link);
      // Check for 404 or error
      // Log any broken links
    }
    
    If you find 10 links, test 10.
    If you find 100 links, test 100.
    If you find 500 links, test 500.
    TEST THEM ALL.
    ```
 
 6. **FIX ALL BROKEN LINKS IMMEDIATELY**
    ```
    For EVERY 404 found:
    - Create the missing page
    - Or fix the incorrect link
    - Re-test with Playwright to confirm it's fixed
    - Do not move on until ZERO 404s exist
    ```
 
 7. **Fix Every Broken Link Found**
    ```
    Whatever links are in the header/footer:
    - Test them ALL with Playwright
    - If they return 404, either fix the link or create the page
    - Common broken links: About, Contact, Privacy, Terms, Blog, etc.
    - Do not assume any link works - TEST IT
    ```
 
 8. **Final Verification Report**
    ```
    Only after testing EVERY link, generate report:
    - Total links found in header: [number]
    - Total links found in footer: [number]
    - Total directory entries tested: [number]
    - Total taxonomy pages tested: [number]
    - Total unique URLs tested: [number]
    - 404 errors found and fixed: [list]
    - Final status: MUST be "Zero 404s found"
    ```
 
 **❌ UNACCEPTABLE:**
 - "I tested a few links and they work"
 - "I checked some pages"
 - "The main pages seem to work"
 - "I verified the important links"
 
 **✅ REQUIRED:**
 - "I tested all 47 header links - all working"
 - "I tested all 23 footer links - all working"
 - "I tested all 85 directory entries - all working"
 - "I tested all 35 taxonomy pages - all working"
 - "Total: 190 unique URLs tested, zero 404s"
 
 **THE WEBSITE IS NOT COMPLETE UNTIL EVERY SINGLE LINK WORKS**

 ## ✅ ONLY NOW REPORT BACK TO THE USER
 
 **NOW that you have a COMPLETE, WORKING website with ZERO 404s, you can report:**
 - "Website complete and verified at http://localhost"
 - "All [X] directory entries created and tested"
 - "All [X] taxonomy pages working"
 - "Playwright verified [X] total links - ZERO 404 errors"
 - "Ready for deployment with ./migrate_now.sh"
 
 **If you haven't done ALL of the above, GO BACK and finish the website.**

 ### Phase 3: Deployment to Digital Ocean
 1. **Setup infrastructure**
    - Run `./setup_ssh_and_deploy.sh` (one-time SSH setup)
    - Run `python3 create_droplet_with_ssh.py`
    - Wait 5-10 minutes for installation
 
 2. **Migrate to production**
    - Run `./migrate_now.sh`
    - Verify custom theme transferred
    - Check that permalinks work (auto-configured)
 
 3. **Final configuration**
    - Point domain to droplet IP
    - Install SSL certificate
    - Configure backups

 ---

 ## 📚 Directory Website Development

 ### SEO Page Structure Requirements

 **IMPORTANT:** Do NOT use Rank Math during development. Focus on native SEO implementation.
 Rank Math will only be added at launch for Search Console submission.

 Every page must have:
 - **Meta Title**: Maximized to 60 characters with keywords
 - **Meta Description**: Maximized to 160 characters with compelling copy
 - **H1 Title**: Unique and keyword-rich
 - **Page Content**: Minimum 300-500 words of unique, valuable content
 - **Schema Markup**: LocalBusiness, Product, or Review schema as appropriate
 - **Open Graph tags**: For social sharing
 - **Internal Links**: 3-5 contextual links to related pages

 Generate these page types for maximum ranking potential:
 - "Best [Product] in [City]" - for every city
 - "Top 10 [Category] in [State]" - for every state
 - "[Product] near me" - location-based pages
 - "[Category] Reviews [Year]" - fresh content pages
 - "Compare [Product A] vs [Product B]" - comparison pages
 - "[Product] for [Use Case]" - intent-based pages
 - "Cheap/Affordable [Product] in [Location]" - price-focused pages

 ### Review System Framework

 Frame reviews contextually based on the directory type:
 - For restaurants: "[Cuisine] lovers who dined at [Restaurant] can leave a review"
 - For products: "[Product] users who tried [Brand] can share their experience"
 - For services: "Customers who used [Service] from [Company] can rate their experience"
 - For venues: "Visitors who went to [Venue] can share their thoughts"

 Review form should include:
 - Overall star rating (1-5 stars)
 - Category-specific ratings (e.g., Quality, Service, Value, Location)
 - Written review with minimum 50 characters
 - Photo upload option
 - "Would you recommend?" Yes/No
 - Verified purchase/visit checkbox
 - Helpful/Not Helpful voting on other reviews

 ### Research Phase with Jina AI

 When building directory websites, use Jina AI for comprehensive research:

 ```bash
 # Search for information (use s.jina.ai)
 curl "https://s.jina.ai/?q=YOUR_SEARCH_TERM" \
   -H "Authorization: Bearer $JINA_API_KEY"

 # Scrape individual pages (use r.jina.ai)
 curl "https://r.jina.ai/https://example.com/page" \
   -H "Authorization: Bearer $JINA_API_KEY"
 ```

 **Important Research Guidelines:**
 - Create detailed JSON for each directory page
 - If a page 404s or doesn't scrape properly, retry the scrape
 - DO NOT use Jina to scrape CSS from design sites

 ### Finding Royalty-Free Images

 ```bash
 # Search for Unsplash images using Jina
 curl "https://s.jina.ai/?q=YOUR_IMAGE_DESCRIPTION+unsplash" \
   -H "Authorization: Bearer $JINA_API_KEY"
 
 # Then scrape the found Unsplash pages for non-premium images
 curl "https://r.jina.ai/https://unsplash.com/photos/..." \
   -H "Authorization: Bearer $JINA_API_KEY"
 ```

 ### Directory Page JSON Format

 Each directory entry should have comprehensive data:

 ```json
 {
   "id": "unique-identifier",
   "name": "Company/Service Name",
   "category": "Technology Category",
   "description": "Detailed description...",
   "features": ["feature1", "feature2", "..."],
   "pricing": {
     "model": "subscription/one-time/freemium",
     "tiers": [...]
   },
   "images": {
     "logo": "url-from-unsplash",
     "screenshots": ["url1", "url2"],
     "hero": "hero-image-url"
   },
   "metadata": {
     "founded": "year",
     "headquarters": "location",
     "employees": "range",
     "funding": "amount"
   },
   "links": {
     "website": "url",
     "documentation": "url",
     "pricing": "url"
   },
   "tags": ["tag1", "tag2"],
   "lastUpdated": "timestamp"
 }
 ```

 ### CSS Development Guidelines

 **IMPORTANT:** Create extremely detailed and complex CSS files that are well-thought-out:

 - Don't write short, simple CSS - make it comprehensive
 - Include detailed animations and transitions
 - Add hover states, focus states, and active states
 - Create responsive breakpoints for all screen sizes
 - Include print styles and accessibility features
 - Use CSS custom properties for theming
 - Add detailed comments explaining complex sections
 - Implement sophisticated grid and flexbox layouts
 - Include fallbacks for older browsers

 Example of detailed CSS approach:
 ```css
 /* Component: Directory Card
    Purpose: Display individual directory entries
    States: default, hover, active, disabled, loading
    Breakpoints: mobile-first approach with 5 breakpoints
    Accessibility: WCAG 2.1 AA compliant */
 
 .directory-card {
   /* Base styles with extensive properties */
   /* Multiple transition effects */
   /* Complex shadow systems */
   /* Detailed spacing scales */
 }
 ```

 ## 🚀 Quick Deploy Workflow

 When a user clones this repository and wants to deploy WordPress to Digital Ocean,
 execute these commands in order:

 ```bash
 # 1. Setup environment
 cp .env.example .env
 # User must edit .env and add DO_API_TOKEN and JINA_API_KEY

 # 2. Install Python dependencies
 pip3 install python-dotenv requests

 # 3. Start local WordPress
 docker-compose up -d

 # 4. Setup SSH keys (one-time)
 ./setup_ssh_and_deploy.sh

 # 5. Create Digital Ocean droplet
 python3 create_droplet_with_ssh.py

 # 6. Wait for installation (5-10 minutes)
 sleep 300

 # 7. Migrate local WordPress to droplet
 ./migrate_now.sh
 ```

 ## 📁 Project Structure

 ```
 wordpress-claude-code-wizard/
 ├── .env                          # DO_API_TOKEN goes here
 ├── docker-compose.yml            # Local WordPress environment
 ├── Dockerfile                    # Custom Apache/PHP image
 ├── wp-config.php                # Environment-aware configuration
 ├── setup_ssh_and_deploy.sh      # SSH key automation
 ├── create_droplet_with_ssh.py   # Droplet creation script
 ├── migrate_now.sh               # Migration script
 └── wp-content/
     ├── themes/
     │   └── my-custom-theme/     # Starter theme
     └── plugins/
         └── custom-post-types/    # CPT plugin
 ```

 ## 🎨 WordPress Development Guide

 ### Theme Development

 Users can modify the custom theme in `wp-content/themes/my-custom-theme/`:

 ```bash
 # Create new page template
 cat > wp-content/themes/my-custom-theme/page-about.php << 'EOF'
 <?php
 /* Template Name: About Page */
 get_header();
 ?>
 <main class="site-main">
     <div class="container">
         <h1><?php the_title(); ?></h1>
         <?php the_content(); ?>
     </div>
 </main>
 <?php get_footer(); ?>
 EOF

 # Create custom single post template
 cat > wp-content/themes/my-custom-theme/single.php << 'EOF'
 <?php get_header(); ?>
 <main class="site-main">
     <article>
         <h1><?php the_title(); ?></h1>
         <div class="meta">Posted on <?php echo get_the_date(); ?></div>
         <?php the_content(); ?>
     </article>
 </main>
 <?php get_footer(); ?>
 EOF

 # Create archive template
 cat > wp-content/themes/my-custom-theme/archive.php << 'EOF'
 <?php get_header(); ?>
 <main class="site-main">
     <h1><?php the_archive_title(); ?></h1>
     <?php while (have_posts()) : the_post(); ?>
         <article>
             <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
             <?php the_excerpt(); ?>
         </article>
     <?php endwhile; ?>
 </main>
 <?php get_footer(); ?>
 EOF
 ```

 ### Adding Navigation Menus

 Add to `wp-content/themes/my-custom-theme/functions.php`:

 ```php
 // Register multiple menu locations
 register_nav_menus(array(
     'primary' => __('Primary Menu', 'my-custom-theme'),
     'footer' => __('Footer Menu', 'my-custom-theme'),
     'social' => __('Social Links Menu', 'my-custom-theme'),
 ));

 // Add menu support
 add_theme_support('menus');
 ```

 Display menus in theme templates:

 ```php
 // In header.php
 <?php wp_nav_menu(array('theme_location' => 'primary')); ?>

 // In footer.php
 <?php wp_nav_menu(array('theme_location' => 'footer')); ?>
 ```

 ### WP-CLI Commands (Inside Docker Container)

 ```bash
 # Access the WordPress container
 docker exec -it wp-dev bash

 # Install WP-CLI (if not already installed)
 curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
 chmod +x wp-cli.phar
 mv wp-cli.phar /usr/local/bin/wp

 # Create pages
 wp post create --post_type=page --post_title='Home' --post_status=publish
 wp post create --post_type=page --post_title='About Us' --post_status=publish
 wp post create --post_type=page --post_title='Services' --post_status=publish
 wp post create --post_type=page --post_title='Contact' --post_status=publish
 wp post create --post_type=page --post_title='Blog' --post_status=publish

 # Set static homepage
 wp option update page_on_front 2  # Use page ID
 wp option update show_on_front page
 wp option update page_for_posts 5  # Blog page ID

 # Create menu
 wp menu create "Main Menu"
 wp menu location assign main-menu primary
 wp menu item add-post main-menu 2  # Add pages to menu
 wp menu item add-post main-menu 3
 wp menu item add-post main-menu 4

 # Install popular plugins
 wp plugin install contact-form-7 --activate
 wp plugin install wordpress-seo --activate
 wp plugin install elementor --activate
 wp plugin install woocommerce --activate
 wp plugin install updraftplus --activate

 # Create users
 wp user create [USER_1] [EMAIL_1] --role=editor --user_pass=[PASSWORD_1]
 wp user create [USER_2] [EMAIL_2] --role=author --user_pass=[PASSWORD_2]

 # Update site options
 wp option update blogname "My Awesome Site"
 wp option update blogdescription "A WordPress site built with Claude Code Wizard"
 wp option update timezone_string "America/New_York"

 # Set permalinks
 wp rewrite structure '/%postname%/'
 wp rewrite flush
 ```

 ### Custom Post Types

 The included plugin already creates Portfolio and Testimonial post types. To add
 more:

 ```php
 // Add to wp-content/plugins/custom-post-types/custom-post-types.php

 public function register_team_post_type() {
     $args = array(
         'labels' => array(
             'name' => 'Team Members',
             'singular_name' => 'Team Member',
         ),
         'public' => true,
         'has_archive' => true,
         'supports' => array('title', 'editor', 'thumbnail'),
         'menu_icon' => 'dashicons-groups',
         'show_in_rest' => true,
     );
     register_post_type('team', $args);
 }
 // Add to __construct(): add_action('init', array($this,
 'register_team_post_type'));
 ```

 ### Advanced Theme Features

 ```php
 // Add to functions.php

 // Custom image sizes
 add_theme_support('post-thumbnails');
 add_image_size('hero', 1920, 600, true);
 add_image_size('team-member', 400, 400, true);

 // Widget areas
 function my_widgets_init() {
     register_sidebar(array(
         'name' => 'Homepage Widgets',
         'id' => 'homepage-widgets',
         'before_widget' => '<div class="widget">',
         'after_widget' => '</div>',
     ));
 }
 add_action('widgets_init', 'my_widgets_init');

 // Custom logo support
 add_theme_support('custom-logo', array(
     'height' => 100,
     'width' => 400,
     'flex-height' => true,
     'flex-width' => true,
 ));

 // Gutenberg support
 add_theme_support('align-wide');
 add_theme_support('editor-styles');
 add_theme_support('wp-block-styles');
 ```

 ## 🔧 Troubleshooting Commands

 ```bash
 # Check if Docker containers are running
 docker ps | grep wp-

 # View Docker logs
 docker-compose logs wordpress

 # Restart containers
 docker-compose restart

 # Access MySQL directly
 docker exec -it wp-mysql mysql -u wordpress -pwordpress_password wordpress

 # Check droplet status
 cat .droplet_info | python3 -m json.tool

 # SSH to droplet
 ssh -i ~/.ssh/wordpress_deploy root@$(cat .droplet_info | python3 -c "import
 json,sys; print(json.load(sys.stdin)['ip_address'])")

 # View WordPress error logs on droplet
 ssh -i ~/.ssh/wordpress_deploy root@YOUR_IP "tail -f /var/log/apache2/error.log"

 # Check cloud-init status
 ssh -i ~/.ssh/wordpress_deploy root@YOUR_IP "cloud-init status"

 # Delete droplet (cleanup)
 python3 -c "
 import requests, json, os
 api_token = os.getenv('DO_API_TOKEN')
 with open('.droplet_info') as f:
     droplet_id = json.load(f)['droplet_id']
 headers = {'Authorization': f'Bearer {api_token}'}
 response =
 requests.delete(f'https://api.digitalocean.com/v2/droplets/{droplet_id}',
 headers=headers)
 print('Droplet deleted' if response.status_code == 204 else 'Failed')
 "
 ```

 ### 🚨 Fixing 404 Errors on Pages

 If you encounter 404 errors on pages after deployment, the scripts now handle this
 automatically. However, if you still have issues:

 ```bash
 # SSH to droplet
 ssh -i ~/.ssh/wordpress_deploy root@YOUR_IP

 # Check if permalinks are set correctly
 wp --allow-root rewrite structure
 
 # Manually set permalinks and flush
 wp --allow-root rewrite structure '/%postname%/'
 wp --allow-root rewrite flush

 # Verify Apache configuration
 cat /etc/apache2/sites-enabled/wordpress.conf
 # Should show: AllowOverride All

 # Check .htaccess exists and is correct
 cat /var/www/html/.htaccess
 
 # Restart Apache
 systemctl restart apache2
 ```

 **Note:** The deployment scripts now automatically:
 - Install WP-CLI on the server
 - Configure Apache with AllowOverride All
 - Set permalinks to /%postname%/
 - Create proper .htaccess file
 - Flush rewrite rules after migration

 ## 📊 Production Deployment Checklist

 Before deploying to production:

 1. ✅ Update passwords in wp-config.php
 2. ✅ Set WP_DEBUG to false
 3. ✅ Update salts (automatic during migration)
 4. ✅ Install SSL certificate (certbot --apache)
 5. ✅ Configure domain DNS
 6. ✅ Enable firewall (ufw)
 7. ✅ Set up backups
 8. ✅ Configure email settings

 ## 🎯 Complete Workflow Summary

 1. **Clone repo** → Get complete WordPress development environment
 2. **Docker up** → Local WordPress running instantly
 3. **Develop** → Theme, plugins, content - everything
 4. **Setup SSH** → One-time automated key configuration
 5. **Create droplet** → Automated via API with WordPress installation
 6. **Migrate** → Transfer everything to production
 7. **Point domain** → Update DNS A record
 8. **SSL** → Run certbot for HTTPS
 9. **Live** → Production WordPress site running!

 ## 💡 Key Features This Provides

 - **Zero DevOps knowledge required** - Just need DO API token
 - **Perfect environment parity** - Docker matches production exactly
 - **Complete WordPress control** - Full admin access, all features
 - **Real VPS** - Not shared hosting, full server control
 - **One-command deployment** - Actually automated, not marketing speak
 - **Cost effective** - $6/month for production site
 - **No vendor lock-in** - Standard WordPress on standard Ubuntu
 - **Version controlled** - Everything in Git
 - **Instant local development** - Changes visible immediately
 - **Professional workflow** - Local → Staging → Production capable

 ## 🚨 Important Notes

 - Always test locally before deploying
 - Keep backups of production database
 - Use strong passwords in production
 - Update WordPress, themes, and plugins regularly
 - Monitor server resources on Digital Ocean
 - The migration script replaces the entire WordPress installation
 - Custom plugins/themes in wp-content are preserved
 - Database is completely replaced with local version

 ## 🔄 Updating Production Site

 To update your production site after local changes:

 ```bash
 # Make changes locally
 # Test everything at http://localhost

 # Re-run migration to update production
 ./migrate_now.sh

 # Your production site is now updated with all local changes
 ```

 This is a complete local-to-production WordPress development and deployment
 pipeline that doesn't exist anywhere else in this form!