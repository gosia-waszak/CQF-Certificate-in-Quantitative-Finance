"""
Q2 Credit Curve
CDS Pricing Questions

"""

import numpy
from collections import defaultdict


class Credit_Pricing:


	def __init__(self, rr, dt, cds_spread):
		self.survival_probs = {}
		self.sum_across_terms = defaultdict(int)
		self.T_n_dict = {}

		self.recov = 1 - rr
		self.dt = dt
		self.cds_spread = cds_spread	
		

	def _generate_df_fixed(self, maturity, rate):
		"""
		Generates discount factors (for a fixed rate)
		"""
		self.disc_factors = []
		for yr in range(0, maturity + 1):
			self.disc_factors.append(numpy.exp(-yr * rate))

	def get_implied_surv_prob(self, cur_yr):
		"""
		Computes implied survival probability
		"""
		if cur_yr not in self.survival_probs:
			if cur_yr == 0:
				surv_probs = 1
			elif cur_yr == 1:
				surv_probs = self.recov/(self.recov + self.dt * self.cds_spread[cur_yr])
			else:
				t_n = self.survival_probs[cur_yr - 1] * self.recov/(self.recov + self.dt * self.cds_spread[cur_yr])
				surv_probs = t_n + self.sum_across_terms[cur_yr - 2]/(self.disc_factors[cur_yr] * (self.recov + self.dt * self.cds_spread[cur_yr]))
			self.survival_probs[cur_yr] = surv_probs
		else:
			return self.survival_probs[cur_yr]

		return self.survival_probs[cur_yr]
	
	def get_T_n(self, yr, maturity):
		"""
		Intermediate term results
		"""
		idx = list(reversed(range(1, maturity))).index(yr)
		self.T_n_dict[idx] = []
		for j in range(0, yr):
			term_n_j = self.disc_factors[idx + 1]*(self.recov * self.get_implied_surv_prob(idx)-(self.recov + self.dt * self.cds_spread[j + idx + 2]) * self.get_implied_surv_prob(idx + 1))
			self.T_n_dict[idx].append(term_n_j)
        # sum across terms
		for i in range(0, len(self.T_n_dict.keys())):
			self.sum_across_terms[idx] += self.T_n_dict[i][len(self.T_n_dict.keys())-i-1]


	def print_survival_probs(self, maturity):
		[print("Survival probability in Year {}: {}".format(i, self.survival_probs[i])) for i in range(1, maturity + 1)]
	
	def cds_bootstrapping(self, maturity, rate):
		self._generate_df_fixed(maturity, rate)
		for yr in reversed(range(1, maturity)):
			self.get_T_n(yr, maturity)
		term_surv = self.get_implied_surv_prob(maturity)

def main():
	# Task inputs
	maturity = 5
	rr = 0.4
	dt = 1
	rate = 0.008
	cds_spread = [0, 0.014176, 0.016536, 0.018856, 0.020732, 0.021838]
	
	# Solution start
	credit_pricer = Credit_Pricing(rr, dt, cds_spread)
	credit_pricer.cds_bootstrapping(maturity, rate)
	credit_pricer.print_survival_probs(maturity)

if __name__ == '__main__':
    main()


