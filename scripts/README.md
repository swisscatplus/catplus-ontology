# Transform Sample Data

Scripts to prepare sample data:

## Agilent Files

Aiglent files are only parsed for their metadata, otherwise they are kept as data files on an S3

In order to have example files for the parsers, we provide a simple and complex example on this repo and have reduced the file size of the agilent data by running a small script on them:

```
python3 scripts/reduce_numeric_data.py example/simple-model/bravo-1/100-A1-Agilent.json example/simple-model/bravo-1/100-A1-Agilent-no-data.json
rm example/simple-model/bravo-1/100-A1-Agilent.json
```

## Test Script

```
python3 scripts/reduce_numeric_data.py scripts/test.json scripts/test-no-data.json
```
