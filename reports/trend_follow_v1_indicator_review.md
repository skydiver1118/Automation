# Trend Follow v1 Indicator Review

## What TrendSpider Shows

The selected strategy is `Trend Follow v1`, using `Trend Pullback ATR Strategy - Signals` on the daily chart. The visible backtest window is `24 Jul 2018 / 01 Mar 2026`.

Visible tabular metrics:

| Metric | Value |
| --- | ---: |
| Net performance | 499.0% |
| Asset performance | 666.8% |
| Positions | 26 |
| Wins | 80% |
| Losses | 20% |
| Max DD | -44.0% |
| Average win | 11.34% |
| Average loss | -5.00% |
| Average return | 8.07% |
| Reward/risk ratio | 2.27 |
| Expectancy | 1.6 |

## Important Wiring Check

The Strategy Tester condition text currently shows:

| Tester side | Signal used |
| --- | --- |
| Entry condition | `Trend Pullback ATR Strategy - Signals`, `Exit` signal emerged |
| Exit condition | `Trend Pullback ATR Strategy - Signals`, `Entry` signal emerged |

The indicator comments say the original strategy should be:

| Tester side | Signal used |
| --- | --- |
| Entry condition | `Entry` |
| Exit condition | `Exit` |

So the current setup appears to be a swapped test: it enters where the original system would exit, and exits where the original system would enter. That may be intentional, but it should be labeled separately from the normal trend-following version before tuning.

## Indicator Logic Extracted

Inputs observed:

| Parameter | Current |
| --- | ---: |
| Fast EMA | 21 |
| Mid EMA | 50 |
| Trend EMA | 200 |
| RSI Length | 14 |
| Long RSI Min | 50 |
| Long RSI Max | 70 |
| Use Volume Filter | true |
| Volume SMA Length | 20 |
| Volume Multiplier | 1.0 |
| ATR Length | 14 |
| Stop ATR Multiplier | 1.5 |
| Reward/Risk Target | 2.0 |
| Use ATR Trailing Stop | true |
| Trailing ATR Multiplier | 2.0 |
| Max Bars In Trade | 40 |

Long entry requires:

- `close > EMA 200`
- `EMA 21 > EMA 50`
- `EMA 50 > EMA 200`
- close crosses above `EMA 21`
- RSI is between `50` and `70`
- candle closes above open
- volume is at least `20 SMA(volume) * 1.0`

Exit logic:

- Updates ATR trailing stop first.
- Exits by priority: stop, target, trend, time.
- Long stop is entry minus `ATR * 1.5`, trailed by highest high minus `ATR * 2.0`.
- Target is entry plus risk times `2.0`.
- Trend exit is close below `EMA 50`.
- Time exit is after `40` bars.
- If stop and target are both touched in one candle, the script classifies it as a stop.

## Suggested Test Order

1. Run wiring sanity checks first:
   - `original_normal`: Entry=`Entry`, Exit=`Exit`
   - `swapped_any_exit`: Entry=`Exit`, Exit=`Entry`
   - Keep the current visible result as `swapped_any_exit` until proven otherwise.

2. Isolate exit reasons:
   - Entry=`Entry`, Exit=`Exit: Target only`
   - Entry=`Entry`, Exit=`Exit: Stop only`
   - Entry=`Entry`, Exit=`Exit: Trend only`
   - Entry=`Entry`, Exit=`Exit: Time only`
   - This reveals whether the -44% drawdown is mostly stop behavior, late trend exits, or holding too long.

3. Reduce drawdown:
   - Test trend exit from close below `EMA 50` to close below `EMA 21`.
   - Test `Max Bars In Trade`: `20`, `30`, `40`.
   - Test `Trailing ATR Multiplier`: `1.5`, `2.0`, `2.5`.

4. Improve entry quality:
   - Test `Long RSI Min`: `50`, `55`, `60`.
   - Test `Volume Multiplier`: `1.0`, `1.2`, `1.5`.
   - This should reduce weak pullback recoveries, but may lower trade count.

5. Improve trade count:
   - Test `Long RSI Max`: `70`, `75`, `80`.
   - Test `Volume Multiplier`: `0.8`, `1.0`.
   - Only 26 positions over the full window, so robustness needs more samples if performance stays comparable.

## First Parameter Matrix

| Variant | Entry | Exit | EMA Fast/Mid/Trend | RSI Min/Max | Stop ATR | Trail ATR | Max Bars | Goal |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| baseline_swapped | Exit | Entry | 21/50/200 | 50/70 | 1.5 | 2.0 | 40 | Preserve current visible setup |
| original_baseline | Entry | Exit | 21/50/200 | 50/70 | 1.5 | 2.0 | 40 | Verify normal system |
| faster_exit | Entry | Exit | 21/50/200 | 50/70 | 1.5 | 1.5 | 30 | Reduce drawdown |
| quality_entry | Entry | Exit | 21/50/200 | 55/70 | 1.5 | 2.0 | 40 | Filter weak signals |
| looser_opportunity | Entry | Exit | 21/50/200 | 50/75 | 1.5 | 2.0 | 40 | Increase sample size |
| wider_stop | Entry | Exit | 21/50/200 | 50/70 | 2.0 | 2.5 | 40 | Test whether stops are too tight |

The strongest first move is the wiring sanity check. If the normal system underperforms the swapped setup, the current strategy is less a trend-follow entry and more a pullback-after-exit reversal system, which should be tuned differently.
