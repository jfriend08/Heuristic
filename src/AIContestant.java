import java.io.BufferedReader;
import java.io.InputStreamReader;

/**
 * Created by ylc265 on 9/23/15.
 */
public class AIContestant extends NoTippingPlayer{
    private static BufferedReader br;

    AIContestant(int port) {
        super(port);
    }

    protected String process(String command) {

        return "hi";
    }

    public static void main(String[] args) throws Exception {
        br = new BufferedReader(new InputStreamReader(System.in));
        new AIContestant(Integer.parseInt(args[0]));
    }
}
