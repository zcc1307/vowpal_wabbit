import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab
import os
import glob
import pandas as pd
import scipy.stats as stats
from itertools import compress
from math import sqrt
import argparse
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap
from matplotlib.font_manager import FontProperties
from collections import Counter
import random


class model:
	def __init__(self):
		pass

def sum_files(result_path):
	prevdir = os.getcwd()
	os.chdir(result_path)
	dss = sorted(glob.glob('*.sum'))
	os.chdir(prevdir)
	return dss

def parse_sum_file(sum_filename):
	f = open(sum_filename, 'r')
	#f.seek(0, 0)
	table = pd.read_table(f, sep='\s+',lineterminator='\n',error_bad_lines=False)

	return table

def get_z_scores(errors_1, errors_2, sizes):
	z_scores = []
	for i in range(len(errors_1)):
		#print i
		z_scores.append( z_score(errors_1[i], errors_2[i], sizes[i]) )
	return z_scores

def z_score(err_1, err_2, size):
	if (abs(err_1) < 1e-6 or abs(err_1) > 1-1e-6) and (abs(err_2) < 1e-6 or abs(err_2) > 1-1e-6):
		return 0

	#print err_1, err_2, size, sqrt( (err_1*(1 - err_1) + err_2*(1-err_2)) / size )

	z = (err_1 - err_2) / sqrt( (err_1*(1 - err_1) + err_2*(1-err_2)) / size )
	return z
	#print z

def is_significant(z):
	if (stats.norm.cdf(z) < 0.05) or (stats.norm.cdf(z) > 0.95):
		return True
	else:
		return False

def plot_comparison(errors_1, errors_2, sizes):
	#print title
	plt.plot([0,1],[0,1])
	z_scores = get_z_scores(errors_1, errors_2, sizes)
	sorted_z_scores = sorted(enumerate(z_scores), key=lambda x:x[1])
	#for s in sorted_z_scores:
	#	print s, is_significant(s[1])

	significance = map(is_significant, z_scores)
	results_signi_1 = list(compress(errors_1, significance))
	results_signi_2 = list(compress(errors_2, significance))
	plt.scatter(results_signi_1, results_signi_2, s=18, c='r')

	insignificance = [not b for b in significance]
	results_insigni_1 = list(compress(errors_1, insignificance))
	results_insigni_2 = list(compress(errors_2, insignificance))

	plt.scatter(results_insigni_1, results_insigni_2, s=2, c='k')

	len_errors = len(errors_1)
	wins_1 = [z_scores[i] < 0 and significance[i] for i in range(len_errors) ]
	wins_2 = [z_scores[i] > 0 and significance[i] for i in range(len_errors) ]
	num_wins_1 = wins_1.count(True)
	num_wins_2 = wins_2.count(True)

	return num_wins_1, num_wins_2

def alg_info(alg_name, result_lst):
	if (alg_name[0] == 0):
		return result_lst[0]
	if (alg_name[2] == True and alg_name[3] == True and alg_name[0] == 2):
		return result_lst[1]
	if (alg_name[2] == False and alg_name[3] == False and alg_name[0] == 1):
		return result_lst[2]
	if (alg_name[2] == False and alg_name[3] == True and alg_name[0] == 1):
		return result_lst[3]
	if (alg_name[2] == True and alg_name[3] == False and alg_name[0] == 1):
		return result_lst[4]
	if (alg_name[2] == True and alg_name[3] == True and alg_name[1] == 2 and alg_name[4] == 2):
		return result_lst[5]
	if (alg_name[2] == True and alg_name[3] == True and alg_name[1] == 4 and alg_name[4] == 2):
		return result_lst[6]
	if (alg_name[2] == True and alg_name[3] == True and alg_name[1] == 8 and alg_name[4] == 2):
		return result_lst[7]
	if (alg_name[2] == True and alg_name[3] == True and alg_name[1] == 16 and alg_name[4] == 2):
		return result_lst[8]
	if (alg_name[2] == True and alg_name[3] == True and alg_name[1] == 2 and alg_name[4] == 3):
		return result_lst[9]
	if (alg_name[2] == True and alg_name[3] == True and alg_name[1] == 4 and alg_name[4] == 3):
		return result_lst[10]
	if (alg_name[2] == True and alg_name[3] == True and alg_name[1] == 8 and alg_name[4] == 3):
		return result_lst[11]
	if (alg_name[2] == True and alg_name[3] == True and alg_name[1] == 16 and alg_name[4] == 3):
		return result_lst[12]
	if (alg_name[2] == True and alg_name[3] == False and alg_name[0] == 2):
		return result_lst[13]
	return result_lst[14]

