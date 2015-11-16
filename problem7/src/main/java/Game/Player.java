package Game;

import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

/**
 * Created by islam on 11/1/15.
 */
public class Player {

    private PlayerId playerId;
    private LinkedList<Piece> unused;
    private List<Piece> inPlay = new LinkedList<Piece>();
    private List<Piece> dead = new LinkedList<Piece>();
    private String playerName;
    private String nextMove;


    public Player(PlayerId playerId, int pieces, String playerName){
        this.playerId = playerId;
        this.playerName = playerName;

        this.unused = new LinkedList<Piece>();
        for(int i = 0; i < pieces; i++){
            Piece piece = new Piece(playerId);
            this.unused.add(piece);
        }
    }

    public void advanceTime(){
        //For all inplay pieces move them
        for(Piece piece: inPlay){
            piece.advance();
        }
        //If any of the pieces become dead then remove from the inplay
        Iterator<Piece> iterator = inPlay.iterator();
        while (iterator.hasNext()){
            Piece piece = iterator.next();
            if(piece.isDead()){
                iterator.remove();
                dead.add(piece);
            }
        }
    }

    /**
     * Used to make the initial move for a an unused piece, requires the node and the program for the piece
     */
    public boolean place(Node node, List<Direction> program){
        if(node.isFree() && unused.size() > 0){
            Piece nextPiece = unused.pop();
            nextPiece.programPiece(program);
            nextPiece.placeOnNode(node);
            node.place(nextPiece);
            inPlay.add(nextPiece);
            return true;
        }else {
            return false;
        }
    }

    public String getPlayerName(){
        return this.playerName;
    }

    public void setNextMove(String nextMove){
        this.nextMove = nextMove;
    }

    public String getNextMove(){
        return this.nextMove;
    }

    public String toString(){
        clearDead();

        return null;
    }

    private void clearDead(){
        Iterator<Piece> iterator = this.inPlay.iterator();
        while (iterator.hasNext()){
            Piece piece = iterator.next();
            if(piece.isDead()){
                iterator.remove();
                this.dead.add(piece);
            }
        }
    }

    public String getPlayerId(){
        return this.playerId.name();
    }

    public int unusedCount(){
        return this.unused.size();
    }

    public int deadCount(){
        return dead.size();
    }

    public int inPlayCount(){
        return inPlay.size();
    }

    public int getScore(){
        int score  = 0;
        for(Piece piece: this.inPlay){
            score = score + piece.getNodesEaten();
        }

        for(Piece piece: this.dead){
            score = score + piece.getNodesEaten();
        }
        return score;
    }
}
