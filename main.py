print('hello mars')

with open("mission_computer_main.log", "r", encoding="utf-8") as file:
    lines = file.readlines()
    
for line in lines:
    print(line.strip())
    
def read_log_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print('파일을 찾을 수 없습니다.')
        return []
    except Exception as e:
        print('파일 열기 오류:', e)
        return []
    
    log_list = []
    for i, line in enumerate(lines):
        line = line.strip()
        if i == 0:
            continue # 첫 줄은 header
        parts = line.split(',', 2)
        if len(parts) == 3:
            log_list.append(parts)
            

    return log_list       

 

def main():
    logs = read_log_file('mission_computer_main.log')
    
    print('📄 로그 파일 내용 (리스트 형태):')
    for log in logs:
        print(log)

         
    sorted_logs = sorted(logs, key=lambda x: x[0], reverse=True)
        
    print('\n 시간 역순 정렬 결과:')
    for log in sorted_logs:
            print(log)
               
               
    
    log_dict = {}
    for log in sorted_logs:
        timestamp = log[0]
        event = log[1]
        message = log[2]
        log_dict[timestamp] = {
            'event': event,
            'message': message
        }
        
    return log_dict
               
if __name__ == '__main__':
    log_dict = main() 
    
import json

with open('mission_computer_main.json', 'w', encoding='utf-8') as f:
    json.dump(log_dict, f, ensure_ascii=False, indent=4)

keyword = input('검색할 단어를 입력하세요: ')
for time, info in log_dict.items():
    if keyword in info['message']:
        print(time, info['event'], info['message']) 
        