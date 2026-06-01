package home.parham.roadtomsc.problem;

import home.parham.roadtomsc.domain.Chain;
import home.parham.roadtomsc.domain.Link;
import home.parham.roadtomsc.domain.Node;

import java.util.Collections;
import java.util.List;

/**
 * Config represents problem configuration
 * by configuration we mean parameters that are given
 * by user.
 */
public class Config {

    /**
     * physical nodes
     */
    private List<Node> nodes;

    /**
     * physical links
     */
    private List<Link> links;

    /**
     * SFC requests chains
     */
    private List<Chain> chains;

    /**
     * VNFMs parameters
     */
    private int vnfmRam, vnfmCores, vnfmCapacity, vnfmRadius, vnfmBandwidth, vnfmLicenseFee;

    public Config(
            List<Node> nodes,
            List<Link> links,
            List<Chain> chains,
            int vnfmRam,
            int vnfmCores,
            int vnfmCapacity,
            int vnfmRadius,
            int vnfmBandwidth,
            int vnfmLicenseFee
    ) {
        this.nodes = nodes;
        this.links = links;
        this.chains = chains;
        this.vnfmRam = vnfmRam;
        this.vnfmCores = vnfmCores;
        this.vnfmCapacity = vnfmCapacity;
        this.vnfmRadius = vnfmRadius;
        this.vnfmBandwidth = vnfmBandwidth;
        this.vnfmLicenseFee = vnfmLicenseFee;
    }

    public List<Node> getNodes() {
        return Collections.unmodifiableList(nodes);
    }

    public List<Link> getLinks() {
        return Collections.unmodifiableList(links);
    }

    public List<Chain> getChains() {
        return Collections.unmodifiableList(chains);
    }

    public int getVnfmRam() {
        return vnfmRam;
    }

    public int getVnfmCores() {
        return vnfmCores;
    }

    public int getVnfmCapacity() {
        return vnfmCapacity;
    }

    public int getVnfmRadius() {
        return vnfmRadius;
    }

    public int getVnfmBandwidth() {
        return vnfmBandwidth;
    }

    public int getVnfmLicenseFee() {
        return vnfmLicenseFee;
    }

    /**
     * @param name of the target node
     * @return index of a first node that has the given name otherwise -1
     */
    public int getNodeIndex(String name) {
        for (int i = 0; i < this.nodes.size(); i++)  {
            if (this.nodes.get(i).getName().equals(name)) {
                return i;
            }
        }
        return -1;
    }
}
