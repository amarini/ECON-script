from optparse import OptionParser

usage = 'usage: %prog [options]'
parser = OptionParser(usage)
parser.add_option('--input', dest='input_dir', help='Input Directory',default="inputs")
parser.add_option('--output', dest='output_file', help='Output file.',default="c1.pdf")
(opts, args) = parser.parse_args()

import os,sys
import ROOT
from glob import glob
import re

files=glob("%s/Hbb_pu0_pt_thr*_nocut.root"%opts.input_dir)
files.extend( glob("%s/Hbb_pu200_pt_thr*_nocut.root"%opts.input_dir) )
#Hbb_pu0_pt_thr0_nocut.root
c=ROOT.TCanvas()
histos=[]

same=""
colors=[38,46,8,ROOT.kOrange,ROOT.kGray,ROOT.kMagenta,ROOT.kBlack]
leg=ROOT.TLegend(.1,.1,.5,.5)
fOut=ROOT.TFile.Open(re.sub('\.pdf\|\.png','.root',opts.output_file),"RECREATE")

for ifile,f in enumerate(files):
    print "Opening file",f
    thr=re.sub('_.*','',re.sub('.*thr','',f))
    label="Threshold %s"%thr 
    if 'pu200' in f: label+="Pileup 200"
    if int(thr)==1 or int(thr)==2 or int(thr)==3: continue

    fIn=ROOT.TFile.Open(f)
    fOut.cd()
    h=fIn.Get("Tau21").Clone("Tau21_"+f)

    h.SetLineWidth(2)
    h.SetLineColor(colors[ifile%len(colors)])

    h.DrawNormalized("HIST " + same)
    #h.Draw("HIST " + same)
    histos.append(h)

    leg.AddEntry(h,label)
    if same=="":same="SAME"
    #raw_input ("ok?")

leg.Draw()
c.Modified()
c.Update()

raw_input("ok?")

fOut.cd()
c.Write()
for h in histos: h.Write()
c.SaveAs(opts.output_file)
c.SaveAs(re.sub('\.pdf','.png',opts.output_file))
