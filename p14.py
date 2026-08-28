n = int(input("Enter number: "))
root = int(n**0.5) + 1

if n <= 1:
    print("Not a prime number")
elif n == 2:
    print("Prime number")
elif n % 2 == 0:
    print("Not a prime number")
else:
    for i in range(2, root):
        if n % i == 0:
            print("Not a prime number")
            break
    else:
        print("Prime number")