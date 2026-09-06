// Requires test-only Playwright on NODE_PATH and its Chromium installation.
// Run: node scripts/tests/p2p-proof.cjs [test-name-pattern]
// Optional P2P_PROOF_ARTIFACTS writes before/after live screenshots to a local directory.
// Every pair uses the real public PeerJS broker and native WebRTC. Only the
// named failure/coordinate cases replace responses or APIs; the live test does not.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const file = path.resolve(__dirname, '../../apps/quantum-worlds/p2p-proof.html');
const url = pathToFileURL(file).href;
const IPAPI = 'https://ipapi.co/json/';
const CDN = 'https://cdn.jsdelivr.net/npm/peerjs@1.5.2/dist/peerjs.min.js';
const unavailable = 'unavailable (lookup failed — not fabricated)';
const originFixture = { latitude: 0, longitude: 0 };
const quarterEarthFixture = { latitude: 0, longitude: 90 };
const tests = [];
const test = (name, run) => tests.push({ name, run });
const text = (page, id) => page.locator('#' + id).textContent();
const count = async page => Number(await text(page, 'msg-count'));
const waitText = (page, id, pattern) => page.waitForFunction(
    ({ id, pattern }) => new RegExp(pattern).test(document.getElementById(id).textContent),
    { id, pattern }, { timeout: 25000 },
);

async function online(page) {
    await page.waitForFunction(() => !document.getElementById('copy-btn').disabled, null, { timeout: 25000 });
    const link = await page.locator('#share-link').inputValue();
    assert.equal(new URL(link).searchParams.get('peer'), await text(page, 'my-id'));
    return link;
}

async function settled(a, b) {
    await Promise.all([a, b].map(page => waitText(page, 'status', 'connected — verified direct')));
    await Promise.all([a, b].map(page => page.waitForFunction(() =>
        document.getElementById('my-loc').textContent !== 'looking up…'
        && !['looking up…', 'no peer connected'].includes(document.getElementById('peer-loc').textContent))));
    // Initial hello/location updates must settle before measuring pointer-only traffic.
    await b.waitForTimeout(150);
}

async function drag(page, x, y, steps = 8, { cancel = false, button = 'left' } = {}) {
    await page.locator('#surface').scrollIntoViewIfNeeded();
    const me = await page.locator('#dot-me').boundingBox();
    const surface = await page.locator('#surface').boundingBox();
    assert.ok(me && surface);
    await page.mouse.move(me.x + me.width / 2, me.y + me.height / 2);
    await page.mouse.down({ button });
    if (cancel) await page.locator('#dot-me').dispatchEvent('pointercancel', { pointerId: 1, pointerType: 'mouse' });
    await page.mouse.move(surface.x + surface.width * x, surface.y + surface.height * y, { steps });
    await page.mouse.up({ button });
}

async function samePosition(sender, receiver) {
    const expected = await sender.locator('#dot-me').evaluate(el => ({ x: parseFloat(el.style.left), y: parseFloat(el.style.top) }));
    await receiver.waitForFunction(({ x, y }) => {
        const el = document.getElementById('dot-peer');
        return !el.hidden && Math.abs(parseFloat(el.style.left) - x) < 0.1 && Math.abs(parseFloat(el.style.top) - y) < 0.1;
    }, expected);
    await waitText(receiver, 'latency', '^-?\\d+ ms$');
}

async function movement(sender, receiver, x, y, steps = 8) {
    const before = await receiver.locator('#dot-peer').boundingBox();
    const counts = await Promise.all([count(sender), count(receiver)]);
    await drag(sender, x, y, steps);
    await samePosition(sender, receiver);
    await receiver.waitForFunction(min => Number(document.getElementById('msg-count').textContent) >= min, counts[1] + steps);
    const after = await receiver.locator('#dot-peer').boundingBox();
    const finalCounts = await Promise.all([count(sender), count(receiver)]);
    assert.ok(before && after && Math.hypot(after.x - before.x, after.y - before.y) > 20, 'visible peer dot must actually move');
    assert.deepEqual(finalCounts.map((n, i) => n - counts[i]), [steps, steps]);
    return {
        pointerMoves: steps,
        peerPixels: [before.x, before.y, after.x, after.y].map(n => Math.round(n * 100) / 100),
        delay: await text(receiver, 'latency'),
        counters: counts.map((n, i) => `${n}->${finalCounts[i]}`),
    };
}

