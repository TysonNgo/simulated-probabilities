var n, l;
var trials;
var selection;
setN(document.getElementById('num-lines').value);
setL(document.getElementById('num-legs').value);
setTrials(document.getElementById('num-trials').value);
var chart = document.getElementById('chart');
var ctx = chart.getContext('2d');
var selectCtx = document.getElementById('selected').getContext('2d');
var prob = document.getElementById('probability');
var probCtx = prob.getContext('2d');

function setN(val){ // lines
	n = Number(val);
	n = n > 1 ? Math.round(n) : 2;
}

function setL(val){ // legs
	l = Number(val);
	l = l >= 0 ? Math.round(l) : 0;
}

function setTrials(val){
	trials = Number(val);
	trials = trials > 0 ? Math.round(trials) : 1
}

function setSelection(lines, val){
	var s = document.getElementById('select-line');
	s.min = 1;
	s.max = lines.width;
	selection = Number(val);
	selection = selection ? Math.round(selection) : s.min;
	selection = Math.min(selection, s.max);
	document.getElementById('select-line').value = selection;
}

function disableInput(){
	document.getElementById('num-lines').disabled = true;
	document.getElementById('num-legs').disabled = true;
	document.getElementById('num-trials').disabled = true;
	document.getElementById('select-line').disabled = true;
	document.getElementById('run').disabled = true;
}
function enableInput(){
	document.getElementById('num-lines').disabled = false;
	document.getElementById('num-legs').disabled = false;
	document.getElementById('num-trials').disabled = false;
	document.getElementById('select-line').disabled = false;
	document.getElementById('run').disabled = false;
}

var Lines = function(lines, legs){
	this.lines = [new Line(0)];
	this.width =  lines;
	this.height = legs;

	for (var i=1; i<lines; i++){
		var line = new Line(i);
		var left = this.lines[this.lines.length-1];
		line.left = left;
		left.right = line;
		this.lines.push(line);
	}

	var legsLeft = legs;
	while (legsLeft > 0){
		var pos = Math.floor(Math.random()*legs);
		var dir = Math.round(Math.random()) ? 'left' : 'right';
		var line = this.lines[Math.floor(Math.random()*this.lines.length)]
		this.height = Math.max(this.height , line.addLeg(pos, dir));
		legsLeft--;
	}

	this.getDestination = function(lineIndex){
		var line = this.lines[lineIndex];
		var h = this.height;
		for (var i=0; i<h; i++){
			if (i in line.legs){
				line = line.legs[i];
			}
		}
		return line;
	}
}

var Line = function(i){
	this.i = i;
	this.left = null;
	this.right = null;
	this.legs = {
		// pos: left || right
	};

	this.addLeg = function(pos, dir){ // dir: 'left' || 'right'
		if (!this.left && !this.right) throw new Error('no line to connect leg');
		if (!dir) throw new Error('missing direction');
		if (pos >= 0 && Number.isInteger(pos)){
			switch(dir){
				case 'left': if (!this.left) dir = 'right'; break; 
				case 'right': if (!this.right) dir = 'left'; break;
				default: throw new Error('invalid direction '+dir)
			}

			while (pos in this.legs || pos in this[dir].legs){
				pos++;
			}

			this.legs[pos] = this[dir];
			this[dir].legs[pos] = this;
			return pos;
		}
	}

}

var Probability = function(n){
	this.p = Array(n).fill(0);
	this.total = 0;

	this.increment = function(i){
		this.p[i]++;
		this.total++;
	}

	this.getProbability = function(i){
		return this.p[i]/this.total;
	}
}

function on(event, elemId, onchange){
	document.getElementById(elemId)['on'+event] = onchange;
}

function clearCanvas(ctx){
	ctx.clearRect(0, 0, chart.width, chart.height);
	ctx.beginPath();
}

function renderLines(lines){
	clearCanvas(selectCtx);
	clearCanvas(ctx);
	var w = lines.width;
	var h = lines.height;
	var offsetY = chart.height*0.05;
	var lineSpacing = chart.width/w;
	var legSpacing = (chart.height-2*offsetY)/h;

	var prevLegs = {};

	/*
	for (var i=0;i<h;i++){
			ctx.fillText(i, 0, offsetY+i*legSpacing);
	}
	*/

	for (var i=0; i<w; i++){
		prevLegs[i] = {};
		var x = i*lineSpacing+lineSpacing/2;
		ctx.moveTo(x, 0);
		ctx.lineTo(x, chart.height);

		var line = lines.lines[i];
		var legs = line.legs;

		//if (i === w-1) break;

		for (var l in line.legs){
			if (i === 0 || (!(l in prevLegs[i-1]) || prevLegs[i-1][l].i !== i)){
				ctx.moveTo(x, offsetY+l*legSpacing);
				ctx.lineTo((i+1)*lineSpacing+lineSpacing/2, offsetY+l*legSpacing)
			}
			prevLegs[i][l] = line.legs[l];
		}
	}
	ctx.lineWidth = 2;
	ctx.strokeStyle = '#000';
	ctx.stroke()
	
	var x = (selection-1)*lineSpacing+lineSpacing/2;
	ctx.beginPath();
	ctx.strokeStyle = '#00f'
	ctx.lineWidth = 5;
	ctx.moveTo(x, 0);
	ctx.lineTo(x, chart.height);
	ctx.stroke();
}

