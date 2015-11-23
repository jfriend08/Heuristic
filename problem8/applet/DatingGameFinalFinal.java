package datinggamefinalfinal;

import processing.core.PApplet;
import data.*;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.*;


public class DatingGameFinalFinal extends PApplet {

	/**
	 * 
	 */
	private static final long serialVersionUID = 7894611403364472258L;
	private boolean gameOver = false;
	private boolean gameSetup = false;
	private boolean menuSetup = false;
	private boolean menuActive = true;
	private boolean gameActive = false;
	private int N = 5;//default
	private Candidate[] candidateSelection = null;
	private Matchmaker[] matchmaker = null;
	private Person person = null;
	private Tab[] tabs = null;
	private int activeTab = 1;
	private Vector<Double> graphPoints = new Vector<Double>();
		
	int clock = 120;
	int frameCount = 0;
	int numMatchmakers = 1;
	boolean timer = false;
	
	private menuIcon mOne, mTwo, easy, med, hard, yes, no;
	private Icon next, prev;

	
	public void setup() {
		
		size(1280,768);
		Icon.pApplet = this;
		Square.pApplet = this;
		Rectangle.pApplet = this;
		Candidate.pApplet = this;
		Tab.pApplet = this;
		Person.pApplet = this;
		Matchmaker.pApplet = this;
		menuIcon.pApplet = this;
		initMenuIcon();
	}
	public void initMenuIcon() { // initialize the icons on the menu
		
		//number of matchmakers
		mOne = new menuIcon(550,280,32,255,0,0);
		mTwo = new menuIcon(550,320,32,0,0,255);
		
		//difficulty level
		easy = new menuIcon(550,400,32,204,255,153);
		med = new menuIcon(640,400,32,102,255,102);
		hard = new menuIcon(550,440,32,0,204,102);
		
		//timer ON or OFF
		yes = new menuIcon(550,520,32,102,255,204);
		no = new menuIcon(640,520,32,102,204,204);
	}
	public void initMatchmaker() { // initialize each matchmaker
		matchmaker = new Matchmaker[numMatchmakers];
		int x = 16; //score positions
		int y = 280;
		boolean active = false;
		for(int i = 0; i < numMatchmakers; i++) {
			if(i == 0) //initially matchmaker one is active and makes the first candidate selection
				active = true;
			else 
				active = false;
			matchmaker[i] = new Matchmaker(x,y,active);
			y += 64;
		}
	}
	
	public void initGraphPoints() {//create 21 points on the graph and initialize their score values
		double positive = 1.0;
		for(int i = 0; i < 10; i++) { //round off to one decimal point
			graphPoints.add(i, positive);
			positive -= 0.1;
			positive = ((double)((int)(positive * 100)))/100;

		}
		
		graphPoints.add(10,0.0);
		double negative = -0.1;
		for(int i = 11; i < 21; i++) { //round off to one decimal point
			graphPoints.add(i, negative);
			negative += -0.1;
			negative = ((double)((int)(negative * 100)))/100;
		}
	}
	
	public void initIcons() { // icons on game page to toggle between candidate sets
		next = new Icon(956,675,96,32,204,255,102);
		prev = new Icon(200,675,96,32,255,255,102);
	}
	
