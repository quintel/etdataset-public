# Weather-year heat demand curves

Generates heat demand profiles used in the ETM based on temperature, irradiation, wind and G2A params.
Outputs the following curves:
* 12 household insulation curves (per residence type and for high/medium/low insulation level)
* `buildings_heating`
* `agriculture_heating`
* `air_temperature.csv`

## Setup

```bash
pip install -r requirements.txt
```

## Running the tool

### By area code

Name one or more area codes as they appear in `source_analyses/` and both
folders are resolved for you:

```bash
python -m weather_years nl
```

reads `source_analyses/nl/2023/13_curves/weather_years/` and writes
`data/nl/2023/13_curves/output/`. Every year with an input folder is generated,
so most areas need nothing but their code; `--year` narrows it to one, and
several areas can be named at once:

```bash
python -m weather_years nl --year 2023
python -m weather_years nl BE_belgium
```

The etdataset checkout is found by searching upwards for a folder holding both
`source_analyses/` and `data/`, so this works from any directory.
`--etdataset-root` overrides it.

Every area's inputs are read and validated before anything is written, so a
mistyped area code fails the whole run rather than leaving half the output
folders rewritten. Output folders are overwritten in place.

### By explicit path
Alternatively, custom input and output folders can be specified. In the example below, the input files are in folder `input` and curves will be exported to folder `output`.

```bash
python -m weather_years \
  --temperature input/air_temperature.csv \
  --irradiation input/irradiation.csv \
  --wind-speed input/wind_speed.csv \
  --g2a-parameters input/G2A_parameters.csv \
  --output output/
```

Only temperature and irradiation are required; without wind speed and G2A
parameters the curves for buildings and agriculture are skipped. The thermostat defaults
to the ECN schedule in `weather_years/data/`. `--output` also overrides the
derived destination when an area code is given, as long as it resolves to a
single weather year.

### Options

- `--thermostat` — 24-row `low,medium,high` CSV in °C.
- `--smoothing {shared,per-profile}` — see below.

## Inputs

| Input | Unit | Required |
|---|---|---|
| temperature | °C | yes |
| irradiation | J/cm²/h (KNMI convention) | yes |
| thermostat | °C, 24 rows × `low`/`medium`/`high` | no, defaults to the ECN schedule |
| wind speed | m/s | only for buildings/agriculture |
| G2A parameters | 1 or 8760 rows of `reference`,`slope`,`constant` | only for buildings/agriculture |


### The NL 2023 inputs

`python -m weather_years nl` reads
`source_analyses/nl/2023/13_curves/weather_years/`, which is where these inputs
now live. They were assembled from two folders that had them split up:

| File | Originally from |
|---|---|
| `air_temperature.csv` | `data/nl/2023/13_curves/output/air_temperature.csv` — the pipeline stored temperature as an output, not an input |
| `irradiation.csv` | `data/nl/2023/13_curves/input/heat and electricity/` |
| `wind_speed.csv` | `data/nl/2023/13_curves/input/heat and electricity/` |

## How it works

Two independent methods produce the curves.

**Households** (12 profiles: 4 house types × 3 insulation levels). A physical
model of a house in `house.py`. Each hour it compares the indoor temperature to
the thermostat setpoint and demands heat if the house is too cold, while losing
heat through the envelope and gaining heat from sunlight through the windows.
Indoor temperature carries over between hours, so the house has thermal inertia.
The house types, their R-values, surface areas, window areas and behaviour
fitting numbers are a table in `house_types.py`. They are based on the Dutch context,
so adaptations for different areas would require changes to that table.

**Buildings and agriculture** (2 profiles, identical to each other). The Dutch
gas-sector G2A formula: demand rises linearly once an effective temperature drops
below a reference point.

Every profile is normalised to sum to 1/3600, as they are hourly profiles expressing
shares of annual demand.

### Smoothing

A single-house curve is too spiky to represent a neighbourhood, since 300
households do not switch their heating on at the same minute. `smoothing.py`
interpolates the curve to 6-minute resolution, copies it 300 times with
normally distributed time offsets (σ = 2–3 hours, depending on insulation),
sums the copies and resamples back to hourly values. Background:
https://refman.energytransitionmodel.com/publications/2118

Two sources of randomness are available:

- `--smoothing shared` (default) draws every profile from one random stream in
  generation order. This is how the weather years ETM currently ships were
  generated. It also means a profile depends on how many profiles preceded it,
  so regenerating one house type alone does **not** give the curve it had in the
  full run.
- `--smoothing per-profile` seeds a stream per curve key, so a profile is the
  same whether generated alone or in a set — and every value changes relative
  to `shared`.

## Tests

```bash
pytest
```

The suite runs entirely on synthetic weather built in `tests/conftest.py` — sine
waves carrying the features the generator reacts to, not a measured year.

- `test_generator.py` — what comes out and which way it moves. Every assertion is
  either structural (curve count, length, normalisation, naming) or directional
  (colder days need more heat, sunlight offsets it, wind adds to it), never the
  value of a particular hour.
- `test_cli.py` — the two ways of naming inputs, where the files land, the
  messages a mistake gets, and that two runs write byte-identical files.
