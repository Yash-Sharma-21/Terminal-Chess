class Piece:
    def __init__(self,color):
        self.color=color
        self.has_moved=False    
    def valid_moves(self,board,row,col):
        return[]

class SlidingPieces(Piece):
    def get_sliding_moves(self,board,i,j,directions):
        moves=[]
        for dr,dc in directions:
            new_row=i+dr
            new_col=j+dc
            while 0<=new_row<8 and 0<=new_col<8:
                if board[new_row][new_col] is None:
                    moves.append((new_row,new_col))
                elif board[new_row][new_col].color!=self.color:
                    moves.append((new_row,new_col))
                    break
                else:
                    break
                new_row+=dr
                new_col+=dc
        return moves

class Pawn(Piece):
    def valid_moves(self,board,row,col):
        moves=[]
        direction=-1 if self.color=='white' else 1
        
        # 1 step
        new_row=row+direction
        if 0<=new_row<8 and board[new_row][col] is None:
            moves.append((new_row,col))

            # 2 step
            if (self.color=='white' and row==6) or (self.color=='black' and row==1):
                if board[row+2*direction][col] is None:
                    moves.append((row+2*direction,col))
        
        # captures
        for dc in [-1,1]:
            new_col=col+dc
            new_row=row+direction
            if 0<=new_col<8 and 0<=new_row<8:
                if board[new_row][new_col] is not None and board[new_row][new_col].color!=self.color:
                    moves.append((new_row,new_col))
        return moves

class Rook(SlidingPieces):
    def valid_moves(self,board,row,col):
        direction=[(0,1),(0,-1),(1,0),(-1,0)]
        return self.get_sliding_moves(board,row,col,direction)

class Bishop(SlidingPieces):
    def valid_moves(self, board, row, col):
        direction=[(1,1),(1,-1),(-1,1),(-1,-1)]
        return self.get_sliding_moves(board,row,col,direction)

class King(Piece):
    def valid_moves(self,board,row,col):
        moves=[]
        direction=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        for dr,dc in direction:
            new_row=row+dr
            new_col=col+dc
            if 0<=new_row<8 and 0<=new_col<8:
                if board[new_row][new_col] is None or board[new_row][new_col].color!=self.color:
                    moves.append((new_row,new_col))        
        return moves

class Queen(SlidingPieces):
    def valid_moves(self, board, row, col):        
        direction=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        return self.get_sliding_moves(board,row,col,direction)

class Knight(Piece):
    def valid_moves(self, board, row, col):
        moves=[]
        direction=[(2,1),(2,-1),(1,2),(1,-2),(-2,1),(-2,-1),(-1,2),(-1,-2)]
        for dr,dc in direction:
            new_row=row+dr
            new_col=col+dc
            if 0<=new_row<8 and 0<=new_col<8:
                if board[new_row][new_col] is None or board[new_row][new_col].color!=self.color :
                    moves.append((new_row,new_col))
        return moves
