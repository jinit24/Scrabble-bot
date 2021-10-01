def NextMoveAB(board, state, turn, depth, max_depth, alpha, beta):

    # Maximizer
    if(turn == 'W'):

      best_move = [-inf, (-1,-1)]
      for i in range(8):
        for j in range(8):

          p = copy.deepcopy(board[i][j])
          if(p != '' and p[0]=='W'):

            moves = copy.deepcopy(state[p]['Moves'])
            capture_m = copy.deepcopy(state[p]['Pieces Attacking'])

            for m in capture_m:
              og = copy.deepcopy(board[m[1]][m[2]])
              board[i][j] = ""
              board[m[1]][m[2]] = p
              update_state(board,state)

              # print("White's turn, move made is", p ,m, evaluate_position(board, state, 'W'), depth, moves)
              # print_board(board)

              if(depth == max_depth):
                x = evaluate_position(board, state, 'W')
                if(x > best_move[0]):
                  best_move = [x, p, m]
              else:
                val = NextMoveAB(board, state, 'B', depth + 1, max_depth, alpha, beta)
                if(val[0] > best_move[0]):
                  best_move = [val[0], p, m]

              board[m[1]][m[2]] = og
              board[i][j] = p
              update_state(board,state)

              if(best_move[0] >= beta):
                return best_move

              alpha = max(alpha, best_move[0])

            for m in moves:

              board[i][j] = ""
              board[m[0]][m[1]] = p
              update_state(board,state)
              # print("White's turn, move made is", p ,m, evaluate_position(board, state, 'W'), depth, moves)
              # print_board(board)

              if(depth == max_depth):
                x = evaluate_position(board, state, 'W')
                if(x > best_move[0]):
                  best_move = [x, p, m]
              else:
                val = NextMoveAB(board, state, 'B', depth + 1, max_depth, alpha, beta)
                if(val[0] > best_move[0]):
                  best_move = [val[0], p, m]

              board[m[0]][m[1]] = ""
              board[i][j] = p
              update_state(board,state)

              if(best_move[0] >= beta):
                return best_move

              alpha = max(alpha, best_move[0])

      return best_move
    # Minimizer
    else:

      best_move = [inf, (-1,-1)]
      for i in range(8):
        for j in range(8):

          p = copy.deepcopy(board[i][j])
          if(p!='' and p[0]=='B'):

            moves = copy.deepcopy(state[p]['Moves'])
            capture_m = copy.deepcopy(state[p]['Pieces Attacking'])

            for m in capture_m:
              og = copy.deepcopy(board[m[1]][m[2]])
              board[i][j] = ""
              board[m[1]][m[2]] = p
              update_state(board,state)

              if(depth == max_depth):
                x = evaluate_position(board, state, 'B')
                if(x < best_move[0]):
                  best_move = [x, p, m]
              else:
                val = NextMoveAB(board, state, 'W', depth + 1, max_depth, alpha, beta)
                if(val[0] < best_move[0]):
                  best_move = [val[0], p, m]

              board[m[1]][m[2]] = og
              board[i][j] = p
              update_state(board,state)

              if(best_move[0] <= alpha):
                return best_move

              beta = min(beta, best_move[0])

            for m in moves:

              board[i][j] = ""
              board[m[0]][m[1]] = p
              update_state(board,state)
              # print("Black's turn, move made is", p, m, evaluate_position(board, state, 'B'), depth)
              # print_board(board)

              if(depth == max_depth):
                x = evaluate_position(board, state, 'B')
                if(x < best_move[0]):
                  best_move = [x, p, m]
              else:
                val = NextMoveAB(board, state, 'W', depth + 1, max_depth, alpha, beta)
                if(val[0] < best_move[0]):
                  best_move = [val[0], p, m]

              board[m[0]][m[1]] = ""
              board[i][j] = p
              update_state(board,state)   

              if(best_move[0] <= alpha):
                return best_move

              beta = min(beta, best_move[0])

      return best_move