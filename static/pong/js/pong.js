var canvas = document.getElementById('pongCanvas');
var ctx = canvas.getContext('2d');
document.addEventListener("keydown", keyDownHandler, false); // écouteur d'événement
document.addEventListener("keyup", keyUpHandler, false); // écouteur d'événement

//#region Variables
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var updateInterval;

var posBord = 10;

let lastTime = Date.now();

//#endregion

//#region Variables Object
let ball = {
	x: canvas.width / 2,
	y: canvas.height / 2,
	speedX: canvas.width / 150,
	speedY: 0,
	Bradius: canvas.height / 50,
	speedBaseX: canvas.width / 100, // Vitesse de déplacement horizontal de la balle
	speedBaseY: canvas.height / 100 * 0, // Vitesse de déplacement vertical de la balle
	Bcolor: 'blue'
}

function initializeBall(speed) {
	ball = {
		x: canvas.width / 2,
		y: canvas.height / 2,
		speedX: speed,
		speedY: 0,
		Bradius: canvas.height / 50,
		speedBaseX: canvas.width / 100, // Vitesse de déplacement horizontal de la balle
		speedBaseY: canvas.height / 100 * 0, // Vitesse de déplacement vertical de la balle
		Bcolor: 'blue'
	}
}

let IA = {
	destYRT: canvas.height / 2,
	destYL: canvas.height / 2,
	activate: false
}

let paddle = {
	leftHeight: canvas.width / 10,
	leftWidth: canvas.height / 50,
	rightHeight: canvas.width / 10,
	rightWidth: canvas.height / 50,
	leftY: (canvas.height - canvas.width / 10) / 2, // start in the middle of the canvas
	rightY: (canvas.height - canvas.width / 10) / 2, // start in the middle of the canvas
	speed: canvas.height / 80,	// Vitesse de déplacement des raquettes
	centreR: 0,
	centreL: 0,
	marge: 10,
	angle: 5
}

let inputs = {
	upLeft: false,
	downLeft: false,
	upRight: false,
	downRight: false
}

let UI = {
	leftScore: 0,
	rightScore: 0,
	leftName: host_name,
	rightName: name_player2,
	drawTrajectory: false
}

function initializeUI(player1, player2) {
	UI.leftName = player1;
	UI.rightName = player2;
	UI.leftScore = 0;
	UI.rightScore = 0;
	UI.drawTrajectory = false;
}

function createManager(mode = 0) {
	return {
		mode: mode,
		pause: false,
		putBackBallBool: false,
		countdownInt: 3,
		countdownBool: false,
		partyDuration: Date.now(),
		inputs: false,
		waiting: true,
	};
}

let manager = createManager();

function initializeManager(modeI) {
	manager = createManager(modeI);
}

let directionXtmp = ball.speedX;
let directionYtmp = ball.speedY

//#endregion

//#region Exported functions

run();

export function startGameFunctionPVP() {
	manager.inputs = true;
	manager.waiting = false;
	UI.rightName = name_player2;
	initializeBall(0);

}
window.startGameFunctionPVP = startGameFunctionPVP;

//#endregion

//#region Input
function keyDownHandler(e) {
	if (!manager.pause) {
		if (e.key == "z" || e.key == "Z") {
			inputs.upLeft = true;
		}
		else if (e.key == "s" || e.key == "S") {
			inputs.downLeft = true;
		}
		else if (e.key == "ArrowUp") {
			if (!IA.activate)
				inputs.upRight = true;
		}
		else if (e.key == "ArrowDown") {
			if (!IA.activate)
				inputs.downRight = true;
		}
	}
	if (e.key == " ") {
		pauseGame();
	}
}

function keyUpHandler(e) {
	if (e.key == "z" || e.key == "Z") {
		inputs.upLeft = false;
	}
	else if (e.key == "s" || e.key == "S") {
		inputs.downLeft = false;
	}
	else if (e.key == "ArrowUp") {
		if (!IA.activate)
			inputs.upRight = false;
	}
	else if (e.key == "ArrowDown") {
		if (!IA.activate)
			inputs.downRight = false;
	}
}

