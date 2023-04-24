import EconEvalInputData as D
import ProbabilisticClasses as Cls
import ProbabilisticSupport as Support
import ProbilisticParamClasses as P

N_COHORTS = 200  # number of cohorts
POP_SIZE = 500  # population size of each cohort

# create a multi-cohort to simulate under mono therapy
multiCohortMono = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=POP_SIZE,
    therapy=P.Therapies.MONO
)

multiCohortMono.simulate(sim_length=D.SIM_LENGTH)

# create a multi-cohort to simulate under combo therapy
multiCohortCombo = Cls.MultiCohort(
    ids=range(N_COHORTS, 2*N_COHORTS),
    pop_size=POP_SIZE,
    therapy=P.Therapies.COMBO
)

multiCohortCombo.simulate(sim_length=D.SIM_LENGTH)

# print the estimates for the mean survival time and mean time to AIDS
Support.print_outcomes(multi_cohort_outcomes=multiCohortMono.multiCohortOutcomes,
                       therapy_name=P.Therapies.MONO)
Support.print_outcomes(multi_cohort_outcomes=multiCohortCombo.multiCohortOutcomes,
                       therapy_name=P.Therapies.COMBO)

# draw survival curves and histograms
Support.plot_survival_curves_and_histograms(multi_cohort_outcomes_mono=multiCohortMono.multiCohortOutcomes,
                                            multi_cohort_outcomes_combo=multiCohortCombo.multiCohortOutcomes)

# print comparative outcomes
Support.print_comparative_outcomes(multi_cohort_outcomes_mono=multiCohortMono.multiCohortOutcomes,
                                   multi_cohort_outcomes_combo=multiCohortCombo.multiCohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(multi_cohort_outcomes_mono=multiCohortMono.multiCohortOutcomes,
                       multi_cohort_outcomes_combo=multiCohortCombo.multiCohortOutcomes)