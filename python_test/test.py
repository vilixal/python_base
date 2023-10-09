def check_lucky(number):
    i,j=0,0
    number=str(number)
    len_n=len(number)
    if len_n>2 and len_n%2:
        left_n = number[:len_n//2]
        right_n= number[len_n//2+1:]
        for num in left_n:
            i+=int(num)
        for num in right_n:
            j+=int(num)
        return i==j


def get_prime_numbers(n):
    prime_numbers = []
    for number in range(2, n+1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
    return prime_numbers


for number in get_prime_numbers(n=50000):
    if check_lucky(number):
        print(number)