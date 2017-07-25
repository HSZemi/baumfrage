#! /usr/bin/env python3

import sys
import os
import csv
import json
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

plt.rc('axes', axisbelow=True)

def diagram56(reasons, n_groups, title, pdf):

	vals_longer_5 = []
	vals_longer_6 = []
	vals_nolonger_6 = []
	labels_y = []

	for k in sorted(reasons, key=lambda k: reasons[k]['longer_5']):
		vals_longer_5.append(reasons[k]['longer_5'])
		vals_longer_6.append(reasons[k]['longer_6'])
		vals_nolonger_6.append(reasons[k]['nolonger_6'])
		labels_y.append(k)

	fig, ax = plt.subplots()

	index = np.arange(n_groups)
	bar_width = 0.25

	opacity = 1

	rects1 = plt.barh(index + (bar_width), vals_longer_5, bar_width,
			alpha=opacity,
			color='#b33b3b',
			edgecolor=None,
			linewidth=0,
			label='Longer_5')

	rects2 = plt.barh(index, vals_longer_6, bar_width,
			alpha=opacity,
			color='#246b6b',
			edgecolor=None,
			linewidth=0,
			label='Longer_6')

	rects3 = plt.barh(index - bar_width, vals_nolonger_6, bar_width,
			alpha=opacity,
			color='#82a738',
			edgecolor=None,
			linewidth=0,
			label='notLonger_6')

	plt.xlabel('Anteil (bzgl. Untergruppe)')
	plt.ylabel('Grund')
	plt.title(title)
	plt.grid(color='gray')
	plt.xlim(0,1)
	plt.yticks(index + bar_width / 2, labels_y)
	plt.legend(loc='best')

	plt.tight_layout()
	#plt.show()	
	pdf.savefig(fig)
	plt.close()
	
def simplebar(data, n_groups, title, xlabel, ylabel, labels_x, pdf, data2=None, label1=None, label2=None, titlesize=14, color1='#b33b3b', color2='#246b6b'):

	fig, ax = plt.subplots()

	index = np.arange(n_groups)
	bar_width = 0.25

	opacity = 1
	
	pos1 = index
	if data2:
		pos1 = index - (bar_width/2)

	rects1 = plt.bar(pos1, data, bar_width,
			alpha=opacity,
			color=color1,
			edgecolor=None,
			linewidth=0,
			label=label1)
	
	if data2:
		rects2 = plt.bar(index + (bar_width/2), data2, bar_width,
				alpha=opacity,
				color=color2,
				edgecolor=None,
				linewidth=0,
				label=label2)
		

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title, fontsize=titlesize)
	plt.grid(color='gray')
	plt.xticks(index + bar_width / 2, labels_x)
	if data2:
		plt.legend(loc='best')

	#plt.show()
	
	plt.xlim([min(index) - 0.2, max(index) + 0.5])
	locs, labels = plt.xticks()
	plt.setp(labels, rotation=270)
	plt.tight_layout()
	pdf.savefig(fig)
	plt.close()
	
def diagram2(data, title, pdf):

	fig, ax = plt.subplots()

	
	scatter1 = plt.scatter(data['x'], data['y'],
			color='b')
	line1 = plt.plot([1,7,16],[0,180,180], color='#000000')

	plt.xlabel('Semester')
	plt.ylabel('CP')
	plt.title(title)
	ylim = plt.ylim()
	plt.ylim(0,ylim[1])
	plt.xlim(0,17)
	plt.grid(color='gray')
	#plt.legend(loc='best')

	plt.tight_layout()
	#plt.show()	
	pdf.savefig(fig)
	plt.close()


if len(sys.argv) != 3:
	print("Usage: {} <path_with_json_data_files> <output.pdf>".format(sys.argv[0]))
	sys.exit()

rawdata = []
data = {}
#keys = set()

