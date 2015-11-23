package datinggamefinalfinal;

import java.util.*;
import processing.core.PApplet;

public class Candidate extends Rectangle{
	
	public Vector<Integer> attrValue = new Vector<Integer>();
	private Vector<String> attrName = new Vector<String>();
	private int x;
	private int y;
	public int tabID; // page ID
	private int claim; //ID of matchmaker that claimed this candidate
	private String name; // candidate name
	private boolean selected = false;
	public static PApplet pApplet;
	private double score;
	
	public Candidate(int x, int y, int tabID, String name) { //size - width and height
		super(x,y,150,480);
		this.x = x;
		this.y = y;
		this.tabID = tabID;
		this.name = name;
		claim = 0; // no one has selected this candidate
	}
	
	public void setAttrVal(int attrValue, int index) {
		this.attrValue.add(index, attrValue);
	}
	
	public void resetAttrVal(int attrValue, int index) {
		this.attrValue.set(index, attrValue);
	}
	
	public void setAttrName(String attrName, int index) {
		this.attrName.add(index, attrName);
	}
	
	public boolean isColliding(int mx, int my) {
		boolean collision = false;
		if(mx >= x && mx <= x + 150 && my >= y && my <= y + 480)
			collision = true;
		else
			collision = false;
		
		return collision;
	}
	
	public void setSel() {
		selected = true;
	}
	
	public void setClaim(int claim) {
		this.claim = claim;
	}
	
	public boolean getSel() {
		return selected;
	}
	
	public void setScore(double score) {
		this.score = score;
	}
	
	public double getScore() {
		return score;
	}
	
	public String getName() {
		return name;
	}
	
	public double getClaim() {
		return claim;
	}
	public void draw() {
		pApplet.fill(255,255,255);
		super.draw();
		pApplet.fill(0,0,0);
		int tmpY = y + 64;
		pApplet.text("" + name, x + 8, y + 32);
		for(int i = 0; i < attrValue.size(); i++) { 
			pApplet.text("" + attrName.get(i), x + 8, tmpY);
			pApplet.text("" + attrValue.get(i), x + 135, tmpY);
			tmpY += 20;
		}
		
		if(selected) { //also display score
			if(claim == 1)
				pApplet.fill(255,0,0);
			else if(claim == 2)
				pApplet.fill(0,0,255);
			pApplet.rect(x + 125, y + 460, 16, 16);
			pApplet.text("SCORE: " + score, x + 8, y + 465);

		}
		else {
			pApplet.fill(255,255,255);
			pApplet.rect(x + 125, y + 460, 16, 16);
		}
		
	}
}
	
