var n;
var l;
var ctx = document.getElementById('chart').getContext('2d');

var Lines = function(lines, legs){
	this.lines = [new Line()];

	for (var i=0; i<lines-1; i++){
		var line = new Line();
		var left = this.lines[this.lines.length-1];
		line.left = left;
		left.right = line;
		line.i = i;
		this.lines.push(line);
	}

	var legsLeft = legs;
	while (legsLeft > 0){
		var pos = Math.floor(Math.random()*legs);
		var dir = Math.round(Math.random()) ? 'left' : 'right';
		var line = this.lines[Math.floor(Math.random()*this.lines.length)]
		line.addLeg(pos, dir);
		legsLeft--;
	}

	this.getWidth = function(){
		return this.lines.length;
	}

	this.getHeight = function(){
		var h = 0;
		for (var i=0; i<this.lines.length; i++){
			h = Math.max(
				h,
				Object.keys(this.lines[i].legs)
					.reduce((x, y)=> Math.max(Number(x), Number(y)))
			)
		}
		return h;
	}

	this.getDestination = function(lineIndex){
		var line = this.lines[lineIndex];
		for (let i=0; i<=this.getHeight(); i++){
			if (i in line.legs){
				line = line.legs[i];
			}
		}
		return line;
	}
}

var Line = function(){
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

function on(event, elemId, onchange){
	document.getElementById(elemId)['on'+event] = onchange;
}

function renderLines(lines){
	

}

on('change', 'num-people', function(e){
	n = Number(e.target.value);
	n = n > 1 ? Math.round(n) : 2;
	renderLines();
})

on('change', 'num-lines', function(e){
	l = Number(e.target.value);
	l = l >= 0 ? Math.round(l) : 0;
	renderLines();
})

on('click', 'run', function(e){
	alert(1)
})