describe_indicator('VWAP Trend QQQ Signals', 'price', { warmup: 260 });

// Multi-strategy signal pack for TrendSpider Strategy Tester comparisons.
// It keeps the original VWAP signals and adds long-only proxies for the other
// four strategy families from the trading-ideas research note.

const sessionKeyOf = candleTime => {
    const sessionAtCandle = session_of(candleTime, constants.resolution);
    return String(sessionAtCandle.session).slice(0, 10);
};

const makeSeries = fillValue => Array(close.length).fill(fillValue);

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

const exponentialMovingAverage = (values, period) => {
    const result = makeSeries(NaN);
    const multiplier = 2 / (period + 1);
    let seeded = false;
    let average = 0;

    for (let i = 0; i < values.length; i += 1) {
        if (i === period - 1) {
            let seedTotal = 0;
            for (let j = i - period + 1; j <= i; j += 1) {
                seedTotal += values[j];
            }
            average = seedTotal / period;
            result[i] = average;
            seeded = true;
        } else if (seeded) {
            average = ((values[i] - average) * multiplier) + average;
            result[i] = average;
        }
    }
    return result;
};

const rollingStdDev = (values, period, averageSeries) => {
    const result = makeSeries(NaN);
    for (let i = period - 1; i < values.length; i += 1) {
        const average = averageSeries[i];
        let squaredDiffTotal = 0;
        for (let j = i - period + 1; j <= i; j += 1) {
            squaredDiffTotal += Math.pow(values[j] - average, 2);
        }
        result[i] = Math.sqrt(squaredDiffTotal / period);
    }
    return result;
};

const relativeStrengthIndex = period => {
    const result = makeSeries(NaN);
    let gains = 0;
    let losses = 0;

    for (let i = 1; i < close.length; i += 1) {
        const change = close[i] - close[i - 1];
        const gain = change > 0 ? change : 0;
        const loss = change < 0 ? -change : 0;

        if (i <= period) {
            gains += gain;
            losses += loss;
            if (i === period) {
                gains /= period;
                losses /= period;
            }
        } else {
            gains = ((gains * (period - 1)) + gain) / period;
            losses = ((losses * (period - 1)) + loss) / period;
        }

        if (i >= period) {
            result[i] = losses === 0 ? 100 : 100 - (100 / (1 + (gains / losses)));
        }
    }
    return result;
};

const crossedAbove = (leftPrevious, leftCurrent, rightPrevious, rightCurrent) => (
    leftPrevious <= rightPrevious && leftCurrent > rightCurrent
);

const crossedBelow = (leftPrevious, leftCurrent, rightPrevious, rightCurrent) => (
    leftPrevious >= rightPrevious && leftCurrent < rightCurrent
);

const volumeSma20 = simpleMovingAverage(volume, 20);
const closeSma5 = simpleMovingAverage(close, 5);
const closeSma20 = simpleMovingAverage(close, 20);
const closeSma50 = simpleMovingAverage(close, 50);
const closeSma200 = simpleMovingAverage(close, 200);
const closeStd20 = rollingStdDev(close, 20, closeSma20);
const ema50 = exponentialMovingAverage(close, 50);
const ema200 = exponentialMovingAverage(close, 200);
const rsi2 = relativeStrengthIndex(2);

const vwapSeries = [];
const firstBarBias = [];
const vwapLongEntry = [];
const vwapShortEntry = [];
const vwapLongExit = [];
const vwapShortExit = [];
const orbLongEntry = [];
const orbLongExit = [];
const momentumLongEntry = [];
const momentumLongExit = [];
const maCrossLongEntry = [];
const maCrossLongExit = [];
const smaCrossLongEntry = [];
const smaCrossLongExit = [];
const absMomentum252Entry = [];
const absMomentum252Exit = [];
const rsiBbLongEntry = [];
const rsiBbLongExit = [];
const connorsRsi2Entry = [];
const connorsRsi2Exit = [];

let currentSession = '';
let cumulativePv = 0;
let cumulativeVolume = 0;
let barsInSession = 0;
let firstDirection = 0;
let firstBarHigh = NaN;
let firstBarLow = NaN;

