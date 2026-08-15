describe_indicator('MAG7 Momentum Rotation Leg', 'lower', { warmup: 260 });

// MAG7 monthly momentum rotation leg for TrendSpider Strategy Tester.
// Run this on each MAG7 chart. The signal is active when the chart ticker
// ranks in the top N of the MAG7 universe by momentum.

const peer1 = input.text('Peer 1', 'AAPL');
const peer2 = input.text('Peer 2', 'MSFT');
const peer3 = input.text('Peer 3', 'GOOGL');
const peer4 = input.text('Peer 4', 'AMZN');
const peer5 = input.text('Peer 5', 'NVDA');
const peer6 = input.text('Peer 6', 'META');
const peer7 = input.text('Peer 7', 'TSLA');
const lookback = input.number('Lookback', 135, { min: 20, max: 320 });
const topCount = input.number('Top Count', 2, { min: 1, max: 7 });

const normalizeTicker = symbol => String(symbol || '')
    .toUpperCase()
    .replace('.', '/')
    .trim();

const chartTicker = normalizeTicker(constants.ticker);
const rawPeers = [peer1, peer2, peer3, peer4, peer5, peer6, peer7].map(normalizeTicker);
const peerSymbols = [];

for (let rawIndex = 0; rawIndex < rawPeers.length; rawIndex += 1) {
    const symbol = rawPeers[rawIndex];
    if (symbol && symbol !== chartTicker && !peerSymbols.includes(symbol)) {
        peerSymbols.push(symbol);
    }
}

const fetchDailyClose = async symbol => {
    const data = await request.history(symbol, 'D', {
        ext_session: constants.session.lengthMinutes == constants.ext_session.lengthMinutes
    });
    assert(!data.error, `Fetch ${symbol}: ${data.error}`);
    return interpolate_sparse_series(
        land_points_onto_series(data.time, data.close, time, 'ge'),
        'constant'
    );
};

const peerCloses = [];
for (let peerIndex = 0; peerIndex < peerSymbols.length; peerIndex += 1) {
    peerCloses.push(await fetchDailyClose(peerSymbols[peerIndex]));
}

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

const rankRows = endIndex => {
    const rows = [{ ticker: chartTicker, score: averageDailyReturn(close, endIndex, lookback) }];

    for (let peerIndex = 0; peerIndex < peerSymbols.length; peerIndex += 1) {
        rows.push({
            ticker: peerSymbols[peerIndex],
            score: averageDailyReturn(peerCloses[peerIndex], endIndex, lookback)
        });
    }

    return rows
        .filter(row => row.score !== null && isFinite(row.score))
        .sort((left, right) => right.score - left.score);
};

let selected = 0;
let rankValue = null;
let lastMonthKey = '';

const selectedState = close.map((_, candleIndex) => {
    const previousIndex = candleIndex - 1;
    const sessionAtCandle = session_of(time[candleIndex], constants.resolution);
    const monthKey = String(sessionAtCandle.session).slice(0, 7);
    const monthChanged = monthKey !== lastMonthKey;

    if (monthChanged && previousIndex >= lookback) {
        const rows = rankRows(previousIndex);
        selected = 0;
        rankValue = null;

        for (let rankIndex = 0; rankIndex < rows.length; rankIndex += 1) {
            if (rows[rankIndex].ticker === chartTicker) {
                rankValue = rankIndex + 1;
                selected = rankValue <= topCount ? 1 : 0;
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

register_signal(selectedState, 'MAG7 Rot Selected');
register_signal(entrySignal, 'MAG7 Rot Entry');
register_signal(exitSignal, 'MAG7 Rot Exit');
