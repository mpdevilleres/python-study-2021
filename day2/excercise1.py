# input a number
# allow number to be 0 - 10
# message: invalid input
# determine if it prime number and also determine of it is odd or even
# eg.
# n prime odd
# n not-prime even
# submission 1:46pm

# prime numbers are numbers that have factors of 1 and itself

# input is a number with constraints which allow 0-10 only
def main():
    n = int(input("Please enter a number: "))

    if n < 0:
        print('invalid')
        return
    elif n > 10:
        print('invalid')
        return

    # check if it is prime 0-10 (2, 3, 5, 7)
    if n in (2, 3, 5, 7):
        is_prime = True
    else:
        is_prime = False

    # check if it is odd or even
    if n % 2 == 0:
        is_even = True
    else:
        is_even = False

    print(n, end=' ')
    if is_prime:
        print('prime', end=' ')
    else:
        print('not-prime', end=' ')

    if is_even:
        print('even')
    else:
        print('odd')


main()