function drawLegs(lines, i){
	clearCanvas(selectCtx);
	var w = lines.width;
	var h = lines.height;
	var offsetY = chart.height*0.05;
	var lineSpacing = chart.width/w;
	var legSpacing = (chart.height-2*offsetY)/h;
	var line = lines.lines[i];
	
	var x = lineSpacing*line.i+lineSpacing/2;
	selectCtx.moveTo(x, 0);

	for (var i=0; i<h; i++){
		x = lineSpacing*line.i+lineSpacing/2;
		if (i in line.legs){
			selectCtx.lineTo(x, offsetY+i*legSpacing)

			line = line.legs[i];
			x = lineSpacing*line.i+lineSpacing/2;
			selectCtx.lineTo(x, offsetY+i*legSpacing);
			selectCtx.moveTo(x, offsetY+i*legSpacing);
		}
	}

	x = lineSpacing*line.i+lineSpacing/2;
	selectCtx.lineTo(x, chart.height)

	selectCtx.lineWidth = 5;
	selectCtx.strokeStyle = 'rgba(255,0,0,0.8)';
	selectCtx.stroke();

}

function renderProbability(lines, probability){
	clearCanvas(probCtx);

	var w = lines.width;
	var h = prob.height*0.80;
	var lineSpacing = chart.width/w;

	for (var i=0; i<w; i++){
		var per = probability.getProbability(i);
		var x = i*lineSpacing+lineSpacing/2;
		probCtx.moveTo(x, h);
		probCtx.lineTo(x, h-h*per);
		probCtx.strokeStyle = '#00f';
		probCtx.lineWidth = 10;
		probCtx.stroke();
	}

	probCtx.fillText('distribution', 0, prob.height);
	//probCtx.fillText(probability.getProbability(0), 0, prob.height);
}

function runTrials(){
	return new Promise(function(resolve, reject){
		var p = new Probability(lines.width);
		for (var i = 0; i<trials; i++){
			lines = new Lines(n, l);
			var r = trials <= 1000 ? 1000/trials : 1;
			var d = lines.getDestination(selection-1).i;

			p.increment(d);

			if (i <= 1000){
				(function(lines, p){
					setTimeout(function (){
						renderLines(lines);
						drawLegs(lines, selection-1);
						if (i === trials-1){
							resolve();
						}
					}, r*i);
				})(lines, p);
			}
		}
		setTimeout(function(){
			renderProbability(lines, p);
			resolve();
		}, 1100);
	});
}

function run(e){
	disableInput();
	clearCanvas(probCtx);
	runTrials().then(function(){
		enableInput();
		e.target.focus();
	});
}

lines = new Lines(n, l)
document.getElementById('select-line').disabled = false;
setSelection(lines, 1);
renderLines(lines)

on('change', 'num-lines', function(e){
	setN(e.target.value);
	lines = new Lines(n, l);
	clearCanvas(probCtx);
	renderLines(lines);
})

on('change', 'num-legs', function(e){
	setL(e.target.value);
	lines = new Lines(n, l);
	clearCanvas(probCtx);
	renderLines(lines);
})

on('change', 'num-trials', function(e){
	setTrials(e.target.value);
})

on('change', 'select-line', function(e){
	setSelection(lines, e.target.value);
	clearCanvas(probCtx);
	renderLines(lines)
})

on('click', 'run', run)

function enter(e){
	if (e.which === 13){
		e.preventDefault();
		run(e);
	}
}
document.getElementById('num-lines').onkeydown = enter;
document.getElementById('num-legs').onkeydown = enter;
document.getElementById('num-trials').onkeydown = enter;
document.getElementById('select-line').onkeydown = function(e){
	enter(e);
	if (e.which === 9){
		console.log(e)
		e.preventDefault();
		document.getElementById('num-lines').focus();
	}
}

document.getElementById('num-lines').focus();