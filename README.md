# ECON-script

## Production 

### Area Setup

>https://twiki.cern.ch/twiki/bin/view/CMS/HGCALTriggerPrimitivesSimulation#Installation_for_users

### script

Copy the scripts:

~~~bash
cd L1Trigger/L1THGCal/
cmsenv
git clone git@github.com:amarini/ECON-script production
cd production
~~~

Run production (modify cmd.sh):

~~~bash
source cmd.sh
~~~

cmd.sh is setup for running on lxplus/lxbatch/condor

setup for productions

* Particle Gun: what=pgun pdgid=11 pt=30
* Higgs GGH Hmm: what=ggh_hmm
* Higgs VBF Hmm: what=vbf_hmm
* Higgs GGH Hbb (at least OneB in the right eta region): what=ggh_hbb 
* Pileup: pu=xxx (for the time being only 0. Need to find/produce suitable MinBias RelVal)
