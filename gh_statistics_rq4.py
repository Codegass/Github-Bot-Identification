from scipy.stats import mannwhitneyu
import pandas as pd
import re

def conduct_tests():
    df_bot = pd.read_csv('/Users/rehmanh/Desktop/Research/Chenhao Bot Study/RQ4_WithBots.csv', index_col=False)
    df_without_bot = pd.read_csv('/Users/rehmanh/Desktop/Research/Chenhao Bot Study/RQ4_WithOutBots.csv', index_col=False)

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
    cq_bot = df_bot['Comment Count'].tolist()
    cq_not_bot = df_without_bot['Comment Count'].tolist()
    
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

if __name__ == '__main__':
    conduct_tests()
    