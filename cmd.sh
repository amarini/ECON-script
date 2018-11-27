
mkdir /eos/user/k/klute/Nero/2018_11_HGC
#for thr in 0; 
for thr in 0 5 10; 
do
for pu in 0 200; 
do
    suffix="_nocut"
    CONDOR="--condor"
    #CONDOR=""
    PROXY="--proxy"
    #OUTDIR="/eos/user/k/klute/Nero/2018_11_HGC/Hbb_pu${pu}_pt${pt}_thr${thr}${suffix}/"
    #mkdir -p $OUTDIR
    #python sendOnBatch.py ${CONDOR} ${PROXY} -n 200 -q 1nd --options="maxEvents=100 thr=$thr pu=${pu} what=ggh_hbb" -e fake --put-in=${OUTDIR} -d mysub/Hbb_pu${pu}_thr${thr}${suffix} -i testHGCalL1T_cfg.py -o hgcalNtuples.root

    OUTDIR="/eos/user/k/klute/Nero/2018_11_HGC/HbbBoost_pu${pu}_pt${pt}_thr${thr}${suffix}/"
    mkdir -p $OUTDIR
    python sendOnBatch.py ${CONDOR} ${PROXY} -n 200 -q 1nd --options="maxEvents=500 thr=$thr pu=${pu} what=ggh_hbb_boost pt=500" -e fake --put-in=${OUTDIR} -d mysub/HbbBoost_pu${pu}_thr${thr}${suffix} -i testHGCalL1T_cfg.py -o hgcalNtuples.root
done
done

### NU GUN
#for thr in 0 5 10; 
#do
#    pu=200
#    suffix="_nocut"
#    PROXY="--proxy"
#    CONDOR="--condor"
#    OUTDIR="/eos/user/k/klute/Nero/2018_11_HGC/NuGun_pu${pu}_pt${pt}_thr${thr}${suffix}/"
#    mkdir -p $OUTDIR
#    python sendOnBatch.py ${CONDOR} ${PROXY} -n 200 -q 1nd --options="maxEvents=100 thr=$thr pu=${pu} what=pgun pdgid=12" -e fake --put-in=${OUTDIR} -d mysub/NuGun_pu${pu}_thr${thr}${suffix} -i testHGCalL1T_cfg.py -o hgcalNtuples.root
#done
