# Tips for data exploration

```shell
$ INPUT_CSV="01-june2014.csv"
$ head -n 1 "${INPUT_CSV}"
"hash","Date","btc","usd","rate","ship_from","vendor_name","name","description"
```

Print the list of vendors from a given CSV file:

```shell
$ INPUT_CSV="01-june2014.csv"
$ csvtool col 7 "${INPUT_CSV}" | sort | uniq | less
```
