#!/bin/bash

mkdir inputs
for dir in `ls /eos/user/k/klute/Nero/2018_11_HGC`; do

echo 
echo "----------------------------------"
echo "|      $dir    |"
echo "----------------------------------"
echo 
#python substructure.py --input='/eos/user/k/klute/Nero/2018_11_HGC/Hbb_pu0_pt_thr0_nocut/*.root' --output=Hbb_pu0_pt_thr0.root
python substructure.py --input="/eos/user/k/klute/Nero/2018_11_HGC/${dir}/*.root" --output=inputs/${dir}.root

done
