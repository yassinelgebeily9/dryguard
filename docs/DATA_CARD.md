# Dataset card — exploratory and matched subsets

## Provenance and selection

Source: the UAB Wireless Information Networking Group's public
RFID-Reader-FX7500 repository, pinned at commit
`790b419e86b508c38487d679658a8bad266237be`, retrieved 2026-10-02.
The complete file list and Git blob hashes are in `data/manifest.json`.

The selection takes 12 filenames at evenly spaced indices in each of five
sorted session folders, restricted to names containing `Soil_(Dry)` or
`Soil_(Wet)`. Filenames ending `_moving.csv` are excluded. This is a small,
systematically selected convenience subset for exploration. It is neither
random nor representative of the entire repository. Files without an explicit
wet/dry name and other materials are outside this milestone. Absence of a
`moving` suffix does not establish that a measurement was static.

## Unit of observation and labels

Each CSV is treated as one recording. Each row is a reader event. Neither
files nor rows should automatically be assumed statistically independent.
The notebook maps exactly `obs == Soil_(Dry)` to dry and `obs == Soil_(Wet)`
to wet. It checks that the label agrees with the filename. These describe
the authors' experimental conditions, not a laundry dryness threshold.

`moist` is retained as the source's reported moisture value. This subset has
values 0.01, 0.06, 0.12, 0.18, and 0.24. The notebook does not convert them
to calibrated textile water content or independently verify their calibration.
One source file has one value per checked setting; different files can differ.

| Column | Interpretation in this project |
| --- | --- |
| `peakRssi` | Received signal strength in dBm; candidate signal feature |
| `phase` | Source phase in degrees; circular encoding needed for later modeling |
| `time_reader` | Reader timestamp; used for within-recording elapsed time |
| `power` | Transmit power in dBm; experimental condition |
| `channel` | Recorded RF channel/frequency in MHz |
| `pos_y` | Recorded position/distance field, in m; retain source geometry meaning |
| `depth` | Recorded depth field in m |
| `moist` | Reported moisture value; target/reference metadata |
| `obs` | Experimental condition used to derive the wet/dry label |
| `session`, `source_file` | Provenance added during loading; grouping metadata |

The upstream data-management code interprets phase in degrees and `pos_y`
as a distance field. See the pinned repository's `src/data_management.py`.

## Quality checks and findings

- 60 source files, 54,537 rows, no missing values in the nine checked signal,
  label, and condition fields; this does not certify all 32 original columns.
- No exact duplicate source rows across the selected files.
- One tag type, one antenna, one channel, and one recorded depth (0.096 m).
- 12 dry files in one session; 48 wet files across four sessions.
- Power spans 10–29 dBm and `pos_y` spans 0.075–1.543 m.
- The observed first-to-last-read span varies from about 0.086 to 60.535 s.
  This is not the commanded recording duration. Read count divided by this
  span is not a verified read rate, especially for sparse records.

The reported plots weight files equally by using each file's median RSSI.
They are descriptive, without causal estimates or confidence intervals.

## Evaluation limits

Session and wet/dry label are confounded in the selected subset. The source
filename inventory also places all explicitly dry-labeled files in one of
these preliminary-measurement session folders. This audit does not prove
there are no additional useful dry observations elsewhere in the repository.

A random row split would mix reads from the same recording between training
and testing. A file split avoids that specific leakage but does not establish
new-session performance. Holding out the only dry session leaves training
without dry examples. Independent dry and wet sessions are needed for the
stronger evaluation we want.

Do not feed `obs`, `moist`, filenames, source session, or absolute timestamps
to an RSSI-only or RSSI-plus-phase classifier. They can expose the labels or
acquisition conditions. Match or explicitly account for power and geometry
when designing the next experiment. If recording length or read count becomes
a feature, first confirm a common acquisition interval.

## Relation to Dryguard

This is soil data from a laboratory setup, with no laundry drying trajectories
or textile dryness reference. It supports learning acquisition, auditing,
feature construction, and evaluation design. It cannot validate detection of
dry garments in a rotating dryer. That needs textile data, independently
measured moisture, and evaluation on unseen drying cycles.

## Matched comparison extension

The additional manifest is `data/matched/manifest.json`. It selects all non-moving
wet filenames with recorded power and position matching one of the original
12 dry recordings, then verifies the CSV contents. Selection does not depend on
RSSI. This targeted search is not an exhaustive audit of all possible dry files.

Six new wet recordings match four existing dry recordings, giving six comparisons
and ten unique recordings. Together with the original subset there are 66 unique
files, not 70. The extension uses the same pinned commit and verifies Git blob
hashes. The original 60-file tables and statistics above remain unchanged.

For each pair, all rows must agree on power, `pos_y`, tag type, channel, antenna
index and depth. Other geometry fields and physical setup equivalence have not
been established. All dry recordings come from `2025-02-28b`; the added wet files
come from `2025-03-06b`, `2025-03-07a` and `2025-03-11b`.

Wet median RSSI is 7–15 dB weaker in the six comparisons. Greater reported moisture
does not consistently give weaker RSSI. Two dry files are reused, so pairs are not
independent. The ECDF plots describe within-recording read distributions; the IQR
is the width of the middle 50% of reads, not uncertainty in the estimated median.
Matching recorded settings does not remove session confounding or prove causation.

The complete, untruncated pinned GitHub tree contained 818 explicitly dry-labeled
soil CSVs and 2,121 wet-labeled soil CSVs, including one wet file with a moving
suffix. Every explicitly dry-labeled filename was in one session. Other labels
were not exhaustively checked for additional dry conditions.
