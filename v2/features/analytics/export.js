/**
 * Analytics Export - Export analytics data
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../../core/event-bus.js';
import { AnalyticsTracker } from './tracker.js';

class AnalyticsExport {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {AnalyticsExport}
     */
    static getInstance() {
        if (!AnalyticsExport.#instance) {
            AnalyticsExport.#instance = new AnalyticsExport();
        }
        return AnalyticsExport.#instance;
    }

    constructor() {
        if (AnalyticsExport.#instance) {
            return AnalyticsExport.#instance;
        }

        this.events = EventBus.getInstance();
        this.tracker = AnalyticsTracker.getInstance();
    }

    /**
     * Export analytics to JSON
     * @param {Object} options
     * @returns {Object}
     */
    toJSON(options = {}) {
        const {
            includeEvents = true,
            includeSummary = true,
            includeUsage = true,
            dateRange = null
        } = options;

        const data = {
            exportedAt: new Date().toISOString(),
            version: 1,
            source: 'Local First Tools v2'
        };

        if (includeSummary) {
            data.summary = this.tracker.getSummary();
        }

        if (includeUsage) {
            data.toolUsage = this.tracker.getToolUsage();
            data.categoryUsage = this.tracker.getCategoryUsage();
        }

        if (includeEvents) {
            let events = this.tracker.getEvents();

            if (dateRange) {
                const { start, end } = dateRange;
                events = events.filter(e =>
                    e.timestamp >= start.getTime() &&
                    e.timestamp <= end.getTime()
                );
            }

            data.events = events;
            data.eventCount = events.length;
        }

        return data;
    }

    /**
     * Export analytics to CSV
     * @param {Object} options
     * @returns {string}
     */
    toCSV(options = {}) {
        const {
            type = 'events', // 'events', 'usage', 'summary'
            dateRange = null
        } = options;

        switch (type) {
            case 'events':
                return this.#eventsToCSV(dateRange);
            case 'usage':
                return this.#usageToCSV();
            case 'summary':
                return this.#summaryToCSV();
            default:
                return this.#eventsToCSV(dateRange);
        }
    }

    /**
     * Export events to CSV
     * @param {Object} dateRange
     * @returns {string}
     */
    #eventsToCSV(dateRange) {
        let events = this.tracker.getEvents();

        if (dateRange) {
            const { start, end } = dateRange;
            events = events.filter(e =>
                e.timestamp >= start.getTime() &&
                e.timestamp <= end.getTime()
            );
        }

        const headers = ['Timestamp', 'Event Type', 'Tool ID', 'Tool Title', 'Category', 'Details'];
        const rows = events.map(e => [
            new Date(e.timestamp).toISOString(),
            e.type,
            e.toolId || '',
            e.toolTitle || '',
            e.category || '',
            JSON.stringify(e.data || {})
        ]);

        return this.#arrayToCSV([headers, ...rows]);
    }

    /**
     * Export usage to CSV
     * @returns {string}
     */
    #usageToCSV() {
        const usage = this.tracker.getToolUsage();

        const headers = ['Tool ID', 'Title', 'Category', 'Open Count', 'Last Opened'];
        const rows = Object.entries(usage).map(([id, data]) => [
            id,
            data.title || '',
            data.category || '',
            data.count || 0,
            data.lastOpened ? new Date(data.lastOpened).toISOString() : ''
        ]);

        return this.#arrayToCSV([headers, ...rows]);
    }

    /**
     * Export summary to CSV
     * @returns {string}
     */
    #summaryToCSV() {
        const summary = this.tracker.getSummary();

        const headers = ['Metric', 'Value'];
        const rows = Object.entries(summary).map(([key, value]) => [
            this.#formatMetricName(key),
            typeof value === 'object' ? JSON.stringify(value) : value
        ]);

        return this.#arrayToCSV([headers, ...rows]);
    }

    /**
     * Convert array to CSV string
     * @param {Array} data
     * @returns {string}
     */
    #arrayToCSV(data) {
        return data.map(row =>
            row.map(cell => {
                const str = String(cell);
                // Escape quotes and wrap in quotes if contains comma, quote, or newline
                if (str.includes(',') || str.includes('"') || str.includes('\n')) {
                    return `"${str.replace(/"/g, '""')}"`;
                }
                return str;
            }).join(',')
        ).join('\n');
    }

    /**
     * Format metric name
     * @param {string} name
     * @returns {string}
     */
    #formatMetricName(name) {
        return name
            .replace(/([A-Z])/g, ' $1')
            .replace(/^./, str => str.toUpperCase())
            .trim();
    }

    /**
     * Download JSON export
     * @param {Object} options
     */
    downloadJSON(options = {}) {
        const data = this.toJSON(options);
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        this.#download(blob, `analytics-${this.#getDateStamp()}.json`);
    }

    /**
     * Download CSV export
     * @param {Object} options
     */
    downloadCSV(options = {}) {
        const csv = this.toCSV(options);
        const blob = new Blob([csv], { type: 'text/csv' });
        const type = options.type || 'events';
        this.#download(blob, `analytics-${type}-${this.#getDateStamp()}.csv`);
    }

    /**
     * Download blob
     * @param {Blob} blob
     * @param {string} filename
     */
    #download(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.events.emit(EVENTS.NOTIFICATION, {
            message: `Exported ${filename}`,
            type: 'success'
        });
    }

    /**
     * Get date stamp for filenames
     * @returns {string}
     */
    #getDateStamp() {
        return new Date().toISOString().split('T')[0];
    }

    /**
     * Generate report
     * @param {Object} options
     * @returns {Object}
     */
    generateReport(options = {}) {
        const {
            dateRange = null,
            format = 'object'
        } = options;

        const summary = this.tracker.getSummary();
        const usage = this.tracker.getToolUsage();
        const categoryUsage = this.tracker.getCategoryUsage();

        // Calculate top tools
        const topTools = Object.entries(usage)
            .sort((a, b) => (b[1].count || 0) - (a[1].count || 0))
            .slice(0, 10)
            .map(([id, data]) => ({
                id,
                title: data.title,
                count: data.count
            }));

        // Calculate top categories
        const topCategories = Object.entries(categoryUsage)
            .sort((a, b) => (b[1].count || 0) - (a[1].count || 0))
            .slice(0, 5)
            .map(([category, data]) => ({
                category,
                count: data.count
            }));

        // Get event distribution
        let events = this.tracker.getEvents();
        if (dateRange) {
            const { start, end } = dateRange;
            events = events.filter(e =>
                e.timestamp >= start.getTime() &&
                e.timestamp <= end.getTime()
            );
        }

        const eventTypes = {};
        for (const event of events) {
            eventTypes[event.type] = (eventTypes[event.type] || 0) + 1;
        }

        // Activity by day of week
        const dayActivity = [0, 0, 0, 0, 0, 0, 0];
        for (const event of events) {
            const day = new Date(event.timestamp).getDay();
            dayActivity[day]++;
        }

        // Activity by hour
        const hourActivity = Array(24).fill(0);
        for (const event of events) {
            const hour = new Date(event.timestamp).getHours();
            hourActivity[hour]++;
        }

        const report = {
            generatedAt: new Date().toISOString(),
            period: dateRange ? {
                start: dateRange.start.toISOString(),
                end: dateRange.end.toISOString()
            } : 'all time',
            summary: {
                totalTools: summary.totalTools,
                totalOpens: summary.totalOpens,
                totalSearches: summary.totalSearches,
                uniqueToolsUsed: summary.uniqueToolsUsed,
                totalSessions: summary.totalSessions
            },
            topTools,
            topCategories,
            eventDistribution: eventTypes,
            activityByDayOfWeek: {
                sunday: dayActivity[0],
                monday: dayActivity[1],
                tuesday: dayActivity[2],
                wednesday: dayActivity[3],
                thursday: dayActivity[4],
                friday: dayActivity[5],
                saturday: dayActivity[6]
            },
            peakHour: hourActivity.indexOf(Math.max(...hourActivity)),
            totalEvents: events.length
        };

        if (format === 'html') {
            return this.#reportToHTML(report);
        }

        return report;
    }

    /**
     * Convert report to HTML
     * @param {Object} report
     * @returns {string}
     */
    #reportToHTML(report) {
        return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics Report - ${report.generatedAt}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background: #0a0a0a;
            color: #e5e5e5;
        }
        h1, h2, h3 { color: #fff; }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: #1a1a1a;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #60a5fa;
        }
        .stat-label { color: #888; font-size: 0.875rem; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 2rem;
        }
        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #333;
        }
        th { color: #888; }
        .footer { color: #666; font-size: 0.875rem; margin-top: 2rem; }
    </style>
</head>
<body>
    <h1>Analytics Report</h1>
    <p>Generated: ${new Date(report.generatedAt).toLocaleString()}</p>
    <p>Period: ${typeof report.period === 'string' ? report.period : `${new Date(report.period.start).toLocaleDateString()} - ${new Date(report.period.end).toLocaleDateString()}`}</p>

    <h2>Summary</h2>
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-value">${report.summary.totalOpens}</div>
            <div class="stat-label">Total Opens</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${report.summary.uniqueToolsUsed}</div>
            <div class="stat-label">Unique Tools</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${report.summary.totalSearches}</div>
            <div class="stat-label">Searches</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${report.summary.totalSessions}</div>
            <div class="stat-label">Sessions</div>
        </div>
    </div>

    <h2>Top Tools</h2>
    <table>
        <thead><tr><th>#</th><th>Tool</th><th>Opens</th></tr></thead>
        <tbody>
            ${report.topTools.map((t, i) => `
                <tr><td>${i + 1}</td><td>${t.title || t.id}</td><td>${t.count}</td></tr>
            `).join('')}
        </tbody>
    </table>

    <h2>Top Categories</h2>
    <table>
        <thead><tr><th>#</th><th>Category</th><th>Opens</th></tr></thead>
        <tbody>
            ${report.topCategories.map((c, i) => `
                <tr><td>${i + 1}</td><td>${c.category}</td><td>${c.count}</td></tr>
            `).join('')}
        </tbody>
    </table>

    <h2>Activity by Day</h2>
    <table>
        <thead><tr><th>Day</th><th>Events</th></tr></thead>
        <tbody>
            ${Object.entries(report.activityByDayOfWeek).map(([day, count]) => `
                <tr><td>${day.charAt(0).toUpperCase() + day.slice(1)}</td><td>${count}</td></tr>
            `).join('')}
        </tbody>
    </table>

    <p>Peak activity hour: ${report.peakHour}:00</p>

    <div class="footer">
        <p>Local First Tools v2 Analytics Export</p>
    </div>
</body>
</html>
        `;
    }

    /**
     * Download HTML report
     * @param {Object} options
     */
    downloadReport(options = {}) {
        const html = this.generateReport({ ...options, format: 'html' });
        const blob = new Blob([html], { type: 'text/html' });
        this.#download(blob, `analytics-report-${this.#getDateStamp()}.html`);
    }
}

export { AnalyticsExport };