function lisenInput() {
	if (manager.pause || !manager.inputs)
		return;
	if (inputs.upLeft) {
		paddle.leftY -= paddle.speed;
		if (paddle.leftY < 0) {
			paddle.leftY = 0;
		}
	}
	else if (inputs.downLeft) {
		paddle.leftY += paddle.speed;
		if (paddle.leftY + paddle.leftHeight > canvas.height) {
			paddle.leftY = canvas.height - paddle.leftHeight;
		}
	}
	if (inputs.upRight) {
		paddle.rightY -= paddle.speed;
		if (paddle.rightY < 0) {
			paddle.rightY = 0;
		}
	}
	else if (inputs.downRight) {
		paddle.rightY += paddle.speed;
		if (paddle.rightY + paddle.rightHeight > canvas.height) {
			paddle.rightY = canvas.height - paddle.rightHeight;
		}
	}
}
//#endregion

//#region IA
function IATrajectory(ox, oy, speedX, speedY, stop) {

	if (stop++ == 4)
		return;
	if (manager.putBackBallBool || manager.pause || ball.speedX == 0)
		return;
	var dx = ox;
	var dy = oy;

	if (speedX > 0) {
		while (dx < canvas.width - ball.Bradius) {
			dy += speedY;
			dx += speedX;
			if (dy < ball.Bradius || dy > canvas.height - ball.Bradius) break;
		}
	} else {
		while (dx > ball.Bradius) {
			dy += speedY;
			dx += speedX;
			if (dy < ball.Bradius || dy > canvas.height - ball.Bradius) break;
		}
	}

	dx = Math.max(ball.Bradius, Math.min(dx, canvas.width - ball.Bradius));
	dy = Math.max(ball.Bradius, Math.min(dy, canvas.height - ball.Bradius));

	if (dx != ball.Bradius && dx != canvas.width - ball.Bradius)
		IATrajectory(dx, dy, speedX, -speedY, stop);
	else if (ball.speedX > 0)
		IA.destYRT = dy;
	if (UI.drawTrajectory)
		drawLine(ox, oy, dx, dy);
}

function startUpdatingAI() {
	if (IA.activate) {
		updateInterval = setInterval(IAUpdate, 1000);
	}
}

function stopUpdatingAI() {
	clearInterval(updateInterval);
	lastTime = Date.now();
}

function IAUpdate() {
	IA.destYL = IA.destYRT + Math.random() * paddle.leftHeight - paddle.leftHeight / 2;
	// console.log(Date.now() - lastTime); // Affiche le temps écoulé depuis le dernier appel
	lastTime = Date.now();
}

function IAMove() {
	paddle.centreR = paddle.rightY + paddle.rightHeight / 2;
	paddle.centreL = paddle.leftY + paddle.leftHeight / 2;
	if (manager.pause || manager.putBackBallBool)
		return;
	var centrePaddle = paddle.rightY + paddle.rightHeight / 2;	/// centre de la raquette
	var ecart = IA.destYL - centrePaddle;
	var aiPaddleSpeed = paddle.speed * 1;  // AI moves twice as fast

	if (ecart > 0) {
		paddle.rightY += aiPaddleSpeed;
		if (paddle.rightY + paddle.rightHeight > canvas.height) {
			paddle.rightY = canvas.height - paddle.rightHeight;
		}
	} else if (ecart < 0) {
		var moveAmount = Math.min(-ecart, aiPaddleSpeed);
		paddle.rightY -= moveAmount;
		if (paddle.rightY < 0) {
			paddle.rightY = 0;
		}
	}
}

function IAManager() {
	if (manager.putBackBallBool || manager.pause)
		stopUpdatingAI();
	else if (IA.activate)
		IAMove();
}
//#endregion

//#region draw
function changeColor() {

	var red = Math.floor(Math.random() * 256);
	var green = Math.floor(Math.random() * 256);
	var blue = Math.floor(Math.random() * 256);
	ball.Bcolor = "rgb(" + red + "," + green + "," + blue + ")";
}

function drawPaddle()// Fonctioner qui dessine les raquettes
{
	ctx.beginPath();
	ctx.rect(5, paddle.leftY, paddle.leftWidth, paddle.leftHeight);
	ctx.rect(canvas.width - paddle.rightWidth - 5, paddle.rightY, paddle.rightWidth, paddle.rightHeight);
	var grd = ctx.createLinearGradient(0, 0, 0, canvas.height);
	grd.addColorStop(0, "blue");
	grd.addColorStop(1, "red");

	ctx.fillStyle = grd;
	ctx.fill();
	ctx.closePath();
}

