/*
 * In The Name Of God
 * ======================================
 * [] Project Name : roadtomsc
 *
 * [] Package Name : home.parham.roadtomsc.problem
 *
 * [] Creation Date : 17-08-2019
 *
 * [] Created By : Parham Alvani (parham.alvani@gmail.com)
 * =======================================
 */

package home.parham.roadtomsc.problem;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.List;

public class Solution {
    private int cost;
    /**
     * Placement array for each chain and empty array indicates error in placement
     */
    private List<List<String>> vnfPlacement;
    /**
     * Name of chain's manager physical server and `-` indicates error in placement
     */
    private List<String> vnfmPlacement;
    /**
     * Route from Manageable vnf to its manager and empty array indicates error in routing
     */
    private List<List<List<String>>> vnfmRoutes;
    /**
     * Number of the used VNFMs instances
     */
    private int vnfmInstances;

    public Solution(int cost, List<List<String>> vnfPlacement, List<String> vnfmPlacement, List<List<List<String>>> vnfmRoutes, int vnfmInstances) {
        this.cost = cost;
        this.vnfPlacement = vnfPlacement;
        this.vnfmPlacement = vnfmPlacement;
        this.vnfmRoutes = vnfmRoutes;
        this.vnfmInstances = vnfmInstances;
    }

    public int getCost() {
        return cost;
    }

    public List<List<String>> getVnfPlacement() {
        return vnfPlacement;
    }

    public List<String> getVnfmPlacement() {
        return vnfmPlacement;
    }

    public List<List<List<String>>> getVnfmRoutes() {
        return vnfmRoutes;
    }

    @Override
    public String toString() {
        StringWriter sw = new StringWriter();
        PrintWriter writer = new PrintWriter(sw);

        writer.println();
        writer.printf("Cost: %d\n", this.getCost());
        writer.println();

        int acceptedChains = 0;
        writer.println();
        List<List<String>> vnfPlacement = this.getVnfPlacement();
        for (int c = 0; c < vnfPlacement.size(); c++) {
            writer.printf("Chain %d:\n", c);
            for (int i = 0; i < vnfPlacement.get(c).size(); i++) {
                writer.printf("Node %d is mapped on %s\n", i, vnfPlacement.get(c).get(i));
            }
            acceptedChains += vnfPlacement.get(c).size() != 0 ? 1 : 0;
        }
        writer.println();

        writer.println();
        writer.printf("%d chains are accepted", acceptedChains);
        writer.println();

        writer.println();
        writer.printf("%d vnfms are used", this.vnfmInstances);
        writer.println();

        writer.println();
        List<String> vnfmPlacement = this.getVnfmPlacement();
        for (int c = 0; c < vnfmPlacement.size(); c++) {
            writer.printf("Chain %d manager is %s\n", c, vnfmPlacement.get(c));
        }
        writer.println();

        writer.println();
        List<List<List<String>>> vnfmRoutes = this.getVnfmRoutes();
        for (int c = 0; c < vnfmRoutes.size(); c++) {
            writer.printf("Chain %d Management Routes:\n", c);
            for (int i = 0; i < vnfmRoutes.get(c).size(); i++) {
                writer.printf("%d: %s\n", i, vnfmRoutes.get(c).get(i).toString());
            }
        }
        writer.println();

        writer.flush();

        return sw.toString();
    }
}
