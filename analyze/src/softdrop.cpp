/* Andrea Carlo Marini
 * Wed Nov 21 15:51:43 CET 2018
 * This is python interface to softdrop utils
 */

#ifndef SOFTDROP_H
#define SOFTDROP_H

//fastjet
#include "fastjet/PseudoJet.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/contrib/Njettiness.hh"
#include "fastjet/contrib/NjettinessPlugin.hh"
#include "fastjet/contrib/SoftDrop.hh"


using namespace fastjet;
using namespace std;

class fastjet_interface{
    public:
        int maxTau_{3};
        float R_{0.8};

        JetDefinition AKDef{JetDefinition(antikt_algorithm, R_)};
        fastjet::contrib::SoftDrop softdrop_ {fastjet::contrib::SoftDrop(1., 0.15, R_)};
        fastjet::contrib::Njettiness *tau_ { new fastjet::contrib::Njettiness(fastjet::contrib::OnePass_KT_Axes(), fastjet::contrib::NormalizedMeasure(1., R_)) };

        float getTaus(const std::vector<PseudoJet> &input_particles, int i);
};

#ifndef ONLY_SOFTDROP_H
#define ONLY_SOFTDROP_H

float fastjet_interface::getTaus(const std::vector<PseudoJet> &input_particles, int i)
{
        vector<float> taus;
        // Rereun cluster sequence
        ClusterSequence seq(input_particles, AKDef);
        auto allJets=sorted_by_pt(seq.inclusive_jets(0.0));
        if (allJets.size()>0)
        {
            auto& leadingJet(allJets[0]);
            PseudoJet sdJet((softdrop_)(leadingJet));
            const auto& sdconsts = sorted_by_pt(sdJet.constituents());
            for(int tau=1;tau<=maxTau_;++tau)
            {
                taus. push_back( tau_->getTau(tau, sdconsts));
            }
        }
        return taus[i];
}
#endif
#endif
