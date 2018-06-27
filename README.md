# A simple tool to run FIO and parse the result

## Usage

### FIO

Use FIO on different devices and collect the FIO results to OUTPUT

```
DIR=/data1 OUTPUT=./log1 ./run_fio.sh
DIR=/data2 OUTPUT=./log2 ./run_fio.sh
```

## Collection

### Latency


```bash
python parse_latency.py -i ./log1/com -i ./log1/com
```

It will generate following files in the directory './output'

```bash
read100-lat-mean.csv
read100-lat-p99.csv
read70-lat-mean.csv
read70-lat-p99.csv
write100-lat-mean.csv
write100-lat-p99.csv
write30-lat-mean.csv
write30-lat-p99.csv
```

`read100` means 100% read, `read70` means 70% read + 30% write, and so on. 

### Bandwidth

```bash
python parse_bw.py -i ./log1/com -i ./log1/com
```

It will generate following files in the directory './output'

```bash
read100-bandwidth.csv
read70-bandwidth.csv
write100-bandwidth.csv
write30-bandwidth.csv
```

### Read Latency with different block size

```bash
python parse_var_bs.py -i ./log1/var-bs -i ./log2/var-bs
```

It will generate following files in the directory './output'

```bash
read100-bs-lat-mean.csv
read100-bs-lat-p99.csv
```

### TL;DR

You can use `./gen_output.sh` to generate all the CSV files directly, like:

```bash
./gen_output.sh ./log1 ./log2
```

After you generate all CSV files, you can use many tools to convert them to Markdown table, or paste them to the Excel.

## TODO

- Use pyplot to generate the chart