import random

def display_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board):
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != " ":
            return True

    for col in range(len(board[0])):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return True

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return True

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return True

    return False

def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = random.choice(players)
    winner = False

    while not winner and not is_board_full(board):
        display_board(board)
        print(f"It's {current_player}'s turn")
        row = int(input("Enter row (0, 1, or 2): "))
        col = int(input("Enter column (0, 1, or 2): "))

        if board[row][col] == " ":
            board[row][col] = current_player
            if check_winner(board):
                winner = current_player
            else:
                current_player = "O" if current_player == "X" else "X"
        else:
            print("That position is already taken!")

    display_board(board)
    if winner:
        print(f"{winner} wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()
