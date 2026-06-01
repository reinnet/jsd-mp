# Simulation

## Introduction

Problem formulation has been implemented in [IBM CPLEX](https://www.ibm.com/analytics/cplex-optimizer).
This formulation can be configured in many aspects and reflects the VNFM placement problem with VNFM
in a data center. Results are placed in the results folder along with their configuration.

## Up and Running

For running simulation, you need a working installation of CPLEX and Java/Maven on your system
then you can run the simulation with the following command:

```sh
cd simulation
CPLEX_LIB="$HOME/ibm/ILOG/CPLEX_Studio128/cplex/bin/x86-64_linux"
test -f cplex.jar || echo "Please provide 'cplex.jar' in the current directory"
gradle build
sed -i "s#cplexLibrary =.*#cplexLibrary = ${CPLEX_LIB}#g" build.gradle
gradle run --args config
```

## Exact Results
There are the reults of using this simulation for solving the real problem of placing the NFV chains on k-ary fat tree.
In these results there is no constraint on license fee of VNFMs.

> 4 vCPU, 16GB of RAM, without GC limit, 12GB heap size, 8 chains

| k-ary fat tree | time     |
|----------------|----------|
| 6              | 4 sec    |
| 8              | 7 sec    |
| 10             | 1 min    |
| 12             | 5:20 min |

> 4 vCPU, 16GB of RAM, without GC limit, 12GB heap size, 12-ary fat tree

| chains | time         |
|--------|--------------|
| 8      | 5:20 min     |
| 10     | 7:06 min     |
| 11     | 16:33 min    |
| 12     | OOM Killed   |

> 8 vCPU, 22GB of RAM, without GC limit, 12GB heap size, 12-ary fat tree

| chains | time         |
|--------|--------------|
| 12     | 14:53 min    |

## Heuristic Results

Each instance has a price between 20 to 30.
We have 100 chains, and each chain has a length between 5 to 7. I have run each test with 3 different versions of the algorithm and report the proportion of the final revenue to optimal revenue.

| revenue per instance | Bari | Parham | Parham + Better VNFM Placement |
|----------------------|------|--------|--------------------------------|
| 10 - 20              | 60   | 65     | 68                             |
| 15 - 25              | 61   | 81     | 82                             |

As the numbers show, the placement algorithm do better when the per instances revenue increase.
