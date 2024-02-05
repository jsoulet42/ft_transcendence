var canvas = document.getElementById('pongCanvas');
var ctx = canvas.getContext('2d');
document.addEventListener("keydown", keyDownHandler, false); // écouteur d'événement
document.addEventListener("keyup", keyUpHandler, false); // écouteur d'événement

canvas.width = window.innerWidth * 0.2;
canvas.height = window.innerHeight * 0.2;

let ball = {
	x: canvas.width / 2,
	y: canvas.height / 2,
	speedX: 10,
	speedY: 0,
	Bradius: canvas.height / 50,
	speedBaseX: 20, // Vitesse de déplacement horizontal de la balle
	speedBaseY: 0, // Vitesse de déplacement vertical de la balle
	Bcolor: 'blue'
};
let IA = {
	destYRT: 0,
	destYL: 0,
	move: false
}
var angle = 5;
var paddleLeftHeight = canvas.width / 15;
var paddleLeftWidth = canvas.height / 50;
var paddleRightHeight = canvas.width / 15;
var paddleRightWidth = canvas.height / 50;
var paddleLeftY = (canvas.height - paddleLeftHeight) / 3; // start in the middle of the canvas
var paddleRightY = (canvas.height - paddleRightHeight) / 2; // start in the middle of the canvas
var upLeft = false;
var downLeft = false;
var upRight = false;
var downRight = false;
var posBord = 10;
var leftScore = 0;
var rightScore = 0;
var marge = 10;
var debug1 = 0;
var debug2 = 0;

let paddleSpeed = 10; // Vitesse de déplacement des raquettes

var pause = false;
var putBackBallBool = false;
startUpdatingAI();

function drawScore() {
	ctx.font = "1em Arial";
	ctx.fillStyle = 'white';
	ctx.fillText("Score: " + leftScore, 15, 25);
	ctx.fillText("Score: " + rightScore, canvas.width - 100, 25);
}

async function putBackBall(directionX) {
	putBackBallBool = true;
	stopUpdatingAI();
	// Stop the ball for 1 second
	ball.speedX = 0;
	ball.speedY = 0;
	for (let i = 0; i < 100; i++) {
		ball.Bradius += 0.5; // Increase the size of the ball
		if (i % 10 == 0)
			changeColor();
		await delay(10); // Wait for 0.1 seconds
	}
	startUpdatingAI();
	await delay(1000); // Wait for 1 second

	putBackBallBool = false;
	// Place the ball at the center of the canvas for 1 second
	ball.x = canvas.width / 2;
	ball.y = canvas.height / 2;
	ball.Bradius = canvas.height / 50;
	await delay(1000); // Wait for 1 second

	// Send the ball
	while (pause)
		await delay(100);
	ball.speedX = ball.speedBaseX * directionX;
	ball.speedY = (Math.random() * 2 - 1) * ball.speedBaseY;
}

