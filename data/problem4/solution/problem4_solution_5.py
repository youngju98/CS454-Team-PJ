def calculate(n: int) -> int:
    def check_valid(i, col):
        k = 0
        valid = True
        while k < i and valid:
            if col[i] == col[k] or abs(col[i] - col[k]) == i - k:
                valid = False
            k += 1
        return valid

    def recursive(n, i, col, count): 
        if check_valid(i, col):
            if i == n - 1:
                count[0] += 1
            else:
                for j in range(n):
                    col[i + 1] = j
                    recursive(n, i + 1, col, count)

    col = n * [0]
    count = [0]
    recursive(n, -1, col, count)
    return count[0]