keys = ["q1", "q2_fsem", "q2_lp", "q3", "q4", "q5-dependencies", "q5-failed-admission", "q5-failed-module", "q5-family", "q5-future", "q5-grade-improvement", "q5-job", "q5-long-project-group", "q5-minor-subject", "q5-modules-o-plenty", "q5-moved-module", "q5-other", "q5-pg2", "q5-planned", "q5-thesis-problems", "q6-dependencies", "q6-failed-admission", "q6-failed-module", "q6-family", "q6-future", "q6-grade-improvement", "q6-job", "q6-long-project-group", "q6-minor-subject", "q6-modules-o-plenty", "q6-moved-module", "q6-other", "q6-pg2", "q6-planned", "q6-thesis-problems", "q7", "q8", "timestamp", "userid"]

ids = {"q1-teacher":"Nein, ich studiere noch Informatik auf Lehramt.",
"q1-currentstudent":"Nein, ich studiere noch im Bachelorstudiengang Informatik.",
"q1-formerteacher":"Ja, ich habe meinen Bachelorabschluss im Lehramt Informatik (LA BA Gym Ge) an der Uni Bonn erworben.",
"q1-formerstudent":"Ja, ich habe meinen Bachelorabschluss in Informatik (B.Sc.) an der Uni Bonn erworben.",
"q1-external":"Ja, ich habe meinen Bachelorabschluss woanders erworben.",
"q1-other":"Nein, ich studiere gar nicht Informatik.",

"q2-fsem":"In welchem Fachsemester befindest du dich aktuell?",
"q2-lp":"Wie viele Leistungspunkte hast du bislang erworben?",

"q3-fsem":"Im wievielten Fachsemester wirst du dein Bachelorstudium voraussichtlich abschließen?",

"q4-fsem":"Im wievielten Fachsemester hast du dein Bachelorstudium abgeschlossen?",

"q5-failed-admission":"Zulassung zu mindestens einer Modulabschlussprüfung nicht geschafft",
"q5-failed-module":"Mindestens ein Modul nicht bestanden",
"q5-moved-module":"Module in spätere Semester verschoben",
"q5-minor-subject":"Probleme mit dem Nebenfach",
"q5-dependencies":"Ungünstige Modulabhängigkeiten",
"q5-grade-improvement":"Notenverbesserung in mindestens einem Pflichtmodul",
"q5-modules-o-plenty":"Mehr Wahlpflichtmodule als nötig besucht",
"q5-pg2":"Zweite Projektgruppe belegt",
"q5-long-project-group":"Projektgruppe hat zu lange gedauert",
"q5-thesis-problems":"Thema der Bachelorarbeit wurde einmal zurückgegeben / Bachelorarbeit wurde einmal nicht bestanden",
"q5-job":"Belastung durch Nebenjob oder Beruf",
"q5-future":"Ich will/wollte zuerst wissen, was ich danach mache, bevor ich das Studium abschließe.",
"q5-family":"Familiäre oder persönliche Gründe",
"q5-planned":"Ich hatte nie vor, in Regelstudienzeit fertig zu werden",
"q5-other":"Weiteres",

"q6-failed-admission":"Zulassung zu mindestens einer Modulabschlussprüfung nicht geschafft",
"q6-failed-module":"Mindestens ein Modul nicht bestanden",
"q6-moved-module":"Module in spätere Semester verschoben",
"q6-minor-subject":"Probleme mit dem Nebenfach",
"q6-dependencies":"Ungünstige Modulabhängigkeiten",
"q6-grade-improvement":"Notenverbesserung in mindestens einem Pflichtmodul",
"q6-modules-o-plenty":"Mehr Wahlpflichtmodule als nötig besucht",
"q6-pg2":"Zweite Projektgruppe belegt",
"q6-long-project-group":"Projektgruppe hat zu lange gedauert",
"q6-thesis-problems":"Thema der Bachelorarbeit wurde einmal zurückgegeben / Bachelorarbeit wurde einmal nicht bestanden",
"q6-job":"Belastung durch Nebenjob oder Beruf",
"q6-future":"Ich will/wollte zuerst wissen, was ich danach mache, bevor ich das Studium abschließe.",
"q6-family":"Familiäre oder persönliche Gründe",
"q6-planned":"Ich hatte nie vor, in Regelstudienzeit fertig zu werden",
"q6-other":"Weiteres",

"q7-other":"Mit der Bachelorarbeit beschäftige ich mich noch nicht",
"q7-currentlyworking":"Ich arbeite aktuell an meiner Bachelorarbeit",
"q7-unsure":"Ich bin unsicher / traue mir die Bachelorarbeit aktuell noch nicht zu",
"q7-clueless":"Ich weiß nicht genau wo ich anfangen soll mit der Suche nach einer Bachelorarbeit",
"q7-search-supervision-topic":"Ich suche derzeit aktiv eine Betreuung und ein Thema für meine Bachelorarbeit",
"q7-search-topic":"Ich suche derzeit mit meiner Betreuung ein Thema für meine Bachelorarbeit",
"q7-search-supervision":"Ich habe bereits ein Thema und suche dafür eine Betreuung",

"q8-both-same":"Ja, Thema und Betreuung blieben gleich",
"q8-same-supervision":"Ja, ein anderes Thema unter der gleichen Betreuung",
"q8-similar-topic":"Ja, ein ähnliches Thema unter anderer Betreuung",
"q8-referral":"Jein, mir wurden anderes Thema und Betreuung vermittelt",
"q8-no":"Nein."}

