
#python ./gobang.py --chess_file=example/3.txt
def Search(board, boundary, EMPTY, BLACK, WHITE, isblack):
    alpha, beta = -float('inf'), float('inf')
    return AlphaBetaSearch(board, boundary, EMPTY, BLACK, WHITE, isblack, alpha, beta)

'''def print_test(test : list[list]):
    打印棋盘上所有点的评价值，在alphabeta剪枝搜索中调用
    for i in range(15):
        for j in range(15):
            print(test[i][j], '\t', end = '')
        print()'''
 
def AlphaBetaSearch(board, boundary, EMPTY, BLACK, WHITE, isblack, alpha, beta, depth = 2) -> tuple[int, int, int]:
    i, j = 0, 0
    if depth == 0:
        return 0, 0, evaluate(board, boundary, EMPTY, BLACK, WHITE)
    if isblack:
        #test = [[0 for i in range(15)] for j in range(15)]
        value = -float('inf')
        next_states = get_successors(board, boundary, 1)
        for x, y, state, new_boundary in next_states:
            _, _, alpha1 = AlphaBetaSearch(state, new_boundary, EMPTY, BLACK, WHITE, False, alpha, beta, depth - 1)
            #test[x][y] = alpha1
            if alpha1 > value:
                i, j, value = x, y, alpha1
                alpha = max(alpha, value)
            if alpha >= beta:
                break
        #print_test(test)
        return i, j, value
    else:
        value = float('inf')
        next_states = get_successors(board, boundary, 0)
        for x, y, state, new_boundary in next_states:
            _, _, beta1 = AlphaBetaSearch(state, new_boundary, EMPTY, BLACK, WHITE, True, alpha, beta, depth - 1)
            if beta1 < value:
                i, j, value = x, y, beta1
                beta = min(beta, value)
            if alpha >= beta:
                break
        return i, j, value
      
black_pattern_scores = {(-1, 1, 1, -1) : 50,               #活二
                  (-1, 1, -1, 1, -1) : 50,                 #活二
                (1, 1, -1, 1, -1) : 200,                   #眠三
                (-1, 1, 1, 1) : 500,                       #眠三
                (1, 1, 1, -1) : 500,                       #眠三
                (-1, 1, 1, 1, -1) : 5000,                  #活三
                (-1, 1, -1, 1, 1, -1) : 5000,              #活三
                (-1, 1, 1, -1, 1, -1) : 5000,              #活三
                (1, 1, 1, -1, 1) : 6000,                   #冲四
                (1, 1, -1, 1, 1) : 6000,                   #冲四
                (1, -1, 1, 1, 1) : 6000,                   #冲四
                (1, 1, 1, 1, -1) : 6000,                   #冲四
                (-1, 1, 1, 1, 1) : 6000,                   #冲四
                (-1, 1, 1, 1, 1, -1) : 100000,             #活四
                (1, 1, 1, 1, 1) : 99999999}                #连五
white_pattern_scores = {(-1, 0, 0, -1) : 30,               #活二
                  (-1, 0, -1, 0, -1) : 30,                 #活二
                (0, 0, -1, 0, -1) : 100,                   #眠三
                (-1, 0, 0, 0) : 300,                       #眠三
                (0, 0, 0, -1) : 300,                       #眠三
                (-1, 0, 0, 0, -1) : 3000,                  #活三
                (-1, 0, -1, 0, 0, -1) : 3000,              #活三
                (-1, 0, 0, -1, 0, -1) : 3000,              #活三
                (0, 0, 0, -1, 0) : 4000,                   #冲四
                (0, 0, -1, 0, 0) : 4000,                   #冲四
                (0, -1, 0, 0, 0) : 4000,                   #冲四
                (0, 0, 0, 0, -1) : 4000,                   #冲四
                (-1, 0, 0, 0, 0) : 4000,                   #冲四
                (-1, 0, 0, 0, 0, -1) : 80000,              #活四
                (0, 0, 0, 0, 0) : 99999999}                #连五
def evaluate(board : list[list], boundary : int, EMPTY : int = -1, BLACK : int = 1, WHITE : int = 0) -> int:
    '''评价函数，传入棋盘，返回棋盘的评价值  black_score - white_score'''
    black_score = 0
    white_score = 0
    cnt = 0                                                 #统计活三和冲四的总数，如果大于等于2，则必胜，返回一个较大的值
    for pattern, score in black_pattern_scores.items():
        if score >= 3000:
            cnt += 1
        black_score += count_pattern(board, boundary, pattern) * score
    for pattern, score in white_pattern_scores.items():
        if score >= 3000:
            cnt -= 1
        white_score += count_pattern(board, boundary, pattern) * score
    if abs(cnt) >= 2:
        return black_score - white_score + cnt * 20000
    return black_score - white_score 


def _coordinate_priority(coordinate):
    #落子优先级改为从中间向四周
    x, y = coordinate[0], coordinate[1]
    return max(abs(x - 7), abs(y - 7))
    
def get_successors(board : list[list], boundary : int, color : int, priority=_coordinate_priority, EMPTY = -1):
    from copy import deepcopy
    next_board = deepcopy(board)
    range1 = max(7 - boundary - 1, 0)
    range2 = min(7 + boundary + 1, 14)
    idx_list = [(x, y) for x in range(range1, range2 + 1) for y in range(range1, range2 + 1)]
    idx_list.sort(key = priority)
    for x, y in idx_list:
        if board[x][y] == EMPTY:
            next_board[x][y] = color
            new_boundary = boundary + 1 if (x == range1 or x == range2 or y == range1 or y == range2) else boundary
            new_boundary = min(new_boundary, 7)     #确保不超过7
            yield (x, y, next_board, new_boundary)
            next_board[x][y] = EMPTY


def get_pattern_locations(board : list[list], boundary : int, pattern : tuple) -> list[tuple]:
    ROWS = len(board)
    DIRE = [(1, 0), (0, 1), (1, 1), (1, -1)]
    pattern_list = []
    palindrome = True if tuple(reversed(pattern)) == pattern else False
    for x in range(7 - boundary, 7 + boundary + 1):
        for y in range(7 - boundary, 7 + boundary + 1):
            if pattern[0] == board[x][y]:
                if len(pattern) == 1:
                    pattern_list.append((x, y, 0))
                else:
                    for dire_flag, dire in enumerate(DIRE):
                        if _check_pattern(board, ROWS, x, y, pattern, dire[0], dire[1]):
                            pattern_list.append((x, y, dire_flag))
                    if not palindrome:
                        for dire_flag, dire in enumerate(DIRE):
                            if _check_pattern(board, ROWS, x, y, pattern, -dire[0], -dire[1]):
                                pattern_list.append((x, y, dire_flag + 4))
    return pattern_list

# get_pattern_locations 调用的函数
def _check_pattern(board, ROWS, x, y, pattern, dx, dy):
    for goal in pattern[1:]:
        x, y = x + dx, y + dy
        if x < 0 or y < 0 or x >= ROWS or y >= ROWS or board[x][y] != goal:
            return False
    return True

def count_pattern(board, boundary, pattern):
    # 获取给定的棋子排列的个数
    return len(get_pattern_locations(board, boundary, pattern))

def is_win(board, color, EMPTY=-1):
    # 检查在当前 board 中 color 是否胜利
    pattern1 = (color, color, color, color, color)          # 检查五子相连
    pattern2 = (EMPTY, color, color, color, color, EMPTY)   # 检查「活四」
    return count_pattern(board, pattern1) + count_pattern(board, pattern2) > 0

