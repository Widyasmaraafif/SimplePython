import tkinter as tk
import random


class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.level_frame = None
        self.game_frame = None
        self.refresh_button = None
        self.message_label = None

        # Default game settings
        self.ROW = 5
        self.COL = 5
        self.MINES = 5

        # Show level selection screen
        self.show_level_selection()

    def show_level_selection(self):
        """Tampilkan layar awal untuk memilih level"""
        if self.game_frame:
            self.game_frame.destroy()

        self.level_frame = tk.Frame(self.master)
        self.level_frame.pack()

        title_label = tk.Label(self.level_frame, text="Minesweeper", font=("Arial", 24))
        title_label.pack(pady=10)

        easy_button = tk.Button(self.level_frame, text="Easy (5x5)", font=("Arial", 14),
                                command=lambda: self.start_game(5, 5, 5))
        easy_button.pack(pady=5)

        medium_button = tk.Button(self.level_frame, text="Medium (10x10)", font=("Arial", 14),
                                  command=lambda: self.start_game(10, 10, 15))
        medium_button.pack(pady=5)

        hard_button = tk.Button(self.level_frame, text="Hard (15x15)", font=("Arial", 14),
                                command=lambda: self.start_game(15, 15, 30))
        hard_button.pack(pady=5)

    def start_game(self, rows, cols, mines):
        """Mulai permainan baru dengan pengaturan level"""
        self.ROW = rows
        self.COL = cols
        self.MINES = mines

        if self.level_frame:
            self.level_frame.destroy()

        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack()

        self.new_game()

    def new_game(self):
        """Inisialisasi permainan baru"""
        self.board = self.initialize_board()
        self.buttons = {}
        self.revealed = [[False for _ in range(self.COL)] for _ in range(self.ROW)]
        self.game_over = False

        # Hapus pesan game over jika ada
        if self.message_label:
            self.message_label.destroy()
            self.message_label = None

        # Hapus tombol refresh jika ada
        if self.refresh_button:
            self.refresh_button.destroy()
            self.refresh_button = None

        # Buat tombol-tombol di grid
        self.create_buttons()

        # Taruh bom di grid
        self.place_mines()

        # Hitung jumlah bom di sekitar setiap sel
        self.calculate_numbers()

    def initialize_board(self):
        """Buat board awal tanpa bom"""
        return [[' ' for _ in range(self.COL)] for _ in range(self.ROW)]

    def place_mines(self):
        """Letakkan bom di board secara acak"""
        mines_placed = 0
        while mines_placed < self.MINES:
            row = random.randint(0, self.ROW - 1)
            col = random.randint(0, self.COL - 1)
            if self.board[row][col] != '*':
                self.board[row][col] = '*'
                mines_placed += 1

    def calculate_numbers(self):
        """Hitung jumlah bom di sekitar setiap sel"""
        for row in range(self.ROW):
            for col in range(self.COL):
                if self.board[row][col] == '*':
                    continue
                mine_count = 0
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        if 0 <= r < self.ROW and 0 <= c < self.COL and self.board[r][c] == '*':
                            mine_count += 1
                if mine_count > 0:
                    self.board[row][col] = str(mine_count)

    def create_buttons(self):
        """Buat tombol-tombol di grid"""
        for row in range(self.ROW):
            for col in range(self.COL):
                button = tk.Button(
                    self.game_frame, text=' ', width=4, height=2,
                    command=lambda r=row, c=col: self.reveal_cell(r, c)
                )
                button.grid(row=row, column=col)
                self.buttons[(row, col)] = button

    def reveal_cell(self, row, col):
        """Tampilkan isi sel ketika diklik"""
        if self.game_over or self.revealed[row][col]:
            return
        self.revealed[row][col] = True

        # Jika sel adalah bom
        if self.board[row][col] == '*':
            self.buttons[(row, col)].config(text='*', bg='red')
            self.game_over = True
            self.show_game_over_message("You Lost!")
            self.show_refresh_button()
            return

        # Jika sel bukan bom
        self.buttons[(row, col)].config(text=self.board[row][col], bg='lightgray')
        if self.board[row][col] == ' ':
            # Jika tidak ada bom di sekitar, buka sel-sel di sekitarnya
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.ROW and 0 <= c < self.COL and not self.revealed[r][c]:
                        self.reveal_cell(r, c)

        # Cek apakah pemain menang
        if self.check_win():
            self.game_over = True
            self.show_game_over_message("Congratulations! You Won!")
            self.show_refresh_button()

    def show_game_over_message(self, message):
        """Tampilkan pesan saat game selesai"""
        if self.message_label:
            self.message_label.destroy()
        self.message_label = tk.Label(self.game_frame, text=message, font=("Arial", 16))
        self.message_label.grid(row=self.ROW, column=0, columnspan=self.COL, pady=5)

    def check_win(self):
        """Periksa apakah semua sel yang bukan bom sudah terbuka"""
        for row in range(self.ROW):
            for col in range(self.COL):
                if self.board[row][col] != '*' and not self.revealed[row][col]:
                    return False
        return True

    def show_refresh_button(self):
        """Tampilkan tombol untuk memulai game baru"""
        if self.refresh_button:
            self.refresh_button.destroy()

        self.refresh_button = tk.Button(
            self.game_frame, text="New Game", command=self.show_level_selection, width=15, height=2
        )
        self.refresh_button.grid(row=self.ROW + 1, column=0, columnspan=self.COL, pady=10)


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
