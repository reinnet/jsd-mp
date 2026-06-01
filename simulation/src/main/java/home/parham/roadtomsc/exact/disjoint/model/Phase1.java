package home.parham.roadtomsc.exact.disjoint.model;

import home.parham.roadtomsc.domain.Chain;
import home.parham.roadtomsc.domain.Types;
import home.parham.roadtomsc.exact.Config;
import ilog.concert.*;

/**
 * Model creates variables, objective and constraints of mathematical
 * model of our problem in CPLEX.
 */
public class Phase1 {
    /**
     * modeler is a CPLEX model builder.
     */
    private final IloModeler modeler;

    /**
     * Configuration instance that provides problem parameters.
     */
    private final Config cfg;

    /**
     * binary variable assuming the value 1 if the _h_th SFC request is accepted;
     * otherwise its value is zero.
     *
     * x[h]
     * .lp format: x (chain number)
     */
    private IloIntVar[] x;


    /**
     * the number of VNF instances of type _k_ that are used in server _w_.
     *
     * y[w][k]
     * .lp format: y (physical node, type)
     */
    private IloIntVar[][] y;

    /**
     * binary variable assuming the value 1 if the VNF node _v_ is served by the VNF instance of type
     * _k_ in the server _w_.
     *
     * z[k][w][v]
     * .lp format: z (type, physical node, chain number _ node number in the chain)
     */
    private IloIntVar[][][] z;

    /**
     * binary variable assuming the value 1 if the virtual link _(u, v)_ is routed on
     * the physical network link from _i_ to _j_.
     *
     * tau[i][j][uv]
     * .lp format: tau (physical link source, physical link destination, chain number _ link number in the chain)
     */
    private IloIntVar[][][] tau;

    /**
     *
     * @param pModeler CPLEX modeler instance
     * @param pCfg configuration instance
     */
    public Phase1(final IloModeler pModeler, final Config pCfg) {
        this.modeler = pModeler;
        this.cfg = pCfg;
    }

    /**
     * Adds model variables.
     *
     * @return Model
     */
    public Phase1 variables() throws IloException {
        xVariable();
        yVariable();
        zVariable();

        tauVariable();

        return this;
    }

    private void xVariable() throws IloException {
        // x
        String[] xNames = new String[this.cfg.getT()];
        for (int i = 0; i < this.cfg.getT(); i++) {
            xNames[i] = String.format("x(%d)", i);
        }
        this.x = this.modeler.boolVarArray(this.cfg.getT(), xNames);
    }

    private void yVariable() throws IloException {
        // y
        String[][] yNames = new String[this.cfg.getW()][this.cfg.getF()];
        for (int i = 0; i < this.cfg.getW(); i++) {
            for (int j = 0; j < this.cfg.getF(); j++) {
                yNames[i][j] = String.format("y(%d,%d)", i, j);
            }
        }
        this.y = new IloIntVar[this.cfg.getW()][this.cfg.getF()];
        for (int i = 0; i < this.cfg.getW(); i++) {
            for (int j = 0; j < this.cfg.getF(); j++) {
                this.y[i][j] = this.modeler.intVar(0, Integer.MAX_VALUE, yNames[i][j]);
            }
        }
    }

    private void zVariable() throws IloException {
        // z
        String[][][] zNames = new String[this.cfg.getF()][this.cfg.getW()][this.cfg.getV()];
        for (int i = 0; i < this.cfg.getF(); i++) {
            for (int j = 0; j < this.cfg.getW(); j++) {
                int v = 0;
                for (int h = 0; h < this.cfg.getT(); h++) {
                    for (int k = 0; k < this.cfg.getChains().get(h).nodes(); k++) {
                        zNames[i][j][k + v] = String.format("z(%d,%d,%d_%d)", i, j, h, k);
                    }
                    v += this.cfg.getChains().get(h).nodes();
                }
            }
        }
        this.z = new IloIntVar[this.cfg.getF()][this.cfg.getW()][this.cfg.getV()];
        for (int i = 0; i < this.cfg.getF(); i++) {
            for (int j = 0; j < this.cfg.getW(); j++) {
                for (int k = 0; k < this.cfg.getV(); k++) {
                    this.z[i][j][k] = modeler.boolVar(zNames[i][j][k]);
                }
            }
        }
    }