target_dir = sys.argv[1]

if not os.path.isdir(target_dir):
	print("Error: '{}' is not a directory.".format(target_dir))
	sys.exit()


rawdata = []

for filename in os.listdir(target_dir):
	fullpath = os.path.join(target_dir, filename)
	if os.path.isfile(fullpath) and fullpath[-5:] == ".json":
		with open(fullpath, "r") as f:
			dataset_raw = json.load(f)
			dataset = {}
			for key in keys:
				if key[:2] in ("q5","q6"):
					if dataset_raw[key[:2]][key]['checked'] == "true":
						dataset[key] = True
					else:
						dataset[key] = False
					if 'extra' in dataset_raw[key[:2]][key]:
						dataset["{}-extra".format(key)] = dataset_raw[key[:2]][key]['extra'].replace("\n","; ") # no newlines in tsv
					else:
						dataset["{}-extra".format(key)] = None
				else:
					dataset[key] = dataset_raw[key]
					if dataset_raw[key] in ("","-"):
						dataset[key] = None
					if dataset_raw[key] == "none":
						dataset[key] = None
					if dataset_raw[key] == ">15":
						dataset[key] = "16"
			rawdata.append(dataset)

for key in keys:
	print(key, end="\t")
	if key[:2] in ("q5","q6"):
		print("{}-extra".format(key), end="\t")
print("")

for item in rawdata:
	for key in keys:
		print(item[key], end="\t")
		if key[:2] in ("q5","q6"):
			print(item["{}-extra".format(key)], end="\t")
	print("")


#print(rawdata)

# Verteilung current / former / currentteacher / formerteacher

distribution_q1 = {}

for item in rawdata:
	if item['q1'] not in distribution_q1:
		distribution_q1[item['q1']] = 0
	distribution_q1[item['q1']] += 1
	
	if item['q1'] not in data:
		data[item['q1']] = []
	data[item['q1']].append(item)
	

#print(distribution_q1)
rszdata = {'former':{'in_rsz':0,'out_of_rsz':0},'current':{'in_rsz':0,'out_of_rsz':0}}

group = "q1-currentstudent"

current_student_longer_5_abs = {}
current_student_longer_6_abs = {}
current_student_notlonger_6_abs = {}
current_student_longer_5 = {}
current_student_longer_6 = {}
current_student_notlonger_6 = {}

current_sem_lp = {'x':[],'y':[]}

q7data = {}

q8data = {}

rsz = 0
not_rsz = 0
for k in keys:
	if k[0:3] == "q5-" and k[-6:] != "-extra":
		current_student_longer_5_abs[k] = 0
	if k[0:3] == "q6-" and k[-6:] != "-extra":
		current_student_longer_6_abs[k] = 0
		current_student_notlonger_6_abs[k] = 0
