## Andrea Carlo Marini -- Wed Nov 21 14:17:55 CET 2018
if __name__=="__main__":
    import optparse

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--input', dest='input_file', help='Input file',default=None)
    parser.add_option('--output', dest='output_file', help='Output file. Override parameters specifications.',default=None)
    (opts, args) = parser.parse_args()

import ROOT
import numpy as np
import math
from glob import glob
import sys
from datetime import datetime

## using pyjet
from pyjet import cluster, DTYPE_EP, DTYPE_PTEPM
from pyjet import (ClusterSequence, ClusterSequenceArea,
                                JetDefinition, PseudoJet,
                                USING_EXTERNAL_FASTJET)

ROOT.gSystem.Load("bin/libFastjetInterface.so")
fi = ROOT.fastjet_interface();

class BaseRun:
    def __init__(self,outer):
        self.outer=outer
        self.histos={}

    def run(self):
        return self

    def finalize(self):
        for h_str in self.histos  :
            h=self.histos[h_str]
            h.Write()
        return self

class SubStructures(BaseRun):
    def __init__(self,outer):
        BaseRun.__init__(self,outer)

        self.histos["Tau32"]=ROOT.TH1D("Tau32","Tau32;tau32;events",100,0,1)
        self.histos["Tau21"]=ROOT.TH1D("Tau21","Tau21;tau21;events",100,0,1)

    def run(self):
        #dRmin=0.8 # for matching
        #for igen, gj in enumerate(self.outer.genjets_):
        #    if gj.Pt()<30: continue
        #    if abs(gj.Eta()) > 3.0 or abs(gj.Eta()) < 1.5 : continue
        #    for itr, jet in enumerate(self.outer.jets_):
        #        if jet.Pt() < 50: continue
        #        if gj.DeltaR(jet) < dRmin: 
        for ijet, jet in enumerate(self.outer.jets_):
            if jet.Pt() < 50: continue
            if abs(jet.Eta()) < 1.5: continue
            if abs(jet.Eta()) > 3.0: continue
            tau32=self.outer.jetprop_[ijet]["tau32"]
            tau21=self.outer.jetprop_[ijet]["tau21"]

            #print "Filling jet",jet.Pt()
            self.histos["Tau21"].Fill(tau21)
            self.histos["Tau32"].Fill(tau32)


