from MarkovModelClasses import Cohort
from ProbilisticParamClasses import ParameterGenerator
import SimPy.StatisticalClasses as Stat
import SimPy.RandomVariantGenerators as RVGs


class MultiCohort:
    """ simulates multiple cohorts with different parameters """

    def __init__(self, ids, pop_size, therapy):
        """
        :param ids: (list) of ids for cohorts to simulate
        :param pop_size: (int) population size of cohorts to simulate
        :param therapy: selected therapy
        """
        self.ids = ids
        self.popSize = pop_size
        self.list_params = []  # list of parameter sets each of which corresponds to a cohort
        self.multiCohortOutcomes = MultiCohortOutcomes()

        # create parameter sets
        self.__populate_parameter_sets(therapy=therapy)

    def __populate_parameter_sets(self, therapy):

        # create a parameter set generator
        param_generator = ParameterGenerator(therapy=therapy)

        # create as many sets of parameters as the number of cohorts
        for i in range(len(self.ids)):
            # create a new random number generator for each parameter set
            rng = RVGs.RNG(seed=i)
            # get and store a new set of parameter
            self.list_params.append(param_generator.get_new_parameters(rng=rng))

    def simulate(self, sim_length):
        """ simulates all cohorts
        :param sim_length: simulation length
        """

        for i in range(len(self.ids)):
            # create a cohort
            cohort = Cohort(id=self.ids[i], pop_size=self.popSize, parameters=self.list_params[i])

            # simulate the cohort
            cohort.simulate(sim_length=sim_length)

            # outcomes from simulating all cohorts
            self.multiCohortOutcomes.extract_outcomes(simulated_cohort=cohort)

        # calculate the summary statistics of from all cohorts
        self.multiCohortOutcomes.calculate_summary_stats()


class MultiCohortOutcomes:
    def __init__(self):

        self.survivalCurves = []  # list of survival curves from all simulated cohorts

        self.meanSurvivalTimes = []  # list of average patient survival time for all simulated cohort
        self.meanTimeToAIDS = []
        self.meanCosts = []
        self.meanQALYs = []

        self.statMeanSurvivalTime = None  # summary statistics of mean survival time
        self.statMeanTimeToAIDS = None
        self.statMeanCost = None
        self.statMeanQALY = None

    def extract_outcomes(self, simulated_cohort):
        """ extracts outcomes of a simulated cohort
        :param simulated_cohort: a cohort after being simulated"""

        # append the survival curve of this cohort
        self.survivalCurves.append(simulated_cohort.cohortOutcomes.nLivingPatients)

        # store mean survival time from this cohort
        self.meanSurvivalTimes.append(simulated_cohort.cohortOutcomes.statSurvivalTime.get_mean())
        # store mean time to AIDS from this cohort
        self.meanTimeToAIDS.append(simulated_cohort.cohortOutcomes.statTimeToAIDS.get_mean())
        # store mean cost from this cohort
        self.meanCosts.append(simulated_cohort.cohortOutcomes.statCost.get_mean())
        # store mean QALY from this cohort
        self.meanQALYs.append(simulated_cohort.cohortOutcomes.statUtility.get_mean())

    def calculate_summary_stats(self):
        """
        calculate the summary statistics
        """

        # summary statistics of mean survival time
        self.statMeanSurvivalTime = Stat.SummaryStat(name='Mean survival time',
                                                     data=self.meanSurvivalTimes)
        # summary statistics of mean time to AIDS
        self.statMeanTimeToAIDS = Stat.SummaryStat(name='Mean time to AIDS',
                                                   data=self.meanTimeToAIDS)
        # summary statistics of mean cost
        self.statMeanCost = Stat.SummaryStat(name='Mean cost',
                                             data=self.meanCosts)
        # summary statistics of mean QALY
        self.statMeanQALY = Stat.SummaryStat(name='Mean QALY',
                                             data=self.meanQALYs)
