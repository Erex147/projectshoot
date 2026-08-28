n = int(input("Enter number: "))
fac = 1
for i in range(1, n + 1):
    fac *= i
print(f"Factorial: {fac}")