async function rtcEvidence(page) {
    return page.evaluate(async () => {
        const pc = conn.channel.peerConnection;
        const stats = await pc.getStats();
        const entries = [...stats.values()];
        const transport = entries.find(s => s.type === 'transport' && s.selectedCandidatePairId);
        const pair = stats.get(transport.selectedCandidatePairId);
        const local = stats.get(pair.localCandidateId);
        const remote = stats.get(pair.remoteCandidateId);
        const data = entries.find(s => s.type === 'data-channel' && s.state === 'open');
        return {
            candidates: [local.candidateType, remote.candidateType],
            iceServers: pc.getConfiguration().iceServers.flatMap(s => s.urls),
            dataChannel: { messagesSent: data.messagesSent, messagesReceived: data.messagesReceived },
        };
    });
}

test('live public broker: two file:// contexts, real drag, then signaling disconnected', async t => {
    const a = await t.open({ geo: 'live', allowIpapiDiagnostics: true });
    const link = await online(a.page);
    const b = await t.open({ href: link, geo: 'live', allowIpapiDiagnostics: true });
    await settled(a.page, b.page);
    if (process.env.P2P_PROOF_ARTIFACTS) {
        await b.page.screenshot({ path: path.join(process.env.P2P_PROOF_ARTIFACTS, 'peer-before.png'), fullPage: true });
    }
    const forward = await movement(a.page, b.page, 0.55, 0.27);
    if (process.env.P2P_PROOF_ARTIFACTS) {
        await b.page.screenshot({ path: path.join(process.env.P2P_PROOF_ARTIFACTS, 'peer-after.png'), fullPage: true });
    }
    const evidence = await Promise.all([rtcEvidence(a.page), rtcEvidence(b.page)]);
    for (const [i, rtc] of evidence.entries()) {
        assert.ok(rtc.candidates.every(type => ['host', 'srflx', 'prflx'].includes(type)));
        assert.ok(rtc.iceServers.every(server => server.startsWith('stun:')));
        assert.ok(rtc.dataChannel.messagesSent > 0 && rtc.dataChannel.messagesReceived > 0);
        assert.equal(rtc.dataChannel.messagesSent + rtc.dataChannel.messagesReceived, await count([a.page, b.page][i]));
    }
    for (const { page } of [a, b]) {
        if (await text(page, 'my-loc') === unavailable) assert.equal(await text(page, 'distance'), '—');
        else assert.match(await text(page, 'distance'), /^[\d,]+ km$|^—$/);
        if ((await text(page, 'peer-loc')).startsWith('unavailable')) {
            assert.equal(await page.locator('#peer-loc').getAttribute('class'), 'v bad');
        }
    }
    await Promise.all([a.page, b.page].map(page => page.evaluate(() => peer.disconnect())));
    await Promise.all([a.page, b.page].map(page => waitText(page, 'status', 'signaling offline')));
    for (const item of [a, b]) {
        await Promise.all(item.sockets.filter(socket => !socket.isClosed()).map(socket => socket.waitForEvent('close')));
        assert.ok(item.sockets.every(socket => socket.isClosed()), 'signaling sockets must really be closed');
        await item.context.route('https://**/*', route => route.abort('aborted'));
    }
    const reverse = await movement(b.page, a.page, 0.82, 0.70);
    return { forward, signalingDisconnectedReverse: reverse, rtc: evidence, liveLocation: await text(a.page, 'my-loc') === unavailable ? 'ipapi unavailable; no invented distance' : 'real API response' };
});

