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
