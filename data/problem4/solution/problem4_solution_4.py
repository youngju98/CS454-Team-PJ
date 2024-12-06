def calculate(n: int) -> int:
    # Backtracking function to place queens
    def backtrack(row: int, cols: set, diagonals1: set, diagonals2: set) -> int:
        # If all queens are placed, we found a solution
        if row == n:
            return 1

        solutions = 0
        for col in range(n):
            # Place the queen
            cols.add(col)
            diagonals1.add(row - col)
            diagonals2.add(row + col)

            # Recur to the next row
            solutions += backtrack(row + 1, cols, diagonals1, diagonals2)

            cols.remove(col)
            diagonals1.remove(row - col)
            diagonals2.remove(row + col)

        return solutions

    # Initialize the backtracking
    return backtrack(0, set(), set(), set())
