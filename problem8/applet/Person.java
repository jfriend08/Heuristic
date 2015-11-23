package datinggamefinalfinal;

import java.util.*;
import processing.core.PApplet;

public class Person extends Rectangle{
	
	public Vector<Double> attrValue = new Vector<Double>();
	private Vector<String> attrName = new Vector<String>();
	private int x;
	private int y;
	public static PApplet pApplet;
	private String name;
	
	public Person(int x, int y) { //size - width and height
		super(x,y,150,150);
		this.x = x;
		this.y = y;
	}
	public void setName(String name) {
		this.name = name;
	}
	
	public void setAttrVal(double attrValue, int index) {
		this.attrValue.add(index, attrValue);
	}
	
	public void setAttrName(String attrName, int index) {
		this.attrName.add(index, attrName);
	}
	
	public void randomize() {
		Collections.shuffle(attrValue);
	}

	public void draw() {
		pApplet.fill(255,255,255);
		super.draw();
		pApplet.fill(0,0,0);
		pApplet.text("PERSON PROFILE", x + 16, y + 16);
		pApplet.text("NAME: " + name, x + 8,y + 48);
	}
	
}