for (let i = 0; i < close.length; i += 1) {
    const key = sessionKeyOf(time[i]);

    if (key !== currentSession) {
        currentSession = key;
        cumulativePv = 0;
        cumulativeVolume = 0;
        barsInSession = 0;
        firstDirection = 0;
        firstBarHigh = NaN;
        firstBarLow = NaN;
    }

    const typicalPrice = (high[i] + low[i] + close[i]) / 3;
    const candleVolume = volume[i] || 0;

    cumulativePv += typicalPrice * candleVolume;
    cumulativeVolume += candleVolume;

    const sessionVwap = cumulativeVolume > 0 ? cumulativePv / cumulativeVolume : typicalPrice;
    vwapSeries.push(sessionVwap);

    const isFirstSessionBar = barsInSession === 0;
    const previousClose = i > 0 ? close[i - 1] : close[i];
    const previousVwap = i > 0 ? vwapSeries[i - 1] : sessionVwap;
    const isEndOfDay = i === close.length - 1 || sessionKeyOf(time[i + 1]) !== key;
    const crossedBelowVwap = crossedBelow(previousClose, close[i], previousVwap, sessionVwap);
    const crossedAboveVwap = crossedAbove(previousClose, close[i], previousVwap, sessionVwap);

    if (isFirstSessionBar) {
        firstDirection = close[i] > sessionVwap ? 1 : (close[i] < sessionVwap ? -1 : 0);
        firstBarHigh = high[i];
        firstBarLow = low[i];
    }

    const hasPrevious = i > 0;
    const lowerBand = closeSma20[i] - (2 * closeStd20[i]);
    const wasMomentum = i > 63 && close[i - 1] > closeSma50[i - 1] && close[i - 1] > close[i - 64];
    const isMomentum = i >= 63 && close[i] > closeSma50[i] && close[i] > close[i - 63];
    const wasAbsMomentum = i > 252 && close[i - 1] > closeSma200[i - 1] && close[i - 1] > close[i - 253];
    const isAbsMomentum = i >= 252 && close[i] > closeSma200[i] && close[i] > close[i - 252];
    const wasMeanReversion = hasPrevious && rsi2[i - 1] < 10 && close[i - 1] < (closeSma20[i - 1] - (2 * closeStd20[i - 1]));
    const isMeanReversion = rsi2[i] < 10 && close[i] < lowerBand;
    const wasConnorsRsi2 = hasPrevious && close[i - 1] > closeSma200[i - 1] && rsi2[i - 1] <= 5;
    const isConnorsRsi2 = close[i] > closeSma200[i] && rsi2[i] <= 5;
    const volumeConfirmed = volumeSma20[i] > 0 && candleVolume > volumeSma20[i];

    vwapLongEntry.push(isFirstSessionBar && firstDirection === 1 ? 1 : 0);
    vwapShortEntry.push(isFirstSessionBar && firstDirection === -1 ? 1 : 0);
    vwapLongExit.push((firstDirection === 1 && (crossedBelowVwap || isEndOfDay)) ? 1 : 0);
    vwapShortExit.push((firstDirection === -1 && (crossedAboveVwap || isEndOfDay)) ? 1 : 0);
    firstBarBias.push(firstDirection);

    orbLongEntry.push((barsInSession > 0 && previousClose <= firstBarHigh && close[i] > firstBarHigh && volumeConfirmed) ? 1 : 0);
    orbLongExit.push((barsInSession > 0 && (close[i] < firstBarLow || crossedBelowVwap || isEndOfDay)) ? 1 : 0);

    momentumLongEntry.push((isMomentum && !wasMomentum) ? 1 : 0);
    momentumLongExit.push((i >= 63 && (close[i] < closeSma50[i] || close[i] < close[i - 63])) ? 1 : 0);
    absMomentum252Entry.push((isAbsMomentum && !wasAbsMomentum) ? 1 : 0);
    absMomentum252Exit.push((i >= 252 && (close[i] < closeSma200[i] || close[i] < close[i - 252])) ? 1 : 0);

    maCrossLongEntry.push((i > 0 && crossedAbove(ema50[i - 1], ema50[i], ema200[i - 1], ema200[i])) ? 1 : 0);
    maCrossLongExit.push((i > 0 && crossedBelow(ema50[i - 1], ema50[i], ema200[i - 1], ema200[i])) ? 1 : 0);
    smaCrossLongEntry.push((i > 0 && crossedAbove(closeSma50[i - 1], closeSma50[i], closeSma200[i - 1], closeSma200[i])) ? 1 : 0);
    smaCrossLongExit.push((i > 0 && crossedBelow(closeSma50[i - 1], closeSma50[i], closeSma200[i - 1], closeSma200[i])) ? 1 : 0);

    rsiBbLongEntry.push((isMeanReversion && !wasMeanReversion) ? 1 : 0);
    rsiBbLongExit.push((close[i] > closeSma20[i] || rsi2[i] > 70) ? 1 : 0);
    connorsRsi2Entry.push((isConnorsRsi2 && !wasConnorsRsi2) ? 1 : 0);
    connorsRsi2Exit.push((close[i] > closeSma5[i] || close[i] < closeSma200[i]) ? 1 : 0);

    barsInSession += 1;
}

paint(vwapSeries, { name: 'Session VWAP', color: '#00bcd4', thickness: 2 });
paint(firstBarBias, { name: 'First Bar Bias', color: '#ffb000', thickness: 1, hidden: true });
paint(ema50, { name: 'EMA 50', color: '#4f8cff', thickness: 1, hidden: true });
paint(ema200, { name: 'EMA 200', color: '#ffb84f', thickness: 1, hidden: true });
paint(closeSma20, { name: 'SMA 20', color: '#ffffff', thickness: 1, hidden: true });
paint(closeSma200, { name: 'SMA 200', color: '#ff5252', thickness: 1, hidden: true });

register_signal(vwapLongEntry, 'VWAP Long Entry');
register_signal(vwapShortEntry, 'VWAP Short Entry');
register_signal(vwapLongExit, 'VWAP Long Exit');
register_signal(vwapShortExit, 'VWAP Short Exit');
register_signal(orbLongEntry, 'ORB Long Entry');
register_signal(orbLongExit, 'ORB Long Exit');
register_signal(momentumLongEntry, 'Momentum Long Entry');
register_signal(momentumLongExit, 'Momentum Long Exit');
register_signal(maCrossLongEntry, 'MA Cross Long Entry');
register_signal(maCrossLongExit, 'MA Cross Long Exit');
register_signal(smaCrossLongEntry, 'SMA Cross Long Entry');
register_signal(smaCrossLongExit, 'SMA Cross Long Exit');
register_signal(absMomentum252Entry, 'Abs Momentum 252 Entry');
register_signal(absMomentum252Exit, 'Abs Momentum 252 Exit');
register_signal(rsiBbLongEntry, 'RSI BB Long Entry');
register_signal(rsiBbLongExit, 'RSI BB Long Exit');
register_signal(connorsRsi2Entry, 'Connors RSI2 Entry');
register_signal(connorsRsi2Exit, 'Connors RSI2 Exit');
