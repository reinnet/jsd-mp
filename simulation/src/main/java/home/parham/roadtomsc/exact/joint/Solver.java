/*
 * In The Name Of God
 * ======================================
 * [] Project Name : roadtomsc
 *
 * [] Package Name : home.parham.roadtomsc.exact
 *
 * [] Creation Date : 18-08-2019
 *
 * [] Created By : Parham Alvani (parham.alvani@gmail.com)
 * =======================================
 */

package home.parham.roadtomsc.exact.joint;

import home.parham.roadtomsc.domain.Link;
import home.parham.roadtomsc.exact.Config;
import home.parham.roadtomsc.exact.joint.model.Model;
import home.parham.roadtomsc.problem.Method;
import home.parham.roadtomsc.problem.Solution;
import ilog.concert.IloException;
import ilog.cplex.IloCplex;

import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Duration;
import java.time.Instant;

public class Solver implements Method {
    private Config cfg;

    public Solver(home.parham.roadtomsc.problem.Config cfg) {
        this.cfg = Config.build(cfg);
    }

    @Override
    public Solution solve() {
        // create and setup the result file
        PrintWriter writer;
        try {
            writer = new PrintWriter(Files.newBufferedWriter(Paths.get("joint-result.txt")));
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }

        try {
            IloCplex cplex = new IloCplex();

            Model model = new Model(cplex, cfg);
            model.variables().objective().constraints();

            cplex.exportModel("joint.lp");

            cplex.setParam(IloCplex.Param.MIP.Tolerances.MIPGap, 0.05); // 5% MIP Gap

            Instant now = Instant.now();
            boolean solved = cplex.solve();
            System.out.printf("Problem solved in %s\n", Duration.between(now, Instant.now()));

            if (solved) {
                writer.println();
                writer.println(" Solution Status = " + cplex.getStatus());
                writer.println();

                writer.println();
                writer.println(" gap = " + cplex.getMIPRelativeGap());
                writer.println();

                writer.println();
                writer.println(" cost = " + cplex.getObjValue());
                writer.println();

                int acceptedChains = 0;
                writer.println();
                writer.println(" >> Chains");
                for (int i = 0; i < cfg.getT(); i++) {
                    if (cplex.getValue(model.getX()[i]) == 1) {
                        writer.printf("Chain %s is accepted.\n", i);
                        acceptedChains++;
                    } else {
                        writer.printf("Chain %s is not accepted.\n", i);
                    }
                }
                writer.println();

                writer.println();
                writer.printf("%d chains are accepted", acceptedChains);
                writer.println();

                writer.println();
                int usedVNFMs = 0;
                for (int i = 0; i < this.cfg.getW(); i++) {
                    usedVNFMs += cplex.getValue(model.getyHat()[i]);
                }
                writer.printf("%d VNFMs is used", usedVNFMs);
                writer.println();

                writer.println();
                writer.println(" >> Instance mapping");
                int v = 0;
                for (int h = 0; h < cfg.getT(); h++) {
                    writer.printf("Chain %d:\n", h);
                    for (int k = 0; k < cfg.getChains().get(h).nodes(); k++) {
                        for (int i = 0; i < cfg.getF(); i++) {
                            for (int j = 0; j < cfg.getW(); j++) {
                                if (cplex.getValue(model.getZ()[i][j][k + v]) == 1) {
                                    writer.printf("Node %d with type %d is mapped on %s\n", k, i, cfg.getNodes().get(j).getName());
                                }
                            }
                        }
                    }
                    v += cfg.getChains().get(h).nodes();
                }
                writer.println();

                writer.println();
                writer.println(" >> Manager mapping");
                for (int h = 0; h < cfg.getT(); h++) {
                    for (int i = 0; i < cfg.getW(); i++) {
                        if (cplex.getValue(model.getzHat()[h][i]) == 1) {
                            writer.printf("Chain %d manager is %s\n", h, cfg.getNodes().get(i).getName());
                        }
                    }
                }
                writer.println();

                writer.println();
                writer.println(" >> Manager instances");
                for (int i = 0; i < cfg.getW(); i++) {
                    writer.printf("%s has %d manager instances\n",
                            cfg.getNodes().get(i).getName(), (int) cplex.getValue(model.getyHat()[i]));
                }
                writer.println();

                writer.println();
                writer.println(" >> Instance and Management links");
                int u = 0;
                v = 0;
                for (int h = 0; h < cfg.getT(); h++) {
                    for (int i = 0; i < cfg.getW(); i++) {
                        for (int j = 0; j < cfg.getW(); j++) {
                            if (cfg.getE()[i][j] > 0) {

                                for (int k = 0; k < cfg.getChains().get(h).links(); k++) {
                                    if (cplex.getValue(model.getTau()[i][j][u + k]) == 1) {
                                        Link l = cfg.getChains().get(h).getLink(k);
                                        writer.printf("Chain %d link %d (%d - %d) is on %s - %s\n", h, k,
                                                l.getSource(), l.getDestination(),
                                                cfg.getNodes().get(i).getName(), cfg.getNodes().get(j).getName());
                                    }
                                }

                                for (int k = 0; k < cfg.getChains().get(h).nodes(); k++) {
                                    if (cplex.getValue(model.getTauHat()[i][j][v + k]) == 1) {
                                        writer.printf("Chain %d node %d manager is on %s - %s\n", h, k,
                                                cfg.getNodes().get(i).getName(), cfg.getNodes().get(j).getName());
                                    }
                                }

                            }
                        }
                    }
                    u += cfg.getChains().get(h).links();
                    v += cfg.getChains().get(h).nodes();
                }
                writer.println();
           } else {
                System.err.printf("Solve failed: %s\n", cplex.getStatus());
            }
        } catch (IloException e) {
            e.printStackTrace();
            return null;
        }

        // close the result file
        writer.flush();
        writer.close();

        return null;
    }
}
