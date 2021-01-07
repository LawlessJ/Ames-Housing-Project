import numpy as np
from scipy.stats import norm, t, chisquare, chi2

#norm.ppf() converts a proportion into its appropriate z-score on a normal distribution
#norm.cdf() will likewise convert a z-score into a proportion, useful for rendering a p-value

def two_tail(phat):
    zstar = (1 -(1 - phat) /2)
    return zstar

def tstar(conf_level, n):
    dof = n-1
    crit_val = t.ppf((1 + conf_level)/2, dof)
    return crit_val

def z_sample_size_calc(phat = 0.5, margin_error = 0.02, confidence = 0.95):
    z = two_tail(confidence)
    z_star = norm.ppf(z)
    n = (np.sqrt((phat * (1 - phat))) / (margin_error/z_star))**2
    if n == int(n):
        return n
    else:
        nint = int(n) +1
        return nint
    return

def t_sample_size_calc(stdev, margin_error, confidence = 0.95):
    z = two_tail(confidence)
    z_star = norm.ppf(z)
    n = ((z_star * stdev)/margin_error) ** 2
    if n == int(n):
        return n
    else:
        n = int(n + 1)
        return n
    return

def z_conf_intv(phat, n, confidence = 0.95):
    z = two_tail(confidence)
    z_score = norm.ppf(z)
    se = np.sqrt((phat * (1-phat))/n)
    margin = (z_score * se)
    return (phat - margin, phat + margin)

def diff_z_intv(phat1, n1, phat2, n2, confidence = 0.95):
    z = two_tail(confidence)
    z_score = norm.ppf(z)
    se_diff = np.sqrt((phat1 * (1-phat1))/n1 + (phat2 * (1-phat2))/n2)
    margin = (z_score * se_diff)
    samp_diff = phat1 - phat2
    return (samp_diff - margin, samp_diff + margin)

def t_conf_intv(xbar, stdev, n, confidence = 0.95):
    dof = n - 1
    t_star = tstar(confidence, n)
    se = t_star * (stdev/np.sqrt(n))
    return xbar - se, xbar + se

def diff_t_intv(sample1, sample2, confidence = 0.95):
    xbar1 = np.mean(sample1)
    xbar2 = np.mean(sample2)
    s1 = np.std(sample1)
    s2 = np.std(sample2)
    n1 = len(sample1)
    n2 = len(sample2)
    if n2 < n1:
        df = n2
    else:
        df = n1
    t_star = tstar(confidence, df)
    diff = xbar1 - xbar2
    se = t_star * np.sqrt((s1**2/n1) + (s2 **2/n2))
    return diff - se, diff + se
 
def one_samp_z_test(phat, p0, n, both_tails = False, alpha = None):
    z_stat = (phat - p0)/ np.sqrt((p0 * (1-p0))/n)
    pval = norm.cdf(z_stat)
    if z_stat > 0:
        pval = 1 - pval
    if both_tails == True:
        pval = 2 * pval
    if alpha != None:
        if pval >= alpha:
            reject = False
        if pval <= alpha:
            reject = True
        return z_stat, pval, reject
    return z_stat, pval

def two_samp_z_test(sample1, sample2, both_tails = False):
    n1 = np.sum(sample1)
    n2 = np.sum(sample2)
    phat1 = sample1[0]/n1
    phat2 = sample2[0]/n2
    pc = (sample1[0] + sample2[0]) / (n1 + n2)
    z_stat = (phat1 - phat2)/ np.sqrt((pc * (1-pc))/n1 + (pc * (1-pc))/n2)
    pval = norm.cdf(z_stat)
    if z_stat > 0:
        pval = 1 - pval
    if both_tails == True:
        pval = 2 * pval
    return z_stat, pval

# creates an "expected" value for chi_square tests
def expected(pop_lists):
    total = 0
    n_lists = [np.sum(sums) for sums in pop_lists]
    total = np.sum(n_lists)
    exp = []
    
    for ind in range(len(pop_lists[0])):
        placer = 0
        x = 0
        while placer < len(pop_lists):
            x += pop_lists[placer][ind]
            placer +=1
        x = (x/total) 
        exp.append(x)
    new_lists = pop_lists
    for groups in range(len(new_lists)):
        for ind in range(len(new_lists[0])):
            new_lists[groups][ind] = n_lists[groups] * exp[ind]
    flat_expected_list = [value for sublist in new_lists for value in sublist]
    return flat_expected_list

def chi2_homogeneity(pop_lists):
    dof = (len(pop_lists) -1) * (len(pop_lists[0]) -1)
    act = [value for sublist in pop_lists for value in sublist]
    exp = expected(pop_lists)
    chi_2, trash = chisquare(act, exp, ddof = dof)
    pval = 1 - chi2.cdf(chi_2, dof)
    return chi_2, pval
