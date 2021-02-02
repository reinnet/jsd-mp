# Joint Service Deployment - Manager Placement

[![Drone (cloud)](https://img.shields.io/drone/build/reinnet/jsd-mp.svg?style=flat-square&logo=drone)](https://cloud.drone.io/reinnet/jsd-mp)

## Introduction

Here we want to solve the placement problem of Virtual Network Functions and in the same time
provide them with VNFMs. This is a NP-Hard problem so here we implement some heuristics to make
solution faster.

## Abu Method

Abu-Lebdeh describe a method based on tabu-search to improve VNFM placement on datacenter that already has VNF placement.
In our work we are considering the VNF placement jointly with VNFM placement so we are going to change it to consider the placement and after that compare it with our method.
In Abu-Lebdeh method there is no way to discard a chain so it can generate infeasible results so we are reserving resources for VNFM to prevent the infeasible situation.

The following variables are available `./jsd_mp/abu` solution to configure it so you need to change them by hand and report them into results.

```python
n_iter
reserve_percentage
```

## Results

Here we use Jupyter Notebook to collect all results from the optimal and heuristic solutions that you can find them at `/results`.

## How to Run

```sh
python jsd_mp/main.py -ss rari -c config/
```
