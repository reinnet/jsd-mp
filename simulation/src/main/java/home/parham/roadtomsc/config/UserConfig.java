/*
 * In The Name Of God
 * ======================================
 * [] Project Name : roadtomsc
 *
 * [] Package Name : home.parham.roadtomsc.config
 *
 * [] Creation Date : 05-07-2019
 *
 * [] Created By : Parham Alvani (parham.alvani@gmail.com)
 * =======================================
 */

package home.parham.roadtomsc.config;

import com.yacl4j.core.ConfigurationBuilder;

import java.io.File;

public class UserConfig {
    private TopologyConfig topology;
    private VNFMConfig vnfm;
    private TypesConfig types;
    private ChainsConfig chains;

    public TopologyConfig getTopology() {
        return topology;
    }

    public VNFMConfig getVNFM() {
        return vnfm;
    }

    public TypesConfig getTypes() {
        return types;
    }

    public ChainsConfig getChains() {
        return chains;
    }

    public static UserConfig load(String dirname) {
        String tplFileName = dirname + File.separator + "topology.yaml";
        String vnfmFileName = dirname + File.separator + "vnfm.yaml";
        String typesFileName = dirname + File.separator + "types.yaml";
        String chainsFileName = dirname + File.separator + "chains.yaml";

        UserConfig cfg = new UserConfig();

        // load configuration from files
        cfg.topology = ConfigurationBuilder.newBuilder()
                .source().fromFile(new File(tplFileName))
                .build(TopologyConfig.class);

        cfg.vnfm = ConfigurationBuilder.newBuilder()
                .source().fromFile(new File(vnfmFileName))
                .build(VNFMConfig.class);

        cfg.types = ConfigurationBuilder.newBuilder()
                .source().fromFile(new File(typesFileName))
                .build(TypesConfig.class);

        cfg.chains = ConfigurationBuilder.newBuilder()
                .source().fromFile(new File(chainsFileName))
                .build(ChainsConfig.class);

        return cfg;
    }

    private UserConfig() {
    }
}
