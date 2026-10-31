from app.engine import evaluate,rank_schemes

def test_eligible():
    assert evaluate({'age':24,'state':'Madhya Pradesh'},{'age_min':18,'states':['Madhya Pradesh']})['status']=='eligible_by_recorded_rules'
def test_ineligible():
    assert evaluate({'age':16},{'age_min':18})['status']=='ineligible'
def test_unknown():
    assert evaluate({}, {'income_max':100000})['status']=='insufficient_information'
def test_unsupported_rule_fails_closed():
    assert evaluate({'age':22},{'residency_certificate':True})['status']=='insufficient_information'
def test_rank():
    schemes=[{'name':'Student scholarship','description':'Education support'},{'name':'Agriculture aid','description':'Farm support'}]
    assert rank_schemes('student education',schemes)[0]['name']=='Student scholarship'
