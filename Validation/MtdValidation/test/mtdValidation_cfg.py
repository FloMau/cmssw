import FWCore.ParameterSet.Config as cms


from Configuration.Eras.Era_Phase2C11I13M9_cff import Phase2C11I13M9
process = cms.Process('mtdValidation',Phase2C11I13M9)

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')

process.load("Configuration.Geometry.GeometryExtended2026D77Reco_cff")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#Setup FWK for multithreaded
process.options.numberOfThreads = 4
process.options.numberOfStreams = 0
process.options.numberOfConcurrentLuminosityBlocks = 0
process.options.eventSetup.numberOfConcurrentIOVs = 1

process.MessageLogger.cerr.FwkReport  = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(100),
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:step3.root'
    )
)

process.mix.digitizers = cms.PSet()
for a in process.aliases: delattr(process, a)

# --- BTL Validation
process.load("Validation.MtdValidation.btlSimHitsValid_cfi")
process.load("Validation.MtdValidation.btlDigiHitsValid_cfi")
process.load("Validation.MtdValidation.btlLocalRecoValid_cfi")
btlValidation = cms.Sequence(process.btlSimHitsValid + process.btlDigiHitsValid + process.btlLocalRecoValid)

# --- ETL Validation
process.load("Validation.MtdValidation.etlSimHitsValid_cfi")
process.load("Validation.MtdValidation.etlDigiHitsValid_cfi")
process.load("Validation.MtdValidation.etlLocalRecoValid_cfi")
etlValidation = cms.Sequence(process.etlSimHitsValid + process.etlDigiHitsValid + process.etlLocalRecoValid)

# --- Global Validation
process.load("Validation.MtdValidation.mtdTracksValid_cfi")
process.load("Validation.MtdValidation.vertices4DValid_cfi")

process.btlDigiHitsValid.LocalPositionDebug = True
process.etlDigiHitsValid.LocalPositionDebug = True
process.btlLocalRecoValid.LocalPositionDebug = True
process.etlLocalRecoValid.LocalPositionDebug = True
process.vertices4DValid.optionalPlots = True

process.validation = cms.Sequence(btlValidation + etlValidation + process.mtdTracksValid + process.vertices4DValid)

process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('DQMIO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:step3_inDQM.root'),
    outputCommands = process.DQMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

process.p = cms.Path( process.mix + process.validation )
process.endjob_step = cms.EndPath(process.endOfProcess)
process.DQMoutput_step = cms.EndPath( process.DQMoutput )

process.schedule = cms.Schedule( process.p , process.endjob_step , process.DQMoutput_step )
