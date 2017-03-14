import csv

def readCSV(fname):
	with open(fname) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			option = row['alpha-2'] + ":" +row['name'] + ","
			print option
		print "\n\n"

def main():
	readCSV("country.csv")


if __name__ == "__main__":main()