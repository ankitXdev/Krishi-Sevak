
# Input: n = 2
# Output: 5
# Explanation: For dice facing number 5 opposite face will have the number 2.

# Input: n = 6
# Output: 1
# Explanation: For dice facing number 6 opposite face will have the number 1.

# In a normal 6-faced dice, 1 is opposite to 6, 2 is opposite to 5, and 3 is opposite to 4.

def rolldice(n):
    if n == 1:
        print(6)
    if n == 2:
        print(5)
    if n == 3:
        print(4)
    if n == 4:
        print(3)
    if n == 5:
        print(2)
    if n == 6:
        print(1)

rolldice(5)