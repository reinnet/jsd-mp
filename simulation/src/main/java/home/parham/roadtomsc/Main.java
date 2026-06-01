package home.parham.roadtomsc;

import home.parham.roadtomsc.config.ChainsConfig;
import home.parham.roadtomsc.config.TopologyConfig;
import home.parham.roadtomsc.config.UserConfig;
import home.parham.roadtomsc.domain.Chain;
import home.parham.roadtomsc.domain.Link;
import home.parham.roadtomsc.domain.Node;
import home.parham.roadtomsc.domain.Types;
import home.parham.roadtomsc.problem.Config;
import home.parham.roadtomsc.problem.ConfigBuilder;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.logging.Logger;
import java.util.stream.Collectors;

public class Main {

    private final static Logger logger = Logger.getLogger(Main.class.getName());

    private static void usage() {
        System.out.println("roadtomsc /path/to/configuration/");
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            usage();
            return;
        }

        // load user configuration
        UserConfig config = UserConfig.load(args[0]);

        // build the model configuration from the loaded configuration

        ConfigBuilder builder = new ConfigBuilder()
                .vnfmRam(config.getVNFM().getRam())
                .vnfmCores(config.getVNFM().getCores())
                .vnfmCapacity(config.getVNFM().getCapacity())
                .vnfmRadius(config.getVNFM().getRadius())
                .vnfmBandwidth(config.getVNFM().getBandwidth())
                .vnfmLicenseFee(config.getVNFM().getLicenseFee());

        // current mapping between node identification and their index in model
        Map<String, Integer> nodes = new HashMap<>();

        // physical nodes {{{
        for (int i = 0; i < config.getTopology().getNodes().size(); i++) {
            nodes.put(config.getTopology().getNodes().get(i).getID(), i);
        }

        for (int i = 0; i < config.getTopology().getNodes().size(); i++) {
            TopologyConfig.NodeConfig nodeConfig = config.getTopology().getNodes().get(i);
            Node node = new Node(
                    nodeConfig.getID(),
                    nodeConfig.getCores(),
                    nodeConfig.getRam(),
                    nodeConfig.getVnfSupport(),
                    new HashSet<>(nodeConfig.getNotManagerNodes().stream().map(nodes::get).collect(Collectors.toList())),
                    nodeConfig.getEgress(),
                    nodeConfig.getIngress()
            );
            builder.addNode(node);
            logger.info(String.format("create physical node (%s) in index %d [%s]", nodeConfig.getID(), i, node));
        }
        // }}}

        // physical links {{{
        config.getTopology().getLinks().forEach(linkConfig -> {
            Link l = new Link(
                    linkConfig.getBandwidth(),
                    nodes.get(linkConfig.getSource()),
                    nodes.get(linkConfig.getDestination())
            );
            builder.addLink(l);
            logger.info(String.format("create physical link from %s to %s [%s]",
                    linkConfig.getSource(), linkConfig.getDestination(), l));
        });
        /// }}}

        // current mapping between vnf type identification and their index in model
        Map<String, Integer> types = new HashMap<>();


        // VNF types {{{
        config.getTypes().getTypes().forEach(typeConfig -> {
            Types.add(typeConfig.getCores(), typeConfig.getRam(),typeConfig.getEgress(),
                    typeConfig.getIngress(), typeConfig.getManageable());
            types.put(typeConfig.getName(), Types.len() - 1);
            logger.info(String.format("create virtual type %s [cores: %d, ram: %d, egress: %b, ingress: %b]",
                    typeConfig.getName(),
                    typeConfig.getCores(),
                    typeConfig.getRam(),
                    typeConfig.getEgress(),
                    typeConfig.getIngress()
            ));
        });
        // }}}

        // SFC requests {{{
        // consider to create requests after creating VNF types
        config.getChains().getChains().forEach(chainConfig -> {
            Chain chain = new Chain(chainConfig.getCost());

            Map<Integer, Integer> vNodes = new HashMap<>();

            for (int i = 0; i < chainConfig.getNodes().size(); i++) {
                ChainsConfig.ChainConfig.NodeConfig n = chainConfig.getNodes().get(i);
                chain.addNode(types.get(n.getType()));
                vNodes.put(i, i);
            }

            chainConfig.getLinks().forEach(linkConfig -> chain.addLink(
                    linkConfig.getBandwidth(),
                    vNodes.get(linkConfig.getSource()),
                    vNodes.get(linkConfig.getDestination())
            ));

            builder.addChain(chain);
        });
        // }}}

        // build configuration
        Config cfg = builder.build();

        // solve using the exact method (joint)
        new home.parham.roadtomsc.exact.joint.Solver(cfg).solve();
        // solve using the exact method (disjoint)
        new home.parham.roadtomsc.exact.disjoint.Solver(cfg).solve();

    }
}
