package datinggamefinalfinal;

import processing.core.PApplet;

public class Matchmaker {
	
	private double bestScore;
	private double candidateCount;
	private double bestCount;
	private boolean active;
	public static PApplet pApplet;
	private int x;
	private int y;
	
	public Matchmaker(int x, int y, boolean active) { //size - width and height
		this.active = active;
		this.x = x;
		this.y = y;
		bestScore = -1.0;
		candidateCount = 0;
		bestCount = 0;
	}
	
	public double getScore() {
		return bestScore;
	}
	
	public double getCount() {
		return bestCount;
	}
	
	public void setScore(double bestScore) {
		this.bestScore = bestScore;
		bestCount = candidateCount;
	}
	
	public void setCandidateCount() {
		candidateCount++;
	}
	
	public boolean isActive() {
		return active;
	}
	
	public void setActive(boolean active) {
		this.active = active;
	}

	public void draw() { //to write out scores
		pApplet.fill(0,0,0);
		pApplet.textSize(16);
		pApplet.text("SCORE: " + bestScore + "," + bestCount,x,y);
		pApplet.textSize(12);

	}
	
}