function delay(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

function drawDebug() {
	var posDebugX = 10;
	var posDebugY = 10;
	var ecart = 20;
	ctx.font = "1em Arial";
	ctx.fillStyle = "#0095DD";
	ctx.fillText("destYRT: " + IA.destYRT.toFixed(2), posDebugY, canvas.height - 5 * ecart + posDebugX);
	ctx.fillText("destYL " + IA.destYL.toFixed(2), posDebugY, canvas.height - 4 * ecart + posDebugX);
	//ctx.fillText("Pos Ball X / Y: " + ball.x.toFixed(2) + " / " + ball.y.toFixed(2), posDebugY, canvas.height - 3 * ecart + posDebugX);
	//ctx.fillText("Right Paddle Y: " + paddleRightY.toFixed(2), posDebugY, canvas.height - 2 * ecart + posDebugX);
	//ctx.fillText("Left Paddle Y: " + paddleLeftY.toFixed(2), posDebugY, canvas.height - 1 * ecart + posDebugX);
}

function changeColor() {

	var red = Math.floor(Math.random() * 256);
	var green = Math.floor(Math.random() * 256);
	var blue = Math.floor(Math.random() * 256);
	ball.Bcolor = "rgb(" + red + "," + green + "," + blue + ")";
}

function collisionDetection() {
	if (putBackBallBool)
		return;
	if (ball.x + ball.Bradius > canvas.width - posBord) // Si la balle touche le bord droit du canvas
	{
		if (ball.y - paddleRightY < - marge || (ball.y - ball.Bradius) - (paddleRightY + paddleRightHeight) > marge) {
			leftScore++;
			putBackBall(-1);
		}
		else {
			var centrePaddle = paddleRightY + paddleRightHeight / 2;	/// centre de la raquette
			if (ball.y < centrePaddle)
				ball.speedY = -1 * (centrePaddle - ball.y) / angle;
			else
				ball.speedY = (ball.y - centrePaddle) / angle;
		}
	}
	else {
		if ((ball.y + ball.Bradius) - paddleLeftY < - marge || (ball.y - ball.Bradius) - (paddleLeftY + paddleLeftHeight) > marge) {
			rightScore++;
			putBackBall(1);
		}
		else {
			var centrePaddle = paddleLeftY + paddleLeftHeight / 2;	/// centre de la raquette
			if (ball.y < centrePaddle)
				ball.speedY = -1 * (centrePaddle - ball.y) / angle;
			else
				ball.speedY = (ball.y - centrePaddle) / angle;
		}
	}
}

function drawBall() {
	// Dessinez la balle à sa nouvelle position
	ctx.beginPath();
	//	ctx.arc(ball.x, ball.y, ball.Bradius, 0, Math.PI * 2);
	ctx.arc(Math.round(ball.x), Math.round(ball.y), ball.Bradius, 0, Math.PI * 2);
	ctx.fillStyle = ball.Bcolor;

	// Mettez à jour les coordonnées de la balle en fonction de sa vitesse
	ball.x += ball.speedX;
	ball.y += ball.speedY;

	// Assurez-vous que la balle rebondisse sur les bords du canvas
	if (ball.x + ball.Bradius > canvas.width - posBord || ball.x - ball.Bradius < posBord) // Si la balle touche le bord gauche ou droit du canvas
	{
		//fonction qui vérifie si la balle touche la raquette gauche
		collisionDetection();
		if (!putBackBallBool)
			changeColor();


		ball.speedX = -ball.speedX; // Inverser la direction horizontale
	}
	if (ball.y + ball.Bradius > canvas.height || ball.y - ball.Bradius < 0) {
		if (!putBackBallBool)
			changeColor();
		ball.speedY = -ball.speedY; // Inverser la direction verticale
	}
	ctx.fill();
	ctx.closePath();
}

function drawVerticalBar() // Dessinez une barre verticale au centre du canvas

{
	var centerX = canvas.width / 2;
	var barHeight = canvas.height;

	// Démarrez un nouveau chemin
	ctx.beginPath();

	// Déplacez le point de départ de la ligne au centre du canvas
	ctx.moveTo(centerX, 0);

	// Tracez une ligne verticale jusqu'au bas du canvas
	ctx.lineTo(centerX, barHeight);

	// Appliquez les styles de ligne et dessinez la ligne
	ctx.strokeStyle = 'black'; // Couleur de la ligne
	ctx.lineWidth = 5; // Épaisseur de la ligne
	ctx.stroke(); // Dessinez la ligne

	// Terminez le chemin
	ctx.closePath();
}

function drawLine(ax, ay, bx, by) {
	ctx.beginPath();
	ctx.moveTo(ax, ay);
	ctx.lineTo(bx, by);
	ctx.strokeStyle = 'black'; // Couleur de la ligne
	ctx.lineWidth = 5; // Épaisseur de la ligne
	ctx.stroke(); // Dessinez la ligne
	ctx.closePath();
}

function keyDownHandler(e)// Fonction de gestion des événements
{
	if (!pause) {
		if (e.key == "z" || e.key == "Z") {
			upLeft = true;
		}
		else if (e.key == "s" || e.key == "S") {
			downLeft = true;
		}
		else if (e.key == "ArrowUp") {
			upRight = true;
		}
		else if (e.key == "ArrowDown") {
			downRight = true;
		}
		else if (e.key == "a") {
			if (ball.speedX >= 0)
				ball.speedX++;
			else
				ball.speedX--;
		}
		else if (e.key == "q" && ball.speedX > 1 && ball.speedY > 1) {
			if (ball.speedX >= 0)
				ball.speedX--;
			else
				ball.speedX++;
			if (ball.speedY >= 0)
				ball.speedY--;
			else
				ball.speedY++;
		}
	}
	if (e.key == " ") {
		pauseGame();
	}
}

function pauseGame() {
	if (pause) {
		ball.speedX = directionX;
		ball.speedY = directionY;
		startUpdatingAI();
		pause = false;
	}
	else {
		stopUpdatingAI();
		directionX = ball.speedX;
		directionY = ball.speedY;
		ball.speedX = 0;
		ball.speedY = 0;
		// pause = false;
		// upLeft = false;
		// downLeft = false;
		// upRight = false;
		// downRight = false;
		pause = true;
	}
}

function keyUpHandler(e) {
	if (e.key == "z" || e.key == "Z") {
		upLeft = false;
	}
	else if (e.key == "s" || e.key == "S") {
		downLeft = false;
	}
	else if (e.key == "ArrowUp") {
		upRight = false;
	}
	else if (e.key == "ArrowDown") {
		downRight = false;
	}
}

function drawPaddle()// Fonctioner qui dessine les raquettes
{
	ctx.beginPath();
	ctx.rect(5, paddleLeftY, paddleLeftWidth, paddleLeftHeight);
	ctx.rect(canvas.width - paddleRightWidth - 5, paddleRightY, paddleRightWidth, paddleRightHeight);
	var grd = ctx.createLinearGradient(0, 0, 0, canvas.height);
	grd.addColorStop(0, "blue");
	grd.addColorStop(1, "red");

	ctx.fillStyle = grd;
	ctx.fill();
	ctx.closePath();
}

function lisenInput() {
	if (pause || putBackBallBool)
		return;
	if (upLeft) {
		paddleLeftY -= paddleSpeed;
		if (paddleLeftY < 0) {
			paddleLeftY = 0;
		}
	}
	else if (downLeft) {
		paddleLeftY += paddleSpeed;
		if (paddleLeftY + paddleLeftHeight > canvas.height) {
			paddleLeftY = canvas.height - paddleLeftHeight;
		}
	}
	if (upRight) {
		paddleRightY -= paddleSpeed;
		if (paddleRightY < 0) {
			paddleRightY = 0;
		}
	}
	else if (downRight) {
		paddleRightY += paddleSpeed;
		if (paddleRightY + paddleRightHeight > canvas.height) {
			paddleRightY = canvas.height - paddleRightHeight;
		}
	}
}
//#region IA
//Fonction qui calcul la trajectoire de la balle
function IATrajectory(ox, oy, speedX, speedY, stop) {

	if (stop++ == 4)
		return;
	if (putBackBallBool || pause || ball.speedX == 0)
		return;
	var dx = ox; //coordonnée du point d'intersection de la balle avec le bord du canvas
	var dy = oy; //coordonnée du point d'intersection de la balle avec le bord du canvas

	// Calculate the intersection point with the canvas border
	if (speedX > 0) {
		// Ball is moving to the right
		while (dx < canvas.width - ball.Bradius) {
			dy += speedY;
			dx += speedX;
			if (dy < ball.Bradius || dy > canvas.height - ball.Bradius) break;
		}
	} else {
		// Ball is moving to the left
		while (dx > ball.Bradius) {
			dy += speedY;
			dx += speedX;
			if (dy < ball.Bradius || dy > canvas.height - ball.Bradius) break;
		}
	}

	// Ensure the intersection point is within the canvas
	dx = Math.max(ball.Bradius, Math.min(dx, canvas.width - ball.Bradius));
	dy = Math.max(ball.Bradius, Math.min(dy, canvas.height - ball.Bradius));

	debug1 = dx;
	debug2 = dy;

	//si la balle ne touche pas les bords droit ou gauche du canvas on refait le calcul pour afficher une nouvelle ligne
	if (dx != ball.Bradius && dx != canvas.width - ball.Bradius)
		IATrajectory(dx, dy, speedX, -speedY, stop);
	else if (ball.speedX > 0)
		IA.destYRT = dy;
	drawLine(ox, oy, dx, dy);
}

var updateInterval;

function startUpdatingAI() {
	updateInterval = setInterval(IAUpdate, 1000);
}

function stopUpdatingAI() {
	clearInterval(updateInterval);
}

function IAUpdate() {
	IA.destYL = IA.destYRT;
}

function IAMove() {
	if (putBackBallBool || pause || ball.speedX == 0)
		return;
	var centrePaddle = paddleRightY + paddleRightHeight / 2;	/// centre de la raquette
	var ecart = IA.destYL - centrePaddle;
	var aiPaddleSpeed = paddleSpeed * 1;  // AI moves twice as fast

	if (ecart > 0) {
		paddleRightY += aiPaddleSpeed;
		if (paddleRightY + paddleRightHeight > canvas.height) {
			paddleRightY = canvas.height - paddleRightHeight;
		}
	} else if (ecart < 0) {
		var moveAmount = Math.min(-ecart, aiPaddleSpeed);
		paddleRightY -= moveAmount;
		if (paddleRightY < 0) {
			paddleRightY = 0;
		}
	}
}

startUpdatingAI();
//#endregion

function draw() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	lisenInput();
	drawPaddle();
	drawVerticalBar();
	IATrajectory(ball.x, ball.y, ball.speedX, ball.speedY, 0)
	drawScore();
	drawDebug();
	drawBall();
	IAMove();
}
setInterval(draw, 10);
