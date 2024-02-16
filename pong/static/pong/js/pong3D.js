import * as THREE from 'three';

window.canvas = document.getElementById('pongCanvas3D');

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight);

const BallMesh = new THREE.SphereGeometry(0.5, 32, 32);

const material = new THREE.MeshPhongMaterial({ color: 'red' });

const light = new THREE.DirectionalLight('white', 1, 0, 0);
light.position.set(5, 10, 0);





//#region material




//#endregion

//#region procedural plane

const geometry = computeGeometry();
let materialPlan = new THREE.PointsMaterial({ size: 0.015, vertexColors: true });

let planeProcedural = {
	mesh: new THREE.Points(geometry, materialPlan)
};

function computeGeometry() {
	const space = 4, nb = 100, amp = 0.1, fre = 1, pi2 = Math.PI * 2

	const geometry = new THREE.BufferGeometry()

	const positions = new Float32Array(nb * nb * 3)
	const colors = new Float32Array(nb * nb * 3)

	let k = 0
	for (let i = 0; i < nb; i++) {
		for (let j = 0; j < nb; j++) {
			const x = i * (space / nb) - space / 2
			const z = j * (space / nb) - space / 2
			const y = amp * (Math.cos(x * pi2 * fre) + Math.sin(z * pi2 * fre))
			positions[3 * k + 0] = x
			positions[3 * k + 1] = y
			positions[3 * k + 2] = z
			const intensity = (y / amp) / 2 + 0.3
			colors[3 * k + 0] = j / nb * intensity
			colors[3 * k + 1] = 0
			colors[3 * k + 2] = i / nb * intensity
			k++
		}
	}
	geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
	geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
	geometry.computeBoundingBox()
	return geometry
}

function animeGeometry(geometry, progress) {
	const space = 4, nb = 100, amp = 0.1, pi2 = Math.PI * 2
	const phase = progress
	const fre = 0.8 + Math.cos(progress) / 2

	let k = 0
	for (let i = 0; i < nb; i++) {
		for (let j = 0; j < nb; j++) {
			const x = i * (space / nb) - space / 2
			const z = j * (space / nb) - space / 2
			const y = amp * (Math.cos(x * pi2 * fre + phase) + Math.sin(z * pi2 * fre + phase))
			geometry.attributes.position.setY(k, y)
			const intensity = (y / amp) / 2 + 0.3
			geometry.attributes.color.setX(k, j / nb * intensity)
			geometry.attributes.color.setZ(k, i / nb * intensity)
			k++
		}
	}
	geometry.attributes.position.needsUpdate = true
	geometry.attributes.color.needsUpdate = true
}

const clock = new THREE.Clock()
let t = 0
//#endregion

// class tablePongClass {
// 	constructor(x, y, z, width, height, depth, color, scene) {
// 		this.geometry = new THREE.BoxGeometry(width, height, depth);
// 		this.material = new THREE.MeshBasicMaterial({ color: color });
// 		this.mesh = new THREE.Mesh(this.geometry, this.material);
// 		this.mesh.position.set(x, y, z);
// 		this.mesh.rotation.x = Math.PI / 2;
// 		scene.add(this.mesh);
// 	}
// }

class tablePongClass {
	constructor(x, y, z, width, height, depth, color, scene) {
		this.geometry = new THREE.BoxGeometry(width, height, depth);

		// Create a gradient texture
		const canvas = document.createElement('canvas');
		canvas.width = 128;
		canvas.height = 128;
		const context = canvas.getContext('2d');

		const gradient = context.createLinearGradient(0, 0, canvas.width, 0);
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
	constructor(x, y, z, width, height, depth, color, scene) {
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

const paddleLeft = new PaddleClasse(-8, 0, 0, 1, 1, 4, 0xff0000, scene); // Red paddle on the left
const paddleRight = new PaddleClasse(8, 0, 0, 1, 1, 4, 0x0000ff, scene); // Blue paddle on the right
const ball = new ballClasse(0, 0, 0, 0.5, 0x00ff00, scene); // Green ball in the middle
const pongTable = new tablePongClass(0, -0.5, 0, 15, 10, 0.5, 0xffff00, scene);
//#endregion


//#region scene.add

scene.add(light);

//#endregion

camera.position.set(0, 10, -1);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ canvas: window.canvas });

renderer.setSize(window.window.innerWidth / 1.5, window.innerHeight / 1.5);
//renderer.setSize(canvas.width, canvas.height);
renderer.setClearColor('black', 1);

function loop() {
	requestAnimationFrame(loop);
	moveBall();
	collisionDetection();
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