def alg_str(alg_name):
	return alg_info(alg_name,
	['Most-Freq',
	'Sim-Bandit',
	'Class-1',
	'Bandit-Only',
	'Sup-Only',
	'MinimaxBandits, split validation',
	'AwesomeBandits with $|\Lambda|$=4, split validation',
	'AwesomeBandits with $|\Lambda|$=8, split validation',
	'AwesomeBandits with $|\Lambda|$=16, split validation',
	'MinimaxBandits, no-split validation',
	'AwesomeBandits with $|\Lambda|$=4, no-split validation',
	'AwesomeBandits with $|\Lambda|$=8, no-split validation',
	'AwesomeBandits with $|\Lambda|$=16, no-split validation',
	'Sim-Bandit-Freeze',
	'unknown'])

def alg_str_compatible(alg_name):
	return alg_info(alg_name,
	['Most-Freq',
	'Sim-Bandit',
	'Class-1',
	'Bandit-Only',
	'Sup-Only',
	'Choices_lambda=2, validation_method=2',
	'Choices_lambda=4, validation_method=2',
	'Choices_lambda=8, validation_method=2',
	'Choices_lambda=16, validation_method=2',
	'Choices_lambda=2, validation_method=3',
	'Choices_lambda=4, validation_method=3',
	'Choices_lambda=8, validation_method=3',
	'Choices_lambda=16, validation_method=3',
	'Sim-Bandit-Freeze',
	'unknown'])

def alg_color_style(alg_name):
	palette = sns.color_palette('colorblind')
	colors = palette.as_hex()
	#colors = [colors[5], colors[4], 'black', colors[2], colors[1], colors[3], 'black', colors[0], 'black', 'black']
	colors = [
	colors[5],
	colors[3],
	'black',
	colors[0],
	colors[1],
	colors[2],
	colors[2],
	colors[2],
	colors[2],
	colors[4],
	colors[4],
	colors[4],
	colors[4],
	'black',
	'black' ]

	styles = [
	'solid',
	'solid',
	'solid',
	'solid',
	'dashed',
	'dotted',
	'dashdot',
	'solid',
	'dashed',
	'dotted',
	'dashdot',
	'solid',
	'dashed',
	'solid',
	'solid']

	return alg_info(alg_name, zip(colors, styles))
	#['black', 'magenta', 'lime', 'green', 'blue', 'darkorange','darksalmon', 'red', 'cyan']

def alg_index(alg_name):
	return alg_info(alg_name,
	[7.0,
	6.0,
	8.0,
	5.0,
	4.0,
	2.0,
	1.0,
	1.2,
	1.5,
	3.0,
	2.0,
	2.2,
	2.5,
	8.5,
	9.0])


def order_legends(indices):
	ax = plt.gca()
	handles, labels = ax.get_legend_handles_labels()
	# sort both labels and handles by labels
	labels, handles, indices = zip(*sorted(zip(labels, handles, indices), key=lambda t: t[2]))
	ax.legend(handles, labels)

def save_legend(mod, indices):
	ax = plt.gca()
	handles, labels = ax.get_legend_handles_labels()
	labels, handles, indices = zip(*sorted(zip(labels, handles, indices), key=lambda t: t[2]))
	#figlegend = pylab.figure(figsize=(26,1))
	#figlegend.legend(handles, labels, 'center', fontsize=26, ncol=8)
	figlegend = pylab.figure(figsize=(17,1.5))
	figlegend.legend(handles, labels, 'center', fontsize=26, ncol=3)
	figlegend.tight_layout(pad=0)
	figlegend.savefig(mod.problemdir+'legend.pdf')

def problem_str(name_problem):
	return 'eps='+str(name_problem[5]) \
			+'_sct='+str(name_problem[0]) \
			+'_scp='+str(name_problem[1]) \
			+'_bct='+str(name_problem[2]) \
			+'_bcp='+str(name_problem[3]) \
			+'_ratio='+str(name_problem[4]) \

