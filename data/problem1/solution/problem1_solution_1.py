def calculate(s):
    stack = []
    result = 0
    num = 0
    sign = 1
    
    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)
        elif char == '+':
            result += sign * num
            num = 0
            sign = 1
        elif char == '-':
            result += sign * num
            num = 0
            sign = -1
        elif char == '(':
            stack.append(result)
            stack.append(sign)
            result = 0
            sign = 1
        elif char == ')':
            result += sign * num
            num = 0
            result *= stack.pop()
            result += stack.pop()
        elif char == '*':
            print("multiply isn't recognizable")
            result = 999
            break
    
    result += sign * num
    
    if result == 999:
        return "Impossible result"
    
    return result