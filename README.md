# Joint Service Deployment - Manager Placement

[![Drone (cloud)](https://img.shields.io/drone/build/reinnet/jsd-mp.svg?style=flat-square&logo=drone)](https://cloud.drone.io/reinnet/jsd-mp)
[![Codecov](https://img.shields.io/codecov/c/gh/reinnet/jsd-mp?logo=codecov&style=flat-square)](https://codecov.io/gh/reinnet/jsd-mp)


## Introduction

Here we want to solve the placement problem of Virtual Network Functions and in the same time
provide them with VNFMs. This is a NP-Hard problem so here we implement some heuristics to make
solution faster.

Methods that we are going to use it at jsd-mp:

- Optimal with CPLEX implemented at [jsd-mp.simulation](https://github.com/reinnet/jsd-mp.simulation)
- MASMAN implemented as `rari` method
- Abu implemented as `abu` method, baed on nearset work but without modification
- Optimized Abu as `oabu` method, based on nearest work but with some modification to have fare comparation

In the jsd-mp problem some functions can be managened and there are the functions that need VNFM,
so the following code snippet find these functions in a chain.

```python
itertools.compress(
        placement.nodes, chain.manageable_functions
)
```

Also we have the following configuration for our VNFM constraints as default:

```yaml
ram: 4
cores: 2
capacity: 10
radius: 100
bandwidth: 10
licenseFee: 100
```

## Abu Method

Abu-Lebdeh describe a method based on tabu-search to improve VNFM placement on datacenter that already has VNF placement.
In our work we are considering the VNF placement jointly with VNFM placement so we are going to change it to consider the placement and after that compare it with our method.
In Abu-Lebdeh method there is no way to discard a chain so it can generate infeasible results so we are reserving resources for VNFM to prevent the infeasible situation.

The following variables are available `./jsd_mp/abu` solution to configure it so you need to change them by hand (with `--options`) and report them into results.

```python
n_iter
reserve_percentage
```

## Optimized Abu Method

Abu-Lebdeh uses tabu-search to improve its VNFM placement but at this method it doesn't use consider our problem constraints,
so here we are going to optimize it based on our constraints.

## Results

Here we use Jupyter Notebook to collect all results from the optimal and heuristic solutions that you can find them at `/results`.
After each run results are written into a `report.csv` that can be loaded into jupyter notebook.

## [Topologies](https://github.com/reinnet/topology)

There are two topology that are considering here, fattree and usnet. There is another project that generate networks with these two topology.
The generated configuration that must be copied and used with this project as follow:

```sh
topology fattree -k 4
cp topology.yaml ../jsd-mp/config/topology.yml
```

Please note that you must also consider to store these configuration for future re-runs.

## [Chains](https://github.com/reinnet/chainer)

We are going to place SFCs on our network and there is project that generate chains.
The generated chains chains can be copied and used with this project as follow:

```sh
chainer -n 100
cp chains.yaml ../jsd-mp/config/chains.yml
```

## How to Run

In the command line you can run jsd-mp with:

```sh
python jsd_mp/main.py -ss rari -c config/ -r 10
```

but if you want to have its result in jupyter notebook then you must:

```sh
python -m ipykernel install --user --name=jsd-mp-krnl
```

In your notebook, Kernel -> Change Kernel. Your kernel should now be an option.
