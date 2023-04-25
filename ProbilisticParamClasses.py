from EconEvalParamClasses import *  # import everything from the EconEvalParamClasses module


class Parameters:
    """ class to include parameter information to simulate the model """

    def __init__(self, therapy):

        self.therapy = therapy              # selected therapy
        self.initialHealthState = HealthStates.CD4_200to500     # initial health state
        self.annualTreatmentCost = 0        # annual treatment cost
        self.transRateMatrix = []                # transition probability matrix of the selected therapy
        self.annualStateCosts = []          # annual state costs
        self.annualStateUtilities = []      # annual state utilities
        self.discountRate = Data.DISCOUNT   # discount rate


class ParameterGenerator:
    """ class to generate parameter values from the selected probability distributions """

    def __init__(self, therapy):

        self.therapy = therapy
        self.probMatrixRVG = []     # list of dirichlet distributions for transition probabilities
        self.lnRelativeRiskRVG = None  # normal distribution for the natural log of the treatment relative risk
        self.annualStateCostRVG = []  # list of gamma distributions for the annual cost of states
        self.annualStateUtilityRVG = []  # list of beta distributions for the annual utility of states
        self.annualTreatmentCostRVG = None   # gamma distribution for treatment cost

        # create Dirichlet distributions for transition probabilities

        # treatment relative risk
        rr_ci = [0.365, 0.71]   # confidence interval of the treatment relative risk

        # find the mean and st_dev of the normal distribution assumed for ln(RR)
        # sample mean ln(RR)

        # sample standard deviation of ln(RR)

        # create a normal distribution for ln(RR)

        # create gamma distributions for annual state cost

            # if cost is zero, add a constant 0, otherwise add a gamma distribution

                # find shape and scale of the assumed gamma distribution
                # no data available to estimate the standard deviation, so we assumed st_dev=cost / 5

                # append the distribution

        # create a gamma distribution for annual treatment cost

        # create beta distributions for annual state utility

            # if utility is zero, add a constant 0, otherwise add a beta distribution

                # find alpha and beta of the assumed beta distribution
                # no data available to estimate the standard deviation, so we assumed st_dev=cost / 4

    def get_new_parameters(self, seed):
        """
        :param seed: seed for the random number generator used to a sample of parameter values
        :return: a new parameter set
        """

        rng = np.random.RandomState(seed=seed)

        # create a parameter set
        param = Parameters(therapy=self.therapy)

        # calculate transition probabilities
        prob_matrix = []    # probability matrix without background mortality added
        # for all health states
        for s in HealthStates:
            # if the current state is not death

                # sample from the dirichlet distribution to find the transition probabilities between hiv states
                # fill in the transition probabilities out of this state


        # sampled relative risk

        # calculate transition probabilities between hiv states
        if self.therapy == Therapies.MONO:
            # calculate transition probability matrix for the mono therapy


        elif self.therapy == Therapies.COMBO:
            # calculate transition probability matrix for the combination therapy

        # sample from gamma distributions that are assumed for annual state costs

        # sample from the gamma distribution that is assumed for the treatment cost

        # sample from beta distributions that are assumed for annual state utilities

        # return the parameter set
        return param
