{/* <canvas id="pongCanvas3D"></canvas>
<script type="module" src="{% static 'pong/js/pong3D.js' %}" defer></script> */}


import * as THREE from 'three';

window.canvas = document.getElementById('pongCanvas3D');

const renderer = new THREE.WebGLRenderer({ canvas: canvas });
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight);


const light = new THREE.SpotLight('white', 1, 0, 0);
camera.position.set(0, 0, 10);
camera.lookAt(0, 0, 0);

light.position.set(0, 10, -10);
light.rotation.set(0, 10, 0);
renderer.setSize(window.window.innerWidth / 2, window.innerHeight / 2);
//renderer.setSize(canvas.width, canvas.height);
renderer.setClearColor('black', 1);

scene.add(light);


//#region Resize

function resizeRendererToDisplaySize(renderer) {
	const canvas = renderer.domElement;
	const width = canvas.clientWidth;
	const height = canvas.clientHeight;
	// const width = window.innerWidth / 2;
	// const height = window.innerHeight / 2;
	const needResize = canvas.width !== width || canvas.height !== height;
	if (needResize) {
		renderer.setSize(width, height, false);
	}
	return needResize;
}

// #pongCanvas3D {
// 	position: absolute;
// 	top: 50%;
// 	left: 50%;
// 	background-color: white;
// 	transform: translate(-50%, -50%);
// 	border-radius: 5vmin;
// }

// /* Apply these styles when the window is at least 768px wide */
// @media (min-width: 768px) {
// 	#pongCanvas3D {
// 		width: 75%;
// 		height: 75%;
// 		transform: translate(-50%, -50%);
// 	}
// }

// /* Apply these styles when the window is less than 768px wide */
// @media (max-width: 767px) {
// 	#pongCanvas3D {
// 		width: 100%;
// 		height: 100%;
// 		transform: translate(-50%, -50%);
// 	}
// }


//#endregion

function rotationLight() {
	light.rotation.x += 0.01;
	light.rotation.y += 0.01;
	light.rotation.z += 0.01;
}

//#region Input

document.addEventListener("keydown", keyDownHandler, false); // écouteur d'événement
document.addEventListener("keyup", keyUpHandler, false); // écouteur d'événement

let inputs = {
	upLeft: false,
	downLeft: false,
	upRight: false,
	downRight: false
};

function keyDownHandler(e)// Fonction de gestion des événements
{
	if (!manager.pauseBool) {
		if (e.key == "z" || e.key == "Z") {
			inputs.upLeft = true;
		}
		else if (e.key == "s" || e.key == "S") {
			inputs.downLeft = true;
		}
		else if (e.key == "ArrowUp") {
			if (!manager.IA.activate)
				inputs.upRight = true;
		}
		else if (e.key == "ArrowDown") {
			if (!manager.IA.activate)
				inputs.downRight = true;
		}
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
		if (!manager.IA.activate)
			inputs.upRight = false;
	}
	else if (e.key == "ArrowDown") {
		if (!manager.IA.activate)
			inputs.downRight = false;
	}
}

function listenInput() {
	if (inputs.upLeft) {
		paddleLeft.move('up');
	}
	else if (inputs.downLeft) {
		paddleLeft.move('down');
	}
	if (inputs.upRight) {
		paddleRight.move('up');
	}
	else if (inputs.downRight) {
		paddleRight.move('down');
	}
}

//#endregion

class managerPong {
	pauseBool = false;

	IA = {
		activate: false,
	};
	pause() {
		this.pauseBool = !this.pauseBool;
	}
}

