import FWCore.ParameterSet.Config as cms 
from Configuration.StandardSequences.Eras import eras

process = cms.Process('DIGI',eras.Phase2)

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.register('pt', 50., VarParsing.multiplicity.singleton,VarParsing.varType.float,"Gun Pt")
options.register('pu', 0, VarParsing.multiplicity.singleton,VarParsing.varType.int,"Pileup")
options.register('thr', 0, VarParsing.multiplicity.singleton,VarParsing.varType.int,"Thr")
options.register('pdgid', 11, VarParsing.multiplicity.singleton,VarParsing.varType.int,"Pdgid")
options.register('what', 11, VarParsing.multiplicity.singleton,VarParsing.varType.string,"pgun") # pgun, ggh_hbb, ggh_hmm, vbf_hmm
options.parseArguments()

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
if options.pu ==0:
    process.load('SimGeneral.MixingModule.mixNoPU_cfi')
else:
    print "->Poisson pileup"
    process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D17_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC14TeV_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


#process.maxEvents = cms.untracked.PSet(
#    input = cms.untracked.int32(10)
#)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('SingleElectronPt10_cfi nevts:10'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.FEVTDEBUGoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    #outputCommands = process.FEVTDEBUGEventContent.outputCommands,
    outputCommands = cms.untracked.vstring(
        'keep *_*_HGCHitsEE_*',
        'keep *_*_HGCHitsHEback_*',
        'keep *_*_HGCHitsHEfront_*',
        'keep *_mix_*_*',
        'keep *_genParticles_*_*',
        'keep *_hgcalTriggerPrimitiveDigiProducer_*_*'
    ),
    fileName = cms.untracked.string('file:test.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("hgcalNtuples.root")
    )



# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

if options.what=='pgun':
    process.generator = cms.EDProducer("FlatRandomPtGunProducer",
            PGunParameters = cms.PSet(
                MaxPt = cms.double(options.pt +0.01),
                MinPt = cms.double(options.pt -0.01),
                PartID = cms.vint32(options.pdgid),
                MinEta = cms.double(1.5),
                MaxEta = cms.double(3.0),
                MaxPhi = cms.double(3.14159265359),
                MinPhi = cms.double(-3.14159265359)
                ),
            Verbosity = cms.untracked.int32(0),
            #psethack = cms.string('single electron pt 50'),
            psethack = cms.string('single electron (pdg=%d) pt %f'%(options.pdgid,options.pt)),
            AddAntiParticle = cms.bool(True),
            firstRun = cms.untracked.uint32(1)
            )
elif options.what=='ggh_hmm':
    process.generator = cms.EDFilter("Pythia8GeneratorFilter",
            comEnergy = cms.double(14000.0),
            crossSection = cms.untracked.double(1.0),
            filterEfficiency = cms.untracked.double(1.0),
            maxEventsToPrint = cms.untracked.int32(0),
            pythiaPylistVerbosity = cms.untracked.int32(0),
            pythiaHepMCVerbosity = cms.untracked.bool(False),
            PythiaParameters = cms.PSet(

                pythia8CommonSettingsBlock,
                pythia8CUEP8M1SettingsBlock,
                processParameters = cms.vstring(
                    'Main:timesAllowErrors    = 10000',
                    'HiggsSM:all=off',
                    'HiggsSM:gg2H=on',
                    '25:m0 = 125.0',
                    '25:onMode = off',
                    '25:onIfMatch = 13 -13',
                    ),

                parameterSets = cms.vstring(
                    'pythia8CommonSettings',
                    'pythia8CUEP8M1Settings',
                    'processParameters')
                )
            )
