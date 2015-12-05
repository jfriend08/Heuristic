	var d=document.createElement("P");
	d.innerHTML='Steps Used: ';
	d.id="disp";
	d.style.position='absolute';
	d.style.left="600px";
	d.style.top="610px";
	var element=document.getElementById("body1");
	element.appendChild(d);
	
	var d=document.createElement("P");
	d.innerHTML='Current Score: 1000';
	d.style.color='white';
	//d.style.font-size='20px';
	d.id="info";
	d.style.position='absolute';
	d.style.left="30px";
	d.style.top="500px";
	var element=document.getElementById("body1");
	element.appendChild(d);
	
	var d=document.createElement("P");
	d.innerHTML='Lives Remaining: ';
	d.id="l-info";
	d.style.position='absolute';
	d.style.left="760px";
	d.style.top="600px";
	var element=document.getElementById("body1");
	element.appendChild(d);
	
	var d=document.createElement("P");
	d.innerHTML='Steps Remaining: ';
	d.id="rem-info";
	d.style.position='absolute';
	d.style.left="760px";
	d.style.top="620px";
	var element=document.getElementById("body1");
	element.appendChild(d);
	
	var d=document.createElement("P");
	d.innerHTML='Current Tile: ';
	d.id="tiledesc";
	d.style.position='absolute';
	d.style.left="430px";
	d.style.top="610px";
	var element=document.getElementById("body1");
	element.appendChild(d);
	
	var d=document.createElement("P");
	d.innerHTML='Select a Maze';
	d.id="phase";
	d.style.position='absolute';
	d.style.left="50px";
	d.style.top="300px";
	d.style.size='20px';
	var element=document.getElementById("body1");
	element.appendChild(d);
	
	
	var status;
	var type;
	var rad_disp;
	var lives;
	var deaths=0;
	var total_time;
	var winnerScore='not set';
	var timeScore='not set';
	var winner='not set';
	var phase=10;
	var numb=0;
	var radius=0;
	var b_placed=0;
	var fb_placed=0;
	var b_list=new Array();
	var fb_list=new Array();
	var exploded=new Array();
	var expCounter=0;
	var grid=new Array()
	for(var i=0;i<20;i++){grid[i]=new Array();}
	var snd = new Audio("explosion.wav");
	var snd2 = new Audio("fexplosion.wav");
	var mvs = new Audio("move.wav");
	var ws = new Audio("win.wav");
	var over = new Audio("death.wav");
	var hwall=new Array();
	var vwall=new Array();
	make_maps();

	
	function makeGrid(){
		winnerScore=1000;
		timeScore=0;
		for(var i=0;i<20;i++){
			for (var j=0;j<10;j++){
				var ID='P-'+i+'-'+j;
				var dID='D-'+i+'-'+j;
				var div = document.createElement("div");
				div.style.width = "40px";
				div.style.height = "40px";
				div.style.position='absolute'
				div.style.top=185+40*j+'px';
				div.style.left=275+40*i+'px';
				div.id=dID;
				div.setAttribute('onclick','boardClick(this)')
				var element=document.getElementById("body1");
				element.appendChild(div);
				
				var para=document.createElement("IMG");
				para.setAttribute('src','dot.png');
				para.style.position='absolute';
				para.style.top=205+40*j+'px';
				para.style.left=291+40*i+'px';
				para.setAttribute('onclick','boardClick(this)');
				para.id=ID;
				grid[i][j]=new Array();
				grid[i][j]=[ID,291+40*i,205+40*j,0];
				var element=document.getElementById("body1");
				element.appendChild(para);
			
			}
		}
	document.getElementById('P-19-0').style.visibility="hidden";
	document.getElementById('P-0-9').style.visibility="hidden";
	}
	
	function place(){
		if (phase==0){
			numb=document.getElementById("nbombs").value;
			radius=document.getElementById("rad").value;
			if(numb<=0 || numb>20){
				alert('Please enter the number of bombs in range 1-20')
			}
			
			else if(radius<=0 || radius>3){
				alert('Please enter the radius in range 1-3')
			}
			else{
				document.getElementById("gameData").style.visibility="hidden";
				var radios = document.getElementsByName("type");
				for (var i = 0; i < radios.length; i++) {       
					if (radios[i].checked) {
						type=radios[i].value;
						break;
					}
				}
				lives=Math.ceil(numb/4);
				total_time=50+6*numb;
				document.getElementById('rem-info').innerHTML="Steps Remaining: "+total_time;
				document.getElementById('l-info').innerHTML="Lives Remaining: "+lives;
				phase=1;
				makeGrid()
				document.getElementById('phase').style.left='50px';
				document.getElementById('phase').innerHTML='Place '+numb+' Bonus Bombs';
				if(type=='cmp'){placeBomb()}
			}
		}
		else{
			alert('Select a board first')
		}
	}
	
	function boardClick(obj){
		if (phase==2){
			var dID=obj.id;
			var ID='P'+dID.slice(1,dID.length);
			var cord=ID.split('-');
			var x=parseInt(cord[1]);
			var y=parseInt(cord[2]);
			if(ID!='P-19-0' && ID!='P-0-9'){
			if(b_list.indexOf(ID)==-1 && fb_list.indexOf(ID)==-1){
					var para=document.getElementById(ID);
					para.setAttribute('src','bomb.png');
					para.style.top=200+40*y+'px';
					para.style.left=280+40*x+'px';
					para.style.visibility="visible";
					b_list[b_placed]=ID;
					b_placed++;

				}	
			}
			if(b_placed==numb){
				phase=3;
				setTimeout(Move,1000);
				return;
			}
		}
		
		else if (phase==1){
			var dID=obj.id;
			var ID='P'+dID.slice(1,dID.length);	
			var cord=ID.split('-');
			var x=parseInt(cord[1]);
			var y=parseInt(cord[2]);
			if(ID!='P-19-0' && ID!='P-0-9'){
				if(b_list.indexOf(ID)==-1 && fb_list.indexOf(ID)==-1){
					var para=document.getElementById(ID);
					para.setAttribute('src','fbomb.png');
					para.style.top=200+40*y+'px';
					para.style.left=280+40*x+'px';
					para.style.visibility="visible";
					fb_list[fb_placed]=ID;
					fb_placed++;
				}
			}
			if(fb_placed==numb){
			document.getElementById('phase').style.left='50px';
			document.getElementById('phase').innerHTML='Place '+numb+' Real Bombs';
				phase=2;
				return;
			}
		}
	}
	

