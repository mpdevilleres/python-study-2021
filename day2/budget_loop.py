AED_RATE = 3.67  # rate against usd


def convert_to_aed(value, count=None):
    if not count:
        return int(value) * AED_RATE
    return int(count) * int(value) * AED_RATE


# User Input Values
budget_total = input('Budget Total USD: ')
size_basket = int(input('Input the Size of your Basket: '))

fruits = []
prices = []
counts = []
prices_aed = []
for i in range(0, size_basket):
    in_fruit = input(f'Input the values for fruit {i+1} [name,price,count]: ')
    # ['apple', '2', '3']
    fruit_specification = in_fruit.split(',')
    price = int(fruit_specification[1])
    count = int(fruit_specification[2])
    fruits.append(fruit_specification[0])
    prices.append(price)
    counts.append(count)

# CONVERSIONS
budget_total_aed = convert_to_aed(budget_total)
for i in range(0, size_basket):
    price = prices[i]
    count = counts[i]
    price_in_aed = convert_to_aed(price, count)
    prices_aed.append(price_in_aed)

print(f'actual budget {budget_total_aed:.2f}', end=' ')

# Calculations
for i in prices_aed:
    # budget_total_aed = budget_total_aed - i
    budget_total_aed -= i

# Final Result
print(f'remaining budget {budget_total_aed:.2f}')
