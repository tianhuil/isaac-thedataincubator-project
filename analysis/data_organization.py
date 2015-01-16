
import pandas as pd
import myplotting as myp

myp.setfigdefaults()

def load_data_file(fname='data/LoanStats3a.csv'):
    """
    Load a Lending Club loan-history, and add some columns for common values
    that we will need later. In particular, convert categorical string-type
    attributes to numbers.
    """
    subgrades = [a + n for a in 'ABCDEFG' for n in '12345']

    # Load all 36 month loans
    dat = pd.read_csv(fname, skiprows=1)
    use = isfinite(dat.member_id) & (dat.term == ' 36 months')
    dat = dat[use]

    # Codes for status of loans
    statuses = \
      [ 'Charged Off',# 0
        'Current',# 1
        'Default',# 2
        'Does not meet the credit policy.  Status:Charged Off',# 3
        'Does not meet the credit policy.  Status:Current',# 4
        'Does not meet the credit policy.  Status:Default',# 5
        'Does not meet the credit policy.  Status:Fully Paid',# 6
        'Does not meet the credit policy.  Status:In Grace Period',# 7
        'Does not meet the credit policy.  Status:Late (31-120 days)',# 8
        'Fully Paid',# 9
        'In Grace Period',# 10
        'Late (16-30 days)',# 11
        'Late (31-120 days)']# 12

    # Loans we consider to have failed
    has_status = [dat.loan_status.apply(lambda x: s == x) for s in statuses]
    
    assert(sum(map(sum, has_status)) == len(dat.index)) # all accounted for
    
    failed = has_status[0] | has_status[2] | has_status[3]
    
    status_code = nan * has_status[0]
    for i in range(len(statuses)): status_code[has_status[i]] = i
        
    # Loans for which we think we know the final reults
    completed = has_status[0] | has_status[2] | has_status[3] | \
            has_status[6] | has_status[9]
    
    dat['status_code'] = status_code
    dat['completed'] = completed
    dat['failed'] = failed

    # LC assigned credit grades and subgrades
    grade = array(dat['grade'].tolist())
    grd = zeros_like(grade, dtype=int)
    for i, g in enumerate(unique(grade)):
        grd[grade == g] = i
    subgrade = array(dat.sub_grade.tolist())
    sgrd = zeros_like(subgrade, dtype=int)
    for i, g in enumerate(subgrades):
        sgrd[subgrade == g] = i
    dat['subgrade_code'] = sgrd

    purp = pd.Series(index=dat.index, dtype=int)
    for i, p in enumerate(unique(dat.purpose)):
        purp[dat.purpose == p] = i
    dat['purpose_code'] = purp
    
    housing = pd.Series(index=dat.index, dtype=int)
    for i, p in [
            (0, 'NONE'), 
            (1, 'OTHER'), 
            (2, 'RENT'), 
            (3, 'OWN'), 
            (4, 'MORTGAGE')]:
        housing[dat.home_ownership == p] = i
    dat['home_code'] = housing

    # Interest rate assigned to loan by LC
    percent2float = (# format: ' 15.0%' | 15.0
        lambda x: float(x[:-1]) if isinstance(x, str) else float(x))
    dat['int_rate'] = dat['int_rate'].apply(percent2float)

    dat['revol_util'] = dat['revol_util'].apply(percent2float)
    dat['is_inc_v'] = dat['is_inc_v'] != 'Not Verified'

    def parse_date(x): return pd.datetime.strptime(x, '%Y-%m-%d')
    accept = dat.accept_d.apply(parse_date)
    last   = dat.last_pymnt_d.fillna(dat.accept_d).apply(parse_date)
    dat['loan_lifetime']  = ((last - accept) / timedelta64(1, 'D'))
    today  = pd.datetime.today()
    dat['loan_age']    = ((today - accept) / timedelta64(1, 'D')).apply(round)

    # Get rid of null values
    dat.desc = dat.desc.fillna(value='')
    dat.total_acc = dat.total_acc.fillna(value=0.)
    dat.annual_inc = dat.annual_inc.fillna(value=0.)

    return dat


def failure_by_attr(df, attr):
    """
    Group the supplied frame by the indicated attribute, and then plot
    the failure rate with standard deviation for each unique value of the
    attribute.
    """
    g = df.groupby(attr)
    failure = g.apply(lambda x: pd.Series(dict(
        rate=float(len(x[x.failed].index)) / x.shape[0], count=x.shape[0])))
    failure['std'] = sqrt(
        failure['rate'] * (1 - failure['rate']) / failure['count'])
    failure.plot(y = 'rate', yerr = 'std', xticks=range(failure.shape[0]), 
                 figsize=(15,6), linestyle='none')
    ylabel('Failure rate +/- STD')