	public void initPerson() { // generate person attribute weights and person name
		Random generator = new Random();
		int numPositive = N;
		int numNegative = 0;
		double sumPositive = 0;
		double sumNegative = 0;
		Vector<Double> positive = new Vector<Double>();
		Vector<Double> negative = new Vector<Double>();
		double tmp;
		double tmp2;
		
		//randomly generate no. of positive weights
		while(numPositive > N - 1) { //don't want too few or too many positive values
			numPositive = generator.nextInt(N) + 2;
		} 
		
		//divide 1 equally by number of positive weights
		tmp = (double)1/numPositive;
		tmp = ((double)((int)(tmp * 100)))/100;
		for(int i = 0; i < numPositive; i++)
			positive.add(i,tmp);
		
		//take pairs of numbers half one and add it to the adjacent
		for(int i = 0; i < numPositive - 1; i = i + 2) {
			tmp = positive.get(i);
			tmp2 = positive.get(i + 1);
		
			tmp = tmp/2;
			tmp2 = tmp2 + tmp;

			tmp = ((double)((int)(tmp * 100)))/100;
			tmp2 = ((double)((int)(tmp2 * 100)))/100;
			
			positive.set(i,tmp);
			positive.set(i + 1, tmp2);
		}
		
		//now take alternate pairs and do the same as above
		for(int i = 0; i + 2 < numPositive; i++) {
			tmp = positive.get(i);
			tmp2 = positive.get(i + 2);
			
			tmp = tmp/2;
			tmp2 = tmp2 + tmp;
		
			tmp = ((double)((int)(tmp * 100)))/100;
			tmp2 = ((double)((int)(tmp2 * 100)))/100;
		
			positive.set(i,tmp);
			positive.set(i + 2, tmp2);
		}
				
		//now add them up and add the difference if less than 1.0 to the first number
		for(int i = 0; i < numPositive; i++) {
			sumPositive = sumPositive + positive.get(i);
		}
		
		if(sumPositive < 1.0) {
			tmp = 1 - sumPositive;
			tmp2 = positive.get(0);
			tmp = tmp + tmp2;
			tmp = ((double)((int)(tmp * 100)))/100;
			positive.set(0, tmp);
		}
			
		//similarly for all negative numbers
		numNegative = N - numPositive;
		tmp = (double)(-1)/numNegative;
		tmp = ((double)((int)(tmp * 100)))/100;		
		for(int i = 0; i < numNegative; i++)
			negative.add(i,tmp);
		
		for(int i = 0; i < numNegative - 1; i = i + 2) {
			tmp = negative.get(i);
			tmp2 = negative.get(i + 1);
			
			tmp = tmp/2;
			tmp2 = tmp2 + tmp;

			tmp = ((double)((int)(tmp * 100)))/100;
			tmp2 = ((double)((int)(tmp2 * 100)))/100;
			
			negative.set(i,tmp);
			negative.set(i + 1, tmp2);
		}
		
		for(int i = 0; i + 2 < numNegative; i++) {
			tmp = negative.get(i);
			tmp2 = negative.get(i + 2);
			
			tmp = tmp/2;
			tmp2 = tmp2 + tmp;

			tmp = ((double)((int)(tmp * 100)))/100;
			tmp2 = ((double)((int)(tmp2 * 100)))/100;
			
			negative.set(i,tmp);
			negative.set(i + 2, tmp2);
		}
				
		for(int i = 0; i < numNegative; i++) {
			sumNegative = sumNegative + negative.get(i);
		}
		if(sumNegative > -1.0) {
			tmp =  sumNegative - (-1);
			tmp2 = negative.get(0);
			tmp = tmp2 - tmp;
			tmp = ((double)((int)(tmp * 100)))/100;
			negative.set(0, tmp);
		}
		 
		//set to person attribute values and shuffle
		person = new Person(8,8);
		
		for(int i = 0; i < numPositive; i++) 
			person.setAttrVal(positive.get(i),i);
		
		for(int k = 0; k < numNegative; k++)
			person.setAttrVal(negative.get(k), k + numPositive);
		person.randomize();
		
		URL urlF = null;

		try 
		{
			urlF = new URL(getCodeBase(),"./data/FNames.txt");
		}
		catch(MalformedURLException e) {}
		
		try { //set person name
			InputStream is = urlF.openStream();
			//InputStream is = new FileInputStream("FNames.txt");
			BufferedReader input = new BufferedReader(new InputStreamReader(is));
			int offset = generator.nextInt(20) + 1;
			String candidateName = null;
			int line = 0;
			while (line != offset) {
				candidateName = input.readLine();
				line++;
			}
			
			person.setName(candidateName);
		}
		catch (IOException e) {System.out.println("" + e);}
		
		
	}
	
