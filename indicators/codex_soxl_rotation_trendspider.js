describe_indicator('Codex SOXL Rotation Signals', 'lower', { warmup: 90 });

// SOXL leg of the SMH/SOXL 3-month relative-strength rotation.
// Intended chart: SOXL, Daily.
// Local backtest rule:
// - At the first trading day of each month, use the prior day's data.
// - Compare 3-month / 63-trading-day total return of SOXL vs SMH.
// - Select SOXL only when SOXL has the stronger return and that return is positive.
// - Otherwise exit SOXL; the local full portfolio rotates to SMH or AGG/BIL,
//   which TrendSpider's single-symbol Strategy Tester cannot hold in the same test.

const compareSymbol = input.text('Compare', 'SMH');
const lookbackBars = input.number('Lookback', 63, { min: 20, max: 126 });

const compareData = await request.history(compareSymbol, 'D', {
    ext_session: constants.session.lengthMinutes == constants.ext_session.lengthMinutes
});

assert(!compareData.error, `Fetch ${compareSymbol}: ${compareData.error}`);

const compareClose = interpolate_sparse_series(
    land_points_onto_series(compareData.time, compareData.close, time, 'ge'),
    'constant'
);

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

let selected = 0;
let lastMonthKey = '';
let soxlScore = null;
let smhScore = null;

const selectedState = close.map((_, candleIndex) => {
    const previousIndex = candleIndex - 1;
    const sessionAtCandle = session_of(time[candleIndex], constants.resolution);
    const monthKey = String(sessionAtCandle.session).slice(0, 7);
    const monthChanged = monthKey !== lastMonthKey;

    if (monthChanged && previousIndex >= lookbackBars) {
        soxlScore = totalReturn(close, previousIndex, lookbackBars);
        smhScore = totalReturn(compareClose, previousIndex, lookbackBars);
        selected = (
            soxlScore !== null
            && smhScore !== null
            && isFinite(soxlScore)
            && isFinite(smhScore)
            && soxlScore > 0
            && soxlScore > smhScore
        ) ? 1 : 0;
    }

    lastMonthKey = monthKey;
    return selected;
});

const soxlScorePct = close.map(() => soxlScore === null ? NaN : soxlScore * 100);
const smhScorePct = close.map(() => smhScore === null ? NaN : smhScore * 100);
const entrySignal = selectedState.map((isSelected, candleIndex) => {
    const wasSelected = candleIndex > 0 ? selectedState[candleIndex - 1] : 0;
    return isSelected === 1 && wasSelected !== 1 ? 1 : 0;
});
const exitSignal = selectedState.map((isSelected, candleIndex) => {
    const wasSelected = candleIndex > 0 ? selectedState[candleIndex - 1] : 0;
    return isSelected !== 1 && wasSelected === 1 ? 1 : 0;
});

paint(selectedState, { name: 'SOXL Selected', color: '#2fcc56', thickness: 2 });
paint(soxlScorePct, { name: 'SOXL 3M %', color: '#2078ff', thickness: 1 });
paint(smhScorePct, { name: 'SMH 3M %', color: '#ffb000', thickness: 1 });
paint(entrySignal, { name: 'Entry Pulse', color: '#00e676', thickness: 2 });
paint(exitSignal, { name: 'Exit Pulse', color: '#ff4d4d', thickness: 2 });

register_signal(selectedState, 'Codex SOXL Selected');
register_signal(entrySignal, 'Codex SOXL Entry');
register_signal(exitSignal, 'Codex SOXL Exit');
