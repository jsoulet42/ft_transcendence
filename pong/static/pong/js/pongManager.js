// Obtenez une référence vers le bouton de réinitialisation
var resetButton = document.getElementById('startButton');
var startIA = document.getElementById('StartIA');
var drawTrajectory = document.getElementById('drawTrajectory');

import { resetScores } from './pong.js';
import { IAActivate } from './pong.js';
import { drawTrajectoryActivate } from './pong.js';

let IAActivateBool = false;
let drawTrajectoryActivateBool = false;

resetButton.addEventListener('click', function() {
	resetScores();
});

startIA.addEventListener('click', function() {
	IAActivateBool = !IAActivateBool;
	IAActivate(IAActivateBool);
});

drawTrajectory.addEventListener('click', function() {
	drawTrajectoryActivateBool = !drawTrajectoryActivateBool;
	drawTrajectoryActivate(drawTrajectoryActivateBool);
});