def noise_type_str(noise_type):
	if noise_type == 1:
		return 'UAR'
	elif noise_type == 2:
		return 'CYC'
	elif noise_type == 3:
		return 'MAJ'

def problem_text(name_problem):
	s=''
	s += 'Ratio = ' + str(name_problem[2]) + ', '
	if abs(name_problem[1]) < 1e-6:
		s += 'noiseless'
	else:
		s += noise_type_str(name_problem[0]) + ', '
		s += 'p = ' + str(name_problem[1])
	return s


def plot_cdf(alg_name, errs):

	#print alg_name
	#print errs
	#print len(errs)

	col, sty = alg_color_style(alg_name)

	plt.step(np.sort(errs), np.linspace(0, 1, len(errs), endpoint=False), label=alg_str(alg_name), color=col, linestyle=sty, linewidth=2.0)

	#

	#raw_input("Press Enter to continue...")

def plot_all_cdfs(alg_results, mod):
	#plot all cdfs:
	print 'printing cdfs..'

	indices = []

	pylab.figure(figsize=(8,6))

	for alg_name, errs in alg_results.iteritems():
		indices.append(alg_index(alg_name))
		plot_cdf(alg_name, errs)

	if mod.normalize_type == 1:
		plt.xlim(0,1)
	elif mod.normalize_type == 2:
		plt.xlim(-1,1)
	elif mod.normalize_type == 3:
		plt.xlim(0, 1)

	plt.ylim(0,1)
	#params={'legend.fontsize':26,
	#'axes.labelsize': 24, 'axes.titlesize':26, 'xtick.labelsize':20,
	#'ytick.labelsize':20 }
	#plt.rcParams.update(params)
	#plt.xlabel('Normalized error',fontsize=34)
	#plt.ylabel('Cumulative frequency', fontsize=34)
	#plt.title(problem_text(mod.name_problem), fontsize=36)
	plt.xticks(fontsize=30)
	plt.yticks(fontsize=30)
	plt.tight_layout(pad=0)

	ax = plt.gca()
	order_legends(indices)
	ax.legend_.set_zorder(-1)
	plt.savefig(mod.problemdir+'cdf.pdf')
	ax.legend_.remove()
	plt.savefig(mod.problemdir+'cdf_nolegend.pdf')
	save_legend(mod, indices)
	plt.clf()

def plot_all_lrs(lrs, mod):
	alg_names = lrs.keys()

	for i in range(len(alg_names)):
		pylab.figure(figsize=(8,6))
		lrs_alg = lrs[alg_names[i]]
		names = mod.learning_rates
		values = [lrs_alg.count(n) for n in names]
		plt.barh(range(len(names)),values)
		plt.yticks(range(len(names)),names)
		plt.savefig(mod.problemdir+alg_str_compatible(alg_names[i])+'_lr.pdf')
		plt.clf()


def plot_all_pair_comp(alg_results, sizes, mod):
	alg_names = alg_results.keys()

	for i in range(len(alg_names)):
		for j in range(len(alg_names)):
			if i < j:
				errs_1 = alg_results[alg_names[i]]
				errs_2 = alg_results[alg_names[j]]

				print len(errs_1), len(errs_2), len(sizes)
				#raw_input('Press any key to continue..')

				num_wins_1, num_wins_2 = plot_comparison(errs_1, errs_2, sizes)

				plt.title( 'total number of comparisons = ' + str(len(errs_1)) + '\n'+
				alg_str(alg_names[i]) + ' wins ' + str(num_wins_1) + ' times, \n' + alg_str(alg_names[j]) + ' wins ' + str(num_wins_2) + ' times')
				plt.savefig(mod.problemdir+alg_str_compatible(alg_names[i])+'_vs_'+alg_str_compatible(alg_names[j])+'.pdf')
				plt.clf()

#def init_results(result_table):
#	alg_results = {}
#	for idx, row in result_table.iterrows():
#		alg_name = (row['warm_start_type'], row['choices_lambda'], row['no_warm_start_update'], row['no_interaction_update'])
#		alg_results[alg_name] = []
#	alg_results[(0, 0, False, False)] = []
#	return alg_results

