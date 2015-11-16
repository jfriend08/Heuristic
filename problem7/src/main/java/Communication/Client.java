package Communication;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Random;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by islam on 11/1/15.
 */
public class Client {

    private static StringBuffer command = new StringBuffer();

    public static void main(String[] args) {

        try {
            Socket socket = new Socket("localhost", 1377);
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String state;
            out.println("REGISTER:" + args[0]);
            while ((state = in.readLine()) != null) {
                if(state.equals("START")){
                    command = new StringBuffer();
                }
                else if(state.equals("END")){
                    out.println(process(command.toString()));
                }else{
                    command.append(state + "\n");
                }
            }
        } catch (IOException eIO) {
            System.out.println("ERROR");
            System.out.println(eIO.getMessage());
        }
    }

    private static String process(String command){
        // System.out.println(command);
        parse(command);
        Random random = new Random();
        String myR = random.nextInt(100) + ",UP,DOWN,LEFT,RIGHT";
        System.out.println("my command: " + myR);
        return myR;
    }

    public static void parse(String command) {
        // System.out.println("yoyo" + command + "yaya");
        String lines[] = command.split("\\r?\\n");
        ArrayList<String[]> boardList = new ArrayList<String[]>();
        ArrayList<String[]> playerList = new ArrayList<String[]>();
        Boolean firstMeedPlayerList = true;

        for (int i=1; i<lines.length; i++){
            String lineElms[] = lines[i].split(",");
            System.out.println(i + " length: " + lineElms.length);
            if( lineElms==null || lineElms.length == 1) {
                continue;
            } else if ( (lineElms==null || lineElms.length == 6)) {
                if (firstMeedPlayerList) {
                    firstMeedPlayerList = false;
                    continue;
                }
                playerList.add(lineElms);
            } else if ( (lineElms==null || lineElms.length == 8)) {
                boardList.add(lineElms);
            } else {
                continue;
            }
        }

        int [] nodeCountArray = new int[boardList.size()];
        System.out.println( Arrays.toString(nodeCountArray));
        for (int i=0; i<boardList.size(); i++){
            System.out.println( "boardList.get(i)[3] " + boardList.get(i)[3] );
            if (boardList.get(i)[3].matches("FREE")) {
                System.out.println("Hi FREE");
                for (int j=4; j<boardList.get(i).length; j++) {
                    if (!boardList.get(i)[j].equals("null")){
                        System.out.println("Hi not null");
                        nodeCountArray[i]++;
                    }
                }
            }
            // System.out.println( i+"th in boardList: " + Arrays.toString(boardList.get(i)) );
        }
        for(int i=0; i<boardList.size(); i++) {
            System.out.println( "Node " +i + " Counts:"+ nodeCountArray[i]);
            System.out.println( i+"th in boardList: " + Arrays.toString(boardList.get(i)) );
        }
        for (int i=0; i<playerList.size(); i++){
            System.out.println( i+"th in playerList: " + Arrays.toString(playerList.get(i)) );
        }
    }
}





