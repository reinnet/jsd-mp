# Joint Service Deployment - Manager Placement

[![Drone (cloud)](https://img.shields.io/drone/build/reinnet/jsd-mp.svg?style=flat-square&logo=drone)](https://cloud.drone.io/reinnet/jsd-mp)

## Introduction

Here we want to solve the placement problem of Virtual Network Functions and in the same time
provide them with VNFMs. This is a NP-Hard problem so here we implement some heuristics to make
solution faster.

## Results

Here we use Jupyter Notebook to collect all results from the optimal and heuristic solutions.

## How to Run

```sh
python jsd_mp/main.py -ss rari -c config/
```
