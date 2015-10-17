import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.StringTokenizer;

/**
 * Created by ylc265 on 9/23/15.
 */
public class AIContestant extends NoTippingPlayer{
    private Random strategy;
    private int player;
    private List<Integer> weights;
    private List<Weight> weights_on_board;
    private int[] board;
    private boolean firstRemove;

    AIContestant(int port) {
        super(port);
    }

    protected String process(String command) {
        if (strategy == null) {
            // initialize
            strategy = new Random();
            // assume player is 2 (0,1) for (player1, player2) respectively
            this.player = 1;
            weights = new ArrayList<Integer>();
            for (int i = 1; i <= 15; i ++) {
                weights.add(i);
            }

            weights_on_board = new ArrayList<Weight>();
            // put the original 3 kg block on board
            weights_on_board.add(new Weight(3, -4, 1));
            board = new int[50];
            board[-4+25] = 3;
            firstRemove = false;
        }
        StringTokenizer tk = new StringTokenizer(command);

        // get the command, and opponent's position and weight last round.
        command = tk.nextToken();
        System.out.println(command);
        int position = Integer.parseInt(tk.nextToken());
        int weight = Integer.parseInt(tk.nextToken());
        System.out.println(position);
        System.out.println(weight);

        // in the beginning of game, whoever gets 0, 0 for position and weight is
        // player 1
        if (position == 0 && weight == 0) {
            this.player = 0;
            firstRemove = true;
        } else {
            // execute previous player's move
            if (command.equals("ADDING")) {
                weights_on_board.add(new Weight(weight, position, (player+1)%2));
                board[position+25] = weight;
            } else {
                // The last user add will end up with the following message
                // REMOVING position weight
                // we must add the position and weight as player 1 before removing.
                if (weights_on_board.size() == 30 && firstRemove) {
                    weights_on_board.add(new Weight(weight, position, (player + 1) % 2));
                    firstRemove = false;
                } else {
                    removeWeight(weights_on_board, position, weight);
                }
            }
        }

        // make the moves
        Weight decision;
        if (command.equals("ADDING")) {
            decision = makeAddMove(weights, board, weights_on_board);
            // update board
            weights_on_board.add(decision);
        } else {
            decision = makeRemoveMove(weights_on_board);
            // update board
            weights_on_board.remove(decision);
        }
        return decision.position + " " + decision.weight;
    }

    public Weight makeAddMove(List<Integer> weights, int[] board, List<Weight> weights_on_board) {
        int index = strategy.nextInt(weights.size());
        int candidate = weights.get(index);
        for (int pos = -25; pos < 25; pos ++) {
            // see if position is taken
            if (board[pos+25] == 0) {
                if (validAddMove(candidate, pos, weights_on_board)) {
                    weights.remove(index);
                    board[pos+25] = candidate;
                    return new Weight(candidate, pos, player);
                }
            }
        }
        // basically we lost
        // below is a dummy.
        Weight returnLosingMove = new Weight(candidate, 1, player);
        for (int pos = -25; pos <= 25; pos ++) {
            if (board[pos+25] == 0) {
                board[pos+25] = candidate;
                returnLosingMove = new Weight(candidate, pos, player);
                break;
            }
        }
        return returnLosingMove;
    }

    private boolean validAddMove(int weight, int position, List<Weight> weights_on_board) {
        List<Weight> temp = new ArrayList<Weight>();
        for (Weight w: weights_on_board) {
            temp.add(w);
        }
        temp.add(new Weight(weight, position, player));
        return verifyGameNotOver(temp);
    }

    public Weight makeRemoveMove(List<Weight> weights_on_board) {
        List<Weight> random_candidate = new ArrayList<Weight>();
        List<Weight> remove_candidate = new ArrayList<Weight>();
        // player 1 can remove anything
        if (player == 0) {
            remove_candidate = weights_on_board;
        } else {
            // player 2 can only remove his/her own piece unless there are none
            remove_candidate = getMyBlocks(weights_on_board, player);
            if (remove_candidate.size() == 0){
                // no more player 2 blocks
                remove_candidate = weights_on_board;
            }
        }
        for (Weight w: remove_candidate) {
            if (canRemove(w, weights_on_board)) {
                random_candidate.add(w);
            }
        }
        // if we can do something
        if (random_candidate.size() != 0) {
            int index = strategy.nextInt(random_candidate.size());
            return random_candidate.get(index);
        } else {
            // we lost so just choose something random
            int index = strategy.nextInt(remove_candidate.size());
            return remove_candidate.get(index);
        }
    }

    private boolean canRemove(Weight weight, List<Weight> weights_on_board) {
        List<Weight> temp = new ArrayList<Weight>();
        for (Weight w: weights_on_board) {
            temp.add(w);
        }
        temp.remove(weight);
        return verifyGameNotOver(temp);
    }

    private List<Weight> getMyBlocks(List<Weight> weights_on_board, int player) {
        List<Weight> returnBlock = new ArrayList<Weight>();
        for (Weight w: weights_on_board) {
            if (w.player == player) {
                returnBlock.add(w);
            }
        }
        return returnBlock;
    }

    private void removeWeight(List<Weight> weights_on_board, int pos, int weight) {
        Weight retW = new Weight(0, 0, 0);
        for (Weight w : weights_on_board) {
            if (w.position == pos && w.weight == weight) {
               retW = w;
            }
        }
        weights_on_board.remove(retW);
    }

    private boolean verifyGameNotOver(List<Weight> weights_on_board) {
        int left_torque = 0;
        int right_torque = 0;
        for (Weight weight: weights_on_board) {
            left_torque -= (weight.position - (-3)) * weight.weight;
            right_torque -= (weight.position - (-1)) * weight.weight;
        }
        boolean gameOver = (left_torque > 0 || right_torque < 0);
        return !gameOver;
    }

    public static void main(String[] args) throws Exception {
        new AIContestant(Integer.parseInt(args[0]));
    }

    public class Weight {
        public int weight;
        public int position;
        public int player;
        public Weight(int weight, int position, int player) {
            this.weight = weight;
            this.position = position;
            this.player = player;
        }
    }

}