test('late IP lookup, zero coordinates, initial dot sync, and real haversine DOM', async t => {
    const a = await t.open({ geoValue: originFixture });
    const b = await t.open({ href: await online(a.page), geo: 'pending' });
    await Promise.all([a.page, b.page].map(page => waitText(page, 'status', 'connected — verified direct')));
    assert.equal(await text(b.page, 'my-loc'), 'looking up…', 'lookup must not block the connection');
    assert.equal(await text(a.page, 'peer-loc'), 'looking up…');
    assert.equal(await a.page.locator('#peer-loc').getAttribute('class'), 'v pending');
    assert.equal(await text(a.page, 'my-loc'), '0.000°, 0.000°');
    await b.geoRoute().fulfill({ json: quarterEarthFixture });
    await settled(a.page, b.page);
    const distances = await Promise.all([text(a.page, 'distance'), text(b.page, 'distance')]);
    assert.deepEqual(distances.map(s => Number(s.replace(/[^\d]/g, ''))), [10008, 10008]);
    const own = await a.page.locator('#dot-me').boundingBox();
    const remote = await b.page.locator('#dot-peer').boundingBox();
    assert.ok(Math.abs(own.x - remote.x) < 1, 'initial remote dot must reflect the actual local dot, not a made-up position');
    assert.equal(await a.page.evaluate(() => haversineKm({ lat: 27.2046, lon: 19.3368 }, { lat: -27.2046, lon: -160.6632 })), 20015);
    return { distances, zeroCoordinateAccepted: true, connectedBeforeLookup: true, initialDotSynced: true, antipodesKm: 20015 };
});

test('geolocation route.abort: exact honest fallback, no coordinates, clean console', async t => {
    const { page } = await t.open({ geo: 'abort' });
    await online(page);
    assert.equal(await text(page, 'my-loc'), unavailable);
    assert.equal(await text(page, 'distance'), '—');
    assert.equal(await count(page), 0);
    return { location: await text(page, 'my-loc'), distance: '—', messages: 0 };
});

test('malformed ipapi responses and denied localStorage stay usable', async t => {
    const values = [null, [], {}, { error: true, ...originFixture }, { latitude: '0', longitude: 1 },
        { latitude: 91, longitude: 1 }, { latitude: 1, longitude: -181 }, { latitude: null, longitude: 1 }];
    for (const geoValue of values) {
        const { page, context } = await t.open({
            geoValue,
            init: () => Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('TEST denied', 'SecurityError'); } }),
        });
        await waitText(page, 'my-loc', '^unavailable');
        assert.equal(await text(page, 'my-loc'), unavailable);
        assert.equal(await text(page, 'distance'), '—');
        assert.ok(await page.locator('#dot-me').isVisible());
        await context.close();
    }
    return { invalidResponsesRejected: values.length, storageDenied: 'no access required' };
});

test('hanging geolocation times out without blocking a live peer ID', async t => {
    const { page } = await t.open({ geo: 'pending' });
    await online(page);
    assert.equal(await text(page, 'my-loc'), 'looking up…');
    await waitText(page, 'my-loc', '^unavailable');
    assert.equal(await text(page, 'my-loc'), unavailable);
    return { peerOnlineBeforeLookup: true, location: await text(page, 'my-loc') };
});

test('blocked and stalled CDN: visible failure and usable offline dot', async t => {
    const statuses = [];
    for (const cdn of ['abort', 'pending', 'empty']) {
        const { page } = await t.open({ cdn });
        await waitText(page, 'status', 'PeerJS (unavailable|CDN timed out|CDN did not provide)');
        assert.ok(await page.locator('#copy-btn').isDisabled());
        assert.equal(await page.locator('#share-link').inputValue(), '');
        assert.equal(await text(page, 'my-id'), 'unavailable (not registered)');
        const before = await page.locator('#dot-me').boundingBox();
        await drag(page, 0.65, 0.25);
        const after = await page.locator('#dot-me').boundingBox();
        assert.ok(Math.abs(after.x - before.x) > 20);
        assert.equal(await count(page), 0);
        statuses.push(await text(page, 'status'));
    }
    return { statuses, offlineDrag: true, pageAndConsoleErrors: 0 };
});

