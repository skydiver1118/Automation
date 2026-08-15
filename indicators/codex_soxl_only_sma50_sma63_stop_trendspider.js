describe_indicator('Codex SOXL Only Signals', 'price', { warmup: 80 });

// Standalone SOXL daily trend strategy.
// Rule replicated from the local search winner:
// - Enter long when SMA50 is above SMA63.
// - Stay long while SMA50 remains above SMA63.
// - Exit when SMA50 is no longer above SMA63 or close falls 10% below entry.
// Intended chart: SOXL, Daily.

const fastLength = input.number('Fast SMA', 50, { min: 2, max: 200 });
const slowLength = input.number('Slow SMA', 63, { min: 3, max: 300 });
const stopPct = input.number('Stop %', 10, { min: 1, max: 80 }) / 100;

const makeSeries = value => Array(close.length).fill(value);

const simpleMovingAverage = (values, period) => {
    const result = makeSeries(NaN);
    let runningTotal = 0;

    for (let i = 0; i < values.length; i += 1) {
        runningTotal += values[i] || 0;
        if (i >= period) {
            runningTotal -= values[i - period] || 0;
        }
        if (i >= period - 1) {
            result[i] = runningTotal / period;
        }
    }

    return result;
};

const fastSma = simpleMovingAverage(close, fastLength);
const slowSma = simpleMovingAverage(close, slowLength);

let inPosition = false;
let entryPrice = NaN;

const selectedState = makeSeries(0);
const entrySignal = makeSeries(0);
const exitSignal = makeSeries(0);
const stopLevel = makeSeries(NaN);

for (let i = 0; i < close.length; i += 1) {
    const trendOn = isFinite(fastSma[i]) && isFinite(slowSma[i]) && fastSma[i] > slowSma[i];

    if (!inPosition && trendOn) {
        inPosition = true;
        entryPrice = close[i];
        entrySignal[i] = 1;
    }

    if (inPosition) {
        selectedState[i] = 1;
        stopLevel[i] = entryPrice * (1 - stopPct);
    }

    const stopHit = inPosition && close[i] <= entryPrice * (1 - stopPct);
    const trendExit = inPosition && !trendOn;

    if (stopHit || trendExit) {
        exitSignal[i] = 1;
        selectedState[i] = 0;
        inPosition = false;
        entryPrice = NaN;
    }
}

paint(fastSma, { name: 'SMA 50', color: '#3b82f6', thickness: 2 });
paint(slowSma, { name: 'SMA 63', color: '#f59e0b', thickness: 2 });
paint(stopLevel, { name: '10% Stop', color: '#ef4444', thickness: 1 });
paint(entrySignal, { name: 'Entry Pulse', color: '#00e676', thickness: 2, hidden: true });
paint(exitSignal, { name: 'Exit Pulse', color: '#ff4d4d', thickness: 2, hidden: true });

register_signal(selectedState, 'Codex SOXL Only Selected');
register_signal(entrySignal, 'Codex SOXL Only Entry');
register_signal(exitSignal, 'Codex SOXL Only Exit');
