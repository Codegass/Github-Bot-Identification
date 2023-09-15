from scipy.stats import mannwhitneyu, pearsonr, spearmanr, norm, kstest, ks_2samp, kendalltau
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
from random import sample

def conduct_tests():
    df_bot = pd.read_csv('/Users/rehmanh/Desktop/Research/Chenhao Bot Study/RQ4_WithBots.csv', index_col=False)
    df_without_bot = pd.read_csv('/Users/rehmanh/Desktop/Research/Chenhao Bot Study/RQ4_WithOutBots.csv', index_col=False)

    comments_bot = pd.read_csv('/Users/rehmanh/Desktop/Research/Chenhao Bot Study/Comments_WithBots.csv', index_col=False)
    comments__without_bot = pd.read_csv('/Users/rehmanh/Desktop/Research/Chenhao Bot Study/Comments_WithOutBots.csv', index_col=False)

    # turnaround time
    tt_bot = df_bot['Turnaround Time'].tolist()
    tt_bot = [(int(re.findall('(\d+)[^\d]days', t)[0]) * 86400) + ( list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[0] * 3600 + list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[1] * 60 + list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[2] )  for t in tt_bot]
    tt_no_bot = df_without_bot['Turnaround Time'].tolist()
    tt_no_bot = [(int(re.findall('(\d+)[^\d]days', t)[0]) * 86400) + ( list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[0] * 3600 + list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[1] * 60 + list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[2] )  for t in tt_no_bot]
    
    res = mannwhitneyu(tt_no_bot, tt_bot, method="auto")
    m_tt = ((sum(tt_no_bot) / len(tt_no_bot)) - (sum(tt_bot) / len(tt_bot))) / ((sum(tt_no_bot) / len(tt_no_bot)))
    print('Turnaround Time Test: {}'.format(res))
    
    # merge time bot
    merge_time_bot = df_bot['Merge Time'].tolist()
    merge_time_bot = [t for t in merge_time_bot if t != '0']
    merge_time_bot = [(int(re.findall('(\d+)[^\d]days', t)[0]) * 86400) + ( list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[0] * 3600 + list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[1] * 60 + list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[2] )  for t in merge_time_bot]
    merge_time_not_bot = df_without_bot['Merge Time'].tolist()
    merge_time_not_bot = [t for t in merge_time_not_bot if t != '0']
    merge_time_not_bot = [(int(re.findall('(\d+)[^\d]days', t)[0]) * 86400) + ( list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[0] * 3600 + list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[1] * 60 + list(map(int, re.findall('days(,?.*)', t)[0].strip().split(':')))[2] )  for t in merge_time_not_bot]
    
    res = mannwhitneyu(merge_time_not_bot, merge_time_bot, method="auto")
    m_mt = ((sum(merge_time_not_bot) / len(merge_time_not_bot)) - (sum(merge_time_bot) / len(merge_time_bot))) / ((sum(merge_time_not_bot) / len(merge_time_not_bot)))
    print('Merge Time Test: {}'.format(res))

    # idle time
    idle_time_bot = df_bot['Idle Time'].tolist()
    idle_time_bot = [t for t in idle_time_bot if t != '0']
    for i, t in enumerate(idle_time_bot):
        if ',' in t:
            idle_time_bot[i] = t.replace(',', '')

    for i, t in enumerate(idle_time_bot):
        if 'day' in t and 'days' not in t:
            idle_time_bot[i] = t.replace('day', 'days')

    for i, t in enumerate(idle_time_bot):
        if 'days' not in t:
            idle_time_bot[i] = '0 days ' + t
    
    idle_time_bot = [(int(re.findall('(\d+)[^\d]days', t)[0]) * 86400) + ( list(map(float, re.findall('days(,?.*)', t)[0].strip().split(':')))[0] * 3600 + list(map(float, re.findall('days(,?.*)', t)[0].strip().split(':')))[1] * 60 + list(map(float, re.findall('days(,?.*)', t)[0].strip().split(':')))[2] )  for t in idle_time_bot]

    idle_time_no_bot = df_without_bot['Idle Time'].tolist()
    idle_time_no_bot = [t for t in idle_time_no_bot if t != '0']        
    for i, t in enumerate(idle_time_no_bot):
        if ',' in t:
            idle_time_no_bot[i] = t.replace(',', '')

    for i, t in enumerate(idle_time_no_bot):
        if 'day' in t and 'days' not in t:
            idle_time_no_bot[i] = t.replace('day', 'days')

    for i, t in enumerate(idle_time_no_bot):
        if 'days' not in t:
            idle_time_no_bot[i] = '0 days ' + t
    idle_time_no_bot = [(int(re.findall('(\d+)[^\d]days', t)[0]) * 86400) + ( list(map(float, re.findall('days(,?.*)', t)[0].strip().split(':')))[0] * 3600 + list(map(float, re.findall('days(,?.*)', t)[0].strip().split(':')))[1] * 60 + list(map(float, re.findall('days(,?.*)', t)[0].strip().split(':')))[2] )  for t in idle_time_no_bot]
    
    res = mannwhitneyu(idle_time_no_bot, idle_time_bot, method="auto")
    m_it = ((sum(idle_time_no_bot) / len(idle_time_no_bot)) - (sum(idle_time_bot) / len(idle_time_bot))) / ((sum(idle_time_no_bot) / len(idle_time_no_bot)))
    print('Idle Time Test: {}'.format(res))

    # churn
    churn_bot = df_bot['Churn'].tolist()
    churn_no_bot = df_without_bot['Churn'].tolist()
    
    res = mannwhitneyu(churn_no_bot, churn_bot, method="auto")
    m_ch = ((sum(churn_no_bot) / len(churn_no_bot)) - (sum(churn_bot) / len(churn_bot))) / ((sum(churn_no_bot) / len(churn_no_bot)))
    print('Churn Test: {}'.format(res))

    # comment quantity
    cq_bot = comments_bot['Comment Count'].tolist()
    cq_not_bot = comments__without_bot['Comment Count'].tolist()
    
    res = mannwhitneyu(cq_not_bot, cq_bot, method="auto")
    m_cq = ((sum(cq_not_bot) / len(cq_not_bot)) - (sum(cq_bot) / len(cq_bot))) / ((sum(cq_not_bot) / len(cq_not_bot)))
    print('Comment Quantity Test: {}'.format(res))

    # developer quantity
    dq_bot = df_bot['Developer Quantity'].tolist()
    dq_not_bot = df_without_bot['Developer Quantity'].tolist()
    
    res = mannwhitneyu(dq_not_bot, dq_bot, method="auto")
    m_dq = ((sum(dq_not_bot) / len(dq_not_bot)) - (sum(dq_bot) / len(dq_bot))) / ((sum(dq_not_bot) / len(dq_not_bot)))
    print('Developer Quantity Test: {}'.format(res))

    print('TuraroundTime-Diff: {}'.format(m_tt))
    print('MergeTime-Diff: {}'.format(m_mt))
    print('IdleTime-Diff: {}'.format(m_it))
    print('Churn-Diff: {}'.format(m_ch))
    print('CommentQuantity-Diff: {}'.format(m_cq))
    print('DeveloperQuantity-Diff: {}'.format(m_dq))

    print('\n\n\nPrinting Statistics Now:\n\n\n')

    df_activity_rate = pd.read_csv('/Users/rehmanh/Desktop/Research/Chenhao Bot Study/RQ4_WithBots_ActivityRates.csv', index_col=False)
    activity_rates = df_activity_rate['Bot Activity Rate'].tolist()

    stat, p_value = kstest(sample(activity_rates, 50), 'norm')
    print('Normal Dist for Activity Rate: {}'.format(p_value))

    """
        Statistics for Turnaround Time
    """

    # stat, p_value = kstest(sample(tt_bot, 50), 'norm')
    # print('P-value for Turnarount Time WITH BOT: {}'.format(p_value))

    # stat, p_value = kstest(sample(tt_no_bot, 50), 'norm')
    # print('P-value for Turnarount Time WITHOUT BOT: {}'.format(p_value))

    # ks2, p_val = ks_2samp(sample(tt_bot, 50), sample(tt_no_bot, 50))
    # print("TEST 2 P VAL: {}".format(p_val))
    
    ar = activity_rates
    if len(activity_rates) > len(tt_bot):
        ar = activity_rates[0:len(tt_bot)]

    corr, _ = pearsonr(tt_bot, tt_bot)
    spear, _ = spearmanr(tt_bot, tt_bot)
    kend, _ = kendalltau(tt_bot, tt_bot)
    print('Person Correlation for Turaround Time: %.3f' % corr)
    print('Spearman Correlation for Turnaround Time: %.3f' % spear)
    print('Kendalls Tau for Turaround Time: %.3f' % kend)
    print('\n')

    """
        Statistics for Merge Time
    """
    ar = activity_rates
    if len(activity_rates) > len(merge_time_bot):
        ar = activity_rates[0:len(merge_time_bot)]
    
    corr, _ = pearsonr(ar, merge_time_bot)
    spear, _ = spearmanr(ar, merge_time_bot)
    kend, _ = kendalltau(ar, merge_time_bot)
    print('Person Correlation for Merge Time: %.3f' % corr)
    print('Spearman Correlation for Merge Time: %.3f' % spear)
    print('Kendalls Tau for Merge Time: %.3f' % kend)
    print('\n')

    """
        Statistics for Idle Time
    """
    # stat, p_value = kstest(sample(idle_time_bot, 50), 'norm')
    # print('P-value for Idle Time WITH BOT: {}'.format(p_value))

    # stat, p_value = kstest(sample(idle_time_no_bot, 50), 'norm')
    # print('P-value for Idle Time WITHOUT BOT: {}'.format(p_value))

    ar = activity_rates
    if len(activity_rates) > len(idle_time_bot):
        ar = activity_rates[0:len(idle_time_bot)]
    
    corr, _ = pearsonr(ar, idle_time_bot)
    spear, _ = spearmanr(ar, idle_time_bot)
    kend, _ = kendalltau(ar, idle_time_bot)
    print('Person Correlation for Idle Time: %.3f' % corr)
    print('Spearman Correlation for Idle Time: %.3f' % spear)
    print('Kendalls Tau for Idle Time: %.3f' % kend)
    print('\n')

    """
        Statistics for Churn
    """
    # stat, p_value = kstest(sample(churn_bot, 50), 'norm')
    # print('P-value for Churn WITH BOT: {}'.format(p_value))

    # stat, p_value = kstest(sample(churn_no_bot, 50), 'norm')
    # print('P-value for Churn WITHOUT BOT: {}'.format(p_value))


    ar = activity_rates
    if len(activity_rates) > len(churn_bot):
        ar = activity_rates[0:len(churn_bot)]
    
    corr, _ = pearsonr(ar, churn_bot)
    spear, _ = spearmanr(ar, churn_bot)
    kend, _ = kendalltau(ar, churn_bot)
    print('Person Correlation for Churn: %.3f' % corr)
    print('Spearman Correlation for Churn: %.3f' % spear)
    print('Kendalls Tau for Churn: %.3f' % kend)
    print('\n')

    """
        Statistics for Comment Quantity
    """
    # stat, p_value = kstest(sample(cq_bot, 50), 'norm')
    # print('P-value for Comment Quantity WITH BOT: {}'.format(p_value))

    # stat, p_value = kstest(sample(cq_not_bot, 50), 'norm')
    # print('P-value for Comment Quantity WITHOUT BOT: {}'.format(p_value))


    ar = activity_rates
    if len(activity_rates) > len(cq_bot):
        ar = activity_rates[0:len(cq_bot)]
    
    corr, _ = pearsonr(ar, cq_bot)
    spear, _ = spearmanr(ar, cq_bot)
    kend, _ = kendalltau(ar, cq_bot)
    print('Person Correlation for Comment Quantity: %.3f' % corr)
    print('Spearman Correlation for Comment Quantity: %.3f' % spear)
    print('Kendalls Tau for Comment Quantity: %.3f' % kend)
    print('\n')

    """
        Statistics for Developer Quantity
    """
    # stat, p_value = kstest(sample(dq_bot, 50), 'norm')
    # print('P-value for Developer Quantity WITH BOT: {}'.format(p_value))

    # stat, p_value = kstest(sample(dq_not_bot, 50), 'norm')
    # print('P-value for Developer Quantity WITHOUT BOT: {}'.format(p_value))
    ar = activity_rates
    if len(activity_rates) > len(dq_bot):
        ar = activity_rates[0:len(dq_bot)]
    
    corr, _ = pearsonr(ar, dq_bot)
    spear, _ = spearmanr(ar, dq_bot)
    kend, _ = kendalltau(ar, dq_bot)
    print('Person Correlation for Developer Quantity: %.3f' % corr)
    print('Spearman Correlation for Developer Quantity: %.3f' % spear)
    print('Kendalls Tau for Developer Quantity: %.3f' % kend)
    print('\n')

if __name__ == '__main__':
    conduct_tests()
    