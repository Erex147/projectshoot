n = int(input("Enter number: "))
temp = n
dsum = 0
csum = 0
psum = 0
for i in range(1, n):
    if n % i == 0:
        dsum += i
while temp > 0:
    r = temp % 10
    csum += r ** 3
    psum = psum * 10 + r
    temp //= 10

if dsum == n:
    print("Perfect number")
if csum == n:
    print("Armstrong number")
if psum == n and n > 9:
    print("Palindrome number")