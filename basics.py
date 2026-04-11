def chess_to_index(pos):
    col=ord(pos[0])-ord('a')
    row=8-int(pos[1])
    return row,col
class Piece:
    def __init__(self,color):
        self.color=color
        self.has_Moved=False    
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
        direction=-1 if self.color=='white' else 1 #(0,0) lies on top left  
        #black pawn moves away from 0 so dir=1 and opposite for white as they move up
        if (self.color=='white'and row==6) or (self.color=='black'and row==1):#2steps on first move of a pawn
            if 0<=row+2*direction<8:
                if board[row+direction][col] is None and board[row+2*direction][col] is None:
                    moves.append((row+2*direction,col))
        #simulating move:
        new_row=row+direction
        if 0<=new_row<8 and board[row+direction][col] is None:
            moves.append((row+direction,col))
        
        #simulating captures:
        for dir in [-1,1]:
            new_col=col+dir
            new_row=row+direction
            if 0<=new_col<8 and 0<=new_row<8:
                if board[new_row][new_col] and board[new_row][new_col].color!=self.color:
                    moves.append((new_row,new_col))
        return moves


class Rook(SlidingPieces):
    def valid_moves(self,board,row,col):
        
        direction=[(0,1),(0,-1),(1,0),(-1,0)]
        moves= self.get_sliding_moves(board,row,col,direction)
        return moves
class Bishop(SlidingPieces):
    def valid_moves(self, board, row, col):
        direction=[(1,1),(1,-1),(-1,1),(-1,-1)]
        moves= self.get_sliding_moves(board,row,col,direction)
        return moves
class King(Piece):
    def valid_moves(self,board,row,col):
        moves=[]
        direction=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        for dir in direction:
            new_col=col+dir[1]
            new_row=row+dir[0]
            if 0<=new_row<8 and 0<=new_col<8:
                if board[new_row][new_col] is None or board[new_row][new_col].color!=self.color:
                    moves.append((new_row,new_col))
        return moves
        if not self.has_Moved:
            #King Side Castle
            if self.can_short_castle(board,row,col):
                moves.append((row,col+2))
            #Queen Side Castle
            if self.can_long_castle(board,row,col):
                moves.append((row,col-2))
            return moves
        def can_short_castle(self,board,row,col):
            rook =board[row][7]
            if rook is not isinstance(rook,Rook) or rook.has_moved:
                return False
            if board[row][5] and board[row][6] :
                return False
            temp_board=Board()
            for c in [col ,col+1,col+2]:
                temp_board.grid[row][col]=None
                temp_board.grid[row][c]=self
                if temp_board.isInCheck(self.color):
                    
class Queen(SlidingPieces):
    def valid_moves(self, board, row, col):        
        direction=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        moves= self.get_sliding_moves(board,row,col,direction)
        return moves
class Knight(Piece):
    def valid_moves(self, board, row, col):
        moves=[]
        direction=[(2,1),(2,-1),(1,2),(1,-2),(-2,1),(-2,-1),(-1,2),(-1,-2)]
        for dir in direction:
            new_col=col+dir[1]
            new_row=row+dir[0]
            if 0<=new_row<8 and 0<=new_col<8:
                if board[new_row][new_col] is None or board[new_row][new_col].color!=self.color :
                    moves.append((new_row,new_col))
        return moves
class Board:
    def __init__(self):
        self.grid=[[None]*8 for _ in range(8)]
        self.turn='white'
        self.setup()
    def setup(self):
        for i in range(8):
            self.grid[6][i]=Pawn('white')
            self.grid[1][i]=Pawn('black')
        self.grid[7][0]=Rook('white')
        self.grid[7][7]=Rook('white')
        self.grid[0][0]=Rook('black')
        self.grid[0][7]=Rook('black')
        self.grid[7][1]=Knight('white')
        self.grid[7][6]=Knight('white')
        self.grid[0][1]=Knight('black')
        self.grid[0][6]=Knight('black')
        self.grid[7][2]=Bishop('white')
        self.grid[7][5]=Bishop('white')
        self.grid[0][2]=Bishop("black")
        self.grid[0][5]=Bishop("black")
        self.grid[7][3]=Queen('white')
        self.grid[0][3]=Queen('black')
        self.grid[7][4]=King('white')
        self.grid[0][4]=King('black')
    def move(self,st,end):
        sr,sc=st
        er,ec=end
        piece=self.grid[sr][sc]
        if not piece:
            return False,False
        if self.turn!=piece.color:
            print("Not your Turn")
            return False,False
        valid=piece.valid_moves(self.grid,sr,sc)
        if(er,ec) not in valid:
            return False,"invalid"
        temp=self.grid[er][ec] # temporily stores piece at (er,ec)
        self.grid[er][ec]=piece
        self.grid[sr][sc]=None
        if self.isInCheck(piece.color):
            self.grid[er][ec]=temp
            self.grid[sr][sc]=piece
            return False,"self_check"

        opponent='black'if piece.color=='white'else 'white'
        check=self.isInCheck(opponent)
        self.turn=opponent
        piece.has_Moved=True
        return True,check
    def print_board(self):
        for row in self.grid:
            line=""
            for p in row:
                if p is None:
                    line+=". "
                else:
                    if type(p).__name__=="Knight":
                        Notation="N"
                    else:
                        Notation=type(p).__name__[0]
                    if p.color=="white":
                        line+=Notation.upper()+" "
                    else:
                        line+=Notation.lower()+" "
            print(line)
    def findKing(self,color):
        for row in range(8):
            for col in range(8):
                p=self.grid[row][col]
                if p and p.color==color and isinstance(p,King):
                    return (row,col)
        return None
    def isInCheck(self,color):
        kingPos=self.findKing(color)
        
        for i in range(8):
            for j in range(8):
                p=self.grid[i][j]
                if p and p.color!=color:
                    if isinstance(p,Pawn):
                        direction=-1 if p.color=='white'else 1
                        for dc in [-1,1]:
                            nr,nc=i+direction,j+dc
                            if (nr,nc)==kingPos:
                                return True
                    else:
                        moves=p.valid_moves(self.grid,i,j)
                        if kingPos in moves:
                            return True
        return False
    def checkMate(self,color):
        if not self.isInCheck(color):
            return False
        for i in range(8):
            for j in range(8):
                piece=self.grid[i][j]
                if piece and piece.color==color:
                    moves=piece.valid_moves(self.grid,i,j)
                    for ni,nj in moves:
                        temp=self.grid[ni][nj]
                        self.grid[ni][nj]=piece
                        self.grid[i][j]=None

                        still_check=self.isInCheck(color)
                        self.grid[i][j]=piece
                        self.grid[ni][nj]=temp
                        if not still_check:
                            return False
        return True

board=Board()
while True:
   
    board.print_board()
    print("turn:",board.turn)
    if board.checkMate(board.turn):
        print("CheckMate !! Game Over!!")
        break
    move=input("Enter Your move(In chess Notations):")
    s,e=move.split()
    start=chess_to_index(s)
    end=chess_to_index(e)
    success,check=board.move(start,end)
    if success:
        print("Move Done")
        if check:
            print("Check!!!!!!")
    else:
        print("Invalid Move: King would be in check" if check == "self_check" else "Invalid Move")