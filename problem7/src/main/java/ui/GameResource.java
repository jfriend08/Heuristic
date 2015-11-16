package ui;

import Game.Game;
import Game.Node;
import Game.Direction;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Path("/game-state")
@Produces(MediaType.APPLICATION_JSON)
public class GameResource {

    @GET
    public GameState getGameState() {
        Map<Integer, Node> nodes = Game.nodes;
        Map<Integer, Map<Direction, Integer>> edges = new HashMap<Integer, Map<Direction, Integer>>();
        Map<String, List<String>> playerStats = new HashMap<String, List<String>>();

        for (Map.Entry<Integer, Node> nodeEntry : nodes.entrySet()) {
            Map<Direction, Integer> edgeInfo = new HashMap<Direction, Integer>();
            
            if(nodeEntry.getValue().up != null) {
                edgeInfo.put(Direction.UP, nodeEntry.getValue().up.getId());
            }
            if(nodeEntry.getValue().down != null) {
                edgeInfo.put(Direction.DOWN, nodeEntry.getValue().down.getId());
            }
            if(nodeEntry.getValue().left != null) {
                edgeInfo.put(Direction.LEFT, nodeEntry.getValue().left.getId());
            }
            if(nodeEntry.getValue().right != null) {
                edgeInfo.put(Direction.RIGHT, nodeEntry.getValue().right.getId());
            }
            edges.put(nodeEntry.getKey(), edgeInfo);
        }

        playerStats =  Game.getInstance().getPlayerStats();
        return new GameState(nodes, edges, playerStats);
    }
}
