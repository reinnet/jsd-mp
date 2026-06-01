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

public interface TypesConfig {
    List<TypeConfig> getTypes();

    interface TypeConfig {
        String getName();
        int getCores();
        int getRam();
        boolean getEgress();
        boolean getIngress();
        boolean getManageable();
    }
}