function drawLine(ax, ay, bx, by) {
	ctx.beginPath();
	ctx.moveTo(ax, ay);
	ctx.lineTo(bx, by);
	ctx.strokeStyle = 'black'; // Couleur de la ligne
	ctx.lineWidth = canvas.height / 150; // Épaisseur de la ligne
	ctx.stroke(); // Dessinez la ligne
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
	ctx.lineWidth = canvas.height / 150; // Épaisseur de la ligne
	ctx.stroke(); // Dessinez la ligne

	// Terminez le chemin
	ctx.closePath();
}

function drawBall() {
	// Dessinez la balle à sa nouvelle position
	ctx.beginPath();
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
		if (!manager.putBackBallBool)
			changeColor();


		ball.speedX = -ball.speedX; // Inverser la direction horizontale
	}
	if (ball.y + ball.Bradius > canvas.height || ball.y - ball.Bradius < 0) {
		if (!manager.putBackBallBool)
			changeColor();
		ball.speedY = -ball.speedY; // Inverser la direction verticale
	}
	ctx.fill();
	ctx.closePath();
}

function drawScore() {
	ctx.font = "2vw Arial";
	ctx.fillStyle = 'white';
	let textWidth = ctx.measureText("Score: " + UI.leftScore).width;
	ctx.fillText("Score: " + UI.leftScore, canvas.width * 0.025, canvas.height * 0.06);
	textWidth = ctx.measureText("Score: " + UI.rightScore).width;
	ctx.fillText("Score: " + UI.rightScore, canvas.width - textWidth - canvas.width * 0.025, canvas.height * 0.06);
	ctx.fillText(UI.leftName, canvas.width * 0.025, canvas.height * 0.12);
	ctx.fillText(UI.rightName, canvas.width - textWidth - canvas.width * 0.025, canvas.height * 0.12);
}

function collisionDetection() {
	if (manager.putBackBallBool)
		return;
	if (ball.x + ball.Bradius > canvas.width - posBord) // Si la balle touche le bord droit du canvas
	{
		if (ball.y - paddle.rightY < - paddle.marge || (ball.y - ball.Bradius) - (paddle.rightY + paddle.rightHeight) > paddle.marge) {
			UI.leftScore++;
			putBackBall(-1);
		}
		else {
			var centrePaddle = paddle.rightY + paddle.rightHeight / 2;	/// centre de la raquette
			if (ball.y < centrePaddle)
				ball.speedY = -1 * (centrePaddle - ball.y) / paddle.angle;
			else
				ball.speedY = (ball.y - centrePaddle) / paddle.angle;
		}
	}
	else {
		if ((ball.y + ball.Bradius) - paddle.leftY < - paddle.marge || (ball.y - ball.Bradius) - (paddle.leftY + paddle.leftHeight) > paddle.marge) {
			UI.rightScore++;
			putBackBall(1);
		}
		else {
			var centrePaddle = paddle.leftY + paddle.leftHeight / 2;	/// centre de la raquette
			if (ball.y < centrePaddle)
				ball.speedY = -1 * (centrePaddle - ball.y) / paddle.angle;
			else
				ball.speedY = (ball.y - centrePaddle) / paddle.angle;
		}
	}
}

//#endregion

//#region manage the game

function Update() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	if (!manager.waiting)
	{
		lisenInput();
		drawScore();
		drawCountdown();
	}
	drawPaddle();
	drawVerticalBar();
	IATrajectory(ball.x, ball.y, ball.speedX, ball.speedY, 0)
	drawBall();
	IAManager();
}

function canvasCheck() {
	let canvas = document.getElementById('pongCanvas');
	if (canvas)
		return;
}

function startGame() {

	setInterval(Update, 10);
	IATrajectory(ball.x, ball.y, ball.speedX, ball.speedY, 0);
	IAUpdate();
	startUpdatingAI();
	initializeBall(ball.speedBaseX);
}

