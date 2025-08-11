def caesar_cipher_decode(target_text, dictionary):
    """
    카이사르 암호를 해독하는 함수입니다.
    target_text : 암호화된 문자열
    dictionary  : 해독된 문자열에서 찾을 단어 리스트(소문자)
    """
    for shift in range(26):  # 0부터 25까지 모든 자리수(밀기 값)를 시도합니다.
        decoded = ''  # 해독된 결과를 저장할 빈 문자열 초기화

        for c in target_text:  # 암호문 한 글자씩 처리
            if 'A' <= c <= 'Z':  # 만약 대문자라면
                # 문자 'A'의 아스키값 65를 빼고 shift만큼 빼서 26글자 범위 내에서 순환,
                # 다시 65를 더해 대문자로 변환 후 decoded에 추가
                decoded += chr((ord(c) - 65 - shift) % 26 + 65)
            elif 'a' <= c <= 'z':  # 만약 소문자라면
                # 'a' 기준으로 같은 방법으로 처리
                decoded += chr((ord(c) - 97 - shift) % 26 + 97)
            else:
                # 알파벳이 아니면 그대로 decoded에 추가
                decoded += c

        # 현재 shift로 해독한 결과 출력 (몇 칸 밀었는지와 결과)
        print(f'{shift:2}칸 밀기 → {decoded}')

        # 소문자로 바꿔서 사전 단어가 포함되어 있는지 확인
        lowered = decoded.lower()
        if any(word in lowered for word in dictionary):
            print(f'\n>>> 키워드 발견! {shift}칸 밀기 해독 결과를 사용합니다.')
            # 키워드가 포함된 해독 결과가 있으면 shift 번호와 결과를 반환하며 함수 종료
            return shift, decoded

    # 26칸 모두 시도했는데 키워드가 없으면 None 반환
    print('\n키워드를 발견하지 못했습니다.')
    return None, None


def main():
    # 해독된 문장에서 찾을 단어 목록(소문자)
    dictionary = ['love', 'mars', 'hello', 'world']

    try:
        # password.txt 파일 열기, UTF-8 인코딩 사용
        with open('password.txt', 'r', encoding='utf-8') as f:
            encrypted_text = f.read().strip()  # 파일 내용 읽고 앞뒤 공백 제거

        print(f'암호문: {encrypted_text}\n')

        # 암호 해독 함수 호출해서 결과 받기
        shift, decoded_text = caesar_cipher_decode(encrypted_text, dictionary)

        if shift is not None:
            # 키워드가 발견된 경우 result.txt 파일에 해독 결과 저장
            with open('result.txt', 'w', encoding='utf-8') as f:
                f.write(decoded_text)
            print('해독 결과가 result.txt 파일에 저장되었습니다.')
        else:
            # 키워드 미발견 시 사용자에게 직접 shift 값을 입력받음
            while True:
                try:
                    shift = int(input('정답 shift 번호를 입력하세요 (0~25): '))
                    if 0 <= shift <= 25:
                        break
                    print('0부터 25 사이의 숫자를 입력하세요.')
                except ValueError:
                    print('숫자를 정확히 입력하세요.')

            # 입력받은 shift 값으로 다시 해독
            result = ''
            for c in encrypted_text:
                if 'A' <= c <= 'Z':
                    result += chr((ord(c) - 65 - shift) % 26 + 65)
                elif 'a' <= c <= 'z':
                    result += chr((ord(c) - 97 - shift) % 26 + 97)
                else:
                    result += c

            # 해독 결과를 다시 result.txt 파일에 저장
            with open('result.txt', 'w', encoding='utf-8') as f:
                f.write(result)
            print('해독 결과가 result.txt 파일에 저장되었습니다.')

    except FileNotFoundError:
        # password.txt 파일이 없을 경우 알려줌
        print('password.txt 파일이 해당 경로에 없습니다.')
    except Exception as e:
        # 그 외 다른 오류가 발생하면 오류 내용 출력
        print(f'오류가 발생했습니다: {e}')


# 이 파일이 직접 실행될 때 main() 함수를 실행한다는 의미
if __name__ == '__main__':
    main()
