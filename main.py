import sys

var_dict = {}
now = 0

def c_bool(bool:str):
    if "==" in bool:
        words = bool.split("==")
        if Type(words[0]) == Type(words[1]):
            return "진실"
        else:
            return "거짓"
    elif "!=" in bool:
        words = bool.split("!=")
        if Type(words[0]) != Type(words[1]):
            return "진실"
        else:
            return "거짓"
    elif bool == "진실" or bool == "거짓":
        return bool
    else:
        raise Exception("이해할 수 없는 조건문입니다.")

def Type(text:str):
    if text.startswith("#"):
        return
    elif text.startswith(" "):
        return Type(text[1:])
    elif text.endswith(" "):
        return Type(text.rstrip())
    elif text.startswith("반복 "):
        t = text[3:]
        words = t.split(":")  # [반복 수, 실행문]가 저장됨
        for i in range(int(Type(words[0]))):
            return Type(words[1])
    elif text.startswith("만약 "):
        t = text[3:]
        words = t.split(":")  # [조건문, 실행문]가 저장됨
        if c_bool(words[0]) == "진실":
            return Type(words[1])
    elif text.startswith("출력 "):
        print(Type(text[3:]))
        return
    elif text.startswith("질문 "):
        return input(Type(text[3:]))
    elif text.startswith("변수"):
        t = text[3:]
        first_part = t.split(None, 1)[0]
        remaining_part = t[len(first_part) + 1:]
        if remaining_part.startswith("는 "):
            var_dict[first_part] = Type(remaining_part[2:])
            return
        elif first_part in var_dict:
            return Type(var_dict[first_part]+Type(remaining_part))
        else:
            raise Exception(f"{first_part} (이)라는 변수는 선언된 적이 없습니다.")
    elif "=" in text:
        c_bool(text)
    elif any(op in text for op in ("+", "-", "*", "/")):
        if any(text.startswith(op) for op in ("+", "-", "*", "/")):
            return text[0]+Type(text[1:])
        return str(eval(text))
    else:
        return text

try:
    file = sys.argv[1]
    if ".jun" in file:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()  # 줄 바꿈 문자를 제거
                now +=1
                Type(line)
    else:
        raise Exception("함태준언어 인터프리터는 확장자가 jun인 함태준언어 파일만 실행 가능합니다.")

except Exception as e:
    print(f"{now}번째 줄에서 문제 발생: {e}")
    exit()