function Move() {
	if(type=='pl'){
		for (var g=0;g<b_list.length;g++){
			var para=document.getElementById(b_list[g]);
			para.setAttribute('src','dot.png');
			var ID=b_list[g];
			var cord=ID.split('-');
			var x=parseInt(cord[1]);
			var y=parseInt(cord[2]);
			para.style.top=205+40*y+'px';
			para.style.left=291+40*x+'px';
		}
		
		var x=0;
		var y=9;
		var para=document.createElement("p");
		var binfo=info(x,y);
		var node=document.createTextNode(binfo);
		para.appendChild(node);
		para.style.position='absolute';
		para.style.top=195+40*y+'px';
		para.style.left=290+40*x+'px';
		para.style.color='black';
		var element=document.getElementById("body1");
		element.appendChild(para);
		document.getElementById("tile-info").innerHTML=binfo;
		document.getElementById('phase').style.left='50px';
		document.getElementById('phase').innerHTML='Move the Rover Using arrow Keys';
	}
	var moveDiv = document.getElementById("movingDiv");
	window.onkeydown = function(e) {
		if (phase==3){
		e.preventDefault();

		if (!e)
		{
			e = window.event;
		}

		var keyCode;
		// pixel wise speed variable
		var speed = 40;       

		if(e.which) {
			keyCode = e.which;
		} else {
			keyCode = e.keyCode;
		}


		//increment/decrement the top or left of the div based on the arrow key movements
		var tp=parseInt(moveDiv.style.top, 10);
		var lt=parseInt(moveDiv.style.left, 10);
		
		if(keyCode === 37) {
			document.getElementById('rover').setAttribute('src','rover_left.png');
			var left=parseInt(moveDiv.style.left, 10) - speed;
			if (left>=280){
			var top=parseInt(moveDiv.style.top, 10);
			var x=Math.floor((lt-275)/40);
			var y=Math.floor((tp-185)/40)+1;
			var ID=x+'-'+y;
			if(vwall.indexOf(ID)==-1){
					update(left,top);
				}
			}
		} else if (keyCode === 38) {
			document.getElementById('rover').setAttribute('src','rover_up.png');
			var top=parseInt(moveDiv.style.top, 10) - speed;
			if (top>=190){
			
			var left=parseInt(moveDiv.style.left, 10);
			var x=Math.floor((lt-275)/40)+1;
			var y=Math.floor((tp-185)/40);
			var ID=x+'-'+y;
			if(hwall.indexOf(ID)==-1){
				update(left,top);
				}
			}
		} else if (keyCode === 39) {
			document.getElementById('rover').setAttribute('src','rover_right.png');	
			var left=parseInt(moveDiv.style.left, 10) + speed;
			if (left<=1040){
			
			var top=parseInt(moveDiv.style.top, 10);
			var x=Math.floor((lt-275)/40)+1;
			var y=Math.floor((tp-185)/40)+1;
			var ID=x+'-'+y;
			if(vwall.indexOf(ID)==-1){
					update(left,top);
				}
			}
		} else if (keyCode === 40) {
			document.getElementById('rover').setAttribute('src','rover_down.png');
			var top=parseInt(moveDiv.style.top, 10) + speed;
			if (top<=550){
			var left=parseInt(moveDiv.style.left, 10);
			var x=Math.floor((lt-275)/40)+1;
			var y=Math.floor((tp-185)/40)+1;
			var ID=x+'-'+y;
			if(hwall.indexOf(ID)==-1){
					update(left,top);
				}
			}
			}
		}
	};
}