	public void initCandidate() {

		Random generator = new Random();
		double value = 0;
		int temp;
		int x; 
		int y;
		candidateSelection = new Candidate[50];
		int cCnt = 0; 
		URL urlM = null;

		try 
		{
			urlM = new URL(getCodeBase(),"./data/MNames.txt");
		}
		catch(MalformedURLException e) {}
		try {
			InputStream is = urlM.openStream();
			//InputStream is = new FileInputStream("data//MNames.txt");
			BufferedReader input = new BufferedReader(new InputStreamReader(is));
			int offset = generator.nextInt(50) + 1;
			String candidateName;
			int line = 0;
			while (line != offset) {
				input.readLine();
				line++;
			}
			
		
			for(int tb = 0; tb < 10; tb++) { //for each tab generate 5 candidates
				x = 240;
				y = 150;
				for(int i = 0; i < 5; i++) 
				{
					candidateName = input.readLine(); //read in candidate name
					candidateSelection[cCnt] = new Candidate(x,y,tb + 1,candidateName);
					for(int k = 0; k < N; k++) //generate attribute value
					{
						temp = (int)(generator.nextDouble() * 100);//round off to two decimal places
						value = ((double)temp)/100;
						if(value < 0.5) // if less that 0.5 set to 0
							candidateSelection[cCnt].setAttrVal(0, k);
						else //else set to 1
							candidateSelection[cCnt].setAttrVal(1, k); 
					}
					x += 155;
					cCnt++;
				}
			}
			
			//loop through candidates and check if ideal candidate was generated
			//if not, randomly select a candidate and modify attribute values 
			//to create an ideal candidate
			double score = 0;
			boolean ideal = false; 
			for(int i = 0; i < 50; i++) {
				score = 0;
				for(int k = 0; k < N; k++) {
					score += candidateSelection[i].attrValue.get(k) * person.attrValue.get(k);
				}
				score = ((double)((int)(score * 100)))/100;
				candidateSelection[i].setScore(score);
				if(score == 1.0)
					ideal = true;
				
				if(ideal) {
					//System.out.println("Ideal generated name:" + candidateSelection[i].getName());
				}
			}
			
			if(!ideal) { //ideal candidate was not generated
				int cIdeal = generator.nextInt(50); //randomly select a candidate
				for(int i = 0; i < N; i++) {
					//set all positive person attributes to 1 and 0 for negative
					if(person.attrValue.get(i) > 0)
						candidateSelection[cIdeal].resetAttrVal(1, i);
					else
						candidateSelection[cIdeal].resetAttrVal(0, i);
				}
				
				candidateSelection[cIdeal].setScore(1.0);				
			}
		}
		catch (IOException e) {
			System.out.println("Exception" + e);
		}
	}
	
	public void initTabs() { //initialize the colored tabs to select a specific set of candidates
		activeTab  = 1; //default active tab
		Random R = new Random();
		Random G = new Random();
		Random B = new Random();


		tabs = new Tab[10];
		int y;
		int x = 200;
		boolean active = false;
		for(int i = 0; i < 10; i++) {
			if(i == 0) {
				active = true;
				y = 50;
			}
			else {
				active = false;
				y = 10;
			
			}
			tabs[i] = new Tab(x,y,R.nextInt(255),G.nextInt(255),B.nextInt(255),active);
			x = x + 80;
		}
			
	}
	
