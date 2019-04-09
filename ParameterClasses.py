from ParameterClasses import get_rate_matrix_combo, get_rate_matrix_mono
from ParameterClasses import HealthStates
from ParameterClasses import Therapies
import InputData as Data


class _Parameters:

    def __init__(self, therapy):

        self.therapy = therapy      # selected therapy
        self.initialHealthState = HealthStates.CD4_200to500     # initial health state
        self.annualTreatmentCost = 0    # annual treatment cost
        self.rateMatrix = []    # transition probability matrix of the selected therapy
        self.annualStateCosts = []      # annual state costs
        self.annualStateUtilities = []  # annual state utilities
        self.discountRate = 0           # discount rate


class ParametersFixed(_Parameters):

    def __init__(self, therapy):

        _Parameters.__init__(therapy=therapy)

        # annual treatment cost
        if self.therapy == Therapies.MONO:
            self.annualTreatmentCost = Data.Zidovudine_COST
        else:
            self.annualTreatmentCost = Data.Zidovudine_COST + Data.Lamivudine_COST

        # transition probability matrix of the selected therapy
        self.rateMatrix = []

        # calculate transition probabilities between hiv states
        if self.therapy == Therapies.MONO:
            # calculate transition probability matrix for the mono therapy
            self.rateMatrix = get_rate_matrix_mono(trans_matrix=Data.TRANS_MATRIX)

        elif self.therapy == Therapies.COMBO:
            # calculate transition probability matrix for the combination therapy
            self.rateMatrix = get_rate_matrix_combo(
                rate_matrix_mono=get_rate_matrix_mono(trans_matrix=Data.TRANS_MATRIX),
                combo_rr=Data.TREATMENT_RR)

        # annual state costs and utilities
        self.annualStateCosts = Data.ANNUAL_STATE_COST
        self.annualStateUtilities = Data.ANNUAL_STATE_UTILITY

        # discount rate
        self.discountRate = Data.DISCOUNT

