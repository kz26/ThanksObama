from imo_api import IMOInterface
from lcd_db import LCDInterface
import random
import re
import bleach

icd10_re = re.compile('^[ABCDEFGHIJKLMNOPQS]')

def gen_icd10_procedures_question():
	# generates a "which procedures are medically necessary for a given ICD10" question
	IMO = IMOInterface()
	icd10 = None
	while not icd10:
		icd10 = LCDInterface.random_icd10()
		if not icd10_re.match(icd10):
			icd10 = None
	imo_term = IMO.get_imo_from_query(icd10)
	sp = [x[0] for x in LCDInterface.get_icd10_procedures(icd10)]
	choices = [random.choice(sp)]
	bp = LCDInterface.get_icd10_unsupported_procedures(icd10)
	if len(bp) >= 4:
		random.shuffle(bp)
		choices.extend([x[0] for x in bp[:4]])
	else:
		sp_set = set(sp)
		while len(choices) < 5:
			p = LCDInterface.random_procedure()
			if p not in sp_set:
				 choices.append(p)
	choices = [bleach.clean(x, tags=[], attributes=[], strip=True).strip(" '\"") for x in choices]
	answer = choices[0]
	random.shuffle(choices)
	return {
		'question': "A patient is diagnosed with <b>%s</b>. An appropriate procedure that might be ordered is" % (imo_term),
		'answer': choices.index(answer),
		'choices': choices
	}

def gen_procedures_icd10_question():
	# generates a "For which condition is the given procedure medically necessary" question
	IMO = IMOInterface()
	icd10s = None
	while not icd10s:
		p_id, p_name = LCDInterface.random_supported_procedure()
		p_name = bleach.clean(p_name, tags=[], attributes=[], strip=True).strip(" '\"")
		icd10s = [x[0] for x in LCDInterface.get_procedure_supported_icd10s(p_id) if icd10_re.match(x[0])]
	choices = [random.choice(icd10s)]
	answer_icd10 = choices[0]
	unsupported_icd10s = [x[0] for x in LCDInterface.get_procedure_unsupported_icd10s(p_id) if icd10_re.match(x[0])]
	if len(unsupported_icd10s) >= 4:
		random.shuffle(unsupported_icd10s)
		choices.extend([x for x in unsupported_icd10s[:4]])
	else:
		icd10s_set = set(icd10s)
		while len(choices) < 5:
			icd10 = LCDInterface.random_icd10()
			if icd10 not in icd10s_set and icd10_re.match(icd10):
				choices.append(icd10)
	choices = [bleach.clean(IMO.get_imo_from_query(x), tags=[], attributes=[], strip=True).strip(" '\"") for x in choices]
	answer = choices[0]
	random.shuffle(choices)
	return {
		'question': "<b>%s</b> is appropriate for which one of the following conditions?" % (p_name),
		'answer': choices.index(answer),
		'choices': choices
	}
	
def gen_question():
	# generates one of the above two question types with equal probability
	if random.random() < 0.5:
		return gen_icd10_procedures_question()
	else:
		return gen_procedures_icd10_question() 	