test('clipboard absent, incomplete, throwing, rejected, false, and acknowledged', async t => {
    const { page } = await t.open();
    await online(page);
    const cases = ['absent', 'missing-method', 'getter-throws', 'method-throws', 'rejected', 'false'];
    for (const variant of cases) {
        await page.evaluate(variant => {
            let value;
            if (variant === 'missing-method') value = {};
            if (variant === 'method-throws') value = { writeText() { throw new Error('TEST denied'); } };
            if (variant === 'rejected') value = { writeText() { return Promise.reject(new Error('TEST denied')); } };
            if (variant === 'false') value = { writeText() { return false; } };
            const descriptor = variant === 'getter-throws'
                ? { get() { throw new DOMException('TEST denied', 'SecurityError'); } } : { value };
            Object.defineProperty(navigator, 'clipboard', { configurable: true, ...descriptor });
        }, variant);
        await page.locator('#copy-btn').click();
        await waitText(page, 'copy-status', '^Clipboard unavailable');
        assert.match(await text(page, 'copy-status'), /link selected; copy it manually/);
    }
    await page.evaluate(() => {
        document.getElementById('copy-status').textContent = '';
        Object.defineProperty(navigator, 'clipboard', { configurable: true, value: {
            writeText(value) { window.__copyValue = value; return new Promise(resolve => { window.__ackCopy = resolve; }); },
        } });
    });
    await page.locator('#copy-btn').click();
    assert.equal(await text(page, 'copy-status'), '', 'a pending write is not a success');
    assert.equal(await page.evaluate(() => window.__copyValue), await page.locator('#share-link').inputValue());
    await page.evaluate(() => window.__ackCopy());
    await waitText(page, 'copy-status', '^Link copied\\.$');
    return { manualFallbacks: cases, copiedOnlyAfterAPIAcknowledgement: true };
});

test('WebRTC missing, signaling aborted, and invalid/absent target IDs fail honestly', async t => {
    const missing = await t.open({ init: () => {
        window.RTCPeerConnection = window.webkitRTCPeerConnection = window.mozRTCPeerConnection = undefined;
    } });
    await waitText(missing.page, 'status', 'WebRTC unavailable');
    const blocked = await t.open({ blockBroker: true });
    await waitText(blocked.page, 'status', 'signaling error');
    assert.equal(await blocked.page.locator('#share-link').inputValue(), '');
    const invalid = await t.open({ href: url + '?peer=bad%3Cpeer' });
    await waitText(invalid.page, 'status', 'invalid peer ID');
    const absent = await t.open({ href: url + '?peer=zero-proof-nobody-' + crypto.randomUUID() });
    await waitText(absent.page, 'status', 'peer-unavailable');
    for (const item of [missing, blocked, invalid, absent]) {
        assert.equal(await count(item.page), 0);
        assert.ok(await item.page.locator('#dot-peer').isHidden());
    }
    return { statuses: await Promise.all([missing, blocked, invalid, absent].map(item => text(item.page, 'status'))) };
});

test('real touch input sends once; cancellation, right-click, bounds, and resize', async t => {
    const a = await t.open({ geoValue: originFixture, viewport: { width: 390, height: 844 }, hasTouch: true });
    const b = await t.open({ href: await online(a.page), geoValue: quarterEarthFixture, viewport: { width: 390, height: 844 } });
    await settled(a.page, b.page);
    const initial = await a.page.locator('#dot-me').boundingBox();
    const before = await Promise.all([count(a.page), count(b.page)]);
    await drag(a.page, 0.6, 0.2, 1, { cancel: true });
    await drag(a.page, 0.8, 0.3, 1, { button: 'right' });
    assert.deepEqual(await a.page.locator('#dot-me').boundingBox(), initial);
    assert.deepEqual(await Promise.all([count(a.page), count(b.page)]), before);
    const cdp = await a.context.newCDPSession(a.page);
    const point = { x: initial.x + 11, y: initial.y + 11, id: 1 };
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [point] });
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ ...point, x: point.x + 70, y: point.y - 70 }] });
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await samePosition(a.page, b.page);
    assert.deepEqual((await Promise.all([count(a.page), count(b.page)])).map((n, i) => n - before[i]), [1, 1]);
    await drag(a.page, -0.2, -0.2, 1);
    await b.page.waitForTimeout(100);
    await a.page.setViewportSize({ width: 260, height: 844 });
    for (const [item, id] of [[a, 'dot-me'], [b, 'dot-peer']]) {
        // The viewport acknowledgement can precede the native resize event.
        await item.page.waitForFunction(id => {
            const dot = document.getElementById(id).getBoundingClientRect();
            const area = document.getElementById('surface').getBoundingClientRect();
            return dot.left >= area.left && dot.top >= area.top && dot.right <= area.right && dot.bottom <= area.bottom;
        }, id, { timeout: 2000 });
        const dot = await item.page.locator('#' + id).boundingBox();
        const area = await item.page.locator('#surface').boundingBox();
        assert.ok(dot.x >= area.x && dot.y >= area.y && dot.x + dot.width <= area.x + area.width && dot.y + dot.height <= area.y + area.height, JSON.stringify({ id, dot, area }));
        assert.ok(await item.page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
    }
    return { realTouchMessagesEach: 1, canceledAndSecondaryDragsSent: 0, smallViewportBounds: true };
});

