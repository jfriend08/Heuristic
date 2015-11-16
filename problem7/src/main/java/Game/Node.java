package Game;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import java.util.LinkedList;
import java.util.List;

/**
 * Created by islam on 11/1/15.
 */
public class Node {
    public int id;
    private int xLoc;
    private int yLoc;
    private Status status;

    @JsonIgnore
    public Node up;
    @JsonIgnore
    public Node down;
    @JsonIgnore
    public Node left;
    @JsonIgnore
    public Node right;

    private Piece occupant;
    private List<Piece> desireOccupancy = new LinkedList<Piece>();


    public Node(int id, int xLoc, int yLoc){
        this.id = id;
        this.xLoc = xLoc;
        this.yLoc = yLoc;
        status = Status.FREE;
    }

    public int getId(){
        return this.id;
    }

    public String toString(){
        String up = nullCheck(this.up);
        String down = nullCheck(this.down);
        String left = nullCheck(this.left);
        String right= nullCheck(this.right);

        return id + "," + xLoc + "," + yLoc + "," + status + "," + up + "," + down + "," + left + "," + right;
    }

    public String nullCheck(Node node){
        if(node == null){
            return "null";
        }else {
            return String.valueOf(node.getId());
        }
    }

    public boolean canMove(Direction direction){

        switch (direction){
            case UP:
                if(up == null){
                    return false;
                }else{
                    return up.isFree();
                }
            case DOWN:
                if(down == null){
                    return false;
                }else{
                    return down.isFree();
                }
            case LEFT:
                if(left == null){
                    return false;
                }else{
                    return left.isFree();
                }
            case RIGHT:
                if(right == null){
                    return false;
                }else{
                    return right.isFree();
                }
            default:return false;
        }
    }

    public void connect(Node node, Direction direction){
        switch (direction){
            case UP:
                up = node;
            case DOWN:
                down = node;
            case LEFT:
                left = node;
            case RIGHT:
                right = node;

        }
    }

    public boolean isFree(){
        return status.equals(Status.FREE);
    }

    public void move(Direction direction){
            switch (direction){
                case UP:
                    up.place(this.occupant);
                    this.occupant.placeOnNode(up);
                    break;
                case DOWN:
                    down.place(this.occupant);
                    this.occupant.placeOnNode(down);
                    break;
                case LEFT:
                    left.place(this.occupant);
                    this.occupant.placeOnNode(left);
                    break;
                case RIGHT:
                    right.place(this.occupant);
                    this.occupant.placeOnNode(right);
                    break;
            }
    }

    public void place(Piece piece){
        this.desireOccupancy.add(piece);
    }

    /**
     * After all pieces have moved onto thier desired node decide which ones to keep and which ones to eject
     */
    public void moveTime(PlayerId playerWithPriority){
        //First check if the node is currently occupied. If so then move the occupant along
        if(this.occupant != null){
            if(this.occupant.getPlayerId().equals(PlayerId.ONE)){
                this.status = Status.EATEN_P1;
            }else{
                this.status = Status.EATEN_P2;
            }
        }

        boolean occuopantSelected = false;
        List<Piece> newPieces = new LinkedList<Piece>();

        for(Piece piece: desireOccupancy){

            if(piece.getPreviousDirection() != null){
                //First order is piece that moved up to get here
                if(piece.getPreviousDirection().equals(Direction.UP)){
                    occupy(piece);
                    occuopantSelected = true;
                }

                //Second is piece that moved left
                if(piece.getPreviousDirection().equals(Direction.LEFT)){
                    if(occuopantSelected){
                        piece.killPiece();
                    }else{
                        occupy(piece);
                        occuopantSelected = true;
                    }
                }

                //Third is a piece that moved down
                if(piece.getPreviousDirection().equals(Direction.DOWN)){
                    if(occuopantSelected){
                        piece.killPiece();
                    }else{
                        occupy(piece);
                        occuopantSelected = true;
                    }
                }

                //Fourth is a piece that moved right
                if(piece.getPreviousDirection().equals(Direction.RIGHT)){
                    if(occuopantSelected){
                        piece.killPiece();
                    }else{
                        occupy(piece);
                        occuopantSelected = true;
                    }
                }
            }

            //Fifth is a new piece
            if(piece.isNewPiece()){
                newPieces.add(piece);
            }
        }

        for(Piece piece: newPieces){
            if(occuopantSelected ||(newPieces.size() > 1 && piece.getPlayerId() != playerWithPriority)){
                piece.killPiece();
            }else{
                occupy(piece);

                occuopantSelected = true;
            }
        }

        desireOccupancy.clear();

    }

    public int getxLoc(){
        return this.xLoc;
    }

    public int getyLoc(){
        return this.yLoc;
    }

    /**
     * Used to connect two nodes. Calculates if the given node is up, down, left, or right of the current node.
     * Returns the direction.
     * @param node
     * @return
     */
    public Direction connect(Node node){

        //If same x then node is above or below
        if(node.getxLoc() == this.xLoc){
            if(node.getyLoc() > this.yLoc){
                this.up = node;
                System.out.println("UP: current:" + this.yLoc + " above: " + node.getyLoc());
                return Direction.UP;
            }else{
                this.down = node;
                System.out.println("DOWN: current:" + this.yLoc + " below: " + node.getyLoc());
                return Direction.DOWN;

            }
        }else{
            //If same Y then node is left or right
            if(node.getxLoc() > this.xLoc){
                this.right = node;
                System.out.println("Right: current:" + this.xLoc + " right: " + node.getxLoc());
                return Direction.RIGHT;
            }else{
                this.left = node;
                System.out.println("Left: current:" + this.xLoc + " left: " + node.getxLoc());
                return Direction.LEFT;
            }
        }
    }

    private void occupy(Piece piece){
        this.occupant = piece;
        if(piece.getPlayerId() == PlayerId.ONE){
            this.status = Status.OCCUPIED_P1;
        }else{
            this.status = Status.OCCUPIED_P2;
        }
    }

    public Status getStatus(){
        return this.status;
    }


}