class jet_clustering:
    ''' Jet Clustering '''
    def __init__(self, input_file, outfile):
        self.chain = ROOT.TChain("hgcalTriggerNtuplizer/HGCalTriggerNtuple")
        nfiles=0
        for template_name in input_file.split(','):
            if '*' in template_name:
                for f in glob(template_name):
                    nfiles+=self.chain.Add(f)
            else: ## regular files, xrootd, ...
                nfiles+=self.chain.Add(template_name)

        print "-> Running on",nfiles,"files"
        self.output = ROOT.TFile(outfile,"RECREATE")
        self.output.cd()
        self.clusterR=0.8
        self.time_=None

        self.cfg={"torun":[]}

    def clear(self):
        self.jets_=[]
        self.jetprop_=[] # jetprop_[0]["xxx"] #radius, axis1, axis2, ptD, mult
        self.genjets_=[]

    def do_clusters(self,ptV,etaV,phiV,energyV ):
        ''' run the clustering on the input std vectors'''
        n=len(ptV)
        if len(etaV) != n : raise ValueError('input vectors have different length')
        if len(phiV) != n : raise ValueError('input vectors have different length')
        if len(energyV) != n : raise ValueError('input vectors have different length')
        
        input_particles = []
        for i in range(0,n):
            p = ROOT.TLorentzVector()
            p.SetPtEtaPhiE(ptV[i],etaV[i],phiV[i],energyV[i])
            input_particles.append( (p.Pt(),p.Eta(),p.Phi(),p.M())  )
       
        ip = np.array( input_particles, dtype=DTYPE_PTEPM)
        sequence=cluster( ip, algo="antikt",ep=False,R=self.clusterR)
        jets = sequence.inclusive_jets()
        
        self.jets_=[]
        self.jetprop_=[]
        for ijet,j in enumerate(jets):
            p=ROOT.TLorentzVector()
            p.SetPtEtaPhiM( j.pt,j.eta,j.phi,j.mass)
            self.jets_.append(p)
            #input_particles = np.array([(k.pt(),k.eta(),k.phi(),k.m()) for k in j.constituents()], dtype=DTYPE_PTEPM)
            input_particles=ROOT.std.vector(PseudoJet)()
            for k in j.constituents():
                input_particles.push_back(ROOT.fastjet.PseudoJet(k.px,k.py,k.pz,k.e))
            #input_particles = [k for k in j.constituents()]
            tau3=fi.getTaus(input_particles,3)
            tau2=fi.getTaus(input_particles,2)
            tau1=fi.getTaus(input_particles,1)
            #print "DEBUG:","pt=%f,eta=%f,phi=%f"%(j.pt,j.eta,j.phi)
            #print "DEBUG:", "n=",len(j.constituents())
            #print "DEBUG:", "tau=",tau3,tau2,tau1
            tau32 = tau3/tau2 if tau2> 0 else -99
            tau21 = tau2/tau1 if tau1> 0 else -99
            self.jetprop_.append({"tau32":tau32,"tau21":tau21})
        return self

    def do_genjets(self,ptV,etaV,phiV,energyV):
        ''' just grab genjets and put in the class collection'''
        for pt, eta, phi, energy in zip( ptV,etaV,phiV,energyV):
            p = ROOT.TLorentzVector()
            p.SetPtEtaPhiE(  pt, eta, phi, energy)
            self.genjets_ .append(p) 
        return self

    def print_progress(self,done,tot,n=30,every=200):
        if done % every != 0  and done < tot-1: return
        a=int(float(done)*n/tot )
        l="\r["
        if a==n: l += "="*n
        elif a> 0: l +=  "="*(a-1) + ">" + " "*(n-a)
        else: l += " "*n
        l+="] %.1f%%"%(float(done)*100./tot)
        if self.time_ == None: self.time_ = datetime.now()
        else: 
            new = datetime.now()
            delta=(new-self.time_)
            H=delta.seconds/3600 
            M=delta.seconds/60 -H*60
            S=delta.seconds - M*60-H*3600
            H+= delta.days*24
            if H>0:
                l+= " in %dh:%dm:%ds "%(H,M,S) 
            else:
                l+= " in %dm:%ds "%(M,S) 
            S=int( (delta.seconds+24*3600*delta.days)*float(tot-done)/float(done) )
            M= S/60
            S-=M*60
            H= M/60
            M-=H*60
            l+= " will end in %dh:%dm:%ds                      "%(H,M,S)
        if a==n: l+="\n"
        print l,
        sys.stdout.flush()
        return self

    def loop(self):
        #todo=[efficiency_pteta(self) ] 
        todo=[]
        print "-> Running on",
        for x in self.cfg["torun"]:
            print x,
            exec("todo.append("+x+"(self))")
        print 
        
        nentries=self.chain.GetEntries()
        for ientry,entry in enumerate(self.chain):
            self.print_progress(ientry,nentries)
            self.clear()

            c3d_pt_ = np.array(entry.cl3d_pt)
            c3d_eta_ = np.array(entry.cl3d_eta)
            c3d_phi_ = np.array(entry.cl3d_phi)
            c3d_energy_ = np.array(entry.cl3d_energy)

            #if "matrix_calibration" in self.cfg.torun or self.doCalibration or 'layer_deposits' in self.cfg.torun:
            #    c3d_clusters_ = np.array(entry.cl3d_clusters)
            #    c3d_nclu_ = np.array(entry.cl3d_nclu)

            #    self.cl_pt_ = np.array(entry.cl_pt)
            #    self.cl_eta_ = np.array(entry.cl_eta)
            #    self.cl_phi_ = np.array(entry.cl_phi)
            #    self.cl_energy_ = np.array(entry.cl_energy)
            #    self.cl_layer_ = np.array(entry.cl_layer)
            #    self.cl_ncells_ = np.array(entry.cl_ncells)
            #    self.cl_cells_ = np.array(entry.cl_cells) ### ?

            genjets_pt_ = np.array(entry.genjet_pt)
            genjets_eta_ = np.array(entry.genjet_eta)
            genjets_phi_ = np.array(entry.genjet_phi)
            genjets_energy_ = np.array(entry.genjet_energy)

            ## produce trigger jets and gen jets
            self.do_clusters(c3d_pt_,c3d_eta_,c3d_phi_,c3d_energy_).do_genjets( genjets_pt_,genjets_eta_,genjets_phi_,genjets_energy_)

            if ientry< 10:
                print "ENTRY",ientry
                print "JETS", len(self.jets_)
                print "JETS PROP", self.jetprop_
                print "---------------------------------"

            ## produce plots
            for x in todo: x.run()
        self.output.cd()
        for x in todo: x.finalize()
        return self

if __name__=="__main__":

    jc=jet_clustering(opts.input_file,opts.output_file)
    jc.cfg['torun']=["SubStructures"]
    jc.loop()