def normalize_score(unnormalized_result, mod):
	if mod.normalize_type == 1:
		l = get_best_error(mod.best_error_table, mod.name_dataset)
		u = max(unnormalized_result.values())
		return { k : ((v - l) / (u - l + 1e-4)) for k, v in unnormalized_result.iteritems() }
	elif mod.normalize_type == 2:
		l = unnormalized_result[(1, 1, True, False)]
		return { k : ((v - l) / (l + 1e-4)) for k, v in unnormalized_result.iteritems() }
	elif mod.normalize_type == 3:
		return unnormalized_result

def get_best_error(best_error_table, name_dataset):
	name = name_dataset[0]
	#print name
	#print best_error_table
	best_error_oneline = best_error_table[best_error_table['dataset'] == name]
	best_error = best_error_oneline.loc[best_error_oneline.index[0], 'avg_error']
	#raw_input("...")
	#print best_error_oneline
	#raw_input("...")
	#print best_error
	#raw_input("...")
	return best_error

def get_maj_error(maj_error_table, name_dataset):
	name = name_dataset[0]
	maj_error_oneline = maj_error_table[maj_error_table['data'] == name]
	maj_error = maj_error_oneline.loc[maj_error_oneline.index[0], 'avg_error']
	return maj_error

#normalized_results[alg_name].append(normalized_errs[i])
#errs = []
#for idx, row in result_table.iterrows():
#	errs.append(row['avg_error'])

def get_unnormalized_results(result_table):
	new_unnormalized_results = {}
	new_lr = {}
	new_size = 0

	i = 0
	for idx, row in result_table.iterrows():
		if i == 0:
			new_size = row['interaction']

		if row['interaction'] == new_size:
			alg_name = (row['warm_start_type'],
			 			row['choices_lambda'],
			 			row['warm_start_update'],
			 			row['interaction_update'],
			 			row['validation_method'])
			new_unnormalized_results[alg_name] = row['avg_error']
			new_lr[alg_name] = row['learning_rate']
		i += 1

	return new_size, new_unnormalized_results, new_lr

def update_result_dict(results_dict, new_result):
	#print results_dict
	for k, v in new_result.iteritems():
		#print k
		results_dict[k].append(v)


