print('hello world')

with open("mission_computer_main.log", "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    print(line.strip())

try:
    with open("mission_computer_main.log", "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        print(line.strip())

except FileNotFoundError:
    print("⚠️ 파일이 없어요! 이름을 확인해 주세요.")

except Exception as e:
    print("⚠️ 다른 문제가 생겼어요:", e)
    
    



