package Game;

import java.util.List;

/**
 * Created by islam on 11/1/15.
 */
public class Piece {
    private PlayerId playerId;
    private Node location;
    private List<Direction> program;
    private int moveCount;
    private boolean isDead;
    private int nodesEaten;

    public Piece(PlayerId playerId){
        this.playerId = playerId;
    }


    public void programPiece(List<Direction> moveOrder){
        if(isValidProgram(moveOrder)){
            program = moveOrder;
        }
    }

    private boolean isValidProgram(List<Direction> moveOrder){
        if(moveOrder == null){
            return false;
        }

        //Should have 4 moves
        if(moveOrder.size() != 4){
            return false;
        }

        //Should have each move type
        return moveOrder.contains(Direction.UP) && moveOrder.contains(Direction.DOWN) &&
                moveOrder.contains(Direction.LEFT) && moveOrder.contains(Direction.RIGHT);
    }

    public void advance(){
        if(isDead == false) {
            final int numberOfDirection = 4;

            if (location != null && isValidProgram(program)) {
                //Search for valid move
                for (int i = moveCount; i < moveCount + numberOfDirection; i++) {
                    Direction nextMove = program.get((moveCount + i) % numberOfDirection);

                    if (location.canMove(nextMove)) {
                        location.move(nextMove);
                        moveCount++;
                        return;
                    }
                }

                //If no valid move available then the piece is dead
                isDead = true;
            }
        }
    }

    public void placeOnNode(Node node){
        this.location = node;
        nodesEaten++;
    }

    public PlayerId getPlayerId(){
        return this.playerId;
    }

    public int getNodesEaten(){
        return this.nodesEaten;
    }

    public boolean isDead(){
        return this.isDead;
    }

    public Direction getPreviousDirection(){
        if(moveCount > 0 ){
            return program.get((moveCount - 1) % 4);
        }else{
            return null;
        }

    }

    public void killPiece(){
        this.isDead = true;
    }

    public boolean isNewPiece(){
        //System.out.println(moveCount);
        return moveCount == 0;
    }

}