class tablePongClass {
	constructor(x, y, z, width, height, depth, color, scene) {
		this.geometry = new THREE.BoxGeometry(width, height, depth);

		// Create a gradient texture
		const tableCanvas = document.createElement('canvas');
		tableCanvas.width = 256;
		tableCanvas.height = 256;
		const context = tableCanvas.getContext('2d');

		const gradient = context.createLinearGradient(0, 0, tableCanvas.width, tableCanvas.height);
		gradient.addColorStop(0, 'red'); // Start color
		gradient.addColorStop(1, 'blue'); // End color

		context.fillStyle = gradient;
		context.fillRect(0, 0, tableCanvas.width, tableCanvas.height);

		const texture = new THREE.CanvasTexture(tableCanvas);

		this.material = new THREE.MeshBasicMaterial({ map: texture });

		this.mesh = new THREE.Mesh(this.geometry, this.material);
		this.mesh.position.set(x, y, z);

		scene.add(this.mesh);
	}
	getCornerCoordinates(vertex) {
		const halfWidth = this.geometry.parameters.width / 2;
		const halfDepth = this.geometry.parameters.depth / 2;
		const height = this.geometry.parameters.height;

		if (vertex === 'topLeft') {
			return new THREE.Vector3(this.mesh.position.x - halfWidth, this.mesh.position.y + height, this.mesh.position.z - halfDepth);
		}
		else if (vertex === 'topRight') {
			return new THREE.Vector3(this.mesh.position.x + halfWidth, this.mesh.position.y + height, this.mesh.position.z - halfDepth);
		}
		else if (vertex === 'bottomLeft') {
			return new THREE.Vector3(this.mesh.position.x - halfWidth, this.mesh.position.y, this.mesh.position.z + halfDepth);
		}
		else if (vertex === 'bottomRight') {
			return new THREE.Vector3(this.mesh.position.x + halfWidth, this.mesh.position.y, this.mesh.position.z + halfDepth);
		}
	}
}

class PaddleClasse {
	constructor(x, y, z, width, height, depth, color, scene, speed, tablePong) {
		const loader = new THREE.TextureLoader();
		loader.load('/static/pong/textures/brick_wall_02_4k.blend/textures/brick_wall_02_diff_4k.jpg', (texture) => {
			texture.wrapS = THREE.RepeatWrapping;
			texture.wrapT = THREE.RepeatWrapping;
			texture.repeat.set(width / height, 1); // Repeat the texture based on the width/height ratio of the paddle

			this.geometry = new THREE.BoxGeometry(width, height, depth);
			this.material = new THREE.MeshBasicMaterial({ map: texture });
			this.mesh = new THREE.Mesh(this.geometry, this.material);
			const tableWidth = tablePong.geometry.parameters.width;
			if (x == "left")
				this.mesh.position.set(-tableWidth / 2 + width, y, z);
			else if (x == "right")
				this.mesh.position.set(tableWidth / 2 - width, y, z);

			scene.add(this.mesh);
		});
		this.speed = speed;
		this.table = tablePong; // Set the table reference
	}

	move(direction) {
		if (!this.table) {
			throw new Error('Table not set for paddle');
		}
		if (direction === 'up') {
			if (this.mesh.position.y + this.geometry.parameters.height / 2 < this.table.mesh.position.y + this.table.geometry.parameters.height / 2) {
				this.mesh.position.y += this.speed;
			}
		}
		else if (direction === 'down') {
			if (this.mesh.position.y - this.geometry.parameters.height / 2 > this.table.mesh.position.y - this.table.geometry.parameters.height / 2) {
				this.mesh.position.y -= this.speed;
			}
		}
	}
}

class ballClasse {
	constructor(x, y, z, speed, radius, color, scene) {
		this.geometry = new THREE.SphereGeometry(radius, 32, 32);
		this.material = new THREE.MeshBasicMaterial({ color: color });
		this.mesh = new THREE.Mesh(this.geometry, this.material);
		this.mesh.position.set(x, y, z);
		this.directionx = 1;
		this.directiony = 0;
		this.speed = speed;
		scene.add(this.mesh);
	}
	paddleLeft = null;
	paddleRight = null;
	setPaddles(paddleLeft, paddleRight) {
		this.paddleLeft = paddleLeft;
		this.paddleRight = paddleRight;
	}
	move() {
		this.mesh.position.x += this.speed * this.directionx;
		this.mesh.position.y += this.speed * this.directiony;
	}
	checkPaddleCollision() {
		if (!this.paddleLeft || !this.paddleRight) {
			throw new Error('Paddles not set for ball');
		}
		const ballPosition = new THREE.Vector3(
			this.mesh.position.x,
			this.mesh.position.y,
			this.mesh.position.z
		);
		if (!this.paddleLeft.mesh || !this.paddleRight.mesh) {
			return;
		}
		const paddleLeftBox = new THREE.Box3().setFromObject(this.paddleLeft.mesh);
		const paddleRightBox = new THREE.Box3().setFromObject(this.paddleRight.mesh);
		const paddleHeight = this.paddleLeft.mesh.geometry.parameters.height;
		const speedFactor = 2;
		if (paddleLeftBox.intersectsSphere(new THREE.Sphere(ballPosition, this.mesh.geometry.parameters.radius))) {
			this.directionx = 1;
			let distanceFromCenter = ballPosition.y - this.paddleLeft.mesh.position.y;
			this.directiony = distanceFromCenter / paddleHeight * speedFactor;
		}

		if (paddleRightBox.intersectsSphere(new THREE.Sphere(ballPosition, this.mesh.geometry.parameters.radius))) {
			this.directionx = -1;
			let distanceFromCenter = ballPosition.y - this.paddleRight.mesh.position.y;
			this.directiony = distanceFromCenter / paddleHeight * speedFactor;
		}

	}

