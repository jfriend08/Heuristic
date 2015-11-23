package datinggamefinalfinal;

import processing.core.PApplet;

public class menuIcon extends Square {
	
	private int R;
	private int G;
	private int B;
	private boolean selected;
	public static PApplet pApplet;//static - pApplet will 
								  //be shared by all instances 
								  //of this class
	
	
	public menuIcon(int x, int y, int size, int R, int G, int B) { //size - width and height
		super(x,y,size);
		this.R = R;
		this.G = G;
		this.B = B;
		selected = false;
	}
	
	public boolean isColliding(int mx, int my) {
		boolean collision = false;
		if(mx >= x && mx <= x + 32 && my >= y && my <= y + 32) {
			collision = true;
		}
		else {
			collision = false;
		}
		
		return collision;
	}
	
	public void setSel(boolean selected) {
		this.selected = selected;
	}

	public void draw() {
		if(!selected)
			pApplet.fill(R,G,B);
		else
			pApplet.fill(0,0,0);
		super.draw();
	}
	
}