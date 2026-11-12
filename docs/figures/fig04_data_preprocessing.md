# Figure 4 — Data preprocessing

**File:** `fig04_data_preprocessing.pdf`

**Suggested caption.** From raw files to model inputs. Each dataset becomes one hourly univariate
series. The series is split in time with embargoes. All statistics (scaler, window length, number
of windows, task thresholds) are fitted on the training split only. The series is then encoded as
three channels in [0, 1] and cut into windows (red box: the leakage boundary).

## Steps

1. **Sources.** Nine public hourly-or-finer datasets: ETTh1, Electricity Load Diagrams, Household
   Power, PJM (PJME), Beijing PM2.5, Jena Climate, Metro Traffic, Bike Sharing, Bitcoin
   (`DATASETS.md`).
2. **raw.** Lossless conversion to Parquet (float64, all columns). The original file is removed only
   after the row count matches.
3. **Hourly univariate series.** Hourly mean (Electricity, Household, Jena), last log-price of the
   hour (Bitcoin), as is (others).
4. **Gaps.** Gaps of up to 6 h are interpolated. Longer gaps stay NaN, and windows that contain NaN
   are dropped. Metro uses the continuous part after the 2014–2015 gap; a missing Bike hour means
   0 rentals.
5. **Length.** Last `max_points` points (profile `min`: 10 000; `max`: full series).
6. **Temporal split** with a 168 h embargo between parts. Profile `min`: 50/25/25; `max`: 60/20/20.
7. **Fitted on train only.** Min–max bounds `lo, hi`; window length T = 168; number of assembled
   windows K = round(n_train / T); pool size N = max(300, 2K); stride s chosen to give about 5 000
   training windows; task thresholds (from the committed `target_params*.json`).
8. **Channels.** Channel 0 is the scaled value. Channels 1–2 are (sin + 1)/2 and (cos + 1)/2 of the
   hour of week (period 168).
9. **Windows.** `(n, T, 3)` with stride s. Train is divided into *core* (generator training) and
   *holdout* (last 10%, early stopping), separated by an embargo of 168 rows (`Config.embargo`).

## Where each output goes

Core windows → generator training. Holdout windows → early stopping. Full train → reference statistics of
the methods that use them. Val → primary fidelity reference and utility test. Train and OOT → the other
fidelity references (`@train`, `@oot`). OOT → utility test.

## Notes for the text

- In profile `min` every dataset has n = 9 664, train = 5 000, val = OOT = 2 332, K = 30, N = 300.
- `data_key` = hash(split, max_points, T) is stored with the processed data. The other stages
  refuse to read processed data whose key does not match the configuration.
