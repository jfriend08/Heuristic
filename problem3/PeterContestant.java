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

    PeterContestant(int port) {
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
            decision = makeAddMove(weights, board, weights_on_board);
            // update board
            weights_on_board.add(decision);
        } else {
            // decision = makeRemoveMove(weights_on_board);

            System.out.printf("Before weights_on_board.size(): %s\n", weights_on_board.size());
            List<Weight> testWeights_on_board = new ArrayList<Weight>(weights_on_board);
            BestAfterDeepThinking resultDeepThink = deepThinkRemoveMove(testWeights_on_board, 1, Integer.MIN_VALUE, Integer.MAX_VALUE);
            System.out.printf("[%s, %s] numWays: %s\n", resultDeepThink.weight, resultDeepThink.position, resultDeepThink.numAvailableMoves);
            // System.out.printf("resultDeepThink.numAvailableMoves: %s, resultDeepThink.weight: %s, resultDeepThink.position: %s\n", resultDeepThink.numAvailableMoves, resultDeepThink.weight, resultDeepThink.position);
            // System.out.printf("-------------------------------\n");

            if (resultDeepThink.weight == 0) {
                decision = makeRemoveMove(weights_on_board);
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

    public BestAfterDeepThinking deepThinkAddMove(List<Integer> weights, List<Integer> hisWeights, int[] board, List<Weight> weights_on_board, int depth, int Avalue, int Bvalue) {
        int alpha = Avalue, beta = Bvalue;
        List<WeightPos> weightPosCandidate = new ArrayList<WeightPos>();
        List<Integer> myTestWeights = weights;
        List<Integer> hisTestWeights = hisWeights;
        int[] testBoard = board;
        List<Weight> test_weights_on_board = weights_on_board;

        if (depth%2==1) {
            //it's me
            weightPosCandidate = getAllCandidates(weights, board, weights_on_board);
        } else {
            //it's him
            weightPosCandidate = getAllCandidates(hisWeights, board, weights_on_board);
        }
        //define leaf node as the 5th depth
        if (depth == 5) {
            return new BestAfterDeepThinking (weightPosCandidate.size(), 0, 0);
        }

        if (depth%2==1) {
            for (WeightPos eachCandidate : weightPosCandidate) {
                myTestWeights.remove(myTestWeights.indexOf(eachCandidate.weight));
                test_weights_on_board.add(new Weight(eachCandidate.weight, eachCandidate.position, player));
                testBoard[eachCandidate.position+25]=eachCandidate.weight;
                BestAfterDeepThinking nextLevelTesting = deepThinkAddMove(myTestWeights,hisTestWeights, testBoard, weights_on_board, depth+1, alpha, beta);
                beta = Math.max(beta, nextLevelTesting.numAvailableMoves);
                if (alpha >= beta) {
                    return new BestAfterDeepThinking(beta, eachCandidate.weight, eachCandidate.position);
                }
            }
            return new BestAfterDeepThinking(alpha, weightPosCandidate.get(weightPosCandidate.size() - 1).weight, weightPosCandidate.get(weightPosCandidate.size() - 1).position);
            // return alpha;
        } else {
            for (WeightPos eachCandidate : weightPosCandidate) {
                hisTestWeights.remove(hisTestWeights.indexOf(eachCandidate.weight));
                test_weights_on_board.add(new Weight(eachCandidate.weight, eachCandidate.position, (player+1)%2));
                testBoard[eachCandidate.position+25]=eachCandidate.weight;
                BestAfterDeepThinking nextLevelTesting = deepThinkAddMove(myTestWeights,hisTestWeights, testBoard, weights_on_board, depth+1, alpha, beta);
                alpha = Math.min(alpha, nextLevelTesting.numAvailableMoves);
                if (alpha >= beta) {
                    return new BestAfterDeepThinking(alpha, eachCandidate.weight, eachCandidate.position);
                }
            }
            return new BestAfterDeepThinking(beta, weightPosCandidate.get(weightPosCandidate.size() - 1).weight, weightPosCandidate.get(weightPosCandidate.size() - 1).position);
            // return beta;
        }

        // System.out.print("All candidats: ");
        // for(WeightPos obj : myWeightPosCandidate) {System.out.printf("Weight: %s, Position: %s", obj.weight, obj.position);}
        // System.out.print("---------------------");
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

    public void makeRemoveMove2(List<Weight> weights_on_board) {
        List<Weight> random_candidate = new ArrayList<Weight>();
        List<Weight> myRemove_candidate = new ArrayList<Weight>();
        List<Weight> hisRemove_candidate = new ArrayList<Weight>();
        // player 1 can remove anything
        if (player == 0) {
            myRemove_candidate = weights_on_board;
            hisRemove_candidate = getMyBlocks(weights_on_board, (player+1)%2);
        } else {
            myRemove_candidate = weights_on_board;
            myRemove_candidate = getMyBlocks(weights_on_board, player);
            if (myRemove_candidate.size() == 0){
                // no more player 2 blocks
                myRemove_candidate = weights_on_board;
            }
        }
    }

    public twoCandidateList get_remove_candidate (List<Weight> weights_on_board) {
        List<Weight> myRemove_candidate = new ArrayList<Weight>();
        List<Weight> hisRemove_candidate = new ArrayList<Weight>();
        if (player == 0) {
            myRemove_candidate = weights_on_board;
            hisRemove_candidate = getMyBlocks(weights_on_board, (player+1)%2);
        } else {
            myRemove_candidate = getMyBlocks(weights_on_board, player);
            hisRemove_candidate = weights_on_board;
            if (myRemove_candidate.size() == 0){
                // no more player 2 blocks
                myRemove_candidate = weights_on_board;
            }
        }
        return new twoCandidateList(myRemove_candidate, hisRemove_candidate);
    }

    public BestAfterDeepThinking deepThinkRemoveMove(List<Weight> weights_on_board, int depth, int alpha, int beta) {
        // List<Weight> testWeights_on_board = new ArrayList<Weight>();
        twoCandidateList candidateLists = get_remove_candidate(weights_on_board);
        List<Weight> myRemove_candidate = new ArrayList<Weight>(candidateLists.myList);
        List<Weight> hisRemove_candidate = new ArrayList<Weight>(candidateLists.hisList);
        // myRemove_candidate = candidateLists.myList;
        // hisRemove_candidate = candidateLists.hisList;

        // System.out.printf("depth: %s\n", depth);
        // System.out.printf("hisRemove_candidate\n");
        // for (Weight obj : hisRemove_candidate) {
        //     System.out.printf("%s ", obj.weight);
        // }
        // System.out.printf("\nmyRemove_candidate\n");
        // for (Weight obj : myRemove_candidate) {
        //     System.out.printf("%s ", obj.weight);
        // }
        // System.out.printf("\n");

        Weight curBestWeight = new Weight(0,0,0);
        if (depth == 3) {
            int numAvailableMoves = 0;
            for(Weight eachWeightCandidate : myRemove_candidate) {
                if (canRemove(eachWeightCandidate, weights_on_board)) {
                    numAvailableMoves++;
                }
            }
            return new BestAfterDeepThinking(numAvailableMoves, 0, 0);
        }

        // List<Weight> myRemove_ValidCandidate = new ArrayList<Weight>();
        // List<Weight> hisRemove_ValidCandidate = new ArrayList<Weight>();
        // for(Weight eachWeightCandidate : myRemove_candidate) {
        //     if (canRemove(eachWeightCandidate, weights_on_board)) {
        //         myRemove_ValidCandidate.add(eachWeightCandidate);
        //     }
        // }
        // for(Weight eachWeightCandidate : hisRemove_candidate) {
        //     if (canRemove(eachWeightCandidate, weights_on_board)) {
        //         Remove_ValidCandidate.add(eachWeightCandidate);
        //     }
        // }
        boolean allNotMoveable = true;
        if (depth%2==1) {
            //it's my term, max node, max alpha
            for (int i=0; i<myRemove_candidate.size(); i++) {
                Weight eachWeightCandidate = myRemove_candidate.get(i);
                if (!canRemove(eachWeightCandidate, weights_on_board)) {
                    continue;
                }
                allNotMoveable = false;
                // System.out.printf("Depth: %s, take my weight: %s\n", depth, eachWeightCandidate.weight);
                List<Weight> testWeights_on_board = new ArrayList<Weight>(weights_on_board);
                testWeights_on_board.remove(eachWeightCandidate);
                BestAfterDeepThinking myDeepTest = deepThinkRemoveMove(testWeights_on_board, depth+1, alpha, beta);
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
                if (canRemove(eachWeightCandidate, weights_on_board)) {
                    continue;
                }
                allNotMoveable = false;
                // System.out.printf("Depth: %s, take his weight: %s\n", depth, eachWeightCandidate.weight);
                List<Weight> testWeights_on_board = new ArrayList<Weight>(weights_on_board);
                testWeights_on_board.remove(eachWeightCandidate);
                BestAfterDeepThinking myDeepTest = deepThinkRemoveMove(testWeights_on_board, depth+1, alpha, beta);
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

    // get all of the weight and position candidates of valid moves of current situation
    public List<WeightPos> getAllCandidates(List<Integer> weights, int[] board, List<Weight> weights_on_board) {
        List<WeightPos> weightPosCandidates = new ArrayList<WeightPos>();
        for (int myRemaindWeight : weights) {
            for (int pos = -25; pos <25; pos++) {
                if(board[pos+25] == 0) {
                    if (validAddMove(myRemaindWeight, pos, weights_on_board)) {
                        weightPosCandidates.add(new WeightPos(myRemaindWeight,pos));
                    }
                }
            }
        }
        return weightPosCandidates;
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

    public class WeightPos {
        public int weight;
        public int position;
        public WeightPos(int weight, int position) {
            this.weight = weight;
            this.position = position;
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

    public class twoCandidateList {
        public List<Weight> myList;
        public List<Weight> hisList;
        public twoCandidateList(List<Weight> myList, List<Weight> hisList) {
            this.myList = myList;
            this.hisList = hisList;
        }
    }

}
