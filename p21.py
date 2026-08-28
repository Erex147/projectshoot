n1 = int(input("Enter number1: "))
n2 = int(input("Enter number2: "))
a = 0
b = 0
hcf = 0
lcm = 0
if n1 > n2:
    a = n1
    b = n2
else:
    a = n2
    b = n1
while b != 0:
    temp = b
    b = a % b
    a = temp
hcf = a
lcm = (n1 * n2) // hcf
print(f"HCF: {hcf}")
print(f"LCM: {lcm}")