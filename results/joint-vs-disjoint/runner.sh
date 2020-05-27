#!/bin/bash
# In The Name of God
# ========================================
# [] File Name : runner.sh
#
# [] Creation Date : 22-05-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================
# This script run exact solution for given number of chains.
# Please note that this script required the following hierarchy:
# |- chainer/
# |- jsd-mp/results/runner.sh
# |- jsd-mp.simulation/
# chainer generates random chain


usage() {
        echo "usage: $0 [-t times] [-n number of chains]"
}

number_of_chains=100
times=10

while getopts "t:n:" argv; do
        case $argv in
                t)
                        times=$OPTARG
                        ;;
                n)
                        number_of_chains=$OPTARG
                        ;;
                h)
                        usage
                        exit
                        ;;
        esac
done

for i in $(seq $times); do
        echo run $i
        # generate a random chain with github.com/reinnet/chainer
        cd ../../chainer/
        ./chainer -n $number_of_chains
        cd -
        mv ../../chainer/chains.yaml chains-$i.yaml
        # execute exact simulation
        cp chains-$i.yaml ../../simulation/config/chains.yaml
        cd ../../simulation
        gradle run --args config
        cd -
        mv ../../simulation/joint-result.txt joint-result-$i.txt
        mv ../../simulation/disjoint-result.txt disjoint-result-$i.txt
done