	public void initAttrNames() { // randomly select a set of N attribute names from file
		Random generator = new Random();
		URL urlA = null;

		try 
		{
			urlA = new URL(getCodeBase(),"./data/Attributes.txt");
		}
		catch(MalformedURLException e) {}
		try {
			InputStream is = urlA.openStream();
			//InputStream is = new FileInputStream("data//Attributes.txt");
			BufferedReader input = new BufferedReader(new InputStreamReader(is));
			int offset = generator.nextInt(30) + 1;
			Vector<String> attrName = new Vector<String>();

			int line = 0;
			while (line != offset) {
				input.readLine();
				line++;
			}
			//set attribute names for person
			for(int i = 0; i < N; i++) {
				attrName.add(i,input.readLine());
				person.setAttrName(attrName.get(i),i);
			}
			
			//set attribute names for each candidate
			for(int i = 0; i < 50; i++) {
				for(int k = 0; k < N; k++)
					candidateSelection[i].setAttrName(attrName.get(k),k);
			}
		}
		catch (IOException e) {}
	}

	public void initTimer() { // initialize timer
		frameCount = 0;
		clock = 120;
	}
	
	public void draw() {
		
		if(gameActive) { // game in progress
			if(!gameSetup) { // if initial setup was not completed
				gameOver = false;
				if(timer)
					initTimer();
				initIcons();
				initPerson();
				initCandidate();
				initAttrNames();
				initTabs();
				initGraphPoints();
				initMatchmaker();
				gameSetup = true;
			}
			background(255);
			if(timer) //display timer only if user selected that option
				drawTime();
			drawLayout();//draw graph outline
			drawTabs();//draw colored tabs
		
			drawCandidates();//display each candidate profile - depending on which tab is actibe
			drawPlot();//plot out matchmakers selection on graph
			drawPerson();//draw person profile which displays person name
			drawIcons();//draw icons on game page - NEXT and PREV
			
			drawMatchmaker();//display each matchmakers score
			if(!gameOver) {//if game not over
				if(timer) {//update clock
					frameCount++;
					//clock
					if(frameCount == 45) {
						clock--;
						frameCount = 0;
						if(clock == 0)//game over if we run out of time
							gameOver = true;
					}
				}
				
				int noMore = 0;
				
				//check if no more candidates available for selection
				for(int i = 0; i < 50; i++) {
					if(candidateSelection[i].getSel())
						noMore++;
				}
				
				//game over if we run out of candidates
				if(noMore == 50)
					gameOver = true;
				
				//check if either Matchmaker holds ideal candidate
				for(int i = 0; i < numMatchmakers; i++)
					if(matchmaker[i].getScore() == 1.0)
						gameOver = true;
			}
			
			if(gameOver) {
				fill(0,0,0);
				textSize(16);
				
				if(numMatchmakers == 1) // if single player game display matchmaker score
					text("GAME OVER! YOUR BEST SCORE: " + matchmaker[0].getScore(), 500, 700);
				else { // check who won?
					if(matchmaker[0].getScore() > matchmaker[1].getScore()) {
						text("GAME OVER! MATCHMAKER ONE WINS!!", 500, 700);
					}
					else if(matchmaker[0].getScore() < matchmaker[1].getScore()) {
						text("GAME OVER! MATCHMAKER TWO WINS!!", 500, 700);
					}
					else { //same candidate score - check candidate count
						if(matchmaker[0].getCount() < matchmaker[1].getCount()) {
							text("GAME OVER! MATCHMAKER ONE WINS!!", 500, 700);
						}
						else {
							text("GAME OVER! MATCHMAKER TWO WINS!!", 500, 700);
						}
					}
					
				}
				
				textSize(12);
			}
			else {
				textSize(14);
				for(int i = 0; i < numMatchmakers; i++)
					if(matchmaker[i].isActive()) {
						if(i == 0)
							fill(255,0,0);
						else
							fill(0,0,255);
						text("MATCHMAKER " + (i + 1) + "'s turn", 500, 700);
					}
				textSize(12);
			}
			 
		}
		
		if(menuActive) {
			if(!menuSetup) { // if menu needs to be reset
				initMenuIcon();
				menuSetup = true;
			}
			background(0);
			drawMenu();
		}
		
	}
	