test('malformed real data-channel frames cannot crash, corrupt distance, or show NaN', async t => {
    const a = await t.open({ geoValue: originFixture });
    const b = await t.open({ href: await online(a.page), geoValue: quarterEarthFixture });
    await settled(a.page, b.page);
    await movement(a.page, b.page, 0.55, 0.25, 1);
    const before = { dot: await b.page.locator('#dot-peer').boundingBox(), delay: await text(b.page, 'latency'), location: await text(b.page, 'peer-loc'), distance: await text(b.page, 'distance') };
    const received = await count(b.page);
    const invalid = ['null', '[]', '42', '{', 'x'.repeat(4096),
        JSON.stringify({ type: 'move', x: 45, y: 45, t: 'bad' }),
        JSON.stringify({ type: 'move', x: 101, y: 45, t: Date.now() }),
        JSON.stringify({ type: 'hello', loc: { lat: 999, lon: 0 }, pending: false }),
        JSON.stringify({ type: 'hello', loc: null }),
        JSON.stringify({ type: 'unknown' })];
    await a.page.evaluate(values => {
        for (const value of values) conn.channel.dataChannel.send(value);
        conn.channel.dataChannel.send(new Uint8Array([0xff, 0x00]));
    }, invalid);
    await b.page.waitForFunction(min => Number(document.getElementById('msg-count').textContent) >= min, received + invalid.length + 1);
    assert.deepEqual({ dot: await b.page.locator('#dot-peer').boundingBox(), delay: await text(b.page, 'latency'), location: await text(b.page, 'peer-loc'), distance: await text(b.page, 'distance') }, before);
    await a.page.evaluate(() => { for (let i = 0; i < 110; i++) conn.channel.dataChannel.send('null'); });
    await b.page.waitForFunction(min => Number(document.getElementById('msg-count').textContent) >= min, received + invalid.length + 111);
    assert.equal(await b.page.locator('#log > div').count(), 100);
    await movement(a.page, b.page, 0.82, 0.72, 1);
    await a.page.clock.setFixedTime(new Date(Date.now() + 60000));
    const skewed = await movement(a.page, b.page, 0.2, 0.2, 1);
    assert.match(skewed.delay, /^-\d+ ms$/, 'clock offset must not be hidden behind a made-up positive delay');
    return { malformedFramesIgnored: invalid.length + 111, logCap: 100, realMovementStillWorks: true, realPointerWithClockOffset: skewed.delay };
});

test('interrupted ICE pauses sending and re-verifies without losing the peer location', async t => {
    const a = await t.open({ geoValue: originFixture });
    const b = await t.open({ href: await online(a.page), geoValue: quarterEarthFixture });
    await settled(a.page, b.page);
    const before = await count(a.page);
    await a.page.evaluate(() => conn.channel.emit('iceStateChanged', 'disconnected'));
    assert.ok(await a.page.locator('#dot-peer').isHidden());
    assert.equal(await text(a.page, 'latency'), '—');
    await drag(a.page, 0.55, 0.25, 1);
    assert.equal(await count(a.page), before, 'unverified path must not send movement');
    await waitText(a.page, 'status', 'connected — verified direct');
    assert.equal(await text(a.page, 'distance'), '10,008 km');
    const resumed = await movement(b.page, a.page, 0.75, 0.75, 1);
    return { unverifiedSends: 0, retainedRealDistance: await text(a.page, 'distance'), resumed };
});