function update(l,t){
	document.getElementById('roverid').setAttribute('src','tile.png');
	mvs.currentTime=0;
	var moveDiv = document.getElementById("movingDiv");
	var x=Math.floor((l-275)/40);
	var y=Math.floor((t-185)/40);
	var ID='P-'+x+'-'+y;
	var tile=document.getElementById(ID);
	mvs.play();
	if((b_list.indexOf(ID)==-1 && fb_list.indexOf(ID)==-1) || ((b_list.indexOf(ID)>=0 || fb_list.indexOf(ID)>=0) && exploded.indexOf(ID)>=0)){
		timeScore+=1;
		winnerScore+=1;
		moveDiv.style.top=t+'px';
		moveDiv.style.left=l+'px';
		var binfo=info(x,y);
		if (grid[x][y][3]==0){
			grid[x][y][3]=1;
			tile.style.visibility="hidden";
			var para=document.createElement("p");
			var node=document.createTextNode(binfo);
			para.appendChild(node);
			para.style.position='absolute';
			para.style.top=195+40*y+'px';
			para.style.left=290+40*x+'px';
			para.style.color='black';
			var element=document.getElementById("body1");
			element.appendChild(para);
		}
	}
	
	else if(b_list.indexOf(ID)>=0){
		document.getElementById('roverid').setAttribute('src','tile-b.png');
		snd.currentTime=0;
		winnerScore+=30;
		timeScore+=1;
		moveDiv.style.top=t+'px';
		moveDiv.style.left=l+'px';
		deaths++;
		exploded[expCounter]=ID;
		expCounter++;
		tile.setAttribute('src','hit.png');
		tile.style.top=t+'px';
		tile.style.left=l+'px';
		snd.play();
		grid[x][y][3]=1;
		var para=document.createElement("p");
		var binfo=info(x,y);
		var node=document.createTextNode(binfo);
		para.appendChild(node);
		para.style.position='absolute';
		para.style.top=195+40*y+'px';
		para.style.left=290+40*x+'px';
		para.style.color='black';
		var element=document.getElementById("body1");
		element.appendChild(para);
	}
	else if(fb_list.indexOf(ID)>=0){
		snd2.currentTime=0;
		winnerScore-=30;
		timeScore+=1;
		moveDiv.style.top=t+'px';
		moveDiv.style.left=l+'px';

		exploded[expCounter]=ID;
		expCounter++;
		tile.setAttribute('src','miss.png');
		tile.style.top=t+'px';
		tile.style.left=l+'px';
		snd2.play();
		grid[x][y][3]=1;
		var para=document.createElement("p");
		var binfo=info(x,y);
		var node=document.createTextNode(binfo);
		para.appendChild(node);
		para.style.position='absolute';
		para.style.top=195+40*y+'px';
		para.style.left=290+40*x+'px';
		para.style.color='black';
		var element=document.getElementById("body1");
		element.appendChild(para);
	}	
	
	document.getElementById("tile-info").innerHTML=binfo;
	
	if(y==0 && x==19){
	phase=4;
	document.getElementById('disp').innerHTML="Steps Used: "+timeScore;
	document.getElementById('info').innerHTML="Final Score: "+winnerScore;
	ws.play();
	document.getElementById('phase').innerHTML="You Won!<br>You Final Score Is: "+winnerScore+"<br>Enter Your Name and<br> Press 'Save My Score'";
	status='win';
	return;
	}
	
	if(deaths>lives || timeScore==total_time){
		phase=4;
		winnerScore=10000;
		document.getElementById('disp').innerHTML="Steps Used: "+timeScore;
		document.getElementById('info').innerHTML="Final Score: "+winnerScore;
		over.play();
		if(deaths>lives){document.getElementById('phase').innerHTML="GAME OVER!<br> Ran Out of Lives!<br>You Final Score Is: "+winnerScore+"<br>Enter Your Name and<br> Press 'Save My Score'";
		document.getElementById('l-info').innerHTML="Lives Remaining: 0"}
		else{document.getElementById('phase').innerHTML="GAME OVER!<br> Ran Out of Time!<br>You Final Score Is: "+winnerScore+"<br>Enter Your Name and<br> Press 'Save My Score'";}
		status='lost';
		return;
	}
	document.getElementById('disp').innerHTML="Steps Used: "+timeScore;
	document.getElementById('info').innerHTML="Current Score: "+winnerScore;
	document.getElementById('rem-info').innerHTML="Steps Remaining: "+(total_time-timeScore);
	document.getElementById('l-info').innerHTML="Lives Remaining: "+(lives-deaths);
}

