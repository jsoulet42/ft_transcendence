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
		paddleLeft.mesh.position.y += paddleLeft.speed;
		if (paddleLeft.mesh.position.y > sceneHeight / 2) {
			paddleLeft.mesh.position.y = sceneHeight / 2;
		}
	}
	else if (inputs.downLeft) {
		paddleLeft.mesh.position.y -= paddleLeft.speed;
		if (paddleLeft.mesh.position.y < -sceneHeight / 2) {
			paddleLeft.mesh.position.y = -sceneHeight / 2;
		}
	}
	if (inputs.upRight) {
		paddleRight.mesh.position.y += paddleRight.speed;
		if (paddleRight.mesh.position.y > sceneHeight / 2) {
			paddleRight.mesh.position.y = sceneHeight / 2;
		}
	}
	else if (inputs.downRight) {
		paddleRight.mesh.position.y -= paddleRight.speed;
		if (paddleRight.mesh.position.y < -sceneHeight / 2) {
			paddleRight.mesh.position.y = -sceneHeight / 2;
		}
	}
}



//#endregion


class managerPong
{
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
		this.mesh.rotation.x = Math.PI / 2;
		scene.add(this.mesh);
	}
}



class PaddleClasse {
	constructor(x, y, z, width, height, depth, color, scene, speed) {
		const loader = new THREE.TextureLoader();
		loader.load('/static/pong/textures/brick_wall_02_4k.blend/textures/brick_wall_02_diff_4k.jpg', (texture) => {
			texture.wrapS = THREE.RepeatWrapping;
			texture.wrapT = THREE.RepeatWrapping;
			texture.repeat.set(width / height, 1); // Repeat the texture based on the width/height ratio of the paddle

			this.geometry = new THREE.BoxGeometry(width, height, depth);
			this.material = new THREE.MeshBasicMaterial({ map: texture });
			this.mesh = new THREE.Mesh(this.geometry, this.material);
			this.mesh.position.set(x, y, z);
			// Add the mesh to the scene in the texture loader callback
			scene.add(this.mesh);
		});
	}
}

class ballClasse {
	constructor(x, y, z, radius, color, scene) {
		this.geometry = new THREE.SphereGeometry(radius, 32, 32);
		this.material = new THREE.MeshBasicMaterial({ color: color });
		this.mesh = new THREE.Mesh(this.geometry, this.material);
		this.mesh.position.set(x, y, z);
		this.direction = 1;
		scene.add(this.mesh);
	}
}


const manager = new managerPong();
const paddleLeft = new PaddleClasse(-8, 0, 0, 1, 1, 4, 0xff0000, scene, 1); // Red paddle on the left
const paddleRight = new PaddleClasse(8, 0, 0, 1, 1, 4, 0x0000ff, scene, 1); // Blue paddle on the right
const ball = new ballClasse(0, 0, 0, 0.5, 0x00ff00, scene); // Green ball in the middle
const pongTable = new tablePongClass(0, -0.5, 0, 15, 10, 0.5, 0xffff00, scene);
//#endregion


//#region scene.add

scene.add(light);

//#endregion

camera.position.set(0, 10, -1);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ canvas: window.canvas });

renderer.setSize(window.window.innerWidth / 2, window.innerHeight / 2);
//renderer.setSize(canvas.width, canvas.height);
renderer.setClearColor('black', 1);

function loop() {
	requestAnimationFrame(loop);
	moveBall();
	collisionDetection();
	listenInput();
	renderer.render(scene, camera);
}

function moveBall() {
	ball.mesh.position.x += 0.1 * ball.direction;

}

function collisionDetection() {

	const ballPosition = new THREE.Vector3(
		ball.mesh.position.x,
		ball.mesh.position.y,
		ball.mesh.position.z
	);

	const planeBox = new THREE.Box3().setFromObject(pongTable.mesh);
	if (ball.direction == 1) {
		ballPosition.x += ball.mesh.geometry.parameters.radius * 2;
	}
	else
		ballPosition.x -= ball.mesh.geometry.parameters.radius * 2;
	if (!planeBox.intersectsSphere(new THREE.Sphere(ballPosition, ball.mesh.geometry.parameters.radius))) {
		ball.direction *= -1;
		console.log('hit');
	}
}



loop();

