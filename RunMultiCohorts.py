import MultiCohortClasses as Cls
import ProbilisticParamClasses as P
import InputData as D
import MultiCohortSupport as Support
import SimPy.RandomVariantGenerators as RVGs
import SimPy.SamplePathClasses as Path
import SimPy.FigureSupport as Fig

N_COHORTS = 3              # number of cohorts
therapy = P.Therapies.MONO  # selected therapy

# create a parameter generator
param_generator = P.ParameterGenerator(therapy=therapy)

# create parameter sets
rng = RVGs.RNG(seed=0)
list_params = []
for i in range(N_COHORTS):
    list_params.append(param_generator.get_new_parameters(rng=rng))

# create multiple cohort
multiCohort = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=D.POP_SIZE,
    list_parameters=list_params
)

multiCohort.simulate(sim_length=D.SIM_LENGTH)

# plot the sample paths
Path.graph_sample_paths(
    sample_paths=multiCohort.multiCohortOutcomes.survivalCurves,
    title='Survival Curves',
    x_label='Time-Step (Year)',
    y_label='Number Survived',
    transparency=0.5)

# plot the histogram of average survival time
Fig.graph_histogram(
    data=multiCohort.multiCohortOutcomes.meanSurvivalTimes,
    title='Histogram of Mean Survival Time',
    x_label='Mean Survival Time (Year)',
    y_label='Count')

# print the outcomes of this simulated cohort
Support.print_outcomes(multi_cohort_outcomes=multiCohort.multiCohortOutcomes,
                       therapy_name=therapy)
