import MultiCohortClasses as Cls
import ProbilisticParamClasses as P
import InputData as D
import SimPy.RandomVariantGenerators as RVGs

N_COHORTS = 10         # number of cohorts

rng = RVGs.RNG(seed=0)

# create a parameter generator
param_generator = P.ParameterGenerator(therapy=P.Therapies.MONO)

# create parameter sets
list_params=[]
for i in range(N_COHORTS):
    list_params.append(param_generator.get_new_parameters(rng=rng))

# create multiple cohort
multiCohort = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=D.POP_SIZE,
    list_parameters=list_params
)

multiCohort.simulate(sim_length=D.SIM_LENGTH)
