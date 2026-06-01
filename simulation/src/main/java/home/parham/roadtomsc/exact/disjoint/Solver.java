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

package home.parham.roadtomsc.exact.disjoint;

import home.parham.roadtomsc.domain.Link;
import home.parham.roadtomsc.exact.Config;
import home.parham.roadtomsc.exact.disjoint.model.Phase2;
import home.parham.roadtomsc.exact.disjoint.model.Phase1;
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
            writer = new PrintWriter(Files.newBufferedWriter(Paths.get("disjoint-result.txt")));
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }

        try {
            IloCplex phase1Cplex = new IloCplex();
            Phase1 phase1 = new Phase1(phase1Cplex, cfg);
            phase1.variables().objective().constraints();

            phase1Cplex.exportModel("phase-1.lp");
            phase1Cplex.setParam(IloCplex.Param.MIP.Tolerances.MIPGap, 0.05); // 5% MIP Gap
            if (!phase1Cplex.solve()) {
                return null;
            }

            IloCplex phase2Cplex = new IloCplex();
            Phase2 phase2 = new Phase2(phase2Cplex, cfg);
            phase2.variables(phase1.getX(), phase1.getY(), phase1.getZ(), phase1.getTau(), phase1Cplex).objective().constraints();

            phase2Cplex.exportModel("phase-2.lp");

            phase2Cplex.setParam(IloCplex.Param.MIP.Tolerances.MIPGap, 0.05); // 5% MIP Gap

            Instant now = Instant.now();
            boolean solved = phase2Cplex.solve();
            System.out.printf("Problem solved in %s\n", Duration.between(now, Instant.now()));

            if (solved) {
                writer.println();
                writer.println(" Solution Status = " + phase2Cplex.getStatus());
                writer.println();

                writer.println();
                writer.println(" gap = " + phase2Cplex.getMIPRelativeGap());
                writer.println();

                writer.println();
                writer.println(" cost = " + phase2Cplex.getObjValue());
                writer.println();

                int acceptedChains = 0;
                writer.println();
                writer.println(" >> Chains");
                for (int i = 0; i < cfg.getT(); i++) {
                    if (phase2Cplex.getValue(phase2.getX()[i]) == 1) {
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
                    usedVNFMs += phase2Cplex.getValue(phase2.getyHat()[i]);
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
                                if (phase2Cplex.getValue(phase2.getZ()[i][j][k + v]) == 1) {
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
                        if (phase2Cplex.getValue(phase2.getzHat()[h][i]) == 1) {
                            writer.printf("Chain %d manager is %s\n", h, cfg.getNodes().get(i).getName());
                        }
                    }
                }
                writer.println();

                writer.println();
                writer.println(" >> Manager instances");
                for (int i = 0; i < cfg.getW(); i++) {
                    writer.printf("%s has %f manager instances\n",
                            cfg.getNodes().get(i).getName(), phase2Cplex.getValue(phase2.getyHat()[i]));
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
                                    if (phase2Cplex.getValue(phase2.getTau()[i][j][u + k]) == 1) {
                                        Link l = cfg.getChains().get(h).getLink(k);
                                        writer.printf("Chain %d link %d (%d - %d) is on %s - %s\n", h, k,
                                                l.getSource(), l.getDestination(),
                                                cfg.getNodes().get(i).getName(), cfg.getNodes().get(j).getName());
                                    }
                                }

                                for (int k = 0; k < cfg.getChains().get(h).nodes(); k++) {
                                    if (phase2Cplex.getValue(phase2.getTauHat()[i][j][v + k]) == 1) {
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
                System.err.printf("Solve failed: %s\n", phase2Cplex.getStatus());
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
