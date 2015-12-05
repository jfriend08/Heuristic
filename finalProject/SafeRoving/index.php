
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<!-- page's title -->
<title>Dr Ecco</title>

<!-- open the css sheet for the style -->
<link href="style.css" rel="stylesheet" type="text/css" media="screen" />


<style>
#rover {
				width: 30px;
				height: 30px;
			}
#movingDiv {
				width: 30px;
				height: 30px;
				position: absolute;
				z-index: 10;
			}

#hscores {
	position: absolute;
	top: 2800px;}
	
#instructions {
	position: absolute;
	top: 1900px;}

#n-tile {
				position: absolute;
				top: 345px;
				left: 200px
			}	
#tile-info {
				position: relative;
				top: -30px;
				left: 15px;
				color:black;
				font-size: 15px;
				z-index: 10;
			}
#info{font-size:25px}
			
</style>
</head>
<body>

<!-- div to get the background and the css style -->
<div id="body1">


<div class="post">
	<h2 class="title"><a href="#">Safe Roving</a></h2>
</div>

<div id="movingDiv" style="top:550px;left:280px;">
		</div>
<div id="n-tile" style="top:600px;left:500px;">
<img id="roverid" src="tile.png">
<p id='tile-info'></p>
		</div>

	
<script src="RovingScript.js"></script>

<script>
function theWinner(){
		if(getWinner() != "not set"){
			top.document.location = "../../index.php?task=Safe Roving&winner="+getWinner()+"&ws="+getWinnerScore();
		}
		else{
			alert ("the winner is not known !");
		}
	}


</script>

<center> 
<br /><br />

<!-- "Save my score" button to save the score in the database -->
<form name ="rovingWinner">
 Player Name: <input type="text" id = "winnername" />
<input type="button" value="Save My Score" onClick="theWinner()">
</form>

<form name ="gameData" id="gameData">
Number of Bombs <input type="text" id = "nbombs" />
Detection Radius <input type="text" id = "rad" />
<input type="radio" name="type" value="pl" checked>Human vs Human
<input type="radio"  name="type" value="cmp">Computer vs Human
<input type="button" value="Submit" onClick="place()">
</form>
</center>
<br /><br />

<div id='instructions'>
<div class="post">
			<h2 class="title"><a href="#">Game Details</a></h2>
			
</div>
<h2>Overview</h2>
<p id='ovr'>
In this game, the rover team wants to reach a certain destination at the end of a maze with the rover on a certain enemy planet.
The problem is that the way to the destination is littered with a two types of bombs, bonus bombs and bad bombs. There is a fixed and equal number of both types of bombs.
The adversary team places both types of bombs in the maze; bonus bombs are visible to the rover team whereas bad bombs are invisible.
The rover has a certain number of lives determined by the number of bombs, and is calculated as follows lives=ceiling[(number of bombs)/4].
The rover can move up, down, left and right only (not diagonally), and moving rover one space counts as one step. The total score is the number of steps accumulated and the initial value of the score is 1000.
If the rover steps over a bad bomb, then its score increases by 30 steps and it loses one life. On the other hand, if the rover steps over a bonus bomb, then its score decreases by 30 steps but there is no change in number of lives. 
Any block in maze that the rover steps over, it becomes visible and if there was bad bomb hidden at that block, then it is shown.
There cannot be any bomb on start and destination block, and there cannot be more than one bomb (of any kind) on one block.
The rover team has a constraint on how many moves rover can make and they have to reach the destination with raw total of steps (steps earned only by moving rover, this does not include the steps earned or lost by bombs) less than a steps limit determined by the number of bombs. This step limit is calculated as follows limit=50+6*(number of bombs). 
If rover runs out steps or lives at any point, then the game is over and the rover team loses and their score is 10000. Otherwise, if the rover reaches destination then the rover team wins.
<br><br>The goal of the rover team is to reach the destination with as low score as possible.
<br><br>
In order to facilitate in detecting and avoiding bombs, the rover team is equipped a detector that shows total number of bombs around a certain block within a certain radius. The detector tells the total number of bad bombs present in the blocks at a distance radius from the centre block in any direction. 
This number does not include the bomb placed on the centre block itself. Therefore, when the rover steps over a block in maze for the first time, the number of bombs in the radius is shown to the rover team.
For instance, if radius=1, then the detector will the total number of bombs in 3x3 region around the centre block where the rover is. For radius=2, the detector will the total number of bombs in 5x5 region around the centre block where the rover is.
<br>
<br>
The game implementation allows user to pick from different mazes, and pass the number of bombs and radius as parameters. The implementation allows both, two humans to play against each other, or human rover team to play against computer adversary team.
If two humans are playing, then on the same maze with same parameters, the player who reaches the destination with lower score wins.
</p>

<br>

<h2>Instructions</h2>
<p id='instr'>
1- Select a maze by clicking on its image.
<br><br>
2-Enter the number of bombs, detection radius and choose a game type, and then submit click. The number of bombs should be in the range 1-20 and the radius should be in the range 1-3.
<br><br>
3-If game type is human vs human, then the adversary team places bonus bombs by clicking on blocks on the board.
<br><br>
4-Then the adversary team places bad bombs by clicking on blocks on the board.
<br><br>
5-After the bad bombs disappear, rover team moves the rover with arrow keys.
<br><br>
6-If game type was human vs computer, then use arrow keys to move the rover.
<br><br>
7-Once the game ends, the rover team can submit their score by entering a name in the text field 'Player Name' and clicking on 'Save My Score' button.
<p>
</div>


<div id="hscores">
<?php
		include '../../functions.php';
		getScores("Safe Roving");

?>
</div>


</div>
</body>
</html>
