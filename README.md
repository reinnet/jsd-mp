# Joint Service Deployment - Manager Placement

[![Drone (cloud)](https://img.shields.io/drone/build/reinnet/jsd-mp.svg?style=flat-square&logo=drone)](https://cloud.drone.io/reinnet/jsd-mp)

## Introduction

Here we want to solve the placement problem of Virtual Network Functions and in the same time
provide them with VNFMs. This is a NP-Hard problem so here we implement some heuristics to make
solution faster.

Methods:

- Optimal
- MASREN
- Abu (baed on nearset work but as is)
- Optimized Abu (based on nearest work but with some moditifcation)

## Abu Method

Abu-Lebdeh describe a method based on tabu-search to improve VNFM placement on datacenter that already has VNF placement.
In our work we are considering the VNF placement jointly with VNFM placement so we are going to change it to consider the placement and after that compare it with our method.
In Abu-Lebdeh method there is no way to discard a chain so it can generate infeasible results so we are reserving resources for VNFM to prevent the infeasible situation.

The following variables are available `./jsd_mp/abu` solution to configure it so you need to change them by hand (with `--options`) and report them into results.

```python
n_iter
reserve_percentage
```

## Results

Here we use Jupyter Notebook to collect all results from the optimal and heuristic solutions that you can find them at `/results`.

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