def plot_all(mod, all_results):

	#all_results = all_results[all_results['corrupt_prob_supervised']!=0.0]
	'''
	grouped_by_problem = all_results.groupby(['corrupt_type_warm_start',
											  'corrupt_prob_warm_start',
											  'corrupt_type_interaction',
											  'corrupt_prob_interaction',
											  'inter_ws_size_ratio',
											  'epsilon'])
	'''
	grouped_by_problem = all_results.groupby(['corrupt_type_warm_start',
											  'corrupt_prob_warm_start',
											  'corrupt_type_interaction',
											  'corrupt_prob_interaction',
											  'inter_ws_size_ratio',
											  'epsilon'])


	#then group by dataset and warm_start size (corresponding to each point in cdf)
	for name_problem, group_problem in grouped_by_problem:
		normalized_results = None
		unnormalized_results = None
		sizes = None
		mod.name_problem = name_problem

		grouped_by_dataset = group_problem.groupby(['dataset',
													'warm_start'])
		#then select unique combinations of (no_supervised, no_bandit, choices_lambda)
		#e.g. (True, True, 1), (True, False, 1), (False, True, 1), (False, False, 2)
		#(False, False, 8), and compute a normalized score

		for name_dataset, group_dataset in grouped_by_dataset:
			result_table = group_dataset

		 	group_dataset = group_dataset.reset_index(drop=True)

			grouped_by_algorithm = group_dataset.groupby(['warm_start_type',
			                                              'choices_lambda',
														  'warm_start_update',
														  'interaction_update',
														  'validation_method'])

			mod.name_dataset = name_dataset

			#The 'learning_rate' would be the only free degree here now. Taking the
			#min aggregation will give us the algorithms we are evaluating.

			#In the future this should be changed if we run multiple folds: we
			#should average among folds before choosing the min
			#result_table = grouped_by_algorithm.min()
			#result_table = result_table.reset_index()

			#print 'grouped by alg = '
			#print grouped_by_algorithm
			#grouped_by_algorithm.describe()

			idx = []

			#print name_problem
			#print name_dataset

			for name_alg, group_alg in grouped_by_algorithm:
				min_error = group_alg['avg_error'].min()
				min_error_rows = group_alg[group_alg['avg_error'] == min_error]
				num_min_error_rows = min_error_rows.shape[0]
				local_idx = random.randint(0, num_min_error_rows-1)
				global_idx = min_error_rows.index[local_idx]
				#group_alg.ix[global_idx, 'learning_rate'] >= 99.0 and
				#if (alg_str(name_alg) == 'Bandit-Only' or alg_str(name_alg) == 'Sup-Only'):
					#print name_dataset
					#group_alg_sorted = group_alg.sort_values(by=['learning_rate'])
					#print alg_str(name_alg), group_alg.ix[global_idx, 'avg_error']
					#print group_alg_sorted.ix[:, ['learning_rate', 'avg_error']]
					#raw_input('..')
				idx.append(global_idx)

			#print ''

			result_table = group_dataset.ix[idx, :]

			#	print grouped_by_algorithm.get_group(key), "\n\n"
			#idx = grouped_by_algorithm.apply(lambda df:df["avg_error"].idxmin())
			#print 'idx = '
			#print idx
			#result_table = group_dataset.ix[idx, :]

			#print result_table
			#print group_dataset
			#raw_input('..')

			#group_dataset.groupby(['choices_lambda','no_supervised',														'no_bandit'])
				#print alg_results
				#dummy = input('')

			#in general (including the first time) - record the error rates of all algorithms
			#print result_table

			new_size, new_unnormalized_result, new_lr = get_unnormalized_results(result_table)
			if len(new_lr) != 4:
			 	continue

			new_unnormalized_result[(0, 0, False, False, 1)] = get_maj_error(mod.maj_error_table, mod.name_dataset)
			new_lr[(0, 0, False, False, 1)] = 0.0
			new_normalized_result = normalize_score(new_unnormalized_result, mod)

			#first time - generate names of algorithms considered
			if normalized_results is None:
				sizes = []
				unnormalized_results = dict([(k,[]) for k in new_unnormalized_result.keys()])
				normalized_results = dict([(k,[]) for k in new_unnormalized_result.keys()])
				lrs = dict([(k,[]) for k in new_unnormalized_result.keys()])

			update_result_dict(unnormalized_results, new_unnormalized_result)
			update_result_dict(normalized_results, new_normalized_result)
			update_result_dict(lrs, new_lr)
			sizes.append(new_size)

			#print 'sizes:'
			#print len(sizes)
			#for k, v in unnormalized_results.iteritems():
			#	print len(v)

		mod.problemdir = mod.fulldir+problem_str(mod.name_problem)+'/'
		if not os.path.exists(mod.problemdir):
			os.makedirs(mod.problemdir)

		#print 'best_errors', mod.best_error_table
		#print 'unnormalized_results', unnormalized_results
		#print 'normalized_results', normalized_results

		if mod.pair_comp_on is True:
			plot_all_pair_comp(unnormalized_results, sizes, mod)
		if mod.cdf_on is True:
			plot_all_cdfs(normalized_results, mod)

		plot_all_lrs(lrs, mod)

def save_to_hdf(mod):
	print 'saving to hdf..'
	store = pd.HDFStore(mod.results_dir+'cache.h5')
	store['result_table'] = mod.all_results
	store.close()

def load_from_hdf(mod):
	print 'reading from hdf..'
	store = pd.HDFStore(mod.results_dir+'cache.h5')
	mod.all_results = store['result_table']
	store.close()

def load_from_sum(mod):
	print 'reading directory..'
	dss = sum_files(mod.results_dir)
	print len(dss)

	#print dss[168]

	all_results = None

	print 'reading sum tables..'
	for i in range(len(dss)):
		print 'result file name: ', dss[i]
		result = parse_sum_file(mod.results_dir + dss[i])

		if (i == 0):
			all_results = result
		else:
			all_results = all_results.append(result)

	print all_results
	mod.all_results = all_results

# This is a hack - need to do this systematically in the future
#def load_maj_error(mod):
#	return parse_sum_file(mod.maj_error_dir)

