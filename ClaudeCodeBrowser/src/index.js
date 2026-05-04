/**
 * Agent Browser - Main Export
 *
 * A headless browser designed for AI agents
 */

export { AgentBrowser } from './browser.js';
export { AgentFormatter } from './agent-formatter.js';
export { SessionManager } from './session-manager.js';

// Re-export default instances
import agentFormatter from './agent-formatter.js';
import sessionManager from './session-manager.js';

export const formatter = agentFormatter;
export const sessions = sessionManager;

// Version
export const VERSION = '1.0.0';