	checkTableTopBottomCollision() {
		const ballTop = this.mesh.position.y + this.mesh.geometry.parameters.radius;
		const ballBottom = this.mesh.position.y - this.mesh.geometry.parameters.radius;
		const tableTop = pongTable.mesh.position.y + pongTable.geometry.parameters.height / 2;
		const tableBottom = pongTable.mesh.position.y - pongTable.geometry.parameters.height / 2;

		// Check if the ball is going to leave the table
		if (ballTop > tableTop || ballBottom < tableBottom) {
			// If the ball is going to leave the table, reverse its direction immediately
			this.directiony *= -1;
		} else {
			// If the ball is not going to leave the table, check for collisions with the table
			const planeBox = new THREE.Box3().setFromObject(pongTable.mesh);
			if (!planeBox.intersectsSphere(new THREE.Sphere(this.mesh.position, this.mesh.geometry.parameters.radius))) {
				this.directiony *= -1;
			}
		}
	}
	checkTableLeftRightCollision() {
		const ballLeft = this.mesh.position.x - this.mesh.geometry.parameters.radius;
		const ballRight = this.mesh.position.x + this.mesh.geometry.parameters.radius;
		const tableLeft = pongTable.mesh.position.x - pongTable.geometry.parameters.width / 2;
		const tableRight = pongTable.mesh.position.x + pongTable.geometry.parameters.width / 2;

		if (ballRight > tableRight || ballLeft < tableLeft) {
			resetBallAfterGoal();
			console.log("Goal");
		}
	}
}


const pongTable = new tablePongClass(0, 0, 0, 26, 13.7, 0.5, 0xffff00, scene);
const manager = new managerPong();
const paddleLeft = new PaddleClasse("left", 0, 0, 0.5, 3, 1, 0xff0000, scene, 0.1, pongTable); // Red paddle on the left
const paddleRight = new PaddleClasse("right", 0, 0, 0.5, 3, 1, 0x0000ff, scene, 0.1, pongTable); // Blue paddle on the right
const ball = new ballClasse(0, 0, 0, 0.5, 0.5, "black", scene); // Green ball in the middle

async function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

async function resetBallAfterGoal() {
	ball.mesh.position.set(0, 0, 0);
	const speedtemp = ball.speed;
	ball.speed = 0;
	if (ball.directionx == 1) {
		score.scoreLeft++;
	}
	else {
		score.scoreRight++;
	}
	displayScore1();
	displayScore2();

	await sleep(1000);
	ball.directionx *= -1;
	ball.directiony = 0;
	ball.speed = speedtemp;
	sendScoreToBackend(score);
}


//#region request back-end



