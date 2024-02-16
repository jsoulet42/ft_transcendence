import * as THREE from 'three';

window.canvas = document.getElementById('pongCanvas3D');

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight);


const light = new THREE.DirectionalLight('white', 1, 0, 0);
light.position.set(5, 10, 0);

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
	constructor(x, y, z, radius, color, scene) {
		this.geometry = new THREE.SphereGeometry(radius, 32, 32);
		this.material = new THREE.MeshBasicMaterial({ color: color });
		this.mesh = new THREE.Mesh(this.geometry, this.material);
		this.mesh.position.set(x, y, z);
		this.directionx = 1;
		this.directiony = 0;
		scene.add(this.mesh);
	}
	paddleLeft = null;
	paddleRight = null;
	setPaddles(paddleLeft, paddleRight) {
		this.paddleLeft = paddleLeft;
		this.paddleRight = paddleRight;
	}
	move() {
		this.mesh.position.x += 0.1 * this.directionx;
		this.mesh.position.y += 0.1 * this.directiony;
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
	const ballPosition = new THREE.Vector3(
		this.mesh.position.x,
		this.mesh.position.y,
		this.mesh.position.z
	);

	const planeBox = new THREE.Box3().setFromObject(pongTable.mesh);

	// Check for collisions with the top and bottom of the table
	if (this.directiony == 1) {
		ballPosition.y += this.mesh.geometry.parameters.radius;
	} else {
		ballPosition.y -= this.mesh.geometry.parameters.radius;
	}

	if (!planeBox.intersectsSphere(new THREE.Sphere(ballPosition, this.mesh.geometry.parameters.radius))) {
		this.directiony *= -1;
	}
}

checkTableLeftRightCollision() {
	const ballPosition = new THREE.Vector3(
		this.mesh.position.x,
		this.mesh.position.y,
		this.mesh.position.z
	);

	const planeBox = new THREE.Box3().setFromObject(pongTable.mesh);

	// Check for collisions with the left and right sides of the table
	if (this.directionx == 1) {
		ballPosition.x += this.mesh.geometry.parameters.radius;
	} else {
		ballPosition.x -= this.mesh.geometry.parameters.radius;
	}

	if (!planeBox.intersectsSphere(new THREE.Sphere(ballPosition, this.mesh.geometry.parameters.radius))) {
		this.directionx *= -1;
	}
}
}


const pongTable = new tablePongClass(0, -0.5, 0, 17, 10, 0.5, 0xffff00, scene);
const manager = new managerPong();
const paddleLeft = new PaddleClasse(-8, 0, 0, 0.5, 3, 0.5, 0xff0000, scene, 0.1, pongTable); // Red paddle on the left
const paddleRight = new PaddleClasse(8, 0, 0, 0.5, 3, 0.5, 0x0000ff, scene, 0.1, pongTable); // Blue paddle on the right
const ball = new ballClasse(0, 0, 0, 0.5, 0x00ff00, scene); // Green ball in the middle


//#region scene.add

scene.add(light);

//#endregion

camera.position.set(0, 0, 10);
camera.lookAt(0, -0, 0);

const renderer = new THREE.WebGLRenderer({ canvas: window.canvas });

renderer.setSize(window.window.innerWidth / 2, window.innerHeight / 2);
//renderer.setSize(canvas.width, canvas.height);
renderer.setClearColor('black', 1);

function loop() {
	requestAnimationFrame(loop);
	if (!manager.pause) {
		ball.move();
		ball.checkPaddleCollision();
		ball.checkTableTopBottomCollision();
		ball.checkTableLeftRightCollision();
	}
	listenInput();
	renderer.render(scene, camera);
}

function Start() {
	ball.setPaddles(paddleLeft, paddleRight);
	loop();
}

Start();

