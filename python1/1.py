import time
import os


print("=== 1. Flag ===")
red_bg = "\033[41m"
white_bg = "\033[47m"
reset = "\033[0m"
print(red_bg + "...###..." + reset)
print(red_bg + "...###..." + reset)
print(red_bg + "...###..." + reset)
print(white_bg + "#########" + reset)
print(white_bg + "#########" + reset)
print(white_bg + "#########" + reset)
print(red_bg + "...###..." + reset)
print(red_bg + "...###..." + reset)
print(red_bg + "...###..." + reset)


print("\n=== 2. Pattern j ===")
print("  ###   ###  ")
print(" #   # #   # ")
print(" #   # #   # ")
print("  ###   ###  ")


print("\n=== 3. Data Percentage ===")
filename = "sequence.txt"
try:
    with open(filename, "r", encoding="utf-8") as f:
        nums = [float(line.strip()) for line in f if line.strip()]
        
    total = len(nums)
    in_r = sum(1 for x in nums if -3 <= x <= 3)
    p1 = (in_r / total) * 100.0
    p2 = 100.0 - p1

    print("Total items: " + str(total))
    print("[-3, 3] range: " + str(round(p1, 1)) + "%")
    print("[" + "#" * int(p1/2.5) + " " * (40 - int(p1/2.5)) + "]")
    
    print("Other numbers: " + str(round(p2, 1)) + "%")
    print("[" + "#" * int(p2/2.5) + " " * (40 - int(p2/2.5)) + "]")

except FileNotFoundError:
    print("Error: 'sequence.txt' not found!")
    print("Please put the file in the same folder as this code.")
except Exception as e:
    print("Error reading file: " + str(e))


print("\n=== 4. Graph y=x/3 ===")
for i in range(10):
    line = ""
    for j in range(20):
        x_val = j * 6.0 / 19.0
        y_val = (9 - i) * 2.0 / 9.0
        if i == 9:
            line += "-"
        elif j == 0:
            line += "|"
        elif abs(y_val - x_val/3.0) < 0.15:
            line += "*"
        else:
            line += " "
    print(line)


print("\n=== 5. Animation ===")
time.sleep(2)
for i in range(3):
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print("Frame " + str(i+1) + ":")
    print("#" * (i+1) + "." * (3-i))
    time.sleep(1)