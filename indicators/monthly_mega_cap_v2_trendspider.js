describe_indicator('Monthly Mega-Cap V2 Selector', 'lower', { warmup: 260 });

// Composer-inspired Monthly Mega-Cap V2 selector.
// Test on Daily charts. The indicator emits signals for the active chart ticker.

const techSymbols = input.text(
    'Tech Symbols',
    'AAPL,MSFT,GOOGL,AMZN,NVDA,TSM,ASML,AVGO,ORCL',
    { hide_in_legend: true }
).split(',').map(value => value.trim()).filter(Boolean);

const defensiveSymbols = input.text(
    'Def Symbols',
    'AZN,BAC,BRK/B,CL,COST,JNJ,KO,LLY,MA,MRK,NVO,PEP,PFE,PG,UNH,V,WMT',
    { hide_in_legend: true }
).split(',').map(value => value.trim()).filter(Boolean);

const techLookback = input.number('Tech Lookback', 135, { min: 20, max: 260 });
const defensiveLookback = input.number('Def Lookback', 210, { min: 60, max: 320 });
const topCount = input.number('Top Count', 2, { min: 1, max: 5 });

const normalizeTicker = symbol => String(symbol || '')
    .toUpperCase()
    .replace('.', '/')
    .trim();

const chartTicker = normalizeTicker(constants.ticker);
const allSymbols = [];
const inputSymbols = [...techSymbols, ...defensiveSymbols].map(normalizeTicker);
for (let inputIndex = 0; inputIndex < inputSymbols.length; inputIndex += 1) {
    if (!allSymbols.includes(inputSymbols[inputIndex])) {
        allSymbols.push(inputSymbols[inputIndex]);
    }
}

const fetchDailyClose = async symbol => {
    const data = await request.history(symbol, 'D');
    assert(!data.error, `Error fetching ${symbol}: ${data.error}`);
    return interpolate_sparse_series(
        land_points_onto_series(data.time, data.close, time, 'ge'),
        'constant'
    );
};

const historyBySymbol = {};
for (let symbolIndex = 0; symbolIndex < allSymbols.length; symbolIndex += 1) {
    const symbol = allSymbols[symbolIndex];
    historyBySymbol[symbol] = await fetchDailyClose(symbol);
}

const averageDailyReturn = (series, endIndex, length) => {
    let returnSum = 0;
    let count = 0;
    const firstIndex = Math.max(1, endIndex - length + 1);

    for (let i = firstIndex; i <= endIndex; i += 1) {
        const previous = series[i - 1];
        const currentValue = series[i];
        if (previous > 0 && currentValue > 0) {
            returnSum += (currentValue / previous) - 1;
            count += 1;
        }
    }

    return count >= Math.min(length, endIndex) ? returnSum / count : null;
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

const rankTop = (symbols, endIndex, scoringFunction, lookback) => symbols
    .map(symbol => ({
        symbol: normalizeTicker(symbol),
        score: scoringFunction(historyBySymbol[normalizeTicker(symbol)], endIndex, lookback)
    }))
    .filter(row => row.score !== null && isFinite(row.score))
    .sort((a, b) => b.score - a.score)
    .slice(0, topCount)
    .map(row => row.symbol);

let heldSymbols = [];
let lastMonthKey = '';
const selectedState = close.map((_, candleIndex) => {
    const previousIndex = candleIndex - 1;
    const sessionAtCandle = session_of(time[candleIndex], constants.resolution);
    const monthKey = String(sessionAtCandle.session).slice(0, 7);
    const monthChanged = monthKey !== lastMonthKey;

    if (monthChanged && previousIndex >= Math.max(techLookback, defensiveLookback)) {
        const topTech = rankTop(techSymbols, previousIndex, averageDailyReturn, techLookback);
        const topDefensive = rankTop(defensiveSymbols, previousIndex, totalReturn, defensiveLookback);
        heldSymbols = [...topTech, ...topDefensive];
    }

    lastMonthKey = monthKey;

    return heldSymbols.includes(chartTicker) ? 1 : 0;
});

const entrySignal = selectedState.map((isSelected, candleIndex) => {
    const wasSelected = candleIndex > 0 ? selectedState[candleIndex - 1] : 0;
    return isSelected === 1 && wasSelected !== 1 ? 1 : 0;
});

const exitSignal = selectedState.map((isSelected, candleIndex) => {
    const wasSelected = candleIndex > 0 ? selectedState[candleIndex - 1] : 0;
    return isSelected !== 1 && wasSelected === 1 ? 1 : 0;
});

paint(selectedState, { name: 'Selected', color: '#2fcc56', thickness: 2 });
paint(entrySignal, { name: 'Entry Pulse', color: '#2078ff', thickness: 2 });
paint(exitSignal, { name: 'Exit Pulse', color: '#ff4d4d', thickness: 2 });

register_signal(selectedState, 'Selected');
register_signal(entrySignal, 'Entry');
register_signal(exitSignal, 'Exit');
