GCC=g++
CXXFLAGS=`root-config --libs --cflags` -O2 -fPIC -I../  -I./
## to use BareObjects
CXXFLAGS += -L$(PWD)/../NeroProducer/Core/bin  -ggdb -lTMVA -l RooFit -l RooFitCore  -l Physics
SOFLAGS=-shared

SRCDIR=src
BINDIR=bin
HPPDIR=interface
AUXDIR=aux

SRC=$(wildcard $(SRCDIR)/*.cpp)
OBJ=$(patsubst $(SRCDIR)/%.cpp, $(BINDIR)/%.o , $(SRC)  )
HPPLINKDEF=$(patsubst $(SRCDIR)/%.cpp, ../interface/%.hpp , $(SRC)  )

.PHONY: all
all:
	$(info, "--- Full compilation --- ")	
	#$(MAKE) clean
	$(MAKE) libFastjetInterface.so


# check if CMSSW is defined
ifndef CMSSW_BASE
$(info No CMSSSW !!!!)
$(info I ll sleep 3s to let you acknowledge it)
$(shell sleep 3s)
CXXFLAGS += -I/usr/include/python2.7 -lpython2.7
else
$(info CMSSW found: $(CMSSW_BASE) )
CXXFLAGS += -I"/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/python/2.7.11-mlhled/include/python2.7"
CXXFLAGS += -I"/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/fastjet/3.3.0-omkpbe/include"
CXXFLAGS += -L"/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/fastjet/3.3.0-omkpbe/lib" -lfastjet
CXXFLAGS += -I"/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/fastjet-contrib/1.033-omkpbe/include"
CXXFLAGS += -L"/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/fastjet-contrib/1.033-omkpbe/lib"  -lNsubjettiness -lRecursiveTools -l fastjetcontribfragile
endif

#libClusteringVetoPlugin.a   libfastjetcontribfragile.so  libJetCleanser.a      libNsubjettiness.a   libScJet.a           libValenciaPlugin.a
#libConstituentSubtractor.a  libFlavorCone.a              libJetFFMoments.a     libQCDAwarePlugin.a  libSoftKiller.a      libVariableR.a
#libEnergyCorrelator.a       libGenericSubtractor.a       libJetsWithoutJets.a  libRecursiveTools.a  libSubjetCounting.a

# check if Combine is present and compiled 

libFastjetInterface.so: $(OBJ) Dict | $(BINDIR)
	$(GCC) $(CXXFLAGS) $(RPATH) $(SOFLAGS) -o $(BINDIR)/$@ $(OBJ) $(BINDIR)/dict.o

$(OBJ) : $(BINDIR)/%.o : $(SRCDIR)/%.cpp | $(BINDIR)
	$(GCC) $(CXXFLAGS) $(RPATH) -c -o $(BINDIR)/$*.o $<

.PHONY: Dict
Dict: $(BINDIR)/dict.o

$(BINDIR)/dict.o: $(SRC) | $(BINDIR)
	genreflex $(SRCDIR)/classes.h -s $(SRCDIR)/classes_def.xml -o $(BINDIR)/dict.cc --deep --fail_on_warnings --rootmap=$(BINDIR)/dict.rootmap --rootmap-lib=libChargedHiggs.so -I interface/ -I../ -I"/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/fastjet/3.3.0-omkpbe/include" -I"/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/fastjet-contrib/1.033-omkpbe/include"
	$(GCC) -c -o $(BINDIR)/dict.o $(CXXFLAGS) -I interface $(BINDIR)/dict.cc

$(BINDIR):
	mkdir -p $(BINDIR)

.PHONY: clean
clean:
	-rm $(OBJ)
	-rm $(BINDIR)/dict*
	-rm $(BINDIR)/libFastjetInterface.so
	-rmdir $(BINDIR)
