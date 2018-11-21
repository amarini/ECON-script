import FWCore.ParameterSet.Config as cms 
from Configuration.StandardSequences.Eras import eras

process = cms.Process('DIGI',eras.Phase2)

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.register('pt', 50., VarParsing.multiplicity.singleton,VarParsing.varType.float,"Gun Pt")
options.register('pu', 0, VarParsing.multiplicity.singleton,VarParsing.varType.int,"Pileup")
options.register('thr', 0, VarParsing.multiplicity.singleton,VarParsing.varType.int,"Thr")
options.register('pdgid', 11, VarParsing.multiplicity.singleton,VarParsing.varType.int,"Pdgid")
options.register('what', "pgun", VarParsing.multiplicity.singleton,VarParsing.varType.string,"pgun") # pgun, ggh_hbb, ggh_hmm, vbf_hmm
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
elif options.what == 'minbias':
    process.generator = cms.EDFilter("Pythia8GeneratorFilter",
            PythiaParameters = cms.PSet(
                parameterSets = cms.vstring(
                    'pythia8CommonSettings', 
                    'pythia8CUEP8M1Settings', 
                    'processParameters'
                    ),
                processParameters = cms.vstring(
                    'SoftQCD:nonDiffractive = on', 
                    'SoftQCD:singleDiffractive = on', 
                    'SoftQCD:doubleDiffractive = on'
                    ),
                pythia8CUEP8M1Settings = cms.vstring(
                    'Tune:pp 14', 
                    'Tune:ee 7', 
                    'MultipartonInteractions:pT0Ref=2.4024', 
                    'MultipartonInteractions:ecmPow=0.25208', 
                    'MultipartonInteractions:expPow=1.6'
                    ),
                pythia8CommonSettings = cms.vstring(
                    'Tune:preferLHAPDF = 2', 
                    'Main:timesAllowErrors = 10000', 
                    'Check:epTolErr = 0.01', 
                    'Beams:setProductionScalesFromLHEF = off', 
                    'SLHA:keepSM = on', 
                    'SLHA:minMassSM = 1000.', 
                    'ParticleDecays:limitTau0 = on', 
                    'ParticleDecays:tau0Max = 10', 
                    'ParticleDecays:allowPhotonRadiation = on'
                    )
                ),
            comEnergy = cms.double(14000.0),
            crossSection = cms.untracked.double(71390000000.0),
            filterEfficiency = cms.untracked.double(1.0),
            maxEventsToPrint = cms.untracked.int32(0),
            pythiaHepMCVerbosity = cms.untracked.bool(False),
            pythiaPylistVerbosity = cms.untracked.int32(1)
            )
else: raise ValueError("Options %s unimplemented"%options.what)


import os,random
random.seed = os.urandom(10) #~10^14
process.RandomNumberGeneratorService.generator.initialSeed = random.randint(0,999999)

process.mix.digitizers = cms.PSet(process.theDigitizersValid)

if options.pu !=0:
    pufiles=[
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_0.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_100.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_101.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_103.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_104.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_105.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_106.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_107.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_108.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_109.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_10.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_110.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_111.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_112.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_113.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_114.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_115.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_116.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_117.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_118.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_119.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_11.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_120.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_121.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_122.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_123.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_124.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_125.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_126.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_127.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_128.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_129.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_12.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_130.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_131.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_132.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_133.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_134.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_135.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_136.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_137.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_138.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_139.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_13.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_140.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_141.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_142.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_143.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_144.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_145.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_146.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_147.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_148.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_149.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_14.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_150.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_151.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_152.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_153.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_154.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_155.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_156.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_157.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_158.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_159.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_15.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_160.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_161.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_162.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_163.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_164.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_165.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_166.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_167.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_168.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_169.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_16.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_170.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_172.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_173.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_174.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_176.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_177.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_178.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_179.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_17.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_180.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_181.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_182.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_183.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_184.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_185.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_186.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_187.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_188.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_189.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_18.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_190.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_191.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_192.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_193.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_194.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_195.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_196.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_197.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_198.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_199.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_19.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_1.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_20.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_21.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_22.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_23.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_24.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_25.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_26.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_27.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_28.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_29.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_2.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_30.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_31.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_32.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_33.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_34.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_35.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_36.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_37.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_38.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_39.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_3.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_40.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_41.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_42.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_43.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_44.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_45.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_46.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_47.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_48.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_49.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_4.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_50.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_51.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_52.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_53.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_54.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_55.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_56.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_57.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_58.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_59.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_5.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_60.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_61.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_62.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_63.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_64.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_65.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_66.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_67.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_68.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_69.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_6.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_70.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_71.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_72.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_73.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_74.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_75.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_76.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_77.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_78.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_79.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_7.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_80.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_81.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_82.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_83.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_84.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_85.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_86.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_87.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_88.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_89.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_8.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_90.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_91.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_92.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_93.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_94.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_95.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_97.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_98.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_99.root',
        'file:/eos/user/k/klute/Nero/RelValMinBias_102/step2_9.root',
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

