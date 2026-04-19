from flask import Flask,request,jsonify
from Engine.board import Board
from Engine.utils import chess_to_index

app=Flask(__name__)

board=Board()#Global Board
@app.route('/')
def home():
    return "Running Chess API"




if __name__=='__main__':
    app.run(debug=True)

