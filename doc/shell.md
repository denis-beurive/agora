

Print all the transaction amounts in USB for a given vendor:

    grep -i "thesecretsociety"  data/03-aug2014.csv | cut -'d,' -f4 | sort -n

Print all the transaction amounts in BTC and USB for a given vendor:

    grep -i "thesecretsociety"  data/03-aug2014.csv | cut -'d,' -f3,4 | sort -n

Print the third field and sort it:

    cat res | tr -s ' ' | cut -d ' ' -f 3 | sort -n

