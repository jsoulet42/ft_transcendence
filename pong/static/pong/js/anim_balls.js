let x = 0;
let y = 0;
let dx = 1;
let dy = 1;

let speed = 3;

function setup()
{
	createCanvas(windowWidth, windowHeight);
	x = random(width);
	y = random(height);
}

function draw()
{
	background(30);
	noStroke();

	fill(220);

	if (dx === 1)
	{
		if (x > width - 50)
		{
			dx = -1
		}
		x = x + speed;
	}
	else
	{
		if(x < 50)
		{
			dx = 1
		}
		x = x - speed;
	}

	if (dy === 1)
	{
		if (y > height - 50)
		{
			dy = -1
		}
		y = y + 2 * speed;
	}
	else
	{
		if (y < 50)
		{
			dy = 1
		}
		y = y - 2 * speed;
	}

	ellipse(x, y, 100, 100);
}

function mousePressed()
{
	if(speed === 3)
	{
		speed = 0;
	}
	else if(speed === 0)
	{
		speed = 3;
	}
}
