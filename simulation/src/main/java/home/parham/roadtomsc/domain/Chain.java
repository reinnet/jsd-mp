package home.parham.roadtomsc.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Chain {
    private ArrayList<Types.Type> chain;
    private ArrayList<Link> links;

    private int cost;

    public Chain(int cost) {
        this.chain = new ArrayList<>();
        this.links = new ArrayList<>();
        this.cost = cost;
    }

    public void addNode(int id) {
        this.chain.add(Types.get(id));
    }

    public void addLink(int bandwidth, int source, int destination) {
        this.links.add(new Link(bandwidth, source, destination));
    }

    public Types.Type getNode(int index) {
        return this.chain.get(index);
    }

    public Link getLink(int index) {
        return this.links.get(index);
    }

    public List<Types.Type> getNodes() {
        return Collections.unmodifiableList(this.chain);
    }

    public int nodes() {
        return this.chain.size();
    }

    public int links() {return this.links.size(); }

    public int getCost() {
        return cost;
    }
}
