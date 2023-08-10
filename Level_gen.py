import random
file = open("levels.csv", "a")

alphabet = ["a", "b"]

level = 3
completed = 0

num_cases = 30
task = "Machine accepts strings having ab"

test_cases = []

def gen_test_cases():
    for _ in range(30):
        ret = "ab"
        for j in range(random.randint(0, 10)):
            ret += alphabet[random.randint(0, 1)]
        ret += "ba"
        test_cases.append(ret)

gen_test_cases()
f = [level, completed, num_cases, task]
print(test_cases)
# exit()
for i in f:
    file.write(str(i))
    file.write(',')

for m in test_cases:
    file.write(m)
    file.write("|")
file.write('\n')