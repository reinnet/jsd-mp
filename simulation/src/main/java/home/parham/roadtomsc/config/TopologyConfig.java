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

public interface TopologyConfig {
    List<NodeConfig> getNodes();
    List<LinkConfig> getLinks();

    interface NodeConfig {
        String getID();
        int getRam();
        int getCores();
        boolean getVnfSupport();
        List<String> getNotManagerNodes();
        boolean getEgress();
        boolean getIngress();
    }

    interface LinkConfig {
        String getSource();
        String getDestination();
        int getBandwidth();
    }
}