for item in data[group]:
	in_rsz = False
	if item['q3'] and int(item['q3']) > 6:
		not_rsz += 1
		rszdata['current']['out_of_rsz'] += 1
	if item['q3'] and int(item['q3']) <= 6:
		in_rsz = True
		rsz += 1
		rszdata['current']['in_rsz'] += 1
	for key in current_student_longer_5_abs:
		if item[key]:
			current_student_longer_5_abs[key] += 1
	if in_rsz:
		for key in current_student_notlonger_6_abs:
			if item[key]:
				current_student_notlonger_6_abs[key] += 1
	else:
		for key in current_student_longer_6_abs:
			if item[key]:
				current_student_longer_6_abs[key] += 1
	
	current_sem_lp['x'].append(int(item['q2_fsem']))
	current_sem_lp['y'].append(int(item['q2_lp']))
	
	if item['q7'] not in q7data:
		q7data[item['q7']] = 0
	q7data[item['q7']] += 1
	

		

for k in current_student_longer_5_abs:
	current_student_longer_5[k] = current_student_longer_5_abs[k] / not_rsz
for k in current_student_longer_6_abs:
	current_student_longer_6[k] = current_student_longer_6_abs[k] / not_rsz
for k in current_student_notlonger_6_abs:
	current_student_notlonger_6[k] = current_student_notlonger_6_abs[k] / rsz

reasons = {}
for k in current_student_longer_5:
	key = k[3:]
	reasons[key] = {"longer_5":0,"longer_6":0,"nolonger_6":0}
	reasons[key]['longer_5'] = current_student_longer_5[k]
for k in current_student_longer_6:
	key = k[3:]
	reasons[key]['longer_6'] = current_student_longer_6[k]
	reasons[key]['nolonger_6'] = current_student_notlonger_6[k]
	
reasons_abs = {}
for k in current_student_longer_5_abs:
	key = k[3:]
	reasons_abs[key] = {"longer_5":0,"longer_6":0,"nolonger_6":0}
	reasons_abs[key]['longer_5'] = current_student_longer_5_abs[k]
for k in current_student_longer_6:
	key = k[3:]
	reasons_abs[key]['longer_6'] = current_student_longer_6_abs[k]
	reasons_abs[key]['nolonger_6'] = current_student_notlonger_6_abs[k]
	


group = "q1-formerstudent"

former_student_longer_5_abs = {}
former_student_longer_6_abs = {}
former_student_notlonger_6_abs = {}
former_student_longer_5 = {}
former_student_longer_6 = {}
former_student_notlonger_6 = {}

rsz = 0
not_rsz = 0
for k in keys:
	if k[0:3] == "q5-" and k[-6:] != "-extra":
		former_student_longer_5_abs[k] = 0
	if k[0:3] == "q6-" and k[-6:] != "-extra":
		former_student_longer_6_abs[k] = 0
		former_student_notlonger_6_abs[k] = 0
for item in data[group]:
	in_rsz = False
	if item['q4'] and int(item['q4']) > 6:
		rszdata['former']['out_of_rsz'] += 1
		not_rsz += 1
	if item['q4'] and int(item['q4']) <= 6:
		in_rsz = True
		rsz += 1
		rszdata['former']['in_rsz'] += 1
	for key in former_student_longer_5_abs:
		if item[key]:
			former_student_longer_5_abs[key] += 1
	if in_rsz:
		for key in former_student_notlonger_6_abs:
			if item[key]:
				former_student_notlonger_6_abs[key] += 1
	else:
		for key in former_student_longer_6_abs:
			if item[key]:
				former_student_longer_6_abs[key] += 1
		

for k in former_student_longer_5_abs:
	former_student_longer_5[k] = former_student_longer_5_abs[k] / not_rsz
for k in former_student_longer_6_abs:
	former_student_longer_6[k] = former_student_longer_6_abs[k] / not_rsz
for k in former_student_notlonger_6_abs:
	former_student_notlonger_6[k] = former_student_notlonger_6_abs[k] / rsz


formerreasons = {}
for k in former_student_longer_5:
	key = k[3:]
	formerreasons[key] = {"longer_5":0,"longer_6":0,"nolonger_6":0}
	formerreasons[key]['longer_5'] = former_student_longer_5[k]
for k in former_student_longer_6:
	key = k[3:]
	formerreasons[key]['longer_6'] = former_student_longer_6[k]
	formerreasons[key]['nolonger_6'] = former_student_notlonger_6[k]

