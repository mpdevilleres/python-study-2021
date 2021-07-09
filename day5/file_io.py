import csv

# a - append
# r - read
# w - overwrite writing

with open('tmp.txt', 'r') as file:
    file.readlines()

with open('tmp.txt', 'w') as file:
    file.write('Hello World')

with open('tmp.txt', 'a') as file:
    file.write('Hello World')

with open('tmp.txt', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

with open('tmp.txt', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['value_A', 'value_B', 'just another value'])
