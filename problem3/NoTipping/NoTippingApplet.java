// NoTippingApplet
//
// version 1.0
// location: \java\notipping\
//
// Tyler Neylon, 2002
//

import java.applet.*;
import java.lang.*;
import java.awt.*;
import java.awt.image.*;
import java.awt.event.*;
import java.util.Vector;

public class NoTippingApplet
        extends Applet {

    public void init() {
    }

	public void start() {
		new NoTippingFrame();
	}
}

class NoTippingFrame extends Frame {
	public NoTippingFrame() {
		setLayout(new BorderLayout());
		NoTippingComponent main_display = new NoTippingComponent();
		add(main_display, "Center");
		Container toolbar = new Panel();
		GridBagLayout gbl = new GridBagLayout();
		GridBagConstraints gbc = new GridBagConstraints();
		toolbar.setLayout(gbl);
		gbc.fill = GridBagConstraints.BOTH;
		gbc.weightx = 1.0;

		Button b = new Button("Restart");
		b.setActionCommand("Restart");
		b.addActionListener(main_display);
		gbl.setConstraints(b, gbc);
		toolbar.add(b);

		b = new Button("Undo");
		b.setActionCommand("Undo");
		b.addActionListener(main_display);
		gbl.setConstraints(b, gbc);
		toolbar.add(b);

		/*
		b = new Button("Forward");
		b.setActionCommand("Forward");
		b.addActionListener(main_display);
		gbl.setConstraints(b, gbc);
		toolbar.add(b);
		*/

		TextField tf = new TextField();
		//tf.setActionCommand("Hi");
		tf.addActionListener(main_display);
		gbl.setConstraints(tf, gbc);
		toolbar.add(tf);

		b = new Button("Help");
		b.setActionCommand("Help");
		b.addActionListener(main_display);
		gbl.setConstraints(b, gbc);
		toolbar.add(b);

		/*
		b = new Button("Options");
		gbl.setConstraints(b, gbc);
		toolbar.add(b);
		*/

		addWindowListener(new WindowCloser());

		add(toolbar, "North");
		setTitle("The No Tipping Game");
		pack();
		setVisible(true);
		setEnabled(true);
	}
}

class WindowCloser extends WindowAdapter {
	public void windowClosing(WindowEvent e) {
		System.out.println("windowClosing(WindowEvent)");
		e.getWindow().dispose();
	}
}