	public void drawMenu() {
		
		fill(255,255,255);
		rect(500,200,200,400);
		
		fill(204,102,153);
		textSize(36);
		text("THE DATING GAME v1.0", 412, 150);
				
		fill(204,102,204);
		textSize(18);
		text("MENU", 575, 220);
		
		fill(0,0,0);
		textSize(12);
		text("SELECT # OF MATCHMAKERS: ", 510, 260);
		
		mOne.draw();
		fill(0, 0, 0);
		text("ONE", 513, 300);
		
		mTwo.draw();
		fill(0, 0, 0);
		text("TWO", 513, 340);

		fill(0,0,0);
		text("SELECT DIFFICULTY LEVEL: ", 510, 380);
		
		easy.draw();
		fill(0, 0, 0);
		text("EASY", 510, 420);
		
		med.draw();
		fill(0, 0, 0);
		text("MED", 605, 420);
		
		hard.draw();
		fill(0, 0, 0);
		text("HARD", 510, 460);
		
		text("TIMER:", 510, 500);
		
		yes.draw();
		fill(0, 0, 0);
		text("YES:", 510, 540);
		
		no.draw();
		fill(0, 0, 0);
		text("NO:", 605, 540);

		text("PRESS 'r' TO START ", 575, 590);
		
		fill(255,204,0);
		textSize(14);
		text("ARCHITECT: Anjali Menon (aam465@nyu.edu)", 32,32);
		textSize(12);
	}
	
	public void drawMatchmaker() {//update score
		for(int i = 0; i < numMatchmakers; i++)
			matchmaker[i].draw(); 
	}
	
	public void drawTime() {
		fill(0,0,0);
		textSize(18);
		text("TIME: " + clock,32,200);
		textSize(12);
	}
	
	public void drawPerson() {
		person.draw();
	}

	public void drawPlot() {
		//find all selected candidates 
		//check which matchmaker claimed them
		//accordingly change color on graph
		double score;
		int y = 28;
		for(int i = 0; i < 50; i++) {
			if(candidateSelection[i].getSel()) {
				if(candidateSelection[i].getClaim() == 1)
					fill(255,0,0);//matchmaker red
				else
					fill(0,0,255);//matchmaker blue
				
				score = candidateSelection[i].getScore();
				score = ((double)((int)(score * 10)))/10;
				
				//compare score with graph point
				for(int k = 0; k < 21; k++) {
					//retrieve score round off to one decimal point
					if(score == graphPoints.get(k)) {
						//plot
						rect(1180,y + 30*k,68,10);
					}				
				}
			}
		}
		
	}
	public void drawLayout() {
		fill(0,0,0);
		text("IDEAL CANDIDATE", 1136, 18);
		text("TROLL", 1200, 668);
		               
		stroke(153);
		line(1248,28,1248,658);
		
		fill(255,255,255);
		rect(200,100,850,560);
		
		if(numMatchmakers < 2) {
			fill(255,0,0);
			textSize(16);
			text("MATCHMAKER ONE",16,260);
			
		}
		else {
			fill(255,0,0);
			textSize(16);
			text("MATCHMAKER ONE",16,260);
			fill(0,0,255);
			text("MATCHMAKER TWO",16,323);
			
		}
		textSize(12);
	}

	
	public void drawIcons() {
		prev.draw();
		textSize(14);
		fill(0,0,0);
		text("PREV",228,698);
		
		next.draw();
		fill(0,0,0);
		text("NEXT",986,698);
		
		text("CONTROLS:",8,564);
		
		textSize(12);
		text("* Press 'r' to return to MENU", 8, 600);
		
		text("* Click candidate profile to select", 8, 618);

		text("* Click colored tabs above", 8, 636);
		text("(OR)", 8, 654);

		text("Click PREV or NEXT to ", 8, 672);
		text("toggle between candidate ", 8, 690);
		text("sets -- >", 8, 708);

	}
	