function info(x,y){
	var xt;
	var yt;
	var bcnt=0;
	for (var g=0;g<2*radius+1;g++){
		xt=x-radius+g;
		for (var h=0;h<2*radius+1;h++){
			yt=y-radius+h;
			if ((xt!=x || yt!=y) && b_list.indexOf('P-'+xt+'-'+yt)>=0){
				bcnt++;
			}
		}
	}
	return bcnt;
}

function make_maps(){
	var para=document.createElement("IMG");
	para.setAttribute('src','board1.png');
	para.style.position='absolute';
	para.style.top='185px';
	para.style.left='275px';
	para.setAttribute('onclick','select(this)');
	para.id="map1"
	var element=document.getElementById("body1");
	element.appendChild(para);
	
	var para=document.createElement("IMG");
	para.setAttribute('src','board-s1.png');
	para.style.position='absolute';
	para.style.top='600px';
	para.style.left='275px';
	para.setAttribute('onclick','select(this)');
	para.id="map-s1"
	var element=document.getElementById("body1");
	element.appendChild(para);
	
	var para=document.createElement("IMG");
	para.setAttribute('src','board-s2.png');
	para.style.position='absolute';
	para.style.top='1015px';
	para.style.left='275px';
	para.setAttribute('onclick','select(this)');
	para.id="map-s2"
	var element=document.getElementById("body1");
	element.appendChild(para);
	
	var para=document.createElement("IMG");
	para.setAttribute('src','board-s3.png');
	para.style.position='absolute';
	para.style.top='1430px';
	para.style.left='275px';
	para.setAttribute('onclick','select(this)');
	para.id="map-s3"
	var element=document.getElementById("body1");
	element.appendChild(para);
}

