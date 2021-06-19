AED_RATE = 3.67  # rate against usd


def convert_to_aed(value, count=None):
    if not count:
        return int(value) * AED_RATE
    return int(count) * int(value) * AED_RATE


# User Input Values
budget_total = input('Budget Total USD: ')
price_apple = input('Price of apple USD: ')
count_apple = input('Count of apple/s: ')
price_banana = input('Price of banana USD: ')
count_banana = input('Count of banana/s: ')
price_pear = input('Price of pear USD: ')
count_pear = input('Count of pear/s: ')
price_strawberry = input('Price of strawberry USD: ')
count_strawberry = input('Count of strawberry/s: ')

# Conversion of rates
budget_total_aed = convert_to_aed(budget_total)
price_apple_aed = convert_to_aed(price_apple, count_apple)
price_banana_aed = convert_to_aed(price_banana, count_banana)
price_pear_aed = convert_to_aed(price_pear, count_pear)
price_strawberry_aed = convert_to_aed(price_strawberry, count_strawberry)

# Calculations
remaining_budget_aed = budget_total_aed - price_apple_aed - price_banana_aed - price_pear_aed - price_strawberry_aed

print(budget_total_aed, 'AED')
print(remaining_budget_aed, 'AED')
