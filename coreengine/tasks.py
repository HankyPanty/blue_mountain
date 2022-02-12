from coreengine.models import *
import pandas as pd

def get_questions_from_sheet(sheet_path):
	read_file = pd.DataFrame(pd.read_excel(sheet_path, engine='openpyxl')).transpose()
	length = len(read_file) - 1 if len(read_file)>0 else 0
	data_team_wise = {}
	list_data = []
	try:
		for i in range(length):
			data = dict(read_file[i])
			if data_team_wise.get(data["team"], []):
				data_team_wise[data["team"]].append([data["question"], data["opt_1"], data["opt_2"], data["opt_3"], data["opt_4"], data["answer"], data["image"], data["explaination"]])
			else:
				data_team_wise[data["team"]] = [[data["question"], data["opt_1"], data["opt_2"], data["opt_3"], data["opt_4"], data["answer"], data["image"], data["explaination"]]]
	except:
		pass
	for key in data_team_wise:
		list_data.append([key, data_team_wise[key]])
	return list_data