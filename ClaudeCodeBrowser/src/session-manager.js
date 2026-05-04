import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * SessionManager - Handles session persistence and state management
 */
export class SessionManager {
  constructor(sessionsDir = null) {
    this.sessionsDir = sessionsDir || path.join(__dirname, '..', 'sessions');
    this._ensureSessionsDir();
  }

  async _ensureSessionsDir() {
    try {
      await fs.access(this.sessionsDir);
    } catch {
      await fs.mkdir(this.sessionsDir, { recursive: true });
    }
  }

  /**
   * Save session state
   */
  async save(name, data) {
    await this._ensureSessionsDir();

    const session = {
      name,
      savedAt: new Date().toISOString(),
      url: data.url,
      cookies: data.cookies,
      history: data.history,
      viewport: data.viewport,
      userAgent: data.userAgent,
      metadata: data.metadata || {}
    };

    const filename = path.join(this.sessionsDir, `${name}.json`);
    await fs.writeFile(filename, JSON.stringify(session, null, 2));

    return { success: true, filename, session };
  }

  /**
   * Load session state
   */
  async load(name) {
    const filename = path.join(this.sessionsDir, `${name}.json`);

    try {
      const content = await fs.readFile(filename, 'utf-8');
      const session = JSON.parse(content);
      return session;
    } catch (error) {
      throw new Error(`Session "${name}" not found`);
    }
  }

  /**
   * List all saved sessions
   */
  async list() {
    await this._ensureSessionsDir();

    try {
      const files = await fs.readdir(this.sessionsDir);
      const sessions = [];

      for (const file of files) {
        if (file.endsWith('.json')) {
          const content = await fs.readFile(
            path.join(this.sessionsDir, file),
            'utf-8'
          );
          const session = JSON.parse(content);
          sessions.push({
            name: session.name,
            savedAt: session.savedAt,
            url: session.url
          });
        }
      }

      return sessions;
    } catch {
      return [];
    }
  }

  /**
   * Delete a session
   */
  async delete(name) {
    const filename = path.join(this.sessionsDir, `${name}.json`);

    try {
      await fs.unlink(filename);
      return { success: true };
    } catch {
      throw new Error(`Session "${name}" not found`);
    }
  }

  /**
   * Delete all sessions
   */
  async deleteAll() {
    await this._ensureSessionsDir();

    const files = await fs.readdir(this.sessionsDir);
    let deleted = 0;

    for (const file of files) {
      if (file.endsWith('.json')) {
        await fs.unlink(path.join(this.sessionsDir, file));
        deleted++;
      }
    }

    return { success: true, deleted };
  }

  /**
   * Export session to apply to browser
   */
  async exportForBrowser(name) {
    const session = await this.load(name);

    return {
      url: session.url,
      cookies: session.cookies,
      viewport: session.viewport,
      userAgent: session.userAgent
    };
  }

  /**
   * Create session from browser state
   */
  async createFromBrowser(name, browser) {
    const url = await browser.getCurrentUrl();
    const cookies = await browser.getCookies();
    const history = browser.getHistory();

    return await this.save(name, {
      url,
      cookies,
      history,
      viewport: browser.options.viewport,
      userAgent: browser.options.userAgent
    });
  }
}

export default new SessionManager();
