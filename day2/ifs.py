# # defining if statements
#
# if (condition1):
#     pass
# elif (condition2):
#     pass
# else:
#     pass
#
# # example
# if count == 1:
#     print('count is not 0')

n = int(input("input a number: "))

if n % 2 == 0:
    print(n, 'is divisible by 2')

elif n % 3 == 0:
    print(n, 'is divisible by 3')

elif n % 5 == 0:
    print(n, 'is divisible by 5')

else:
    print(n, "undetermined")
# if it divisible by 2
# if it divisible by 3
# if it divisible by 5
# if it divisible by 7
