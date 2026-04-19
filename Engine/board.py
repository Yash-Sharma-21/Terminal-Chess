from .pieces import Pawn,King,Knight,Queen,Rook,Bishop
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

    def can_short_castle(self, row, col):
        if self.turn != self.grid[row][col].color:
            return False
            
        king = self.grid[row][col]
        rook = self.grid[row][7]
        
        if not rook or not isinstance(rook, Rook) or rook.has_moved or king.has_moved:
            return False
            
        if self.grid[row][5] is not None or self.grid[row][6] is not None:
            return False
            
        # Check squares between king and rook are not under attack
        if self.isInCheck(self.turn):
            return False
            
        # Check each square the king moves through
        for c in [col+1, col+2]:
            # Temporarily move king
            temp_king = self.grid[row][col]
            self.grid[row][col] = None
            self.grid[row][c] = temp_king
            
            if self.isInCheck(self.turn):
                self.grid[row][col] = temp_king
                self.grid[row][c] = None
                return False
                
            self.grid[row][col] = temp_king
            self.grid[row][c] = None
            
        return True

    def can_long_castle(self, row, col):
        if self.turn != self.grid[row][col].color:
            return False
            
        king = self.grid[row][col]
        rook = self.grid[row][0]
        
        if not rook or not isinstance(rook, Rook) or rook.has_moved or king.has_moved:
            return False
            
        if (self.grid[row][1] is not None or 
            self.grid[row][2] is not None or 
            self.grid[row][3] is not None):
            return False
            
        # Check squares between king and rook are not under attack
        if self.isInCheck(self.turn):
            return False
            
        # Check each square the king moves through
        for c in [col-1, col-2]:
            # Temporarily move king
            temp_king = self.grid[row][col]
            self.grid[row][col] = None
            self.grid[row][c] = temp_king
            
            if self.isInCheck(self.turn):
                self.grid[row][col] = temp_king
                self.grid[row][c] = None
                return False
                
            self.grid[row][col] = temp_king
            self.grid[row][c] = None
            
        return True

    def get_valid_moves_with_castle(self, piece, row, col):
        moves = piece.valid_moves(self.grid, row, col)
        
        if isinstance(piece, King) and not piece.has_moved:
            if self.can_short_castle(row, col):
                moves.append((row, col+2))
            if self.can_long_castle(row, col):
                moves.append((row, col-2))
                
        return moves

    def move(self,st,end,promoteTo="Q"):
        sr,sc=st
        er,ec=end
        piece=self.grid[sr][sc]

        if not piece:
            return False,False

        if self.turn!=piece.color:
            print("Not your Turn")
            return False,False

        # Get valid moves including castling for king
        valid=self.get_valid_moves_with_castle(piece,sr,sc)
        if (er,ec) not in valid:
            return False,"invalid"

        # Store for rollback
        captured_piece=self.grid[er][ec]
        old_has_moved=piece.has_moved
        
        # Handle castling
        if isinstance(piece,King) and abs(ec-sc)==2:
            if ec>sc:  # Short castle
                rook=self.grid[sr][7]
                # Move rook
                self.grid[er][5]=rook
                self.grid[er][7]=None
                rook.has_moved=True
                # Move king
                self.grid[er][ec]=piece
                self.grid[sr][sc]=None
            else:  # Long castle
                rook=self.grid[sr][0]
                # Move rook
                self.grid[er][3]=rook
                self.grid[er][0]=None
                rook.has_moved=True
                # Move king
                self.grid[er][ec]=piece
                self.grid[sr][sc]=None
        else:
            # Normal move
            self.grid[er][ec]=piece
            self.grid[sr][sc]=None

        # Handle promotion
        promoted=False
        if isinstance(piece,Pawn) and (
            (piece.color=='white' and er==0) or
            (piece.color=='black' and er==7)):
            self.promotion(piece.color,er,ec,promoteTo)
            promoted=True

        # Check if move puts own king in check
        if self.isInCheck(piece.color):
            # Undo move
            self.grid[sr][sc]=piece
            self.grid[er][ec]=captured_piece
            piece.has_moved=old_has_moved
            
            # Undo castling if it happened
            if isinstance(piece,King) and abs(ec-sc)==2:
                if ec>sc:  # Short castle
                    rook=self.grid[er][5]
                    self.grid[sr][7]=rook
                    self.grid[er][5]=None
                    if rook:
                        rook.has_moved=False
                else:  # Long castle
                    rook=self.grid[er][3]
                    self.grid[sr][0]=rook
                    self.grid[er][3]=None
                    if rook:
                        rook.has_moved=False
            
            return False,"self_check"

        # Move is valid
        opponent='black' if piece.color=='white' else 'white'
        check=self.isInCheck(opponent)
        
        self.turn=opponent
        piece.has_moved=True

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
        if not kingPos:
            return False
            
        for i in range(8):
            for j in range(8):
                p=self.grid[i][j]
                if p and p.color!=color:
                    if isinstance(p,Pawn):
                        direction=-1 if p.color=='white' else 1
                        for dc in [-1,1]:
                            if (i+direction,j+dc)==kingPos:
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
                    moves=self.get_valid_moves_with_castle(piece,i,j)
                    for ni,nj in moves:
                        # Try move
                        captured=self.grid[ni][nj]
                        old_has_moved=piece.has_moved
                        self.grid[ni][nj]=piece
                        self.grid[i][j]=None

                        still_check=self.isInCheck(color)

                        # Undo move
                        self.grid[i][j]=piece
                        self.grid[ni][nj]=captured
                        piece.has_moved=old_has_moved

                        if not still_check:
                            return False
        return True
        
    def promotion(self,color,er,ec,promoteTo):
        if promoteTo=="Q":
            self.grid[er][ec]=Queen(color)
        elif promoteTo=="N":
            self.grid[er][ec]=Knight(color)
        elif promoteTo=="R":
            self.grid[er][ec]=Rook(color)
        elif promoteTo=="B":
            self.grid[er][ec]=Bishop(color)
        else:
            self.grid[er][ec]=Queen(color)  # Default to Queen
    def stalemate(self,color):
        if self.isInCheck(color):
            return False
        for i in range(8):
            for j in range(8):
                piece=self.grid[i][j]
                if piece.color==color:
                    moves=piece.valid_moves(self.grid,i,j)
                    if len(moves)!=0:
                        return False
        return True
