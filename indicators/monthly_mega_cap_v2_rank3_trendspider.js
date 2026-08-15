describe_indicator('Monthly Mega-Cap V2 Rank3 Leg', 'lower', { warmup: 260 });

// TrendSpider-compatible diagnostic version.
// It ranks the active chart ticker against two comparison symbols only.
// Use the full selector file for the intended 28-symbol portfolio logic.

const compareA = input.text('Compare A', 'MSFT');
const compareB = input.text('Compare B', 'NVDA');
const useTechScore = input.boolean('Tech Score', true);
const lookback = input.number('Lookback', 135, { min: 20, max: 320 });
const topRank = input.number('Top Rank', 1, { min: 1, max: 3 });

const symbolAData = await request.history(compareA, 'D', {
    ext_session: constants.session.lengthMinutes == constants.ext_session.lengthMinutes
});
const symbolBData = await request.history(compareB, 'D', {
    ext_session: constants.session.lengthMinutes == constants.ext_session.lengthMinutes
});

const symbolAClose = interpolate_sparse_series(
    land_points_onto_series(symbolAData.time, symbolAData.close, time, 'ge'),
    'constant'
);
const symbolBClose = interpolate_sparse_series(
    land_points_onto_series(symbolBData.time, symbolBData.close, time, 'ge'),
    'constant'
);

const averageDailyReturn = (series, endIndex, length) => {
    let returnTotal = 0;
    let count = 0;
    const firstIndex = Math.max(1, endIndex - length + 1);

    for (let i = firstIndex; i <= endIndex; i += 1) {
        const previous = series[i - 1];
        const currentValue = series[i];
        if (previous > 0 && currentValue > 0) {
            returnTotal += (currentValue / previous) - 1;
            count += 1;
        }
    }

    return count >= Math.min(length, endIndex) ? returnTotal / count : null;
};

const totalReturn = (series, endIndex, length) => {
    const startIndex = endIndex - length;
    if (startIndex < 0) {
        return null;
    }

    const startValue = series[startIndex];
    const endValue = series[endIndex];
    if (!(startValue > 0) || !(endValue > 0)) {
        return null;
    }

    return (endValue / startValue) - 1;
};

const scoreFor = (series, endIndex) => useTechScore
    ? averageDailyReturn(series, endIndex, lookback)
    : totalReturn(series, endIndex, lookback);

let selected = 0;
let rankValue = null;
let lastMonthKey = '';

const selectedState = close.map((_, candleIndex) => {
    const previousIndex = candleIndex - 1;
    const sessionAtCandle = session_of(time[candleIndex], constants.resolution);
    const monthKey = String(sessionAtCandle.session).slice(0, 7);
    const monthChanged = monthKey !== lastMonthKey;

    if (monthChanged && previousIndex >= lookback) {
        const rows = [
            { id: 'chart', score: scoreFor(close, previousIndex) },
            { id: 'a', score: scoreFor(symbolAClose, previousIndex) },
            { id: 'b', score: scoreFor(symbolBClose, previousIndex) }
        ].filter(row => row.score !== null && isFinite(row.score))
            .sort((left, right) => right.score - left.score);

        rankValue = null;
        selected = 0;

        for (let rankIndex = 0; rankIndex < rows.length; rankIndex += 1) {
            if (rows[rankIndex].id === 'chart') {
                rankValue = rankIndex + 1;
                selected = rankValue <= topRank ? 1 : 0;
            }
        }
    }

    lastMonthKey = monthKey;
    return selected;
});

const rankSeries = close.map(() => rankValue);
const entrySignal = selectedState.map((isSelected, candleIndex) => {
    const wasSelected = candleIndex > 0 ? selectedState[candleIndex - 1] : 0;
    return isSelected === 1 && wasSelected !== 1 ? 1 : 0;
});
const exitSignal = selectedState.map((isSelected, candleIndex) => {
    const wasSelected = candleIndex > 0 ? selectedState[candleIndex - 1] : 0;
    return isSelected !== 1 && wasSelected === 1 ? 1 : 0;
});

paint(selectedState, { name: 'Selected', color: '#2fcc56', thickness: 2 });
paint(rankSeries, { name: 'Rank', color: '#ffb000', thickness: 1 });
paint(entrySignal, { name: 'Entry Pulse', color: '#2078ff', thickness: 2 });
paint(exitSignal, { name: 'Exit Pulse', color: '#ff4d4d', thickness: 2 });

register_signal(selectedState, 'MMV2 R3 Selected');
register_signal(entrySignal, 'MMV2 R3 Entry');
register_signal(exitSignal, 'MMV2 R3 Exit');
