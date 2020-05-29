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
# |- jsd-mp/
# |- jsd-mp.simulation/
# chainer generates random chain
set -e

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
jsd_mp="$( cd $current_dir/../.. && pwd )"

usage() {
        echo "usage: $0 run [-t times (10)] [-n number of chains (100)]"
        echo "usage: $0 parse"
        echo "usage: $0 clean"
}

run() {
        number_of_chains=100
        times=10

        while getopts "ht:n:" argv; do
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
        echo "execute simulations for ${number_of_chains} chains ${times} times"

        for i in $(seq $times); do
                echo run $i
                # generate a random chain with github.com/reinnet/chainer
                cd $jsd_mp/../chainer/
                ./chainer -n $number_of_chains
                cd -

                mv $jsd_mp/../chainer/chains.yaml chains-$i.yaml
                # execute exact simulation
                cp chains-$i.yaml $jsd_mp/../simulation/config/chains.yaml
                cd $jsd_mp/../simulation
                gradle run --args config
                cd -

                mv $jsd_mp/../simulation/joint-result.txt joint-result-$i.txt
                mv $jsd_mp/../simulation/disjoint-result.txt disjoint-result-$i.txt
        done
}

parse() {
        for ty in joint disjoint; do
                echo
                echo $ty
                echo
                costs=""
                chains=""
                vnfms=""

                for result in $(ls $ty-result-*); do
                        costs="$costs, $(cat $result | grep "cost" | cut -d " " -f 4 -)"
                        chains="$chains, $(cat $result | grep "chains are accepted" | cut -d " " -f 1 -)"
                        vnfms="$vnfms, $(cat $result | grep "VNFMs is used" | cut -d " " -f 1 -)"
                done
                echo
                echo costs = [ $costs ]
                echo chains = [ $chains ]
                echo vnfms = [ $vnfms ]
                echo
        done
}

echo
echo "> jsd-mp root directory located at $jsd_mp"
echo "> assume the following structure:"
echo "  |- chainer/"
echo "  |- jsd-mp/"
echo "  |- jsd-mp.simulation/"
echo

case $1 in
        parse)
                parse
                ;;
        run)
                shift
                run $@
                ;;
        clean)
                rm *.yaml
                rm *.txt
                ;;
esac
