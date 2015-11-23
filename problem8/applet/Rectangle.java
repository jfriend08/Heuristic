package datinggamefinalfinal;

import processing.core.PApplet;

public class Rectangle {

	public int x;
	public int y;
	public int width;
	public int height;
	
	public static PApplet pApplet;//static - pApplet will 
								  //be shared by all instances 
								  //of this class
	
	
	public Rectangle(int x, int y, int width, int height) { //size - width and height
		super();
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
	}

	public void draw() {
		pApplet.rect(x, y, width, height);
	}
	
}