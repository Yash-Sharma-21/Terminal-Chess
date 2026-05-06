function indexToChess(pos) {
    let row = 8 - pos[0]; // convert 0-index row → chess row
    let col = String.fromCharCode('a'.charCodeAt(0) + pos[1]); // 0 → 'a'
    return col + row;
}

const boardDiv = document.getElementById("board");

let selected = null;

// Draw board
function drawBoard(board) {
    boardDiv.innerHTML = "";

    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            let cell = document.createElement("div");
            cell.className = "cell";

            // Show piece (fallback to empty string)
            cell.innerText = board[i][j] || "";

            // Click handler
            cell.addEventListener("click", () => handleClick(i, j));

            boardDiv.appendChild(cell);
        }
    }
}

// Handle clicks
function handleClick(i, j) {
    if (!selected) {
        selected = [i, j];
    } else {
        move(selected, [i, j]);
        selected = null;
    }
}

// Send move to backend
async function move(start, end) {
    try {
        let res = await fetch("/move", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                from: indexToChess(start),
                to: indexToChess(end)
            })
        });

        let data = await res.json();

        if (data.error) {
            alert(data.error);
        } else {
            drawBoard(data.board);
        }
    } catch (err) {
        console.error("Move error:", err);
    }
}

// Load initial board
async function loadBoard() {
    try {
        let res = await fetch("/board");
        let data = await res.json();
        drawBoard(data.board);
    } catch (err) {
        console.error("Load error:", err);
    }
}

// Initial call
loadBoard();