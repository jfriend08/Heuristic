package ui;

import Communication.Connector;
import Game.Game;
import io.dropwizard.Application;
import io.dropwizard.assets.AssetsBundle;
import io.dropwizard.logging.AppenderFactory;
import io.dropwizard.logging.FileAppenderFactory;
import io.dropwizard.setup.Bootstrap;
import io.dropwizard.setup.Environment;
import org.apache.log4j.Level;
import org.apache.log4j.LogManager;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Method;
import java.net.ServerSocket;
import java.net.Socket;

public class UIApplication extends Application<UIConfiguration> {

    @Override
    public void initialize(Bootstrap<UIConfiguration> myConfigurationBootstrap) {
        myConfigurationBootstrap.addBundle(new AssetsBundle("/assets", "/assets", "index.html", "config.yaml"));

    }

    @Override
    public void run(UIConfiguration uiConfiguration, Environment environment) throws Exception {
        final GameResource resource = new GameResource();
        environment.jersey().register(resource);
    }

    public static void main(String[] args) throws Exception {


        Game game = Game.getInstance();
        //Inputs must be done through environment variables because dropwizard is expecting blank args.
        Integer numberOfMoves = Integer.valueOf(System.getProperty("numberOfMoves"));
        game.createBoard(new File(System.getProperty("inputFile")));
        long slowDown = 0;
        if (System.getProperties().containsKey("slowDown")) {
            slowDown = Long.valueOf(System.getProperty("slowDown"));

            UIApplication uiApplication = new UIApplication();
            LogManager.getRootLogger().setLevel(Level.OFF);
            uiApplication.run(args);

            try {
                ServerSocket serverSocket = new ServerSocket(1377);
                Socket player1Socket = serverSocket.accept();
                Runnable connectionHandler = new Connector(player1Socket, 1, numberOfMoves, slowDown);
                new Thread(connectionHandler).start();

                Socket player2Socket = serverSocket.accept();
                Runnable connectionHandler2 = new Connector(player2Socket, 2, numberOfMoves, slowDown);
                new Thread(connectionHandler2).start();

            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}