function sendScoreToBackend(score) {
	let formData = new FormData();
	formData.append('playerRight', score.playerRight);
	formData.append('playerLeft', score.playerLeft);
	formData.append('scoreRight', score.scoreRight);
	formData.append('scoreLeft', score.scoreLeft);
	formData.append('startDate', score.startDate);    
	formData.append('startTime', score.startTime);
	formData.append('timeNow', score.timeNow);

	let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;

	const request = new Request(pongDjangoUrl, {
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

function loop() {
	requestAnimationFrame(loop);
	renderer.render(scene, camera);

	if (!manager.pauseBool) {
		ball.move();
		ball.checkPaddleCollision();
		ball.checkTableTopBottomCollision();
		ball.checkTableLeftRightCollision();
		displayTimeNow();
	}
	// if(resizeRendererToDisplaySize(renderer)){
	// 	const canvas = renderer.domElement;
	// 	camera.aspect = canvas.clientWidth / canvas.clientHeight;
	// 	camera.updateProjectionMatrix();
	// }

	rotationLight();
	listenInput();
}

let score = {

	playerLeft: "Player 1",
	playerRight: "Player 2",
	scoreRight: 0,
	scoreLeft: 0,
	startDate: null,
	startTime: null,
	timeNow: null
}

function Start() {
	score.startTime = Date.now();
	score.startDate = new Date();
	console.log("La partie à commencé à : " + score.startDate.toLocaleString());
	displayScore1();
	displayScore2();
	displayCountdown();

	ball.setPaddles(paddleLeft, paddleRight);
	loop();
}

function updatePartyDuration() {
	if (score.startTime !== null) {
		// Calculez la durée de la partie en secondes et dixièmes de secondes
		const durationInMilliseconds = Date.now() - score.startTime;
		const durationInSeconds = durationInMilliseconds / 1000;
		score.timeNow = durationInSeconds.toFixed(1); // Arrondi à un chiffre après la virgule
	}
}

//#region UI

let countdownValue = 4; // Start countdown at 10 seconds
const countdownElement = document.createElement('div');
const scoreElement = document.createElement('div');
const scoreElement2 = document.createElement('div');
const rect = canvas.getBoundingClientRect();
const timeElement = document.createElement('div');

document.body.appendChild(countdownElement);

function displayCountdown() {
	ball.directionx = 0;
	ball.directiony = 0;
	countdownValue--;
	countdownElement.style.position = 'absolute';
	countdownElement.style.top = '50%';
	countdownElement.style.left = '50%';
	countdownElement.style.transform = 'translate(-50%, -50%)';
	countdownElement.style.fontSize = '20vh';
	countdownElement.style.color = 'white';
	countdownElement.style.zIndex = '2';

	if (countdownValue < 0) {
		countdownValue = 0;
	}
	countdownElement.textContent = Math.ceil(countdownValue).toString();

	if (countdownValue > 0) {
		setTimeout(displayCountdown, 1000);
	}
	else {
		countdownElement.textContent = "";
		ball.directionx = 1;
		ball.directiony = 0;
	}
}
function displayScore1() {

	scoreElement.innerHTML = `
	<p>${score.playerRight}: ${score.scoreRight}</p>`;

	scoreElement.style.position = 'absolute';
	scoreElement.style.top = `${rect.top + rect.height * 0.02}px`;
	scoreElement.style.left = `${rect.left + rect.width * 0.8}px`;
	scoreElement.style.fontSize = '3em';
	scoreElement.style.color = 'white';
	scoreElement.style.zIndex = '2';

	document.body.appendChild(scoreElement);
}
function displayScore2() {

	scoreElement2.innerHTML = `
	<p>${score.playerLeft}: ${score.scoreLeft}</p>`;

	scoreElement2.style.position = 'absolute';
	scoreElement2.style.top = `${rect.top + rect.height * 0.02}px`;
	scoreElement2.style.left = `${rect.left + rect.width * 0.02}px`;
	scoreElement2.style.fontSize = '3em';
	scoreElement2.style.color = 'white';
	scoreElement2.style.zIndex = '2';

	document.body.appendChild(scoreElement2);
}
function displayTimeNow() {
	updatePartyDuration();
	timeElement.innerHTML = `
		<p>Party Duration: ${score.timeNow}</p>
	`;
	timeElement.style.position = 'absolute';
	timeElement.style.top = `${rect.top + rect.height * 0.02}px`;
	timeElement.style.left = `${rect.left + rect.width * 0.4}px`;
	timeElement.style.fontSize = '2em';
	timeElement.style.color = 'white';
	timeElement.style.zIndex = '2';

	document.body.appendChild(timeElement);
}

//#endregion
Start();
