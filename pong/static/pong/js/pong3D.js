import * as THREE from 'three';

window.canvas = document.getElementById('pongCanvas3D');

const renderer = new THREE.WebGLRenderer({ canvas: window.canvas });
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight);


const light = new THREE.SpotLight('white', 1, 0, 0);
camera.position.set(0, 0, 10);
camera.lookAt(0, 0, 0);

light.position.set(0, 0, -10);
light.rotation.set(0, 0, 0);
renderer.setSize(window.window.innerWidth / 2, window.innerHeight / 2);
//renderer.setSize(canvas.width, canvas.height);
renderer.setClearColor('black', 1);

scene.add(light);


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
	if (!manager.pause) {
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
	pause = false;

	IA = {
		activate: false,
	};
}

class tablePongClass {
	constructor(x, y, z, width, height, depth, color, scene) {
		this.geometry = new THREE.BoxGeometry(width, height, depth);

		// Create a gradient texture
		const canvas = document.createElement('canvas');
		canvas.width = 128;
		canvas.height = 128;
		const context = canvas.getContext('2d');

		const gradient = context.createLinearGradient(0, 0, canvas.width, canvas.height);
		gradient.addColorStop(0, 'red'); // Start color
		gradient.addColorStop(1, 'blue'); // End color

		context.fillStyle = gradient;
		context.fillRect(0, 0, canvas.width, canvas.height);

		const texture = new THREE.CanvasTexture(canvas);

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
			this.mesh.position.set(x, y, z);

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
	// collisionDetection() {
	// 	const ballPosition = new THREE.Vector3(
	// 		this.mesh.position.x,
	// 		this.mesh.position.y,
	// 		this.mesh.position.z
	// 	);

	// 	const planeBox = new THREE.Box3().setFromObject(pongTable.mesh);
	// 	if (this.directionx == 1) {
	// 		ballPosition.x += this.mesh.geometry.parameters.radius * 2;
	// 	}
	// 	else
	// 		ballPosition.x -= this.mesh.geometry.parameters.radius * 2;
	// 	if (!planeBox.intersectsSphere(new THREE.Sphere(ballPosition, this.mesh.geometry.parameters.radius))) {
	// 		this.directionx *= -1;
	// 	}
	// }
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
		const speedFactor = 1;
		if (paddleLeftBox.intersectsSphere(new THREE.Sphere(ballPosition, this.mesh.geometry.parameters.radius))) {
			this.directionx *= -1;
			let distanceFromCenter = ballPosition.y - this.paddleLeft.mesh.position.y;
			this.directiony = distanceFromCenter / paddleHeight * speedFactor;
		}

		if (paddleRightBox.intersectsSphere(new THREE.Sphere(ballPosition, this.mesh.geometry.parameters.radius))) {
			this.directionx *= -1;
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

		// Check for collisions with the left and right sides of the table
		if (ballRight > tableRight || ballLeft < tableLeft) {
			// If the ball is going to leave the table, reverse its direction immediately
			this.directionx *= -1;
		} else {
			// If the ball is not going to leave the table, check for collisions with the table
			const planeBox = new THREE.Box3().setFromObject(pongTable.mesh);
			if (!planeBox.intersectsSphere(new THREE.Sphere(this.mesh.position, this.mesh.geometry.parameters.radius))) {
				this.directionx *= -1;
			}
		}
	}
}


const pongTable = new tablePongClass(0, -0.5, 0, 18, 10, 0.5, 0xffff00, scene);
const manager = new managerPong();
const paddleLeft = new PaddleClasse(-8, 0, 0, 1, 3, 1, 0xff0000, scene, 0.1, pongTable); // Red paddle on the left
const paddleRight = new PaddleClasse(8, 0, 0, 1, 3, 1, 0x0000ff, scene, 0.1, pongTable); // Blue paddle on the right
const ball = new ballClasse(0, 0, 0, 0.3, 0.5, "white", scene); // Green ball in the middle

function loop() {
	requestAnimationFrame(loop);
	if (!manager.pause) {
		ball.move();
		ball.checkPaddleCollision();
		ball.checkTableTopBottomCollision();
		ball.checkTableLeftRightCollision();
	}
	rotationLight();

	listenInput();
	renderer.render(scene, camera);
}

function Start() {
	ball.setPaddles(paddleLeft, paddleRight);
	loop();
}

Start();

