.PHONY: datafiles

datafiles:
	wget https://resources.lendingclub.com/LoanStats3a.csv.zip\
    --no-check-certificate -P ./data
	wget https://resources.lendingclub.com/LoanStats3b.csv.zip\
    --no-check-certificate -P ./data
	wget https://resources.lendingclub.com/LoanStats3c.csv.zip\
    --no-check-certificate -P ./data
	unzip data/LoanStats3a.csv.zip -d ./data -o
	unzip data/LoanStats3b.csv.zip -d ./data -o
	unzip data/LoanStats3c.csv.zip -d ./data -o
