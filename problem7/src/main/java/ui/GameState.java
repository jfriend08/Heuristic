package ui;

import Game.Direction;
import Game.Node;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class GameState {
    private Map<Integer, Node> nodes;
    private Map<Integer, Map<Direction, Integer>> edges = new HashMap<Integer, Map<Direction, Integer>>();
    private Map<String,List<String>> playerStats = new HashMap<String, List<String>>();

    public GameState(Map<Integer, Node> nodes, Map<Integer, Map<Direction, Integer>> edges, Map<String, List<String>> playerStats) {
        this.nodes = nodes;
        this.edges = edges;
        this.playerStats = playerStats;

    }

    public Map<Integer, Node> getNodes() {
        return nodes;
    }

    public void setNodes(Map<Integer, Node> nodes) {
        this.nodes = nodes;
    }

    public Map<Integer, Map<Direction, Integer>> getEdges() {
        return edges;
    }

    public void setEdges(Map<Integer, Map<Direction, Integer>> edges) {
        this.edges = edges;
    }

    public Map<String, List<String>> getPlayerStats() {
        return playerStats;
    }

    public void setPlayerStats(Map<String, List<String>> playerStats) {
        this.playerStats = playerStats;
    }
}