elif options.what == 'ggh_hbb':
    process.generator = cms.EDFilter("Pythia8GeneratorFilter",
            comEnergy = cms.double(14000.0),
            crossSection = cms.untracked.double(1.0),
            filterEfficiency = cms.untracked.double(1.0),
            maxEventsToPrint = cms.untracked.int32(0),
            pythiaPylistVerbosity = cms.untracked.int32(0),
            pythiaHepMCVerbosity = cms.untracked.bool(False),
            PythiaParameters = cms.PSet(

                pythia8CommonSettingsBlock,
                pythia8CUEP8M1SettingsBlock,
                processParameters = cms.vstring(
                    'Main:timesAllowErrors    = 10000',
                    'HiggsSM:all=off',
                    #'HiggsSM:ffbar2H=on',
                    'HiggsSM:ff2Hff(t:ZZ)=on',
                    'HiggsSM:ff2Hff(t:WW)=on',
                    '25:m0 = 125.0',
                    '25:onMode = off',
                    '25:onIfMatch = 5 -5',
                    ),

                parameterSets = cms.vstring(
                    'pythia8CommonSettings',
                    'pythia8CUEP8M1Settings',
                    'processParameters')
                )
            )

    process.filter1 = cms.EDFilter("MCSingleParticleFilter",
            MaxEta = cms.untracked.vdouble(3.0, 3.0,-1.5,-1.5),
            MinEta = cms.untracked.vdouble(1.5, 1.5, -3.0, -3.0),
            Status = cms.untracked.vint32(0, 0, 0, 0), # 0 = ignored
            MinPt = cms.untracked.vdouble(20.0, 20.0, 20.0, 20.0),
            ParticleID = cms.untracked.vint32(5, -5, 5, -5)
            )
elif options.what == 'ggh_hmm':
    process.generator = cms.EDFilter("Pythia8GeneratorFilter",
            comEnergy = cms.double(14000.0),
            crossSection = cms.untracked.double(1.0),
            filterEfficiency = cms.untracked.double(1.0),
            maxEventsToPrint = cms.untracked.int32(0),
            pythiaPylistVerbosity = cms.untracked.int32(0),
            pythiaHepMCVerbosity = cms.untracked.bool(False),
            PythiaParameters = cms.PSet(

                pythia8CommonSettingsBlock,
                pythia8CUEP8M1SettingsBlock,
                processParameters = cms.vstring(
                    'Main:timesAllowErrors    = 10000',
                    'HiggsSM:all=off',
                    'HiggsSM:gg2H=on',
                    '25:m0 = 125.0',
                    '25:onMode = off',
                    '25:onIfMatch = 13 -13',
                    ),

                parameterSets = cms.vstring(
                    'pythia8CommonSettings',
                    'pythia8CUEP8M1Settings',
                    'processParameters')
                )
            )
elif options.what == 'vbf_hmm':
    process.generator = cms.EDFilter("Pythia8GeneratorFilter",
            comEnergy = cms.double(14000.0),
            crossSection = cms.untracked.double(1.0),
            filterEfficiency = cms.untracked.double(1.0),
            maxEventsToPrint = cms.untracked.int32(0),
            pythiaPylistVerbosity = cms.untracked.int32(0),
            pythiaHepMCVerbosity = cms.untracked.bool(False),
            PythiaParameters = cms.PSet(

                pythia8CommonSettingsBlock,
                pythia8CUEP8M1SettingsBlock,
                processParameters = cms.vstring(
                    'Main:timesAllowErrors    = 10000',
                    'HiggsSM:all=off',
                    #'HiggsSM:ffbar2H=on',
                    'HiggsSM:ff2Hff(t:ZZ)=on',
                    'HiggsSM:ff2Hff(t:WW)=on',
                    '25:m0 = 125.0',
                    '25:onMode = off',
                    '25:onIfMatch = 13 -13',
                    ),

                parameterSets = cms.vstring(
                    'pythia8CommonSettings',
                    'pythia8CUEP8M1Settings',
                    'processParameters')
                )
            )
else: raise ValueError("Options %s unimplemented"%options.what)


import os,random
random.seed = os.urandom(10) #~10^14
process.RandomNumberGeneratorService.generator.initialSeed = random.randint(0,999999)

process.mix.digitizers = cms.PSet(process.theDigitizersValid)

