import tkinter as tk
import random
import colors

class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('2048游戏')
        self.grid_cells = []
        self.matrix = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        
        # 绑定按键事件
        self.window.bind('<Left>', self.left)
        self.window.bind('<Right>', self.right)
        self.window.bind('<Up>', self.up)
        self.window.bind('<Down>', self.down)

    def init_grid(self):
        background = tk.Frame(self.window, bg='#92877d', width=400, height=400)
        background.grid()

        for i in range(4):
            grid_row = []
            for j in range(4):
                cell = tk.Frame(
                    background,
                    bg='#9e948a',
                    width=100,
                    height=100
                )
                cell.grid(row=i, column=j, padx=5, pady=5)
                t = tk.Label(
                    cell,
                    text="",
                    bg='#9e948a',
                    justify=tk.CENTER,
                    font=('Arial', 30, 'bold'),
                    width=4,
                    height=2
                )
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def init_matrix(self):
        # 初始化时添加两个数字
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        # 在空位置随机添加一个2或4
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.matrix[i][j] = random.choice([2, 4])

    def update_grid_cells(self):
        for i in range(4):
            for j in range(4):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg='#9e948a')
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=colors.BACKGROUND_COLOR_DICT.get(new_number),
                        fg=colors.CELL_COLOR_DICT.get(new_number)
                    )
        self.window.update_idletasks()

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_grid_cells()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_grid_cells()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_grid_cells()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_grid_cells()
        self.game_over()

    def game_over(self):
        if any(0 in row for row in self.matrix):
            return

        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return
                
        for j in range(4):
            for i in range(3):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return

        game_over_frame = tk.Frame(self.window, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(
            game_over_frame,
            text="游戏结束!",
            bg='#ffffff',
            fg='#776e65',
            font=('Arial', 48, 'bold')
        ).pack()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Game2048()
    game.run() 
