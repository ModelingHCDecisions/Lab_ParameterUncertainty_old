from MarkovModelClasses import Cohort
import SimPy.StatisticalClasses as Stat


class MultiCohort:
    """ simulates multiple cohorts with different parameters """

    def __init__(self, ids, pop_size, list_parameters):
        """
        :param ids: (list) of ids for cohorts to simulate
        :param pop_size: (int) population size of cohorts to simulate
        :param list_parameters: (list) of parameters each of which corresponds to one cohort
        """
        self.ids = ids
        self.popSize = pop_size
        self.list_params = list_parameters
        self.multiCohortOutcomes = MultiCohortOutcomes()

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

        self.statMeanSurvivalTime = None  # summary statistics of mean survival time

    def extract_outcomes(self, simulated_cohort):
        """ extracts outcomes of a simulated cohort
        :param simulated_cohort: a cohort after being simulated"""

        # append the survival curve of this cohort
        self.survivalCurves.append(simulated_cohort.cohortOutcomes.nLivingPatients)

        # store mean survival time from this cohort
        self.meanSurvivalTimes.append(simulated_cohort.cohortOutcomes.statSurvivalTime.get_mean())

    def calculate_summary_stats(self):
        """
        calculate the summary statistics
        """

        # summary statistics of mean survival time
        self.statMeanSurvivalTime = Stat.SummaryStat(name='Mean survival time',
                                                     data=self.meanSurvivalTimes)
