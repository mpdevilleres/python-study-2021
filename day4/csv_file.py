import csv

with open('tmp.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=':')
    writer.writerow(['A', 'B', 'C'])
    writer.writerow(['D', 'E', 'F'])

with open('tmp.csv', 'r') as f:
    reader = csv.reader(f, delimiter=":")
    for row in reader:
        print(row)