test('third peer cannot replace the active pair; close clears stale state and permits rejoin', async t => {
    const a = await t.open({ geoValue: originFixture });
    const link = await online(a.page);
    const b = await t.open({ href: link, geoValue: quarterEarthFixture });
    await settled(a.page, b.page);
    const c = await t.open({ href: link });
    await waitText(a.page, 'log', 'declined peer');
    await movement(b.page, a.page, 0.55, 0.25, 1);
    await c.context.close();
    await b.page.evaluate(() => conn.channel.dataChannel.close());
    await waitText(a.page, 'status', 'peer disconnected|connection failed');
    assert.equal(await text(a.page, 'distance'), '—');
    assert.equal(await text(a.page, 'latency'), '—');
    assert.ok(await a.page.locator('#dot-peer').isHidden());
    const d = await t.open({ href: link, geoValue: quarterEarthFixture });
    await settled(a.page, d.page);
    await movement(d.page, a.page, 0.72, 0.72, 1);
    return { extraPeerDeclined: true, staleDistanceAndDelayCleared: true, realRejoinAndMovement: true };
});

test('relay or missing ICE evidence is never presented as direct success', async t => {
    for (const kind of ['relay', 'error']) {
        const a = await t.open();
        const b = await t.open({
            href: await online(a.page),
            init: kind => {
                window.__nativeSends = 0;
                const send = RTCDataChannel.prototype.send;
                RTCDataChannel.prototype.send = function (...args) { window.__nativeSends++; return send.apply(this, args); };
                RTCPeerConnection.prototype.getStats = async () => {
                    if (kind === 'error') throw new Error('TEST stats unavailable');
                    return new Map([
                        ['t', { type: 'transport', selectedCandidatePairId: 'p' }],
                        ['p', { type: 'candidate-pair', localCandidateId: 'l', remoteCandidateId: 'r' }],
                        ['l', { candidateType: 'host' }], ['r', { candidateType: 'relay' }],
                    ]);
                };
            },
            initArg: kind,
        });
        await waitText(b.page, 'status', 'could not verify direct path');
        assert.ok(await b.page.locator('#dot-peer').isHidden());
        assert.equal(await b.page.evaluate(() => window.__nativeSends), 0);
        assert.doesNotMatch(await text(b.page, 'data-path'), /^direct/);
    }
    return { injectedRelayRefused: true, unavailableStatsRefused: true, unverifiedNativeSends: 0 };
});

test('failed or congested sends do not increment counters or escape as page errors', async t => {
    const results = [];
    for (const mode of ['busy', 'peer-send-throws', 'native-send-throws', 'returns-false']) {
        const a = await t.open();
        const b = await t.open({ href: await online(a.page) });
        await settled(a.page, b.page);
        const before = await count(a.page);
        await a.page.evaluate(mode => {
            if (mode === 'busy') Object.defineProperty(conn.channel.dataChannel, 'bufferedAmount', { value: 65537 });
            if (mode === 'peer-send-throws') conn.channel.send = () => { throw new Error('TEST send rejected'); };
            if (mode === 'native-send-throws') conn.channel.dataChannel.send = () => { throw new Error('TEST transport rejected'); };
            if (mode === 'returns-false') conn.channel.send = () => false;
        }, mode);
        await drag(a.page, 0.55, 0.25, 1);
        assert.equal(await count(a.page), before);
        if (mode === 'busy') assert.match(await text(a.page, 'log'), /busy — message not sent/);
        else await waitText(a.page, 'status', 'send failed|peer disconnected|connection failed');
        results.push(mode);
    }
    return { rejectedSendsNotCounted: results };
});

