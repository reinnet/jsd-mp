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

import java.util.List;

public interface ChainsConfig {
    List <ChainConfig> getChains();

    interface ChainConfig {
        int getCost();

        List<LinkConfig> getLinks();

        List<NodeConfig> getNodes();

        interface LinkConfig {
            int getSource();

            int getDestination();

            int getBandwidth();
        }

        interface NodeConfig {
            String getType();
        }
    }
}