	public void drawCandidates() {
		for(int i = 0; i < 50; i++)
			if(activeTab == candidateSelection[i].tabID)
				candidateSelection[i].draw();
			
	}
	
	public void drawTabs() {
		for(int i = 0; i < 10; i++) {
			tabs[i].draw();
		}
	}
	
	public void mouseClicked() {
		if(menuActive) { //check which option was selected
			if(mOne.isColliding(mouseX, mouseY)) {
				numMatchmakers = 1;
				mOne.setSel(true);
				mTwo.setSel(false);
				
			}
			
			if(mTwo.isColliding(mouseX, mouseY)) {
				numMatchmakers = 2;
				mTwo.setSel(true);
				mOne.setSel(false);
			}
			
			if(easy.isColliding(mouseX, mouseY)) {
				N = 5;
				easy.setSel(true);
				med.setSel(false);
				hard.setSel(false);

			}
			
			if(med.isColliding(mouseX, mouseY)) {
				N = 10;
				med.setSel(true);
				easy.setSel(false);
				hard.setSel(false);

			}
			
			if(hard.isColliding(mouseX, mouseY)) {
				N = 20;
				hard.setSel(true);
				easy.setSel(false);
				med.setSel(false);
			}
			
			if(yes.isColliding(mouseX, mouseY)) {
				yes.setSel(true);
				no.setSel(false);
				timer = true;
				
			}
			
			if(no.isColliding(mouseX, mouseY)) {
				no.setSel(true);
				yes.setSel(false);
				timer = false;
			}
		}
		
		if(gameActive) { //check which tab/toggle icon (next/prev) was selected
			
			if(next.isColliding(mouseX, mouseY) && activeTab != 10) {
				tabs[(activeTab - 1) + 1].setActive();
				tabs[activeTab - 1].reset();
				activeTab = activeTab + 1;
				//System.out.println("next: active tab" + activeTab);
			}
			
			if(prev.isColliding(mouseX, mouseY) && activeTab != 1) {
				tabs[(activeTab - 1) - 1].setActive();
				tabs[activeTab - 1].reset();
				activeTab = activeTab - 1;
				//System.out.println("prev: active tab" + activeTab);

			}
			
			for(int i = 0; i < 10; i++) //toggle by colored tabs
					if(tabs[i].isColliding(mouseX,mouseY) && !tabs[i].isActive()) {	
					tabs[i].setActive();
					tabs[activeTab - 1].reset();
					activeTab = i + 1;
				}
		
			if(!gameOver) { // if game not over matchmaker may select candidate
				for(int i = 0; i < 5; i++)
					for(int k = 0; k < 50; k++)
						if(candidateSelection[k].tabID == activeTab) {
							if(candidateSelection[k].isColliding(mouseX,mouseY) && !candidateSelection[k].getSel()) {
						
								//retrieve score
								double score = 0;
								score  = candidateSelection[k].getScore();
								candidateSelection[k].setSel();
						
								//is this the best score for the matchmaker
								//loop through matchmakers to find the active matchmaker 
								//update best score and candidate count
								for(int m = 0; m < numMatchmakers; m++) {
									if(matchmaker[m].isActive()) {
										matchmaker[m].setCandidateCount();
										if(score > matchmaker[m].getScore())
											matchmaker[m].setScore(score);
										
										//make inactive and make next matchmaker active
										if(numMatchmakers > 1)
											matchmaker[m].setActive(false);
										candidateSelection[k].setClaim(m + 1);
								
									}
									else
										matchmaker[m].setActive(true);
								}
							}
						}
			}
		}
	}	
	
	public void keyPressed() {
		//to switch between menu and game
		  if (key == 'r' && menuActive) {
		    gameActive = true;
		    menuActive = false;
		    menuSetup = false;
		  }
		  
		  else if (key == 'r' && gameActive) {
			  gameActive = false;
			  menuActive = true;
			  gameSetup = false;
		  }
	}

}
