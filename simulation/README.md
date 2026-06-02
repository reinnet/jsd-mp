# Simulation

## Introduction

Problem formulation has been implemented in [IBM CPLEX](https://www.ibm.com/analytics/cplex-optimizer).
This formulation can be configured in many aspects and reflects the VNFM placement problem with VNFM
in a data center. Results are placed in the results folder along with their configuration.

## Up and Running

For running the simulation, you need a working installation of CPLEX (tested with
CPLEX Studio 12.8) and Java on your system; a Gradle wrapper (`./gradlew`) is
included, so no separate Gradle install is required. Then run:

```sh
cd simulation
CPLEX_LIB="$HOME/ibm/ILOG/CPLEX_Studio128/cplex/bin/x86-64_linux"
test -f cplex.jar || echo "Please provide 'cplex.jar' in the current directory"
# point the build at your CPLEX native library (keep the quotes: it is a Groovy string)
sed -i "s#cplexLibrary = .*#cplexLibrary = '${CPLEX_LIB}'#" build.gradle
./gradlew run --args config
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

With 100 chains, each of length 5 to 7, three versions of the heuristic were run and their final revenue is reported as a proportion of the optimal revenue, for two per-instance revenue ranges. These results are also reported in the paper under [`../paper/`](../paper/).

| revenue per instance | Bari | MASMAN (VNF phase) | MASMAN (full) |
|----------------------|------|--------------------|---------------|
| 10 - 20              | 60   | 65     | 68                             |
| 15 - 25              | 61   | 81     | 82                             |

As the numbers show, the heuristic does better as the per-instance revenue increases.