(async () => {
    const script = fs.readFileSync(file, 'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
    new vm.Script(script, { filename: file });
    const browser = await chromium.launch({ headless: true });
    let passed = 0, failed = 0, pageErrors = 0, unexpectedConsoleErrors = 0, externalDiagnostics = 0;
    console.log('Playwright ' + require('playwright/package.json').version + '; Chromium ' + browser.version() + '; native PeerJS/WebRTC; no local signaling or data relay');
    try {
        for (const { name, run } of tests) {
            if (process.argv[2] && !new RegExp(process.argv[2]).test(name)) continue;
            const contexts = [], errors = [], consoleErrors = [], expected = [];
            const t = {
                async open(options = {}) {
                    const context = await browser.newContext({ viewport: options.viewport || { width: 1280, height: 1000 }, hasTouch: options.hasTouch || false });
                    contexts.push(context);
                    let pendingGeo;
                    if (options.geo !== 'live') {
                        await context.route(IPAPI, route => {
                            if (options.geo === 'abort') return route.abort('aborted');
                            if (options.geo === 'pending') { pendingGeo = route; return; }
                            return route.fulfill({ json: Object.hasOwn(options, 'geoValue') ? options.geoValue : { error: true } });
                        });
                    }
                    if (options.cdn) await context.route(CDN, route => {
                        if (options.cdn === 'abort') return route.abort('aborted');
                        if (options.cdn === 'empty') return route.fulfill({ contentType: 'application/javascript', body: '' });
                    });
                    if (options.blockBroker) await context.route('https://0.peerjs.com/**', route => route.abort('aborted'));
                    if (options.init) await context.addInitScript(options.init, options.initArg);
                    const page = await context.newPage();
                    const sockets = [];
                    page.on('websocket', socket => sockets.push(socket));
                    page.on('pageerror', error => errors.push(error.message));
                    page.on('console', message => {
                        if (message.type() !== 'error') return;
                        const entry = { text: message.text(), url: message.location().url };
                        const nativeIpapiDiagnostic = (entry.url === IPAPI && /^Failed to load resource:/.test(entry.text))
                            || entry.text.startsWith("Access to fetch at '" + IPAPI + "'");
                        if (options.allowIpapiDiagnostics && nativeIpapiDiagnostic) expected.push(entry);
                        else consoleErrors.push(entry);
                    });
                    await page.goto(options.href || url, { waitUntil: 'domcontentloaded', timeout: 25000 });
                    return { page, context, sockets, geoRoute: () => pendingGeo };
                },
            };
            try {
                const evidence = await run(t);
                assert.deepEqual(errors, [], 'uncaught page exceptions');
                assert.deepEqual(consoleErrors, [], 'unexpected console errors (none are suppressed)');
                console.log('PASS ' + name + ' ' + JSON.stringify({ ...evidence, pageErrors: errors.length, consoleErrors: consoleErrors.length + expected.length, unexpectedConsoleErrors: consoleErrors.length, expectedExternalDiagnostics: expected.length }));
                passed++;
            } catch (error) {
                console.log('FAIL ' + name + '\n' + error.stack);
                if (errors.length || consoleErrors.length) console.log(JSON.stringify({ errors, consoleErrors }));
                for (const context of contexts) {
                    for (const page of context.pages()) {
                        console.log('STATE ' + JSON.stringify(await page.evaluate(() => ({
                            status: document.getElementById('status')?.textContent,
                            log: document.getElementById('log')?.textContent,
                        }))));
                    }
                }
                failed++;
            } finally {
                await Promise.all(contexts.map(context => context.close()));
                pageErrors += errors.length;
                unexpectedConsoleErrors += consoleErrors.length;
                externalDiagnostics += expected.length;
                for (const diagnostic of expected) console.log('EXTERNAL ' + JSON.stringify(diagnostic));
            }
        }
    } finally {
        await browser.close();
    }
    console.log(`RESULT ${passed} passed; ${failed} failed; pageErrors=${pageErrors}; consoleErrors=${unexpectedConsoleErrors + externalDiagnostics}; unexpectedConsoleErrors=${unexpectedConsoleErrors}; expectedExternalDiagnostics=${externalDiagnostics}`);
    if (failed || pageErrors || unexpectedConsoleErrors) process.exitCode = 1;
})().catch(error => { console.error(error); process.exitCode = 1; });