formerreasons_abs = {}
for k in former_student_longer_5_abs:
	key = k[3:]
	formerreasons_abs[key] = {"longer_5":0,"longer_6":0,"nolonger_6":0}
	formerreasons_abs[key]['longer_5'] = former_student_longer_5_abs[k]
for k in former_student_longer_6_abs:
	key = k[3:]
	formerreasons_abs[key]['longer_6'] = former_student_longer_6_abs[k]
	formerreasons_abs[key]['nolonger_6'] = former_student_notlonger_6_abs[k]


for group in data:
	for item in data[group]:
		if item['q8']:
			if item['q8'] not in q8data:
				q8data[item['q8']] = 0
			q8data[item['q8']] += 1

jointreasons_abs = {}

for key in reasons_abs:
	jointreasons_abs[key] = reasons_abs[key]
	for k in reasons_abs[key]:
		jointreasons_abs[key][k] += formerreasons_abs[key][k]

failmovestats = {"none":0,"failonly":0,"moveonly":0,"failmove":0}

for item in rawdata:
	failed = False
	moved = False
	if item['q5-moved-module'] or item['q6-moved-module']:
		moved = True
	if item['q5-failed-admission'] or item['q6-failed-admission'] or item['q5-failed-module'] or item['q5-failed-module']:
		failed = True
	
	if failed and moved:
		failmovestats['failmove'] += 1
	elif failed:
		failmovestats['failonly'] += 1
	elif moved:
		failmovestats['moveonly'] += 1
	else:
		failmovestats['none'] += 1
	
	


with PdfPages(sys.argv[2]) as pdf:
	
	data = []
	labels_x = []
	for k in sorted(distribution_q1, key=distribution_q1.get):
		data.append(distribution_q1[k])
		labels_x.append(k)
	simplebar(data, len(labels_x), "Verteilung auf Gruppen", 'Gruppe', '# Studierende', labels_x, pdf)
	
	data = [rszdata['current']['in_rsz'],rszdata['former']['in_rsz']]
	label1 = 'in_rsz'
	data2 = [rszdata['current']['out_of_rsz'],rszdata['former']['out_of_rsz']]
	label2 = 'out_of_rsz'
	labels_x = ['current','former']
	simplebar(data, len(labels_x), "RSZ nach Gruppen", 'Gruppe', '# Studierende', labels_x, pdf, data2, label1, label2)

	diagram2(current_sem_lp, 'Gruppe: currentstudent', pdf)
	
	n_groups = len(current_student_longer_5)
	diagram56(reasons, n_groups, 'Gruppe: currentstudent', pdf)

	n_groups = len(former_student_longer_5)
	diagram56(formerreasons, n_groups, 'Gruppe: formerstudent', pdf)
	
	for key in jointreasons_abs:
		data = [jointreasons_abs[key]["longer_5"], jointreasons_abs[key]["longer_6"]+jointreasons_abs[key]["nolonger_6"]]
		labels = ["Ja","Nein"]
		simplebar(data, len(labels_x), ids["q5-{}".format(key)], 'studienverlängernd?', '# Studierende', labels, pdf, titlesize=10)
		
	
	
	data = []
	labels_x = []
	colors = []
	for k in sorted(q7data, key=q7data.get):
		data.append(q7data[k])
		labels_x.append(k)
		if k == "q7-other":
			colors.append('#246b6b')
		else:
			colors.append('#b33b3b')
	simplebar(data, len(labels_x), "Wie steht's mit der BA? (currentstudent)", 'Antwort', '# Studierende', labels_x, pdf, color1=colors)
	
	
	data = []
	labels_x = []
	colors = []
	for k in sorted(q8data, key=q8data.get):
		data.append(q8data[k])
		labels_x.append(k)
		if k == "q8-no":
			colors.append('#246b6b')
		else:
			colors.append('#b33b3b')
	simplebar(data, len(labels_x), "PG->BA?", 'Antwort', '# Studierende', labels_x, pdf, color1=colors)

	data = []
	labels_x = []
	for k in sorted(failmovestats, key=failmovestats.get):
		data.append(failmovestats[k])
		labels_x.append(k)
	simplebar(data, len(labels_x), "Modul nicht bestanden und Modul verschoben", 'Gruppe', '# Studierende', labels_x, pdf)



	