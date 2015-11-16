package Communication;

import Game.Game;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.LinkedList;

/**
 * Created by islam on 11/1/15.
 */
public class Connector implements Runnable{
    private Socket clientSocket;
    private int playerId;
    private Game game = Game.getInstance();
    private int numOfMoves;
    private long slowDown;

    public Connector(Socket clientSocket, int playerId, int numOfMoves, long slowDown){
        this.playerId = playerId;
        this.clientSocket = clientSocket;
        this.numOfMoves = numOfMoves;
        this.slowDown = slowDown;
    }

    public void run() {
        try{
            PrintWriter out =  new PrintWriter(clientSocket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            String inputLine;
            LinkedList<String> commands = new LinkedList<String>();
            while ((inputLine = in.readLine()) != null) {
                Thread.sleep(slowDown);
                if(inputLine.contains("REGISTER:")){
                    String commandString = "START\n" + registerPlayer(inputLine) + "\nEND";
                    out.println(commandString);
                }else{
                    commands.add(inputLine);
                }

                if(game.readyForMove(playerId)){
                    if(commands.size() > 0){
                        game.receiveMoves(playerId,commands.pop());
                        out.println("START\n" + poll() + "\nEND");
                    }else{
                        out.println("START\nWAITING\nEND");
                    }
                }
            }
        }catch (IOException e){
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private String registerPlayer(String inputLine){
        String teamName = inputLine.replaceAll("REGISTER:", "");
        return game.registerPlayer(playerId,teamName,numOfMoves);
    }

    private String poll(){
        while(true){
            LinkedList<String> messages = game.getMessages(playerId);
            if(messages.size() > 0){
                for(String message: messages){
                    return message;
                }
            }
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}