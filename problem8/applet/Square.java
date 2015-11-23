package datinggamefinalfinal;

import processing.core.PApplet;

public class Square {

	public int x;
	public int y;
	public int size;
	
	public static PApplet pApplet;//static - pApplet will 
								  //be shared by all instances 
								  //of this class
	
	
	public Square(int x, int y, int size) { //size - width and height
		super();
		this.x = x;
		this.y = y;
		this.size = size;
	}

	public void draw() {
		pApplet.rect(x, y, size, size);
	}
	
}