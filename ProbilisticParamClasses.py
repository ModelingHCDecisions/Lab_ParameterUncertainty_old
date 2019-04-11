from ParameterClasses import *  # import everything from the ParameterClass module
import InputData as Data
import SimPy.RandomVariantGenerators as RVGs
import SimPy.FittingProbDist_MM as MM
import math
import scipy.stats as stat


class Parameters:

    def __init__(self, therapy):

        self.therapy = therapy              # selected therapy
        self.initialHealthState = HealthStates.CD4_200to500     # initial health state
        self.annualTreatmentCost = 0        # annual treatment cost
        self.rateMatrix = []                # transition probability matrix of the selected therapy
        self.annualStateCosts = []          # annual state costs
        self.annualStateUtilities = []      # annual state utilities
        self.discountRate = Data.DISCOUNT   # discount rate


class ParameterGenerator:

    def __init__(self, therapy):

        self.therapy = therapy
        self.probMatrixRVG = []     # list of dirichlet distributions for transition probabilities
        self.lnRelativeRiskRVG = None  # normal distribution for the natural log of the treatment relative risk
        self.annualStateCostRVG = []  # list of gamma distributions for the annual cost of states
        self.annualStateUtilityRVG = []  # list of beta distributions for the annual utility of states

        # transition probabilities
        j = 0
        for prob in Data.TRANS_MATRIX:
            self.probMatrixRVG.append(RVGs.Dirichlet(a=prob[j:]))
            j += 1

        # treatment relative risk
        rr_ci = [0.365, 0.71]   # confidence interval of the treatment relative risk

        # find the mean and st_dev of the normal distribution assumed for ln(RR)
        # sample mean ln(RR)
        mean_ln_rr = math.log(Data.TREATMENT_RR)
        # sample standard deviation of ln(RR)
        std_ln_rr = \
            (math.log(rr_ci[1]) - math.log(rr_ci[0])) / (2 * stat.norm.ppf(1 - 0.05 / 2))

        self.lnRelativeRiskRVG = RVGs.Normal(loc=mean_ln_rr,
                                             scale=std_ln_rr)

        # annual state cost
        for cost in Data.ANNUAL_STATE_COST:

            # if cost is zero, add a constant 0, otherwise add a gamma distribution
            if cost == 0:
                self.annualStateCostRVG.append(RVGs.Constant(value=0))
            else:
                # find shape and scale of the assumed gamma distribution
                fit_output = MM.get_gamma_params(mean=cost, st_dev=cost / 5)
                # append the distribution
                self.annualStateCostRVG.append(
                    RVGs.Gamma(a=fit_output["a"],
                                 loc=0,
                                 scale=fit_output["scale"]))

        # annual state utility
        for utility in Data.ANNUAL_STATE_UTILITY:
            # if utility is zero, add a constant 0, otherwise add a beta distribution
            if utility == 0:
                self.annualStateCostRVG.append(RVGs.Constant(value=0))
            else:
                # find alpha and beta of the assumed beta distribution
                fit_output = MM.get_beta_params(mean=utility, st_dev=utility / 4)
                # append the distribution
                self.annualStateUtilityRVG.append(
                    RVGs.Beta(a=fit_output["a"], b=fit_output["b"]))

    def get_new_parameters(self, rng):
        """
        :param rng: random number generator
        :return: a new parameter set
        """

        # create a parameter set
        param = Parameters(therapy=self.therapy)

        # calculate transition probabilities

        prob_matrix = []    # probability matrix without background mortality added
        # for all health states
        for s in HealthStates:

            # if the current state is death
            if s not in [HealthStates.HIV_DEATH, HealthStates.NATUAL_DEATH]:
                # create a row populated with zeroes
                prob_matrix.append([0] * (len(HealthStates)-1))
                # sample from the dirichlet distribution to find the transition probabilities between hiv states
                sample = self.probMatrixRVG[s.value].sample(rng)
                for j in range(len(sample)):
                    prob_matrix[s.value][s.value + j] = sample[j]

        # calculate transition probabilities between hiv states
        if self.therapy == Therapies.MONO:
            # calculate transition probability matrix for the mono therapy
            param.rateMatrix = get_rate_matrix_mono(trans_prob_matrix=prob_matrix)

        elif self.therapy == Therapies.COMBO:
            # calculate transition probability matrix for the combination therapy
            param.rateMatrix = get_rate_matrix_combo(
                rate_matrix_mono=get_rate_matrix_mono(trans_prob_matrix=prob_matrix),
                combo_rr=Data.TREATMENT_RR)

        # sample from gamma distributions that are assumed for annual state costs
        for dist in self.annualStateCostRVG:
            param.annualStateCosts.append(dist.sample(rng))

        # sample from beta distributions that are assumed for annual state utilities
        for dist in self.annualStateUtilityRVG:
            param.annualStateUtilities.append(dist.sample(rng))

        # return the parameter set
        return param
