package datinggamefinalfinal;

import processing.core.PApplet;

public class Icon extends Rectangle {
	
	private int R;
	private int G;
	private int B;
	public static PApplet pApplet;//static - pApplet will 
								  //be shared by all instances 
								  //of this class
	
	
	public Icon(int x, int y, int width, int height, int R, int G, int B) { //size - width and height
		super(x,y,width,height);
		this.R = R;
		this.G = G;
		this.B = B;
	}
	
	public boolean isColliding(int mx, int my) {
		boolean collision = false;
		if(mx >= x && mx <= x + width && my >= y && my <= y + height) {
			collision = true;
		}
		else {
			collision = false;
		}
		
		return collision;
	}
	
	public void draw() {
		pApplet.fill(R,G,B);
		super.draw();
	}
	
}