function select(obj){
	//document.getElementById('phase').innerHTML=obj.id;
	
	
	document.getElementById("map1").style.visibility='hidden';
	document.getElementById("map-s1").style.visibility='hidden';
	document.getElementById("map-s2").style.visibility='hidden';
	document.getElementById("map-s3").style.visibility='hidden';
	
	
	if(obj.id=='map1'){
		var para=document.createElement("IMG");
		para.setAttribute('src','board1.png');
		para.style.position='absolute';
		para.style.top='185px';
		para.style.left='275px';
		para.id="board";
		var element=document.getElementById("body1");
		element.appendChild(para);
		hwall=['3-1','9-1','10-1','16-1','1-2','6-2','7-2','14-2','15-2','12-3','17-3','18-3','3-4','4-4','5-4','12-4','13-4','9-5','11-5','17-5','1-6','2-6','8-6','9-6','10-6','16-6','19-6','20-6','11-7','3-8','4-8','5-8','9-8','12-8','17-8','18-8','3-9','4-9','17-9','19-9'];
		vwall=['1-8','3-3','3-4','4-2','4-5','5-7','5-8','6-6','6-7','7-3','7-4','8-3','8-4','8-7','8-10','9-4','9-5','10-9','11-1','11-2','12-7','12-8','13-7','14-9','14-10','15-3','15-4','15-8','16-7','16-8','18-4'];
	}
	
	else if (obj.id=='map-s1'){
		var para=document.createElement("IMG");
		para.setAttribute('src','board-s1.png');
		para.style.position='absolute';
		para.style.top='185px';
		para.style.left='275px';
		para.id="board";
		var element=document.getElementById("body1");
		element.appendChild(para);
		hwall=['3-2','4-2','5-2','11-3','12-3','13-3','14-3','15-3','1-4','2-4','10-5','11-5','19-6','20-6','6-7','7-7','8-7','9-7','10-7','16-8','17-8','18-8']
		vwall=['3-7','3-8','5-3','5-4','5-5','5-6','5-7','8-3','8-4','8-5','12-6','12-7','12-8','15-4','15-5','15-6','15-7','15-8','17-3','17-4']

	}
	
	else if (obj.id=='map-s2'){
		var para=document.createElement("IMG");
		para.setAttribute('src','board-s2.png');
		para.style.position='absolute';
		para.style.top='185px';
		para.style.left='275px';
		para.id="board";
		var element=document.getElementById("body1");
		element.appendChild(para);
		hwall=['9-3','11-3','13-3','3-5','4-5','5-5','6-5','7-5','15-5','16-5','17-5','18-5','9-8','11-8','13-8']
		vwall=['7-4','7-6','7-8','10-1','10-2','10-3','10-9','10-10','14-4','14-6','14-8']
	}
	
	else if (obj.id=='map-s3'){
		var para=document.createElement("IMG");
		para.setAttribute('src','board-s3.png');
		para.style.position='absolute';
		para.style.top='185px';
		para.style.left='275px';
		para.id="board";
		var element=document.getElementById("body1");
		element.appendChild(para);
		hwall=['8-4','9-4','10-4','11-4','12-4','15-6','16-6','5-7','6-7','7-7']
		vwall=['4-3','4-4','4-5','4-6','4-7','10-5','10-6','10-7','10-8','10-9','10-10','16-1','16-2','16-3','16-4','16-5','16-6']
	}
	
	phase=0;
	
	var para=document.createElement("IMG");
	para.setAttribute('src','rover_right.png');
	para.id='rover';
	var element=document.getElementById("movingDiv");
	element.appendChild(para);
	document.getElementById('phase').innerHTML="Enter Number of Bombs,<br> Detection Range and<br> Game Type";
	document.getElementById("instructions").style.top='680px';
	document.getElementById("hscores").style.top='1580px';
	
}

