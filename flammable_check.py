import csv

filename = 'Mars_Base_Inventory_List.csv'

try:
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
except FileNotFoundError:
    print(f"파일 {filename}을(를) 찾을 수 없습니다.")
except Exception as e:
    print("오류 발생:", e)
    
def read_csv(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print('❌ 파일을 찾을 수 없습니다.') 
        return []
    except Exception as e:
        print('❌ 파일 읽기 오류:', e)
        return []
        
    inventory = []
    
    for i,line in enumerate(lines):
        if i == 0:
            continue
        line = line.strip()
        parts = line.split(',')
        if len(parts) == 5:
            name = parts[0]
            try:
                flammability = float(parts[4])
            except ValueError:
                flammability = 0.0
            inventory.append([name, flammability])
            
    return inventory
    
def save_to_csv(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('Substance,Flammability\n')
        for item in data:
            file.write(f'{item[0]},{item[1]}\n')

def save_to_bin(data, filename):
    with open(filename, 'wb') as file:
            for item in data:
                line =f'{item[0]}\t{item[1]}\n'
                file.write(line.encode('utf-8'))
                
def read_from_bin(filename):
    with open(filename, 'rb') as file:
        content = file.read()
        print('\n📦 이진 파일 내용:')
        print(content.decode('utf-8'))
        
def main():
    inventory = read_csv('Mars_Base_Inventory_List.csv')

    print('✅ 전체 물질 목록:')
    for item in inventory:
        print(item)

    sorted_list = sorted(inventory, key=lambda x: x[1], reverse=True)

    print('\n🔥 인화성이 높은 순 정렬:')
    for item in sorted_list:
        print(item)

    dangerous = [item for item in sorted_list if item[1] >= 0.7]

    print('\n🚨 위험한 인화물질 목록:')
    for item in dangerous:
        print(item)

    save_to_csv(dangerous, 'Mars_Base_Inventory_danger.csv')
    save_to_bin(sorted_list, 'Mars_Base_Inventory_List.bin')
    read_from_bin('Mars_Base_Inventory_List.bin')

if __name__ == '__main__':
    main()