async function putBackBall(directionX) {
	manager.putBackBallBool = true;
	// Stop the ball for 1 second
	ball.speedX = 0;
	ball.speedY = 0;
	for (let i = 0; i < 50; i++) {
		ball.Bradius += 0.5; // Increase the size of the ball
		if (i % 10 == 0)
			changeColor();
		await delay(10); // Wait for 0.1 seconds
	}
	await delay(500); // Wait for 1 second

	manager.putBackBallBool = false;
	// Place the ball at the center of the canvas for 1 second
	ball.x = canvas.width / 2;
	ball.y = canvas.height / 2;
	ball.Bradius = canvas.height / 50;
	await delay(200); // Wait for 1 second

	// Send the ball
	while (manager.pause)
		await delay(10);
	ball.speedX = ball.speedBaseX * directionX;
	ball.speedY = (Math.random() * 2 - 1) * ball.speedBaseY;
	IATrajectory(ball.x, ball.y, ball.speedX, ball.speedY, 0);
	IA.destYL = IA.destYRT + Math.random() * paddle.leftHeight - paddle.leftHeight / 2;
	startUpdatingAI();

	sendScoreToBackend(score);
}

function delay(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

function pauseGame() {
	if (manager.pause) {
		ball.speedX = directionXtmp;
		ball.speedY = directionYtmp;

		manager.pause = false;
		startUpdatingAI();
	}
	else {
		directionXtmp = ball.speedX;
		directionYtmp = ball.speedY;
		ball.speedX = 0;
		ball.speedY = 0;
		manager.pause = true;
	}
}

async function countdown() {
	if (manager.countdownBool)
		return;
	manager.countdownBool = true;
	await delay(1000);
	manager.countdownBool = false;
	manager.countdownInt--;
	if (manager.countdownInt == 0)
	{
		ball.speedX = ball.speedBaseX;
	}
}

function drawCountdown() {
	if (manager.countdownInt <= 0) {
		return;
	}
	countdown();
	ctx.font = "10vw Arial";
	ctx.fillStyle = 'white';
	ctx.fillText(manager.countdownInt, ctx.canvas.width / 2, ctx.canvas.height / 2); // Dessine le compteur
}

function initializeVariables(mode) {
	clearInterval(Update);

	if (!canvas)
		window.addEventListener('load', canvasCheck);

	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;
	posBord = 10;

	manager.pause = false;
	manager.putBackBallBool = false;
	manager.countdownInt = 3;

	UI.drawTrajectory = false;

	initializeBall(ball.speedBaseX);
	IA.destYRT = canvas.height / 2;
	IA.destYL = canvas.height / 2;
	if (mode == 2)
		IA.activate = true;
	else
		IA.activate = false;

	paddle = {
		leftHeight: canvas.width / 10,
		leftWidth: canvas.height / 50,
		rightHeight: canvas.width / 10,
		rightWidth: canvas.height / 50,
		leftY: (canvas.height - canvas.width / 10) / 2, // start in the middle of the canvas
		rightY: (canvas.height - canvas.width / 10) / 2, // start in the middle of the canvas
		speed: canvas.height / 80,	// Vitesse de déplacement des raquettes
		centreR: 0,
		centreL: 0,
		marge: 10,
		angle: 5
	}

	inputs = {
		upLeft: false,
		downLeft: false,
		upRight: false,
		downRight: false
	}

	UI = {
		leftScore: 0,
		rightScore: 0,
		leftName: host_name,
		rightName: name_player2
	}
	if (mode == 2)
		UI.rightName = "IA";

	startGame();
}

function run() {
	// const urlParams = new URLSearchParams(window.location.search);
	// const mode = urlParams.get('mode');

	let url = new URL(window.location.href);
	let mode = url.pathname.split("/")[3]; // Assuming 'mode' is the fourth segment in the URL

	if (mode == "pvp")
		initializeVariables(1);
	else if (mode == "pve")
		initializeVariables(2);
	else if (mode == "tournament")
		initializeVariables(3);
	else
		console.log("Error: mode not found `" + mode + "`");
}

//#endregion

//#region request backend

let limit = 3;

function sendScoreToBackend(score) {
	if (limit-- <= 0)
		return;
	let formData = new FormData();
	formData.append('game_duration', (new Date() - score.startDate) / 1000);
	formData.append('host_username', host_name);
	formData.append('player1', host_name);
	formData.append('player2', name_player2);
	formData.append('player1_score', UI.leftScore);
	formData.append('player2_score', UI.rightScore);

	let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;

	const request = new Request(save_game, {
		method: 'POST',
		body: formData,
		headers: { 'X-CSRFToken': csrfTokenValue }
	});

	fetch(request)
		.then(response => response.json())
		.then(result => {
			console.log(result); // Vous pouvez traiter le résultat ici
		})
		.catch(error => {
			console.error(`Fetch error: ${error.message}`);
		});
}
//#endregion
