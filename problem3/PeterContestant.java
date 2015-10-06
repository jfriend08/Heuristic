import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.StringTokenizer;
import java.util.Arrays;



public class PeterContestant extends NoTippingPlayer{
    private Random strategy;
    private int player;
    private List<Integer> weights;
    private List<Integer> hisWeights;
    private List<Weight> weights_on_board;
    private int[] board;
    private boolean firstRemove;
    private AddStrategy addStrategy;

    PeterContestant(int port) {
        super(port);
    }

    protected String process(String command) {
        if (strategy == null) {
            // initialize
            strategy = new Random();
            addStrategy = new AddStrategy();
            // assume player is 2 (0,1) for (player1, player2) respectively
            this.player = 1;
            weights = new ArrayList<Integer>();
            for (int i = 1; i <= 15; i ++) {
                weights.add(i);
            }

            weights_on_board = new ArrayList<Weight>();
            // put the original 3 kg block on board
            weights_on_board.add(new Weight(3, -4, 1));
            board = new int[52];
            board[-4+25] = 3;
            firstRemove = false;
        }
        StringTokenizer tk = new StringTokenizer(command);

        // get the command, and opponent's position and weight last round.
        command = tk.nextToken();
        int position = Integer.parseInt(tk.nextToken());
        int weight = Integer.parseInt(tk.nextToken());

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
                    weights_on_board.add(new Weight(weight, position, (player+1)%2));
                    firstRemove = false;
                } else {
                    removeWeight(weights_on_board, position, weight);
                }
            }
        }

        // make the moves
        Weight decision;
        if (command.equals("ADDING")) {
            // //original
            // decision = makeAddMove(weights, board, weights_on_board);
            String addMove = addStrategy.process(position, weight);
            tk = new StringTokenizer(addMove);
            int addPosition = Integer.parseInt(tk.nextToken());
            int addWeight = Integer.parseInt(tk.nextToken());
            decision = new Weight(addWeight, addPosition, player);

            // update board
            weights_on_board.add(decision);
        } else {
            // decision = makeRemoveMove(weights_on_board);

            System.out.printf("Before weights_on_board.size(): %s\n", weights_on_board.size());
            List<Weight> testWeights_on_board = new ArrayList<Weight>(weights_on_board);
            BestAfterDeepThinking resultDeepThink;
            List<Weight> my_candidate = new ArrayList<Weight>();
            my_candidate = getMyBlocks(weights_on_board, player);
            int setDepth;
            if (player == 1){
                setDepth = 8;
            } else {
                setDepth = 9;
            }
            if (my_candidate.size() > setDepth){
                resultDeepThink = deepThinkRemoveMove(testWeights_on_board, 1, setDepth, Integer.MIN_VALUE, Integer.MAX_VALUE);
            } else {
                resultDeepThink = deepThinkRemoveMove(testWeights_on_board, 1, my_candidate.size(), Integer.MIN_VALUE, Integer.MAX_VALUE);
            }

            System.out.printf("[%s, %s] numWays: %s\n", resultDeepThink.weight, resultDeepThink.position, resultDeepThink.numAvailableMoves);
            // System.out.printf("resultDeepThink.numAvailableMoves: %s, resultDeepThink.weight: %s, resultDeepThink.position: %s\n", resultDeepThink.numAvailableMoves, resultDeepThink.weight, resultDeepThink.position);
            // System.out.printf("-------------------------------\n");

            if (resultDeepThink.weight == 0) {
                decision = makeRemoveMove(weights_on_board);
                System.out.printf("[%s, %s] choosed\n", decision.weight, decision.position);
            } else {
                decision = new Weight(resultDeepThink.weight, resultDeepThink.position, player);
            }

            // update board
            removeWeight(weights_on_board, resultDeepThink.position, resultDeepThink.weight);
            // weights_on_board.remove(decision);
            System.out.printf("After weights_on_board.size(): %s\n", weights_on_board.size());
        }
        return decision.position + " " + decision.weight;
    }

    public Weight makeAddMove(List<Integer> weights, int[] board, List<Weight> weights_on_board) {
        int index = strategy.nextInt(weights.size());
        int candidate = weights.get(index);
        for (int pos = -25; pos < 25; pos ++) {
            // see if position is taken
            //Peter: where we can think
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
        //Peter: where we can think
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

    public BestAfterDeepThinking deepThinkRemoveMove(List<Weight> weights_on_board, int depth, int depthSetting, int alpha, int beta) {
        List<Weight> myRemove_candidate = new ArrayList<Weight>();
        List<Weight> hisRemove_candidate = new ArrayList<Weight>();
        int errorFactor = 1;

        if (player == 0) {
            myRemove_candidate = weights_on_board;
            hisRemove_candidate = getMyBlocks(weights_on_board, 1);
        } else {
            // player 2 can only remove his/her own piece unless there are none
            myRemove_candidate = getMyBlocks(weights_on_board, player);
            hisRemove_candidate = weights_on_board;
            if (myRemove_candidate.size() == 0){
                // no more player 2 blocks
                myRemove_candidate = weights_on_board;
            }
        }
        // myRemove_candidate = candidateLists.myList;
        // hisRemove_candidate = candidateLists.hisList;

        // System.out.printf("depth: %s\n", depth);
        // System.out.printf("hisRemove_candidate\n");
        // for (Weight obj : hisRemove_candidate) {
        //     System.out.printf("[%s,%s] ", obj.weight, obj.position);
        // }
        // System.out.printf("\nmyRemove_candidate\n");
        // for (Weight obj : myRemove_candidate) {
        //     System.out.printf("[%s,%s] ", obj.weight, obj.position);
        // }
        // System.out.printf("\n");

        Weight curBestWeight = new Weight(0,0,0);
        if (depth == depthSetting) {
            int numAvailableMoves = 0;
            for(Weight eachWeightCandidate : myRemove_candidate) {
                if (canRemove(eachWeightCandidate, weights_on_board)) {
                    numAvailableMoves++;
                }
            }
            return new BestAfterDeepThinking(numAvailableMoves, 0, 0);
        }

        boolean allNotMoveable = true;
        if (depth%2==1) {
            //it's my term, max node, max alpha
            for (int i=0; i<myRemove_candidate.size(); i++) {
                Weight eachWeightCandidate = myRemove_candidate.get(i);
                if(player == 1 && myRemove_candidate.size() != 1 && eachWeightCandidate.position == -4) {
                    continue;
                }
                if (!canRemove(eachWeightCandidate, weights_on_board)) {
                    continue;
                }
                allNotMoveable = false;
                // System.out.printf("Depth: %s, take my weight: %s\n", depth, eachWeightCandidate.weight);
                List<Weight> testWeights_on_board = new ArrayList<Weight>(weights_on_board);
                testWeights_on_board.remove(eachWeightCandidate);
                BestAfterDeepThinking myDeepTest = deepThinkRemoveMove(testWeights_on_board, depth+1, depthSetting, alpha, beta);
                if (myDeepTest.numAvailableMoves > alpha) {
                    alpha = myDeepTest.numAvailableMoves;
                    curBestWeight = eachWeightCandidate;
                }
                // System.out.printf("Depth: %s, got myDeepTest.numAvailableMoves: %s\n", depth, myDeepTest.numAvailableMoves);
                // System.out.printf("alpha: %s, beta: %s\n", alpha, beta);
                if (alpha >= beta) {
                    return new BestAfterDeepThinking(beta, myDeepTest.weight, myDeepTest.position);
                }
            }
            if (allNotMoveable) {
                return new BestAfterDeepThinking(Integer.MAX_VALUE, curBestWeight.weight, curBestWeight.position);
            } else {
                return new BestAfterDeepThinking(alpha, curBestWeight.weight, curBestWeight.position);
            }
        } else {
            //it's his term, min node, min beta
            for (int i=0; i<hisRemove_candidate.size(); i++) {
                Weight eachWeightCandidate = hisRemove_candidate.get(i);
                if(player == 1 && myRemove_candidate.size() != 1 && eachWeightCandidate.position == -4) {
                    continue;
                }
                if (!canRemove(eachWeightCandidate, weights_on_board)) {
                    continue;
                }
                allNotMoveable = false;
                // System.out.printf("Depth: %s, take his weight: %s\n", depth, eachWeightCandidate.weight);
                List<Weight> testWeights_on_board = new ArrayList<Weight>(weights_on_board);
                testWeights_on_board.remove(eachWeightCandidate);
                BestAfterDeepThinking myDeepTest = deepThinkRemoveMove(testWeights_on_board, depth+1, depthSetting, alpha, beta);
                if(myDeepTest.numAvailableMoves < beta) {
                    beta = myDeepTest.numAvailableMoves;
                    curBestWeight = eachWeightCandidate;
                }
                // System.out.printf("Depth: %s, got myDeepTest.numAvailableMoves: %s\n", depth, myDeepTest.numAvailableMoves);
                // System.out.printf("alpha: %s, beta: %s\n", alpha, beta);
                if(alpha >= beta) {
                    return new BestAfterDeepThinking(alpha, myDeepTest.weight, myDeepTest.position);
                }
            }
            if (allNotMoveable) {
                return new BestAfterDeepThinking(Integer.MIN_VALUE, curBestWeight.weight, curBestWeight.position);
            } else {
                return new BestAfterDeepThinking(beta, curBestWeight.weight, curBestWeight.position);
            }
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
        new PeterContestant(Integer.parseInt(args[0]));
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

    public class BestAfterDeepThinking {
        public int numAvailableMoves;
        public int weight;
        public int position;
        public BestAfterDeepThinking(int numAvailableMoves, int weight, int position) {
            this.numAvailableMoves = numAvailableMoves;
            this.weight = weight;
            this.position = position;
        }
    }

}