    private void tauVariable() throws IloException {
        // tau, tauHat
        String[][][] tauNames = new String[this.cfg.getW()][this.cfg.getW()][this.cfg.getU()];
        for (int i = 0; i < this.cfg.getW(); i++) {
            for (int j = 0; j < this.cfg.getW(); j++) {
                int u = 0;
                for (int h = 0; h < this.cfg.getT(); h++) {
                    for (int k = 0; k < this.cfg.getChains().get(h).links(); k++) {
                        tauNames[i][j][u + k] = String.format("tau(%d,%d,%d_%d)", i, j, h, k);
                    }
                    u += this.cfg.getChains().get(h).links();
                }
            }
        }
        this.tau = new IloIntVar[this.cfg.getW()][this.cfg.getW()][this.cfg.getU()];
        for (int i = 0; i < this.cfg.getW(); i++) {
            for (int j = 0; j < this.cfg.getW(); j++) {
                for (int k = 0; k < this.cfg.getU(); k++) {
                    this.tau[i][j][k] = modeler.boolVar(tauNames[i][j][k]);
                }
            }
        }
    }

    /**
     * Adds objective function
     * @throws IloException
     * @return Model
     */
    public Phase1 objective() throws IloException {
        IloLinearNumExpr expr = this.modeler.linearNumExpr();
        for (int i = 0; i < this.cfg.getT(); i++) {
            expr.addTerm(this.cfg.getChains().get(i).getCost(), this.x[i]);
        }
        this.modeler.addMaximize(expr);

        return this;
    }

    /**
     * Adds model constraints
     * @return Model
     * @throws IloException
     */
    public Phase1 constraints() throws IloException {
        this.nodeMemoryCPUConstraint();
        this.servicePlaceConstraint();
        this.serviceTypeConstraint();
        this.vnfSupportConstraint();

        this.flowConservation();

        this.egressConstraint();
        this.ingressConstraint();

        this.linkBandwidthConstraint();

        return this;
    }

    /**
     * Node Memory/CPU Constraint
     * @throws IloException
     */
    private void nodeMemoryCPUConstraint() throws IloException {
        for (int i = 0; i < this.cfg.getW(); i++) {
            IloLinearNumExpr ramConstraint = this.modeler.linearNumExpr();
            IloLinearNumExpr cpuConstraint = this.modeler.linearNumExpr();

            for (int j = 0; j < this.cfg.getF(); j++) {
                ramConstraint.addTerm(Types.get(j).getRam(), this.y[i][j]); // instance ram
                cpuConstraint.addTerm(Types.get(j).getCores(), this.y[i][j]); // instance cpu
            }

            this.modeler.addLe(cpuConstraint, this.cfg.getNodes().get(i).getCores(),
                    String.format("node_cpu_constraint_node{%d}", i));
            this.modeler.addLe(ramConstraint, this.cfg.getNodes().get(i).getRam(),
                    String.format("node_memory_constraint_node{%d}", i));
        }
    }

    /**
     * Service Place Constraint
     * @throws IloException
     */
    private void servicePlaceConstraint() throws IloException {
        for (int i = 0; i < this.cfg.getF(); i++) {
            for (int j = 0; j < this.cfg.getW(); j++) {
                IloLinearIntExpr constraint = this.modeler.linearIntExpr();

                for (int k = 0; k < this.cfg.getV(); k++) {
                    constraint.addTerm(1, this.z[i][j][k]);
                }

                this.modeler.addLe(constraint, this.y[j][i], String.format("service_place_constraint_type{%d}_node{%d}", i, j));
            }
        }
    }

    /**
     * Service Constraint + Type constraint
     * @throws IloException
     */
    private void serviceTypeConstraint() throws IloException {
        int v = 0;
        for (int h = 0; h < this.cfg.getT(); h++) {
            for (int k = 0; k < this.cfg.getChains().get(h).nodes(); k++) {
                IloLinearIntExpr constraint = this.modeler.linearIntExpr();

                for (int i = 0; i < this.cfg.getF(); i++) {
                    for (int j = 0; j < this.cfg.getW(); j++) {
                        // adds z variable into service constraint if type of z is equal to type of node v
                        if (this.cfg.getChains().get(h).getNode(k).getIndex() == i) {
                            constraint.addTerm(1, this.z[i][j][k + v]);
                        }
                    }
                }

                // if chain `h` is serviced then all of its nodes should be serviced
                this.modeler.addEq(constraint, this.x[h], String.format("service_constraint_chain{%d}_vnf{%d}", h, k));
            }
            v += this.cfg.getChains().get(h).nodes();
        }
    }

    /**
     * make all physical node that does not have egress support to have zero instance with egress type
     * @throws IloException
     */
    private void egressConstraint() throws IloException {
        for (int i = 0; i < this.cfg.getF(); i++) {
            if (!Types.get(i).isEgress()) { // do the following only for egress types
                continue;
            }
            for (int j = 0; j < this.cfg.getW(); j++) {
                // physical node without have egress support must have zero instance with egress type
                if (!this.cfg.getNodes().get(j).isEgress()) {
                    physicalNodeWithoutTypeConstraint(i, j, "egress");
                }
            }
        }
    }

