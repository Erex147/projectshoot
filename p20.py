x = int(input("Enter number: "))
n = int(input("Enter power: "))
sum = 0
for i in range(0, n+1):
    sum += x**i
print(f"Sum: {sum}")