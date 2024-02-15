import * as THREE from 'three';

window.canvas = document.getElementById('pongCanvas3D');

// canvas.width = window.innerWidth / 2;
// canvas.height = window.innerHeight / 2;
window.iw = window.innerWidth;
window.ih = window.innerHeight;

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(70, iw / ih);

const BallMesh = new THREE.SphereGeometry(0.5, 32, 32);

const material = new THREE.MeshPhongMaterial({ color: 'red' });

const light = new THREE.PointLight('white', 1, 0, 0);


//#region procedural plane

const geometry = computeGeometry();
let materialPlan = new THREE.PointsMaterial({ size: 0.015, vertexColors: true });

let planeProcedural = {
	mesh: new THREE.Points(geometry, materialPlan)
};

const planeGeometry = new THREE.PlaneGeometry(15, 10);
const planeMaterial = new THREE.MeshBasicMaterial({color: 0xffff00, side: THREE.DoubleSide});
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = Math.PI / 2;
plane.position.y = -0.5;
scene.add(plane);

//#endregion


let ball = {
	mesh: new THREE.Mesh(BallMesh, material),
	direction: 1,
};

const clock = new THREE.Clock()
let t = 0

scene.add(ball.mesh);
scene.add(light);
//scene.add(planeProcedural.mesh);


//camera.position.set(0, 10, -10);
camera.position.set(0, 10, -1);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ canvas: window.canvas });

renderer.setSize(window.iw / 1.5, window.ih / 1.5);
renderer.setClearColor('cyan');

function loop() {
	requestAnimationFrame(loop);
	moveBall();
	collisionDetection();

	t += clock.getDelta()
	//animeGeometry(geometry, t)
	//plane.mesh.rotation.y = 0.1*t
	renderer.render(scene, camera);
}

function moveBall() {
	ball.mesh.position.x += 0.1 * ball.direction;

}

function collisionDetection() {

	// Adjust the ball position by its radius
	const ballPosition = new THREE.Vector3(
		ball.mesh.position.x,
		ball.mesh.position.y,
		ball.mesh.position.z
	);

	const planeBox = new THREE.Box3().setFromObject(plane);
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

loop();