if options.pu !=0:
    pufiles=[
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/96E7A469-F24B-E811-A4A8-0CC47A4D7630.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/0AE1444B-EF4B-E811-A7DA-0025905B858A.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/E69FC781-EB4B-E811-AE98-0CC47A78A440.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/8849BD86-EB4B-E811-A7AD-0CC47A78A426.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/328AC27D-EB4B-E811-9748-0CC47A4D76CC.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/5CC6AC78-EB4B-E811-959A-0CC47A4C8E26.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/3489A279-EB4B-E811-99ED-0CC47A7C3604.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/E8EB4993-EB4B-E811-9C9C-0CC47A7C340C.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/3C3C7F8C-EB4B-E811-ADD2-0CC47A4D7630.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/90FE9A7D-EB4B-E811-A68E-0CC47A4C8E66.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/103A267D-EB4B-E811-9C31-0CC47A78A456.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/E2A59179-EB4B-E811-94A7-0CC47A4C8E5E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/6C063186-EB4B-E811-9CD4-0CC47A4D765A.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/10AFC379-EB4B-E811-848F-0CC47A4D768E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/EAFB7785-EB4B-E811-B57A-0CC47A4D7632.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/FAC42E7D-EB4B-E811-B365-0CC47A7C3404.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/FC09B078-EB4B-E811-AFC7-0CC47A4D7630.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/A263657D-EB4B-E811-B5BD-0CC47A78A458.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/720E5C7F-EB4B-E811-A186-0CC47A4C8E20.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/0E6A9D78-EB4B-E811-BCD3-0CC47A4C8E86.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/3210EF7A-EB4B-E811-AC01-0CC47A4C8E7E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/BCF7785A-ED4B-E811-BEA1-0CC47A4C8E16.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/84B5987F-EB4B-E811-A53C-0CC47A4D76D2.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/D89F2A03-ED4B-E811-99EC-0CC47A4D75EE.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/56328362-ED4B-E811-9FC0-0CC47A7C351E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/CABA6C18-ED4B-E811-9237-0CC47A78A408.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/C053D313-ED4B-E811-8552-0CC47A78A4B8.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/80B67413-ED4B-E811-A743-0CC47A4C8F06.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/D6946A5C-ED4B-E811-9DCE-0CC47A4C8E70.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/3230AC8E-EB4B-E811-8898-0025905B85B2.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/7865F498-EB4B-E811-A529-0025905A48F0.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/C430638B-EB4B-E811-827E-0025905B85C6.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/3E82698C-EB4B-E811-9AFC-0025905A606A.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/02273292-EB4B-E811-B4CF-0025905A60EE.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/04BEC399-EB4B-E811-9BB4-0025905A60A0.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/56EE0B89-EB4B-E811-A6EC-0025905B85D6.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/0E7A2685-EB4B-E811-9C1C-0025905B861C.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/C26DC494-EB4B-E811-8635-0025905B85CA.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/34D54990-EB4B-E811-A659-0025905A6110.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/62BD858E-EB4B-E811-876D-0025905A6090.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/1AF61A95-EB4B-E811-96A9-0025905A60D2.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/D06E738B-EB4B-E811-AA6F-0025905B85A2.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/BAB32091-EB4B-E811-B08F-0025905A612A.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/2A039585-EB4B-E811-AE88-0025905A60AA.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/62D43A90-EB4B-E811-85C0-0025905A6110.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/48F9CE8C-EB4B-E811-82B0-0025905A605E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/5CB0368C-EB4B-E811-8B79-0025905A60A6.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/DC987D82-EB4B-E811-9FF5-0025905A607E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/047F0FD2-F14B-E811-AB54-0025905A612C.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/DCAB3E20-ED4B-E811-82A2-0025905B8576.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/C6B32C22-ED4B-E811-9647-0025905A48D8.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/6A21B221-ED4B-E811-AA57-0025905B8596.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/0092E26C-ED4B-E811-AB7F-0025905B85CC.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/E4A04574-EF4B-E811-94E5-0CC47A7C3430.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/CA208E22-ED4B-E811-ADD3-0025905A60D0.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/1EF5FB2C-ED4B-E811-A120-0025905A60B8.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/C0EAF621-ED4B-E811-B45E-0025905B8590.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/D8BCC626-ED4B-E811-9D82-0025905A48C0.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/AE253722-ED4B-E811-8284-0025905A6060.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/3C66DC67-ED4B-E811-88D2-0025905A612E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/90039469-ED4B-E811-8998-0025905B85D2.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/FAEACB21-ED4B-E811-B67A-0025905B85DE.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/488DD969-ED4B-E811-87EE-0025905A611E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/CE94B19B-F14B-E811-90B1-0CC47A4C8E26.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/64406899-F14B-E811-BD4C-0CC47A78A440.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/14C9D42A-ED4B-E811-BF75-0025905A6066.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/BE7E6E36-F24B-E811-91C5-0CC47A4C8E20.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/3CFB4028-F24B-E811-A042-0CC47A4D765A.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/4AAFC221-F14B-E811-AFFF-0CC47A7C3604.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/0CD59F06-F24B-E811-A53F-0CC47A4C8E66.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/E2FD7360-F24B-E811-AD83-0CC47A7C3604.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/BC2E9A70-F24B-E811-AC72-0CC47A4C8E86.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/EEEB5160-F24B-E811-9D44-0CC47A4C8E5E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/ACDAEC5E-F24B-E811-AE16-0CC47A78A456.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/BC453FFB-F14B-E811-A39D-0CC47A78A426.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/40332FD1-F14B-E811-A631-0CC47A7C3422.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/CA3F74D7-F14B-E811-999F-0CC47A4D76A0.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/D2434009-F24B-E811-9E29-0CC47A4D768E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/F6E26539-F24B-E811-9D68-0CC47A4C8E1E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/3AA577F9-F14B-E811-9D57-0CC47A4D76CC.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/963E74DA-F14B-E811-B79C-0CC47A78A4A6.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/4C338A0F-F24B-E811-80B5-0CC47A7C340C.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/FE7BAC10-F24B-E811-A263-0CC47A7C3404.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/56713C45-EF4B-E811-BCD3-0025905A611E.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/D6B4AF45-EF4B-E811-819D-0025905A6118.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/C8E60549-EF4B-E811-859A-0025905A48E4.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/F6F377E9-F14B-E811-A4E2-0025905A48B2.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/386E23DD-F04B-E811-89B7-0025905A6110.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/B86E699D-F14B-E811-875D-0025905A6064.root',
        '/store/relval/CMSSW_10_2_0_pre2/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/101X_upgrade2023_realistic_v5_2023D17noPU-v1/20000/BE6833F5-FC4B-E811-8D9B-0025905AA9F0.root',
    ]
    import random
    random.shuffle(pufiles)
    pufiles=pufiles[0:20]
    process.mix.input.nbPileupEvents.averageNumber = cms.double(options.pu)
    process.mix.bunchspace = cms.int32(25)
    process.mix.minBunch = cms.int32(-12)
    process.mix.maxBunch = cms.int32(3)
    process.mix.input.fileNames = cms.untracked.vstring(pufiles)


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.digitisation_step = cms.Path(process.pdigi_valid)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.endjob_step = cms.EndPath(process.endOfProcess)