function placeBomb(){
	var k=0;
	for(var g=0;g<numb;g++){
		var nID;
		var x;
		var y;
		while (k==0){
			x=getRandomInt(19.99);
			y=getRandomInt(9.99);;
			nID='P-'+x+'-'+y;
			if(nID!='P-19-0' && nID!='P-0-9' && fb_list.indexOf(nID)==-1 && b_list.indexOf(nID)==-1){
				var para=document.getElementById(nID);
				para.setAttribute('src','fbomb.png');
				para.style.top=200+40*y+'px';
				para.style.left=280+40*x+'px';
				para.style.visibility="visible";
				fb_list[fb_placed]=nID;
				fb_placed++
				break;
			}
		}
		
		var xt;
		var yt;
		var neighbor=new Array();
		var bcnt=0;
		
		for (var t=0;t<3;t++){
			xt=x-1+t;
			for (var h=0;h<3;h++){
				yt=y-1+h;
				if (xt>=0 && xt<=19 && yt>=0 && yt<=9 &&(xt!=x || yt!=y) && (xt!=0 || yt!=9) && (xt!=19 || yt!=0)){
					if(b_list.indexOf('P-'+xt+'-'+yt)==-1 && fb_list.indexOf('P-'+xt+'-'+yt)==-1){
						neighbor[bcnt]='P-'+xt+'-'+yt;
						bcnt++;
					}
				}
			}
		}	
		
		if(bcnt>0){
			var r=getRandomInt(bcnt-0.01);
			nID=neighbor[r];
			var para=document.getElementById(nID);
			var cord=nID.split('-');
			var x=parseInt(cord[1]);
			var y=parseInt(cord[2]);
			para.setAttribute('src','dot.png');
			para.style.top=205+40*y+'px';
			para.style.left=291+40*x+'px';
			para.style.visibility="visible";
			b_list[b_placed]=nID;
			b_placed++
		}
		
		else{
			while (k==0){
				var x=getRandomInt(19.99);
				var y=getRandomInt(9.99);;
				nID='P-'+x+'-'+y;
				if(nID!='P-19-0' && nID!='P-0-9' && fb_list.indexOf(nID)==-1 && b_list.indexOf(nID)==-1){
					var para=document.getElementById(nID);
					para.setAttribute('src','dot.png');
					para.style.top=205+40*y+'px';
					para.style.left=291+40*x+'px';
					para.style.visibility="visible";
					b_list[b_placed]=nID;
					b_placed++
					break;
				}
			}
		}
	}
	var x=0;
	var y=9;
	var para=document.createElement("p");
	var binfo=info(x,y);
	var node=document.createTextNode(binfo);
	para.appendChild(node);
	para.style.position='absolute';
	para.style.top=195+40*y+'px';
	para.style.left=290+40*x+'px';
	para.style.color='black';
	var element=document.getElementById("body1");
	element.appendChild(para);
	document.getElementById("tile-info").innerHTML=binfo;
	document.getElementById('phase').style.left='50px';
	phase=3;
	document.getElementById('phase').innerHTML='Move the Rover Using arrow Keys';
	Move()
	return
}

function getRandomInt (max) {
		return Math.floor(Math.random()*max);
}

function getWinner(){
	if (status=='win' || status=='lost'){
		winner=document.getElementById("winnername").value;
		return winner
	}
	else{return winner}
}

function getWinnerScore(){
	if (status=='win' || status=='lost'){
		return winnerScore
	}
	else{return 'not set'}
}

	