    /**
     * make all physical node that does not have ingress support to have zero instance with ingress type
     * @throws IloException
     */
    private void ingressConstraint() throws IloException {
        for (int i = 0; i < this.cfg.getF(); i++) {
            if (!Types.get(i).isIngress()) { // do the following only for ingress types
                continue;
            }
            for (int j = 0; j < this.cfg.getW(); j++) {
                // physical node without have ingress support must have zero instance with ingress type
                if (!this.cfg.getNodes().get(j).isIngress()) {
                    physicalNodeWithoutTypeConstraint(i, j, "ingress");
                }
            }
        }
    }

    /**
     * make the physical node with index _j_ to have zero instance with type _i_
     * this function is used by ingress/egress constraints
     * @param i type index
     * @param j physical node index
     */
    private void physicalNodeWithoutTypeConstraint(int i, int j, String type) throws IloException {
        IloLinearIntExpr constraint = this.modeler.linearIntExpr();

        constraint.addTerm(1, this.y[j][i]);

        this.modeler.addEq(constraint, 0, String.format("%s_constraint_type{%d}_node{%d}", type, i, j));
    }

    /**
     * VNF support constraint
     * @throws IloException
     */
    private void vnfSupportConstraint() throws IloException {
        for (int i = 0; i < this.cfg.getW(); i++) {
            if (!this.cfg.getNodes().get(i).isVnfSupport()) {
            	IloLinearIntExpr constraint = this.modeler.linearIntExpr();

                for (int j = 0; j < this.cfg.getF(); j++) {
                    constraint.addTerm(1, this.y[i][j]);
                }

                this.modeler.addEq(constraint, 0, String.format("vnf_support_constraint_node{%d}", i));
            }
        }
    }

    /**
     * Flow conservation
     * @throws IloException
     */
    private void flowConservation() throws IloException {
        // linkConstraint == nodeConstraint
        int v = 0;
        int u = 0;
        for (Chain chain : this.cfg.getChains()) {
            for (int i = 0; i < this.cfg.getW(); i++) {  // Source of Physical link
                for (int l = 0; l < chain.links(); l++) { // Virtual link
                    int virtualSource = chain.getLink(l).getSource() + v;
                    int virtualDestination = chain.getLink(l).getDestination() + v;

                    IloLinearIntExpr linkConstraint = this.modeler.linearIntExpr();
                    IloLinearIntExpr nodeConstraint = this.modeler.linearIntExpr();

                    // link constraint
                    for (int j = 0; j < this.cfg.getW(); j++) { // Destination of Physical link
                        if (this.cfg.getE()[i][j] > 0) {
                            linkConstraint.addTerm(1, this.tau[i][j][u + l]);
                        }
                        if (this.cfg.getE()[j][i] > 0) {
                            linkConstraint.addTerm(-1, this.tau[j][i][u + l]);
                        }
                    }

                    // node constraint
                    for (int k = 0; k < this.cfg.getF(); k++) {
                        if (chain.getNode(virtualSource - v).getIndex() == k) {
                            nodeConstraint.addTerm(1, this.z[k][i][virtualSource]);
                        }
                        if (chain.getNode(virtualDestination - v).getIndex() == k) {
                            nodeConstraint.addTerm(-1, this.z[k][i][virtualDestination]);
                        }
                    }

                    this.modeler.addEq(linkConstraint, nodeConstraint, "flow_conservation");
                }
            }
            v += chain.nodes();
            u += chain.links();
        }
    }

    /**
     * Link Bandwidth Constraint
     * @throws IloException
     */
    private void linkBandwidthConstraint() throws IloException {
        for (int i = 0; i < this.cfg.getW(); i++) {
            for (int j = 0; j < this.cfg.getW(); j++) {
                if (this.cfg.getE()[i][j] > 0) {
                    IloLinearIntExpr constraint = this.modeler.linearIntExpr();

                    int u = 0;
                    int v = 0;
                    for (Chain chain : this.cfg.getChains()) {
                        // VNFs
                        for (int k = 0; k < chain.links(); k++) {
                            constraint.addTerm(chain.getLink(k).getBandwidth(), this.tau[i][j][k + u]);
                        }

                        v += chain.nodes();
                        u += chain.links();
                    }

                    this.modeler.addLe(constraint, this.cfg.getE()[i][j], "link_bandwidth_constraint");
                }
            }
        }
    }

    public IloIntVar[] getX() {
        return x;
    }

    public IloIntVar[][] getY() {
        return y;
    }

    public IloIntVar[][][] getZ() {
        return z;
    }

    public IloIntVar[][][] getTau() {
        return tau;
    }
}
