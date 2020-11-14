function put(i, skip) {
   function checkDraw(board) {
      for (let i = 0; i < 9; i++) {
         if (!(board.charAt(i) === 'X' || board.charAt(i) === 'O')) {
            return false;
         }
      }
      return true;
   }

   let boardCurrent = document.querySelector('#status').innerHTML;

   if (checkWinner(boardCurrent, 'X') || checkWinner(boardCurrent, 'O')) {
      // alert('Game ended!')
   } else if (skip) {
      // computer first
   } else {
      boardCurrent = boardCurrent.substring(0, parseInt(i)) + 'X' + boardCurrent.substring(parseInt(i) + 1);
      fillBoard(boardCurrent);
   }

   if (checkWinner(boardCurrent, 'X') || checkWinner(boardCurrent, 'O')) {
      // this should never happen
   } else if (checkDraw(boardCurrent)) {
      // board full
   } else {
      document.getElementById("mask").setAttribute("class", '');

      let j = minimax(boardCurrent, 'O', true);
      boardCurrent = boardCurrent.substring(0, parseInt(j)) + 'O' + boardCurrent.substring(parseInt(j) + 1);
      setTimeout(function () {
         // console.log('500ms later...');
         fillBoard(boardCurrent);
         document.getElementById("mask").setAttribute("class", 'd-none');
      }, 500);
   }

   // check game end
   if (checkWinner(boardCurrent, 'X')) {
      document.querySelector('#winner').innerHTML =
         '<div class="alert alert-info" role="alert" id="result">Player wins!</div>';

   } else if (checkWinner(boardCurrent, 'O')) {
      document.querySelector('#winner').innerHTML =
         '<div class="alert alert-info" role="alert" id="result">Computer wins!</div>';

   } else if (checkDraw(boardCurrent)) {
      document.querySelector('#winner').innerHTML =
         '<div class="alert alert-info" role="alert" id="result">Draw!</div>';
   }
}

function fillCell(status, n, id) {
   let cellHtml = '<div class="col-4"><div class="outer" id="fill-id">' +
      '<div class="box fill-class" onclick="fill-onclick"></div></div></div>';

   let clickAction = '';
   if (status === 'open') {
      clickAction = 'put(\'' + n + '\')';
   }

   cellHtml = cellHtml.replace(new RegExp('fill-id', "g"), id);
   cellHtml = cellHtml.replace(new RegExp('fill-class', "g"), status);
   cellHtml = cellHtml.replace(new RegExp('fill-onclick', "g"), clickAction);

   return cellHtml;
}

function fillBoard(boardHTML) {
   let fillHtml = "";

   const row = ['A', 'B', 'C'], col = ['1', '2', '3'];

   for (let r in row) {
      for (let c in col) {
         let n = parseInt(r) * 3 + parseInt(c);
         let id = row[r] + col[c];
         let s = boardHTML.charAt(n);

         if (s === 'X') {
            fillHtml += fillCell('user', n, id)
         } else if (s === 'O') {
            fillHtml += fillCell('comp', n, id)
         } else {
            fillHtml += fillCell('open', n, id)
         }
      }
   }

   // console.log(fillHtml)
   document.querySelector('#status').innerHTML = boardHTML;
   document.querySelector('#board').innerHTML = fillHtml;
}

function checkWinner(board, gamer) {
   return (board.charAt(0) === gamer && board.charAt(1) === gamer && board.charAt(2) === gamer)
      || (board.charAt(3) === gamer && board.charAt(4) === gamer && board.charAt(5) === gamer)
      || (board.charAt(6) === gamer && board.charAt(7) === gamer && board.charAt(8) === gamer)
      || (board.charAt(0) === gamer && board.charAt(3) === gamer && board.charAt(6) === gamer)
      || (board.charAt(1) === gamer && board.charAt(4) === gamer && board.charAt(7) === gamer)
      || (board.charAt(2) === gamer && board.charAt(5) === gamer && board.charAt(8) === gamer)
      || (board.charAt(0) === gamer && board.charAt(4) === gamer && board.charAt(8) === gamer)
      || (board.charAt(2) === gamer && board.charAt(4) === gamer && board.charAt(6) === gamer);
}

function minimax(board, gamer, main) {
   // console.log(board + gamer + main);

   function switchGamer(gamer) {
      if (gamer === 'O') {
         return 'X';
      } else {
         return 'O';
      }
   }

   let available = [], availableCount = 0;
   for (let i = 0; i < 9; i++) {
      if (!(board.charAt(i) === 'X' || board.charAt(i) === 'O')) {
         available[availableCount] = i;
         availableCount += 1;
      }
   }

   if (checkWinner(board, 'X')) {
      return 0;
   } else if (checkWinner(board, 'O')) {
      return 2;
   } else if (availableCount === 0) {
      return 1
   }

   let value = [];
   for (let i = 0; i < available.length; i++) {
      let next = available[i];
      let nextBoard = board.substring(0, next) + gamer + board.substring(next + 1);
      value[i] = minimax(nextBoard, switchGamer(gamer));
   }

   if (main) {
      let bestValue = Math.max(...value);
      let candidate = [], candidateCount = 0;
      for (let i = 0; i < available.length; i++) {
         if (value[i] === bestValue) {
            candidate[candidateCount] = available[i];
            candidateCount += 1;
         }
      }

      // console.log(available.toString() + '\n' + value.toString())
      let candidateRandom = Math.floor(Math.random() * candidateCount);
      return candidate[candidateRandom];

   } else {
      if (gamer === 'O') {
         return Math.max(...value);
      } else
         return Math.min(...value);
   }
}

function newGame(compFirst) {
   document.querySelector('#winner').innerHTML = '';

   let boardInit = "012345678";
   fillBoard(boardInit);

   if (compFirst) {
      put(0, true);
   }
}

document.addEventListener("DOMContentLoaded",
   function (event) {
      newGame();
   }
);