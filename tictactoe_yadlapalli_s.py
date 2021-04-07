#Sreya Yadlapalli 12/4/18

def gen_sols():
    sols = []
    sols.append([0, 1, 2])
    sols.append([3, 4, 5])
    sols.append([6, 7, 8])
    sols.append([0, 3, 6])
    sols.append([1, 4, 7])
    sols.append([2, 5, 8])
    sols.append([0, 4, 8])
    sols.append([2, 4, 6])
    return sols

def positions():
    post = {}
    post[0] = (0, 0)
    post[1] = (0, 1)
    post[2] = (0, 2)
    post[3] = (1, 0)
    post[4] = (1, 1)
    post[5] = (1, 2)
    post[6] = (2, 0)
    post[7] = (2, 1)
    post[8] = (2, 2)
    return post

def move(board):
    player = decturn(board)
    result = []
    for index in range(0, 9):
        if board[index] == '.':
            state = board[:index] + player + board[index+1:]
            result.append(state)
    return result

def decturn(board):
    countx = 0
    counto = 0
    for char in board:
        if char == 'X':
            countx += 1
        if char == 'O':
            counto += 1
    if(countx == counto):
        return 'X'
    else:
        return 'O'

def result(board):
    for i in range(0, 3):
        print(board[i], end =" ")
    print()
    for i in range(3, 6):
        print(board[i], end = " ")
    print()
    for i in range(6, 9):
        print(board[i], end = " ")
    print()
    print()

def Minimax_Decision(board, sols):
    return Max_Value(board, sols)

def Max_Value(board, sols):
    if getX(board, sols):
        return board, 1
    if getO(board, sols):
        return board, -1
    if checkDraw(board):
        return board, 0

    value = -1000
    temp = board
    for state in move(board):
        result = Min_Value(state, sols)
        if result[1] > value:
            temp = state
            value = result[1]
        if(value == 1):
            break
    return temp, value

def Min_Value(board, sols):
    if getX(board, sols):
        return board, 1
    if getO(board, sols):
        return board, -1
    if checkDraw(board):
        return board, 0

    value = 1000
    temp = board
    for state in move(board):
        result = Max_Value(state, sols)
        if result[1] < value:
            temp = state
            value = result[1]
        if(value == -1):
            break
    return temp, value

def checkDraw(board):
    count = 0
    for char in board:
        if char == 'X':
            count += 1
        elif char == 'O':
            count += 1
    return count == 9

def getX(board, solutions):
    result = []
    for index in range(0, 9):
        if board[index] == 'X':
            result.append(index)

    isSol = True
    for sol in solutions:
        for pos in sol:
            if pos not in result:
                isSol = False
                break
        if isSol:
            return True
        isSol = True
    return False

def getO(board, sols):
    result = []
    for index in range(0, 9):
        if board[index] == 'O':
            result.append(index)
    isSol = True
    for sol in sols:
        for pos in sol:
            if pos not in result:
                isSol = False
                break
        if isSol:
            return True
        isSol = True
    return False

def oturns(board):
    indexes = []
    for index in range(0, 9):
        if board[index] == '.':
            indexes.append(index)
    return indexes

def main():
    initial = input("Enter a 9 char string with X's, O's, and dots (in all CAPS): ")
    solutions = gen_sols()
    places = positions()

    print("Game start:")
    result(initial)


    if(getX(initial, solutions)):
        print("X wins!")
    elif (getO(initial, solutions)):
        print("O wins!")
    else:
        bool = True
        state = initial
        player = decturn(initial)
        if(player == 'O'):
            print("O's turn: ")
            for move in oturns(initial):
                print(str(move) + " " + str(places[move]))
            print()
            x = int(input("Enter a number to play"))
            state = initial[:x] + 'O' + initial[x+1:]
            result(state)
            if (getO(state, solutions)):
                print("O wins!")
                bool = False

        while(bool):
            final = Minimax_Decision(state, solutions)
            board = final[0]
            print("X's turn: ")
            result(board)
            if (getX(board, solutions)):
                print("X wins!")
                bool = False
                break
            elif (getO(board, solutions)):
                print("O wins!")
                bool = False
                break
            elif checkDraw(board):
                print("DRAW")
                bool = False
                break
            else:
                print("O's turn: ")
                for move in oturns(board):
                    print(str(move) + " " + str(places[move]))
                print()
                x = int(input("Enter a number to play"))
                state = board[:x] + 'O' + board[x + 1:]
                result(state)
                if (getO(state, solutions)):
                    print("O wins!")

if __name__ == '__main__':
    main()