process.load('L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff')
#process.hgcalTriggerPrimitiveDigiProducer.conc_proc.MaxCellsInModule=288
process.hgcalConcentratorProducer.ProcessorParameters.triggercell_threshold_silicon=options.thr
process.hgcalConcentratorProducer.ProcessorParameters.triggercell_threshold_scintillator=options.thr
process.hgcl1tpg_step = cms.Path(process.hgcalTriggerPrimitives)


process.digi2raw_step = cms.Path(process.DigiToRaw)
# don't output FEVTDEBUG
#process.FEVTDEBUGoutput_step = cms.EndPath(process.FEVTDEBUGoutput)

# load ntuplizer
process.load('L1Trigger.L1THGCal.hgcalTriggerNtuples_cff')
#process.ntuple_triggercells.FilterCellsInMulticlusters=cms.bool(False)
#process.ntuple_clusters.FilterClustersInMulticlusters = cms.bool(False)
process.ntuple_step = cms.Path(process.hgcalTriggerNtuples)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.digitisation_step,process.L1simulation_step,process.hgcl1tpg_step,process.digi2raw_step, process.ntuple_step, process.endjob_step)

# filter all path with the production filter sequence
for path in process.paths:
    if options.what=='ggh_hbb':
        getattr(process,path)._seq = process.generator * process.filter1* getattr(process,path)._seq
    else:
        getattr(process,path)._seq = process.generator * getattr(process,path)._seq

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

