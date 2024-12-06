def calculate(n: int) -> int:
    def promising(i, col):
        k = 0
        switch = True
        while k < i and switch:
            if col[i] == col[k] or abs(col[i] - col[k]) == i - k:
                switch = False
            k += 1
        return switch

    def queens(n, i, col, count):
        if promising(i, col):
            if i == n - 1:
                count[0] += 1  # Increment the solution count
            else:
                for j in range(n):
                    col[i + 1] = j
                    queens(n, i + 1, col, count)

    col = n * [0]
    count = [0]  # Using a list to allow modification inside the recursive function
    queens(n, -1, col, count)
    return count[0]