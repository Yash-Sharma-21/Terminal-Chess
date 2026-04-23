from flask import Flask,request,jsonify,render_template
from Engine.board import Board
from Engine.utils import chess_to_index

app=Flask(__name__,template_folder='templates')

board=Board()#Global Board
@app.route('/play')
def play():
    return render_template('index.html')
@app.route('/')
def home():
    return "Running Chess API"

@app.route('/new_game',methods=['POST'])
def new_game():
    global board
    board=Board()
    return jsonify({
        "message":"New Game Started"
    })
@app.route('/board',methods=['GET'])
def get_board():
    result=[]
    for row in board.grid:
        temp=[]
        for p in row:
            if p is None:
                temp.append('.')
            else:
                symbol=p.__class__.__name__[0]
                if p.__class__.__name__=='Knight':
                    symbol='N'
                if p.color=='black':
                    symbol=symbol.lower()
                temp.append(symbol)
    result.append(temp)

    return jsonify({
        "board":result,
        "turn": board.turn

    })
@app.route('/move',methods=['POST'])
def make_move():
    data=request.json
    try:
        start=chess_to_index(data["from"])
        end=chess_to_index(data["to"])
    except:
        return jsonify({"Error":"Invalid Input"}),400
    success,check=board.move(start,end)
    return jsonify({
        "success":success,
        "check":check,
        "turn":board.turn
    })

if __name__=='__main__':
    app.run(debug=True)

