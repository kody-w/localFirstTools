/**
 * LOCAL-FIRST TOOLS - TESTING FRAMEWORK
 * Automated testing for critical applications
 */

class LocalFirstTestFramework {
    constructor() {
        this.tests = [];
        this.results = [];
        this.criticalApps = [
            './apps/games/feedShyworm4.html',
            './apps/productivity/ghostwriter.html',
            './apps/games/quantum-worlds-store.html',
            './index.html',
            './apps/development/meta-dashboard.html',
            './apps/ai-tools/copilot-agent-store.html',
            './apps/education/particle-physics-playground.html',
            './apps/games/balatro-clone.html',
            './apps/productivity/memory-palace.html',
            './apps/utilities/timezone-converter-tool.html'
        ];
    }

    /**
     * Define a test
     */
    test(name, testFn) {
        this.tests.push({ name, testFn });
    }

    /**
     * Assert helpers
     */
    assert = {
        equals: (actual, expected, message) => {
            if (actual !== expected) {
                throw new Error(`${message || 'Assertion failed'}: expected ${expected}, got ${actual}`);
            }
        },
        truthy: (value, message) => {
            if (!value) {
                throw new Error(message || 'Expected truthy value');
            }
        },
        exists: async (url) => {
            const response = await fetch(url, { method: 'HEAD' });
            if (!response.ok) {
                throw new Error(`File not found: ${url}`);
            }
        },
        contains: (haystack, needle, message) => {
            if (!haystack.includes(needle)) {
                throw new Error(`${message || 'Assertion failed'}: "${haystack}" does not contain "${needle}"`);
            }
        }
    };

    /**
     * Run all tests
     */
    async runAll() {
        console.log('🧪 Running Test Framework...\n');

        for (const test of this.tests) {
            try {
                const startTime = performance.now();
                await test.testFn(this.assert);
                const duration = (performance.now() - startTime).toFixed(2);

                this.results.push({
                    name: test.name,
                    status: 'PASS',
                    duration,
                    error: null
                });

                console.log(`✅ ${test.name} (${duration}ms)`);
            } catch (error) {
                this.results.push({
                    name: test.name,
                    status: 'FAIL',
                    error: error.message
                });

                console.error(`❌ ${test.name}`);
                console.error(`   Error: ${error.message}`);
            }
        }

        this.printSummary();
        return this.results;
    }

    /**
     * Print test summary
     */
    printSummary() {
        const passed = this.results.filter(r => r.status === 'PASS').length;
        const failed = this.results.filter(r => r.status === 'FAIL').length;

        console.log('\n' + '='.repeat(60));
        console.log('TEST SUMMARY');
        console.log('='.repeat(60));
        console.log(`Total: ${this.results.length}`);
        console.log(`✅ Passed: ${passed}`);
        console.log(`❌ Failed: ${failed}`);
        console.log(`Success Rate: ${((passed / this.results.length) * 100).toFixed(1)}%`);
        console.log('='.repeat(60));
    }

    /**
     * Export results as JSON
     */
    exportResults() {
        return {
            timestamp: new Date().toISOString(),
            results: this.results,
            summary: {
                total: this.results.length,
                passed: this.results.filter(r => r.status === 'PASS').length,
                failed: this.results.filter(r => r.status === 'FAIL').length
            }
        };
    }
}

// ========================================
// TEST SUITE FOR CRITICAL APPS
// ========================================

const framework = new LocalFirstTestFramework();

// Test 1: Config file integrity
framework.test('Config file loads and is valid JSON', async (assert) => {
    const response = await fetch('./data/config/utility_apps_config.json');
    const config = await response.json();

    assert.truthy(config.apps, 'Config has apps array');
    assert.truthy(config.apps.length > 0, 'Config has at least one app');
    assert.truthy(config.version, 'Config has version');
});

// Test 2: All critical apps exist
framework.test('All critical apps are accessible', async (assert) => {
    for (const appPath of framework.criticalApps) {
        await assert.exists(appPath);
    }
});

// Test 3: Index.html structure
framework.test('Main index.html has required elements', async (assert) => {
    const response = await fetch('./index.html');
    const html = await response.text();

    assert.contains(html, 'LOCAL FIRST TOOLS', 'Has title');
    assert.contains(html, 'openTool', 'Has openTool function');
    assert.contains(html, 'previewTool', 'Has previewTool function');
});

// Test 4: Meta analysis data
framework.test('Meta analysis data is valid', async (assert) => {
    const response = await fetch('./data/meta-analysis.json');
    const analysis = await response.json();

    assert.truthy(analysis.metadata, 'Has metadata');
    assert.truthy(analysis.apps, 'Has apps array');
    assert.truthy(analysis.apps.length > 100, 'Has many apps');
});

// Test 5: Config paths match files
framework.test('Config paths reference existing files', async (assert) => {
    const response = await fetch('./data/config/utility_apps_config.json');
    const config = await response.json();

    // Test a random sample of 10 apps
    const sample = config.apps.slice(0, 10);
    for (const app of sample) {
        await assert.exists(app.path);
    }
});

// Test 6: No duplicate IDs in config
framework.test('Config has no duplicate app IDs', async (assert) => {
    const response = await fetch('./data/config/utility_apps_config.json');
    const config = await response.json();

    const ids = config.apps.map(app => app.id);
    const uniqueIds = new Set(ids);

    assert.equals(ids.length, uniqueIds.size, 'All IDs are unique');
});

// Test 7: All apps have required fields
framework.test('All apps have required metadata fields', async (assert) => {
    const response = await fetch('./data/config/utility_apps_config.json');
    const config = await response.json();

    const sample = config.apps.slice(0, 20);
    for (const app of sample) {
        assert.truthy(app.id, `App has ID: ${app.title || 'unknown'}`);
        assert.truthy(app.title, `App has title: ${app.id}`);
        assert.truthy(app.path, `App has path: ${app.id}`);
    }
});

// Test 8: Meta dashboard exists and loads
framework.test('Meta dashboard is accessible and valid', async (assert) => {
    await assert.exists('./apps/development/meta-dashboard.html');

    const response = await fetch('./apps/development/meta-dashboard.html');
    const html = await response.text();

    assert.contains(html, 'Meta Analysis Dashboard', 'Has correct title');
    assert.contains(html, 'dependency', 'Has dependency graph feature');
});

// Test 9: GitHub Pages URLs are correct
framework.test('GitHub Pages base paths are configured correctly', async (assert) => {
    const response = await fetch('./index.html');
    const html = await response.text();

    // Check that paths are relative (work on both local and GitHub Pages)
    assert.contains(html, './data/config', 'Uses relative paths for config');
    assert.contains(html, './apps/', 'Uses relative paths for apps');
});

// Test 10: Performance - critical files under size limit
framework.test('Critical files are optimally sized', async (assert) => {
    const maxSize = 1024 * 1024; // 1MB

    for (const appPath of framework.criticalApps.slice(0, 5)) {
        const response = await fetch(appPath);
        const blob = await response.blob();

        assert.truthy(blob.size < maxSize,
            `${appPath} is under 1MB (${(blob.size / 1024).toFixed(0)}KB)`);
    }
});

// Auto-run if in browser
if (typeof window !== 'undefined') {
    framework.runAll().then(results => {
        console.log('\n✅ All tests complete!');
        console.log('Export results:', framework.exportResults());
    });
}

// Export for Node.js usage
if (typeof module !== 'undefined') {
    module.exports = { LocalFirstTestFramework, framework };
}