def filter_results(modm, all_results):
	if mod.filter == '1':
		pass
	elif mod.filter == '2':
		#print all_results['warm_start_size'] >= 100
		#raw_input(' ')
		all_results = all_results[all_results['warm_start'] >= 200]
	elif mod.filter == '3':
		all_results = all_results[all_results['num_classes'] >= 3]
	elif mod.filter == '4':
		all_results = all_results[all_results['num_classes'] <= 2]
	elif mod.filter == '5':
		all_results = all_results[all_results['total_size'] >= 10000]
		all_results = all_results[all_results['num_classes'] >= 3]
	elif mod.filter == '6':
		all_results = all_results[all_results['warm_start'] >= 100]
		all_results = all_results[all_results['learning_rate'] == 0.3]
	elif mod.filter == '7':
		all_results = all_results[all_results['warm_start'] >= 100]
		all_results = all_results[all_results['num_classes'] >= 3]

	return all_results


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='result summary')
	parser.add_argument('--results_dir', default='../../../figs/')
	parser.add_argument('--filter', default='1')
	parser.add_argument('--plot_subdir', default='expt1/')
	parser.add_argument('--cached', action='store_true')
	parser.add_argument('--normalize_type', type=int, default=1)
	#parser.add_argument('--epsilon', type=float, default=0.05)

	args = parser.parse_args()

	mod = model()

	mod.results_dir = args.results_dir
	mod.filter = args.filter
	mod.plot_subdir = args.plot_subdir
	mod.normalize_type = args.normalize_type #1: normalized score; 2: bandit only centered score; 3: raw score
	mod.pair_comp_on = False
	mod.cdf_on = True
	mod.maj_error_dir = '../../../figs_all/expt_0509/figs_maj_errors/0of1.sum'
	mod.best_error_dir = '../../../figs_all/expt_0606/0of1.sum'

	mod.fulldir = mod.results_dir + mod.plot_subdir
	if not os.path.exists(mod.fulldir):
		os.makedirs(mod.fulldir)

	#print args.from_hdf
	#raw_input(' ')
	if args.cached is True:
		if os.path.exists(mod.results_dir+'cache.h5'):
			load_from_hdf(mod)
		else:
			load_from_sum(mod)
			save_to_hdf(mod)
	else:
		load_from_sum(mod)


	#first group by corruption mode, then corruption prob
	#then group by warm start - bandit ratio
	#these constitutes all the problem settings we are looking at (corresponding
	#to each cdf graph)
	all_results = mod.all_results

	#print mod.best_error_table[mod.best_error_table['dataset'] == 'ds_160_5.vw.gz']
	#raw_input(' ')

	#print all_results
	#raw_input('..')
	#all_results = all_results[all_results['epsilon'] == args.epsilon]

	all_results = all_results[all_results['choices_lambda'] != 0]

	#ignore the no update row:
	all_results = all_results[(all_results['warm_start_update'] == True) | (all_results['interaction_update'] == True)]
	#ignore the choice_lambda = 4 row
	all_results = all_results[(all_results['choices_lambda'] != 4)]


	all_results = all_results[all_results['learning_rate'] < 1.5]
	#all_results = all_results[(all_results['corrupt_prob_interaction'] >= 0.49) & (all_results['inter_ws_size_ratio'] == 184.0) ]
	# &	( (all_results['dataset'] == 'ds_1110_23.vw.gz') |
	#	  (all_results['dataset'] == 'ds_1113_23.vw.gz') |
	#	  (all_results['dataset'] == 'ds_1238_2.vw.gz') |
	#	  (all_results['dataset'] == 'ds_1483_11.vw.gz') |
	#	  (all_results['dataset'] == 'ds_354_2.vw.gz'))

	#filter choices_lambdas = 2,4,8?
	#if (alg_name[2] == False and alg_name[3] == False and alg_name[1] != 8):
	#	pass
	#else:

	mod.maj_error_table = parse_sum_file(mod.maj_error_dir)
	mod.maj_error_table = mod.maj_error_table[mod.maj_error_table['majority_approx']]
	mod.best_error_table = parse_sum_file(mod.best_error_dir)
	mod.best_error_table = mod.best_error_table[mod.best_error_table['optimal_approx']]
	mod.learning_rates = sorted(all_results.learning_rate.unique())

	all_results = filter_results(mod, all_results)

	plot_all(mod, all_results)

	#if i >= 331 and i <= 340:
	#	print 'result:', result
	#	print 'all_results:', all_results
