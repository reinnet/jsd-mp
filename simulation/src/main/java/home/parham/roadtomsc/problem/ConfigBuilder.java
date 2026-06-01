/*
 * In The Name Of God
 * ======================================
 * [] Project Name : roadtomsc
 *
 * [] Package Name : home.parham.roadtomsc.exact.model
 *
 * [] Creation Date : 02-07-2019
 *
 * [] Created By : Parham Alvani (parham.alvani@gmail.com)
 * =======================================
 */

package home.parham.roadtomsc.problem;

import home.parham.roadtomsc.domain.Chain;
import home.parham.roadtomsc.domain.Link;
import home.parham.roadtomsc.domain.Node;

import java.util.ArrayList;

public class ConfigBuilder {
    /**
     * physical nodes
     */
    private ArrayList<Node> nodes = new ArrayList<>();

    /**
     * physical links
     */
    private ArrayList<Link> links = new ArrayList<>();

    /**
     * SFC requests chains
     */
    private ArrayList<Chain> chains = new ArrayList<>();

    /**
     * VNFMs parameters
     */
    private int vnfmRam, vnfmCores, vnfmCapacity, vnfmRadius, vnfmBandwidth, vnfmLicenseFee;

    public ConfigBuilder vnfmRam(int vnfmRam) {
        this.vnfmRam = vnfmRam;
        return this;
    }

    public ConfigBuilder vnfmCores(int vnfmCores) {
        this.vnfmCores = vnfmCores;
        return this;
    }

    public ConfigBuilder vnfmCapacity(int vnfmCapacity) {
        this.vnfmCapacity = vnfmCapacity;
        return this;
    }

    public ConfigBuilder vnfmRadius(int vnfmRadius) {
        this.vnfmRadius = vnfmRadius;
        return this;
    }

    public ConfigBuilder vnfmBandwidth(int vnfmBandwidth) {
        this.vnfmBandwidth = vnfmBandwidth;
        return this;
    }

    public ConfigBuilder vnfmLicenseFee(int vnfmLicenseFee) {
        this.vnfmLicenseFee = vnfmLicenseFee;
        return this;
    }

    /**
     * Adds physical link to network topology
     *
     * @param link: physical link
     */
    public ConfigBuilder addLink(Link link) {
        this.links.add(link);
        return this;
    }

    /**
     * Adds chain to SFC request collection, note that our problem is offline
     *
     * @param chain: SFC request
     */
    public ConfigBuilder addChain(Chain chain) {
        this.chains.add(chain);
        return this;
    }

    /**
     * Adds physical node to network topology
     *
     * @param node: physical node
     */
    public ConfigBuilder addNode(Node node) {
        this.nodes.add(node);
        return this;
    }


    /**
     * Builds the immutable instance of the model configuration based on the given parameters
     */
    public Config build() {
        return new Config(
                this.nodes,
                this.links,
                this.chains,
                this.vnfmRam,
                this.vnfmCores,
                this.vnfmCapacity,
                this.vnfmRadius,
                this.vnfmBandwidth,
                this.vnfmLicenseFee
        );
    }

}
