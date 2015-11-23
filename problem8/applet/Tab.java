package datinggamefinalfinal;

import processing.core.PApplet;

public class Tab extends Rectangle {
	
	private int R;
	private int G;
	private int B;
	private boolean active;
	public static PApplet pApplet;//static - pApplet will 
								  //be shared by all instances 
								  //of this class
	
	
	public Tab(int x, int y, int R, int G, int B, boolean active) { //size - width and height
		super(x,y,50,75);
		this.R = R;
		this.G = G;
		this.B = B;
		this.active = active;
	}
	
	public void setActive() {
		y = 50;
		active = true;
	}
	
	public void reset() {
		y = 10;
		active = false;
	}
	
	public boolean isActive() {
		return active;
	}
	
	public boolean isColliding(int mx, int my) {
		boolean collision = false;
		if(mx >= x && mx <= x + 50 && my >= y && my <= y + 75)
			collision = true;
		else
			collision = false;
		
		return collision;
	}

	public void draw() {
		pApplet.fill(R,G,B);
		super.draw();
	}
	
}