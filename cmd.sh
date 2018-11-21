
mkdir /eos/user/k/klute/Nero/2018_11_HGC
for thr in 0; 
do
#for thr in 1 2 3 5 10; 
for pu in 200; 
do
    suffix="_nocut"
    CONDOR="--condor"
    #CONDOR=""
    PROXY="--proxy"
    OUTDIR="/eos/user/k/klute/Nero/2018_11_HGC/Hbb_pu${pu}_pt${pt}_thr${thr}${suffix}/"
    mkdir -p $OUTDIR
    python sendOnBatch.py ${CONDOR} ${PROXY} -n 200 -q 1nd --options="maxEvents=100 thr=$thr pu=${pu} what=ggh_hbb" -e fake --put-in=${OUTDIR} -d mysub/Hbb_pu${pu}_thr${thr}${suffix} -i testHGCalL1T_cfg.py -o hgcalNtuples.root
done
done
