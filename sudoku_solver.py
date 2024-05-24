import copy
import random


class Sudoku:
	def __init__(self, board):
		self.board = board
		self.board_copy = copy.deepcopy(self.board)
		self.base = 3

	def print_sudoku(self, name="board", nice_print=False):
		if nice_print:
			self.nice_print(self.__getattribute__(name))
		else:
			print(*self.__getattribute__(name), sep='\n')

	def nice_print(self, board):
		side = len(board)

		def expand_line(line):
			return line[0] + line[5:9].join([line[1:5] * (self.base - 1)] * self.base) + line[9:]

		line0 = "  " + expand_line("╔═══╤═══╦═══╗")
		line1 = "# " + expand_line("║ . │ . ║ . ║ #")
		line2 = "  " + expand_line("╟───┼───╫───╢")
		line3 = "  " + expand_line("╠═══╪═══╬═══╣")
		line4 = "  " + expand_line("╚═══╧═══╩═══╝")

		symbol = " 123456789" if self.base <= 3 else " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		nums = [[""] + [f"({symbol[-n]})" if n < 0 else f" {symbol[n]} " for n in row] for row in self.board]
		coord = "   " + "".join(f" {s}  " for s in symbol[1:side + 1])
		lines = [coord, line0]
		for r in range(1, side + 1):
			line1n = line1.replace("#", str(symbol[r]))
			lines.append("".join(n + s for n, s in zip(nums[r - 1], line1n.split(" . "))))
			lines.append([line2, line3, line4][(r % side == 0) + (r % self.base == 0)])
		lines.append(coord)
		print(*lines, sep="\n")

	def get_number(self, x, y) -> int:
		return self.board[y][x]

	def set_number(self, x, y, number: int) -> None:
		if 10 > number >= 0:
			self.board[y][x] = number

	def get_row(self, row) -> list:
		return self.board[row]

	def get_column(self, column) -> list:
		return [num[column] for num in self.board]

	def get_smaller_square(self, x, y) -> list:
		smaller_square: list = []
		for i in range(3):
			for j in range(3):
				col = ((x // 3) * 3) + i
				row = ((y // 3) * 3) + j
				smaller_square.append(self.get_number(col, row))
		return smaller_square

	def is_sudoku_valid(self) -> bool:
		# unique numbers in rows and columns
		for i in range(9):
			row = self.get_row(i)
			row_w0 = list(filter(lambda n: n != 0, row))  # row without zeros

			column = self.get_column(i)
			column_w0 = list(filter(lambda n: n != 0, column))  # column without zeros
			# compare length of unique numbers in column/row with length of the column/row (without zeros)
			if len(set(column_w0)) != len(column_w0) or len(set(row_w0)) != len(row_w0):
				return False

		# unique numbers for smaller squares
		for i in range(1, 9, 3):
			for j in range(1, 9, 3):
				smaller_square = self.get_smaller_square(i, j)
				smaller_square_w0 = list(filter(lambda n: n != 0, smaller_square))  # smaller square without zeros
				# compare length of unique numbers in square with length of square (without zeros)
				if len(set(smaller_square_w0)) != len(smaller_square_w0):
					return False
		return True

	def is_number_possible_to_insert(self, x, y, number: int) -> bool:
		conditions = [
			self.get_number(x, y) == 0,
			10 > number > 0,
			number not in self.get_column(x),
			number not in self.get_row(y),
			number not in self.get_smaller_square(x, y)
		]
		return True if all(conditions) else False

	def get_all_possible_to_insert(self, x, y) -> list:
		return [num for num in range(1, 10) if self.is_number_possible_to_insert(x, y, num)]

	def find_empty_position(self) -> (int, int) or None:
		for y, subl in enumerate(self.board):
			for x, value in enumerate(subl):
				if value == 0:
					return x, y
		return None

	def solve_backtracking(self, x=0, y=0) -> bool:
		# Check if the program is done, y=9 out of bounds so return
		if x == 8 and y == 9:
			return True
		if y == 9:
			x += 1
			y = 0
		if self.get_number(x, y) > 0:
			return self.solve_backtracking(x, y + 1)

		for num in self.get_all_possible_to_insert(x, y):
			self.set_number(x, y, num)
			if self.solve_backtracking(x, y + 1):
				return True
			self.set_number(x, y, 0)

		return False  # returns false if sudoku isn't solvable

	def generate(self):
		side = self.base ** 2

		# pattern for a baseline valid solution
		def pattern(r, c): return (self.base * (r % self.base) + r // self.base + c) % side

		# randomize rows, columns and numbers (of valid base pattern)
		def shuffle(s): return random.sample(s, len(s))

		r_base = range(self.base)
		print(shuffle(r_base))
		rows = [g * self.base + r for g in shuffle(r_base) for r in shuffle(r_base)]
		cols = [g * self.base + c for g in shuffle(r_base) for c in shuffle(r_base)]
		print(rows)
		print(cols)
		nums = shuffle(range(1, self.base * self.base + 1))
		print(nums)

		# produce board using randomized baseline pattern
		board = [[nums[pattern(r, c)] for c in cols] for r in rows]
		return board


sudoku_board = [[9, 5, 3, 1, 6, 7, 4, 2, 8],
				[4, 2, 8, 3, 5, 9, 7, 6, 1],
				[7, 6, 1, 8, 2, 4, 9, 5, 3],
				[5, 8, 4, 9, 3, 6, 2, 1, 7],
				[6, 3, 9, 7, 1, 2, 5, 8, 4],
				[2, 1, 7, 4, 8, 5, 6, 3, 9],
				[3, 4, 5, 6, 9, 1, 8, 7, 2],
				[8, 7, 2, 5, 4, 3, 1, 9, 6],
				[1, 9, 6, 2, 7, 8, 3, 4, 5]]

sudoku = Sudoku(sudoku_board)
sudoku.print_sudoku(nice_print=True)
