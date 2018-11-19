
for thr in 0; 
do
    suffix="_nocut"
    CONDOR="--condor"
    PROXY="--proxy"
    OUTDIR="/eos/user/k/klute/Nero/2018_11_HGC/Hbb_pu200_pt${pt}_thr${thr}${suffix}/"
    mkdir -p $OUTDIR
    python sendOnBatch.py ${CONDOR} ${PROXY} -n 200 -q 1nd --options="maxEvents=100 thr=$thr pu=0 what=ggh_hbb" -e fake --put-in=${OUTDIR} -d mysub/Hbb_pu200_thr${thr}${suffix} -i testHGCalL1T_cfg.py -o hgcalNtuples.root
done
