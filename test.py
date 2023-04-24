import subprocess

def to_int(array):
    num = 0
    for i in range(len(array)):
        num <<= 8
        num += array[i]
    return num


process = subprocess.Popen(r'C:\Users\Joshua\source\repos\PipesTest\x64\Debug\PipesTest.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)


numbers = [
    100,
    1212,
    101010,
    999,
    12345,
    10,
    100,
    1212,
    101010,
    999,
    12345,
    10,
]

for number in numbers:
    process.stdin.write((str(number) + "\n").encode())
    process.stdin.flush()

for i in range(12):
    temp = int(process.stdout.readline())
    print(temp)

