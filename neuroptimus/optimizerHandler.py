from fitnessFunctions import fF,frange
from optionHandler import optionHandler
import sys
import logging
import numpy as np
import copy
import random
import json
import time
import os
from math import sqrt

from multiprocessing import Pool

from itertools import combinations, product

from types import MethodType
try:
    import copyreg
except:
    import copyreg

import functools
try:
    import cPickle as pickle
except ImportError:
    import pickle
				

def _pickle_method(method):
	func_name = method.__func__.__name__
	obj = method.__self__
	cls = method.__self__.__class__
	return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
	for cls in cls.mro():
		try:
			func = cls.__dict__[func_name]
		except KeyError:
			pass
		else:
			break
	return func.__get__(obj, cls)


try:
	copyreg.pickle(MethodType, _pickle_method, _unpickle_method)
except:
	copyreg.pickle(MethodType, _pickle_method, _unpickle_method)

def callback(c,x,y):
	print(c)


def uniform(random,args):
	"""
	Creates random values from a uniform distribution. Used to create initial population.

	:param random: random number generator object
	:param args: ``dictionary``, must contain key "num_params" and either "_ec" or "self"

	:return: the created random values in a ``list``

	"""
	size=args.get("num_params")
	#bounds=args.get("self").boundaries
	candidate=[]
	for i in range(int(size)):
		candidate.append(random.uniform(0,1))
	return candidate



class bounderObject(object):  #?!
	"""
	Creates a callable to perform the bounding of the parameters.
	:param xmax: list of maxima
	:param xmin: list of minima
	"""
	def __init__(self, xmax, xmin ):
			self.lower_bound = np.array(xmax)
			self.upper_bound = np.array(xmin)
	def __call__(self, **kwargs):
		"""
		Performs the bounding by deciding if the given point is in the defined region of the parameter space.
		This is required by some algorithms as part of their acceptance tests.

		:return: `True` if the point is inside the given bounds.
		"""
		x = kwargs["x_new"]
		tmax = bool(np.all(x <= self.lower_bound))
		tmin = bool(np.all(x >= self.upper_bound))
		return tmax and tmin



class SINGLERUN():
	"""
	An abstract base class to implement a single evaluation process.
	"""
	def __init__(self, reader_obj, option_obj):
		self.fit_obj = fF(reader_obj,  option_obj)
		self.SetFFun(option_obj)
		self.directory = option_obj.base_dir
		self.num_params = option_obj.num_params
		self.boundaries = option_obj.boundaries

	def SetFFun(self,option_obj):
		"""
		Sets the combination function and converts the name of the fitness functions into function instances.
		:param option_obj: an ``optionHandler`` instance
		"""

		try:
			self.ffun=self.fit_obj.objective_fitness
		except KeyError:
			sys.exit("Unknown fitness function!")

		if option_obj.type[-1] != 'features':
			try:
				option_obj.feats=[self.fit_obj.calc_dict[x] for x in option_obj.feats]
			except KeyError:
				print("error with fitness function: ",option_obj.feats," not in: ",list(self.fit_obj.calc_dict.keys()))

class baseOptimizer():
	"""
	An abstract base class to implement the base of an optimization process.
	"""
	def __init__(self, reader_obj,  option_obj):
		self.fit_obj = fF(reader_obj,  option_obj)
		self.SetFFun(option_obj)
		self.rand = random
		self.seed = int(option_obj.seed)
		self.rand.seed(self.seed)
		self.directory = option_obj.base_dir
		self.num_params = option_obj.num_params
		self.number_of_traces = reader_obj.number_of_traces()
		self.num_obj = self.num_params*int(self.number_of_traces)
		self.boundaries = option_obj.boundaries
		self.algo_params =  copy.copy(option_obj.algorithm_parameters)
		open(self.directory+"/eval.txt", "w")
		open(self.directory+"/subfeature_scores.txt", "w")

	def SetFFun(self,option_obj):
		"""
		Sets the combination function and converts the name of the fitness functions into function instances.
		:param option_obj: an ``optionHandler`` instance
		"""

		try:
			self.ffun = self.fit_obj.objective_fitness
		except KeyError:
			sys.exit("Unknown fitness function!")
		
		if option_obj.type[-1]!= 'features':
			try:
				option_obj.feats = [self.fit_obj.calc_dict[x] for x in option_obj.feats]
			except KeyError:
				print("error with fitness function: ",option_obj.feats," not in: ",list(self.fit_obj.calc_dict.keys()))



class InspyredAlgorithmBasis(baseOptimizer):
	def __init__(self, reader_obj,  option_obj):
		baseOptimizer.__init__(self, reader_obj,  option_obj)
		import inspyred
		self.inspyred = inspyred
		self.option_obj = option_obj
		self.bounder = self.inspyred.ec.Bounder([0]*len(option_obj.boundaries[0]),[1]*len(option_obj.boundaries[1]))
		self.size_of_population = self.algo_params.pop("size_of_population")
		self.number_of_generations = self.algo_params.pop("number_of_generations")-1
		self.stat_file = open(self.directory + "/stat_file_inspyred.txt", "w+")
		self.ind_file = open(self.directory + "/ind_file_inspyred.txt", "w+")
		self.number_of_cpu = int(self.algo_params.pop("number_of_cpu",1))
		self.output_level = option_obj.output_level
		self.starting_points = None
		if self.output_level == "1":
			print("starting points: ", self.starting_points)
		self.kwargs = dict(generator=uniform,
						   evaluator=self.inspyred.ec.evaluators.parallel_evaluation_mp,
						   mp_evaluator=self.ffun,
						   mp_nprocs=int(self.number_of_cpu),
						   pop_size=self.size_of_population,
						   seeds=self.starting_points,
						   max_generations=self.number_of_generations,
						   num_params=self.num_params,
						   bounder=self.bounder,
						   statistics_file=self.stat_file,
						   individuals_file=self.ind_file)
	
	def Optimize(self):
			"""
			Performs the optimization.
			"""
			
			logger = logging.getLogger('inspyred.ec')
			logger.setLevel(logging.DEBUG)
			file_handler = logging.FileHandler(self.directory + '/inspyred.log', mode='w')
			file_handler.setLevel(logging.DEBUG)
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			file_handler.setFormatter(formatter)
			logger.addHandler(file_handler)
			self.evo_strat.terminator = self.inspyred.ec.terminators.generation_termination
			if self.output_level=="1":
				self.evo_strat.observer=[self.inspyred.ec.observers.population_observer,self.inspyred.ec.observers.file_observer]
			else:
				self.evo_strat.observer=[self.inspyred.ec.observers.file_observer]
			self.kwargs={k: v for k, v in self.kwargs.items() if v!='None' and v!=None} #maximize equals none can't use if v
			self.algo_params={k: v for k, v in self.algo_params.items() if v!='None' and v!=None} 
			solution = self.evo_strat.evolve(maximize=False,**self.kwargs, **self.algo_params)
			if hasattr(self.evo_strat, "archive"):
				self.final_archive = self.evo_strat.archive

class ScipyAlgorithmBasis(baseOptimizer):

	def __init__(self, reader_obj,  option_obj):
		baseOptimizer.__init__(self, reader_obj,  option_obj)
		from scipy import optimize, array, ndarray 
		self.scipy_optimize = optimize
		self.scipy_array = array
		self.scipy_ndarray = ndarray
		"""try:
			if isinstance(option_obj.starting_points[0], list):
				raise TypeError
			else:
				self.starting_points = [normalize(option_obj.starting_points, self)]
		except TypeError:"""
		self.starting_points = uniform(self.rand, {"num_params": self.num_params, "self": self})
		if option_obj.output_level == "1":
			print("starting points: ", self.starting_points)


class PygmoAlgorithmBasis(baseOptimizer):

	def __init__(self, reader_obj,  option_obj):
		baseOptimizer.__init__(self, reader_obj,  option_obj)
		import pygmo as pg
		self.pg = pg
		self.number_of_generations = int(self.algo_params.pop("number_of_generations"))-1
		self.size_of_population = int(self.algo_params.pop("size_of_population",100))
		self.multiprocessing=False
		self.option_obj=option_obj
		self.pg.set_global_rng_seed(seed = self.seed)
		self.boundaries = [[0]*len(option_obj.boundaries[0]),[1]*len(option_obj.boundaries[1])]
		self.base_dir = option_obj.base_dir
		self.number_of_traces=reader_obj.number_of_traces()
		self.n_obj=len(option_obj.GetFitnessParam()[-1])*int(self.number_of_traces)
		self.number_of_cpu = int(self.algo_params.pop("number_of_cpu",1))
		self.num_islands = int(self.algo_params.pop("number_of_islands",1))

	def Optimize(self):
		
		if not self.option_obj.multi_objective:
			self.n_obj=1
		fitfun=self.ffun
		self.prob = self.pg.problem(Problem(fitfun, self.boundaries, self.n_obj, self.size_of_population, self.number_of_cpu))		
		
		if self.multiprocessing:
			self.mpbfe=self.pg.mp_bfe()
			self.mpbfe.resize_pool(int(self.number_of_cpu))
			self.algorithm.set_bfe(self.pg.bfe())
			self.pgalgo=self.pg.algorithm(self.algorithm)
			self.pgalgo.set_verbosity(1)
			self.population = self.pg.population(prob=self.prob, size=self.size_of_population,b=self.mpbfe)
			"""if os.path.isfile(self.directory+"/checkpoint_pgalgo.pickle"):
				with open(self.directory+"/checkpoint_pgalgo.pickle", 'rb') as outfile:
					self.pgalgo=pickle.load(outfile)
			if os.path.isfile(self.directory+"/checkpoint_pop.pickle"):
				with open(self.directory+"/checkpoint_pop.pickle", 'rb') as outfile:
					self.population=pickle.load(outfile)"""
			self.archi = self.pgalgo.evolve(self.population)
			self.mpbfe.shutdown_pool()
			"""with open(self.directory+"/checkpoint_pop.pickle", "wb") as outfile:
				pickle.dump(self.archi, outfile)
			with open(self.directory+"/checkpoint_pgalgo.pickle", "wb") as outfile:
				pickle.dump(self.pgalgo, outfile)"""
		else:
			self.pgalgo=self.pg.algorithm(self.algorithm)
			self.pgalgo.set_verbosity(1)
			self.archi = self.pg.archipelago(n = self.num_islands,t = self.pg.fully_connected(), algo = self.pgalgo, prob = self.prob, 
						pop_size = self.size_of_population, r_pol = self.pg.fair_replace(.1), s_pol = self.pg.select_best(.1))#, b=self.mpbfe)
			"""if os.path.isfile(self.directory+"/checkpoint_pygmo.pickle"):
				with open(self.directory+"/checkpoint_pygmo.pickle", 'rb') as outfile:
					self.archi=pickle.load(outfile)"""
			self.archi.evolve()
			self.archi.wait()
			for island in self.archi:
				a = island.get_population()
				uda = a.problem.extract(Problem)
			"""with open(self.directory+"/checkpoint_pygmo.pickle", "wb") as outfile:
				pickle.dump(self.archi, outfile)"""
			
		
		
class Problem:	
	def __init__(self, fitnes_fun, bounds, n_obj, size_of_population, number_of_cpu):
		self.bounds = bounds
		self.fitnes_fun = fitnes_fun
		self.n_obj = n_obj
		self.size_of_population = size_of_population
		self.number_of_cpu = number_of_cpu

	def fitness(self, x):
		fitness = self.fitnes_fun(x)
		if self.n_obj > 1:
			fitness = fitness[0]
		return fitness

	def batch_fitness(self, x):
		n = int(len(x)/self.size_of_population)
		x_chunks=[x[i:i + n] for i in range(0, len(x), n)]
		with Pool(self.number_of_cpu) as pool:
			fitness = pool.map(self.fitnes_fun,x_chunks)
		if self.n_obj > 1:
			fitness = [f[0] for f in fitness]
		fitness = [item for sublist in fitness for item in sublist]
		return fitness

	def has_batch_fitness(self):
		return True

	def get_nobj(self):
		return self.n_obj

	def get_bounds(self):
		return(self.bounds[0], self.bounds[1])



class SinglePygmoAlgorithmBasis(baseOptimizer):

	def __init__(self, reader_obj,  option_obj):
		baseOptimizer.__init__(self, reader_obj,  option_obj)
		import pygmo as pg
		self.pg = pg
		self.pgset_global_rng_seed(seed = self.seed)
		self.prob = SingleProblem(self.ffun,option_obj.boundaries)
		self.directory = option_obj.base_dir

	def Optimize(self):
		self.population = self.pg.population(self.prob,**self.algo_params)

		self.algorithm.set_verbosity(1)
		self.evolved_pop = self.algorithm.evolve(self.population)
		
		uda = self.algorithm.extract(self.algo_type)
		self.log = uda.get_log()
		self.write_statistics_file()

		self.best = normalize(self.evolved_pop.champion_x, self) 
		self.best_fitness = self.evolved_pop.champion_f

class BluepyoptAlgorithmBasis(baseOptimizer):
	def __init__(self, reader_obj,  option_obj):
		baseOptimizer.__init__(self, reader_obj,  option_obj)
		import bluepyopt as bpop
		self.bpop = bpop
		self.option_obj = option_obj
		self.seed = option_obj.seed
		self.selector_name  =  "IBEA"
		self.size_of_population = self.algo_params.pop("size_of_population")
		self.number_of_generations = self.algo_params.pop("number_of_generations")
		self.number_of_cpu = int(self.algo_params.pop("number_of_cpu",1))
		self.continue_cp = self.algo_params.pop("continue_cp")
		self.option_obj.multi_objective=True
		self.param_names = self.option_obj.GetObjTOOpt()
		self.number_of_traces = reader_obj.number_of_traces()
		feats = list(zip(self.option_obj.feat_str.split(', '),self.option_obj.weights))
		self.params = [self.bpop.parameters.Parameter(p_name, bounds=(0,1)) for p_name in self.param_names]
		self.param_names = [param.name for param in self.params]
		self.objectives = [self.bpop.objectives.Objective(name=name, value=value) for name,value in feats*self.number_of_traces]


			

	def Optimize(self):
		if self.number_of_cpu > 1:
			from ipyparallel import Client
			from ipyparallel.controller.heartmonitor import HeartMonitor
			print("******************PARALLEL RUN : " + self.selector_name + " *******************")
			#os.system("ipcluster start -n "+str(int(self.number_of_cpu))+"  &")
			c = Client(timeout = 1000, profile=os.getenv('IPYTHON_PROFILE'))
			HeartMonitor.period = 60000
			view = c.load_balanced_view()
			view.map_sync(os.chdir, [str(os.path.dirname(os.path.realpath(__file__)))]*int(self.number_of_cpu))
			map_function = view.map_sync
			print('Using ipyparallel with '+str(len(c))+' engines')
			optimisation = self.bpop.optimisations.DEAPOptimisation(evaluator = self.Evaluator(self.objectives,self.params,self.ffun),map_function=map_function,selector_name=self.selector_name,offspring_size=self.size_of_population,seed=self.seed,**self.algo_params)
			self.solution, self.hall_of_fame, self.logs, self.hist = optimisation.run(int(self.number_of_generations),cp_filename=(self.directory+"/checkpoint.pkl"))
			#os.system("ipcluster stop")
		else:
			print("*****************Single Run : " + self.selector_name + " *******************")
			optimisation = self.bpop.optimisations.DEAPOptimisation(evaluator = self.Evaluator(self.objectives,self.params,self.ffun),selector_name=self.selector_name,offspring_size=self.size_of_population,seed=self.seed,**self.algo_params)
			self.solution, self.hall_of_fame, self.logs, self.hist = optimisation.run(int(self.number_of_generations),cp_filename=(self.directory+"/checkpoint.pkl"),continue_cp=self.continue_cp)


	class Evaluator():
		def __init__(self,objectives,params,fun):
			self.fun = fun
			self.objectives = objectives
			self.params = params
			
		def evaluate_with_lists(self, param_list):
			err = self.fun(param_list)
			return err[0]
		
		def set_neuron_variables_and_evaluate_with_lists(self, param_list=None, target='scores'):
			return self.evaluate_with_lists(param_list=param_list)


		def evaluate(self, param_list=None, target='scores'):
			return self.evaluate_with_lists(param_list, target=target)


class SingleProblem:
	def __init__(self, fitnes_fun, bounds):
		self.bounds = bounds
		self.boundaries = bounds
		self.fitnes_fun = fitnes_fun

	def __getstate__(self):
		bounds = self.bounds
		boundaries = self.boundaries
		f_f = self.fitnes_fun
		return (bounds, boundaries, f_f)

	def __setstate__(self, state):
		self.bounds, self.boundaries, self.fitnes_fun = state


	def fitness(self, x):
		return self.fitnes_fun([normalize(x,self)])

	def get_bounds(self):
		return(self.bounds[0], self.bounds[1])

class RANDOM_SEARCH(baseOptimizer):
	"""
	Basic implementation of random search optimization
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	"""
	def __init__(self, reader_obj,  option_obj):
		baseOptimizer.__init__(self, reader_obj,  option_obj)
		self.number_of_cpu = int(self.algo_params.pop("number_of_cpu",1))
		self.size_of_population = self.algo_params.pop("size_of_population")
			
	def Optimize(self):
		"""
		Performs the optimization.
		"""
		with Pool(processes=int(self.number_of_cpu),maxtasksperchild=1) as pool:
			candidate=[]
			fitness=[]
			for j in range(int(self.size_of_population)):
				candidate.append(uniform(self.rand, {"self":self,"num_params":self.num_params}))
			try:
				fitness=pool.map(self.ffun,candidate)
			except (OSError, RuntimeError) as e:
				raise
		

class ABC_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.algorithm = self.pg.bee_colony(gen = self.number_of_generations, **self.algo_params)

class BH_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.algorithm = self.pg.mbh(self.pg.algorithm(self.pg.scipy_optimize(method="L-BFGS-B", options=self.algo_params)),stop=2)
			
class DE_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.variant = int(self.algo_params.pop("variant"))
		self.algorithm = self.pg.de(gen = self.number_of_generations, variant=self.variant, **self.algo_params)

class DE1220_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		if int(self.size_of_population)<7:
			print("*****************************************************")
			print("DE1220 NEEDS A POPULATION WITH AT LEAST 7 INDIVIDUALS")
			print("*****************************************************")
			self.size_of_population = 7
			
		self.algorithm = self.pg.de1220(gen = self.number_of_generations, **self.algo_params)

class CMAES_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		if int(self.size_of_population) < 5:
			print("***************************************************")
			print("CMA-ES NEEDS A POPULATION WITH AT LEAST 5 INDIVIDUALS")
			print("***************************************************")
			self.size_of_population = 5
		self.algorithm = self.pg.cmaes(gen = self.number_of_generations, **self.algo_params)

class GACO_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.multiprocessing=True
		self.n_gen_mark = int(self.algo_params.pop("n_gen_mark"))
		self.algorithm = self.pg.gaco(gen = self.number_of_generations, n_gen_mark=self.n_gen_mark, **self.algo_params)


class MACO_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.option_obj.multi_objective=True
		self.multiprocessing=True
		self.algorithm = self.pg.maco(gen = self.number_of_generations, **self.algo_params)

class NM_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.algorithm = self.pg.scipy_optimize(method="Nelder-Mead", options=self.algo_params)

class NSGA2_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.option_obj.multi_objective=True
		self.multiprocessing=True
		self.algorithm = self.pg.nsga2(gen = self.number_of_generations, **self.algo_params)

class NSPSO_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.option_obj.multi_objective=True
		self.multiprocessing=True
		self.algorithm = self.pg.nspso(gen = self.number_of_generations, **self.algo_params)

class PRAXIS_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.algorithm = self.pg.nlopt(solver="praxis", **self.algo_params)
		self.algorithm.maxeval=self.number_of_generations

class SDE_PYGMO(SinglePygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		SinglePygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.algo_type = self.pg.de        
		self.algorithm = self.pg.de(gen = self.number_of_generations, **self.algo_params)

class SGA_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		
		self.algorithm = self.pg.sga(gen = self.number_of_generations, **self.algo_params)

class PSO_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.variant = int(self.algo_params.pop("variant"))
		self.algorithm = self.pg.pso(gen = self.number_of_generations, variant = self.variant, **self.algo_params)

class PSOG_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.multiprocessing=True
		self.variant = int(self.algo_params.pop("variant"))
		self.algorithm = self.pg.pso_gen(gen = self.number_of_generations, variant = self.variant, **self.algo_params)

class SADE_PYGMO(PygmoAlgorithmBasis):

	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		if int(self.size_of_population)<7:
			print("***************************************************")
			print("SADE NEEDS A POPULATION WITH AT LEAST 7 INDIVIDUALS")
			print("***************************************************")
			self.size_of_population = 7
		self.variant = int(self.algo_params.pop("variant"))
		self.algorithm = self.pg.sade(gen = self.number_of_generations, variant = self.variant, **self.algo_params)

class XNES_PYGMO(PygmoAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		PygmoAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.algorithm = self.pg.xnes(gen = self.number_of_generations, **self.algo_params)

class FULLGRID_PYGMO(InspyredAlgorithmBasis):
	
	def __init__(self, reader_obj,  option_obj):
		InspyredAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.evo_strat=ec.ES(self.rand)

		if option_obj.output_level=="1":
			self.evo_strat.observer=[observers.population_observer,observers.file_observer]
		else:
			self.evo_strat.observer=[observers.file_observer]
		

		self.resolution = [5,5,5]
		#self.resolution = list(map(lambda x: x if x>=3 else 3, self.resolution))
		
		if(len(self.resolution) < self.kwargs['num_params']):
			print("Not enough values for every parameter. Will expand resolution with threes.")
			self.resolution = self.resolution + [1] * (self.kwargs['num_params'] - len(self.resolution))
			print("New resolution is: ", self.resolution)
			

		elif(len(self.resolution) > self.kwargs['num_params']):
			print("Too many values. Excess resolution will be ignored.")
			self.resolution = self.resolution[0:self.kwargs['num_params']]
			print("New resolution is: ", self.resolution)
			
		
		
		self.grid = [] 
		self.alldims = []
	#self.point = option_obj.point
		#HH
		self.point = [0.12,0.036,0.0003]
		if(not self.point):
			print("No point given. Will take center of grid")
			self.point = list(map(lambda x: int(x/2), self.resolution))
			print("New point is: ", self.point)
			
		#CLAMP
		#self.point = [0.01, 2, 0.3, 3] 
		#align grid on point
		
		for j in range(len(option_obj.boundaries[0])):
			if(self.resolution[j] == 1):
				self.alldims.append([self.point[j]])
				continue
			
			#ugly way to ensure same resolution before and after point included
			upper_bound = option_obj.boundaries[1][j] - float((float(option_obj.boundaries[1][j]))/float(self.resolution[j]-1)/2)
			
			div = float((upper_bound)/(self.resolution[j]-1))
			lower_bound = (self.point[j]/div % 1) * div
			
			upper_bound = upper_bound + lower_bound
			
			self.alldims.append(list(np.linspace(lower_bound,upper_bound,self.resolution[j])))
			
			
		
		for i,t in enumerate(combinations(self.alldims, r=self.num_params-1)):
			plane_dimensions = list(t) 
			optimum_point = [self.point[self.num_params-1-i]]
			plane_dimensions.insert(self.num_params-1-i, optimum_point) 
			print("PLANE", plane_dimensions)

			for t in product(*plane_dimensions):
				print(list(t))
				#exit()
				if(len(self.point)-1-i)==0:
					print(list(t))
					#exit()
				print(list(t))
				self.grid.append(normalize(list(t),self))

				
			if(len(self.point)-1-i)==0:
				print(len(plane_dimensions[0]))



		self.kwargs["seeds"] = self.grid
		self.kwargs["max_generations"] = 0
		self.kwargs["pop_size"] = 1

class BH_SCIPY(ScipyAlgorithmBasis):
	"""
	Implements the ``Basinhopping`` algorithm for minimization from the ``scipy`` package.

	:param reader_obj: an instance of ``DATA`` object
	
	:param option_obj: an instance of ``optionHandler`` object

	.. seealso::

		Documentation of the Simulated Annealing from 'scipy':
			http://docs.scipy.org/doc/scipy-dev/reference/generated/scipy.optimize.basinhopping.html

	"""
	def __init__(self, reader_obj,  option_obj):
		ScipyAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.maxcor = self.algo_params.pop("maxcor")
		self.eps = self.algo_params.pop("eps")
		self.number_of_generations = self.algo_params.pop("number_of_generations")
		self.size_of_population = self.algo_params.pop("size_of_population")


	def Optimize(self):
		"""
		Performs the optimization.
		"""
		self.scipy_optimize.basinhopping(self.ffun,
						x0 = self.scipy_ndarray((self.num_params,),buffer=self.scipy_array(self.starting_points),offset=0,dtype=float),
						niter = self.size_of_population-1, #niter
						niter_success=None,
						minimizer_kwargs={"method":"L-BFGS-B",
										"jac":False,
										"args":[[]],
										"tol":0,
										"bounds": [(0,1)]*len(self.boundaries[0]),
										"options": {'maxfun': self.number_of_generations,"gtol":0,"ftol":0, #maxfun
													'iprint': 2}},
						)

class NM_SCIPY(ScipyAlgorithmBasis):
	"""
	Implements a Nelder-Mead downhill simplex algorithm for minimization from the ``scipy`` package.
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	.. seealso::
		Documentation of the fmin from 'scipy':
			http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fmin.html#scipy.optimize.fmin

	"""
	def __init__(self, reader_obj,  option_obj):
		ScipyAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.number_of_generations = self.algo_params.pop("number_of_generations")
		self.size_of_population = self.algo_params.pop("size_of_population")
		self.number_of_cpu = self.algo_params.pop("number_of_cpu")


	def Optimize(self):
		"""
		Performs the optimization.
		"""
		with Pool(self.number_of_cpu) as pool:
		 	print("*************************number of cpu used: "+str(pool._processes))
		 	self.res=pool.starmap(self.scipy_optimize.minimize,[(self.ffun,self.scipy_ndarray((self.num_params,),
						buffer = self.scipy_array(uniform(self.rand,{"num_params" : self.num_params,"self": self})),offset = 0,dtype = float),
									  ((),),
									  "Nelder-Mead",
									  None,None,None,
									  [(0,1)]*len(self.boundaries[0]),
									  None,
									  0,
									  None,
									  {"maxiter":self.number_of_generations,"maxfev":self.number_of_generations,"xatol":0,"fatol":0,
										  "return_all":True, **self.algo_params,
										  "xatol":0,
										  "fatol":0,}) for i in range(self.size_of_population)])

		

class LBFGSB_SCIPY(ScipyAlgorithmBasis):
	"""
	Implements L-BFGS-B algorithm for minimization from the ``scipy`` package.
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	.. seealso::
		Documentation of the L-BFGS-B from 'scipy':
			http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fmin_l_bfgs_b.html#scipy.optimize.fmin_l_bfgs_b

	"""
	def __init__(self, reader_obj,  option_obj):
		ScipyAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.number_of_generations = self.algo_params.pop("number_of_generations")
		self.size_of_population = self.algo_params.pop("size_of_population")
		self.number_of_cpu = self.algo_params.pop("number_of_cpu")




	def Optimize(self):
		"""
		Performs the optimization.
		"""
		with Pool(self.number_of_cpu) as pool:
		 	self.res=pool.starmap(self.scipy_optimize.minimize,[(self.ffun,self.scipy_ndarray((self.num_params,),
						buffer = self.scipy_array(uniform(self.rand,{"num_params" : self.num_params,"self": self})),offset = 0,dtype = float),
									  ((),),
									  "L-BFGS-B",
									  False,None,None,
									  [(0,1)]*len(self.boundaries[0]),
									  None,
									  0,
									  None,
									  {"maxfun":self.number_of_generations,"gtol":0,"ftol":0, **self.algo_params,})
									   for x in range(self.size_of_population)])
		
		



class grid(baseOptimizer):
	"""
	Implements a brute force algorithm for minimization by calculating the function's value
	over the specified grid.
	.. note::
		This algorithm is highly inefficient and should not be used for complete optimization.
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	:param resolution: number of sample points along each dimensions (default: 10)

	"""
	def __init__(self,reader_obj,option_obj,resolution):
		self.fit_obj=fF(reader_obj,option_obj)
		self.SetFFun(option_obj)
		self.num_params=option_obj.num_params
		self.num_points_per_dim=resolution
		self.boundaries=option_obj.boundaries

	def Optimize(self,optimals):
		"""
		Performs the optimization.
		"""
		_o=copy.copy(optimals)
		_o=normalize(_o, self)
		points=[]
		fitness=[]
		tmp1=[]
		tmp2=[]
		for n in range(self.num_params):
			for c in frange(0,1, float(1)/self.num_points_per_dim):
				_o[n]=c
				tmp1.append(self.fit_obj.ReNormalize(_o))
				tmp2.append(self.ffun([_o],{}))
			points.append(tmp1)
			tmp1=[]
			fitness.append(tmp2)
			tmp2=[]
			_o=copy.copy(optimals)
			_o=normalize(_o, self)
		
class CES_INSPYRED(InspyredAlgorithmBasis):
	"""
	Implements a custom version of ``Evolution Strategy`` algorithm for minimization from the ``inspyred`` package.
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	.. note::
		The changed parameters compared to the defaults are the following:
			* replacer: genrational_replacement
			* variator: gaussian_mutation, blend_crossover
	.. seealso::
		Documentation of the options from 'inspyred':
			http://inspyred.github.io/reference.html#module-inspyred.ec
	"""
	def __init__(self, reader_obj,  option_obj):
		InspyredAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		if int(self.size_of_population) % 2 != 0:
			self.size_of_population = self.size_of_population + 1
			self.kwargs["pop_size"] = self.size_of_population
			print("***************************************************")
			print("CES NEEDS EVEN NUMBER OF INDIVIDUALS")
			print("POPULATION SIZE HAVE BEEN MODIFIED TO "+str(self.size_of_population))
			print("***************************************************")
		
		self.evo_strat=self.inspyred.ec.ES(self.rand)

class CEO_INSPYRED(InspyredAlgorithmBasis):
	"""
	Implements a custom version of ``Evolution Strategy`` algorithm for minimization from the ``inspyred`` package.
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	.. note::
		The changed parameters compared to the defaults are the following:
			* replacer: genrational_replacement
			* variator: gaussian_mutation, blend_crossover
	.. seealso::
		Documentation of the options from 'inspyred':
			http://inspyred.github.io/reference.html#module-inspyred.ec
	"""
	def __init__(self, reader_obj,  option_obj):
		InspyredAlgorithmBasis.__init__(self, reader_obj,  option_obj)
	
		self.evo_strat=self.inspyred.ec.EvolutionaryComputation(self.rand)
		self.evo_strat.replacer=self.inspyred.ec.replacers.generational_replacement
		self.kwargs["mutation_rate"] = 0.25
		self.kwargs["num_elites"] = int(self.size_of_population/2)
		self.kwargs["gaussian_stdev"] = 0.5
		self.evo_strat.selector=self.inspyred.ec.selectors.default_selection
		self.evo_strat.variator=[self.inspyred.ec.variators.gaussian_mutation, self.inspyred.ec.variators.blend_crossover]
			
		

class DE_INSPYRED(InspyredAlgorithmBasis):
	"""
	Implements the ``Differential Evolution Algorithm`` algorithm for minimization from the ``inspyred`` package.
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	.. seealso::
		Documentation of the options from 'inspyred':
			http://inspyred.github.io/reference.html#module-inspyred.ec
	"""
	def __init__(self, reader_obj,  option_obj):
		InspyredAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.kwargs["num_elites"] = int(self.size_of_population/2)
		self.kwargs["num_selected"] = int(self.size_of_population)
		self.evo_strat=self.inspyred.ec.DEA(self.rand)

class EDA_INSPYRED(InspyredAlgorithmBasis):
	"""
	Implements the ``Estimation of Distribution Algorithm`` algorithm for minimization from the ``inspyred`` package.
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	.. seealso::
		Documentation of the options from 'inspyred':
			http://inspyred.github.io/reference.html#module-inspyred.ec
	"""
	def __init__(self, reader_obj,  option_obj):
		InspyredAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.evo_strat=self.inspyred.ec.EDA(self.rand)

class PSO_INSPYRED(InspyredAlgorithmBasis):
	"""
	Implements the ``Particle Swarm`` algorithm for minimization from the ``inspyred`` package.
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	.. seealso::
		Documentation of the Particle Swarm from 'inspyred':
			http://pythonhosted.org/inspyred/reference.html
	"""
	def __init__(self, reader_obj,  option_obj):
		InspyredAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.kwargs["topology"] = self.inspyred.swarm.topologies.star_topology
		self.evo_strat=self.inspyred.swarm.PSO(self.rand)


class NSGA2_INSPYRED(InspyredAlgorithmBasis):
	"""
	Implements the ``Non-Dominated Genetic Algorithm`` algorithm for minimization from the ``inspyred`` package.
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	.. note::
		The changed parameters compared to the defaults are the following:
			* replacer: genrational_replacement
			* variator: gaussian_mutation, blend_crossover
	.. seealso::
		Documentation of the options from 'inspyred':
			http://inspyred.github.io/reference.html#module-inspyred.ec
	"""
	def __init__(self, reader_obj,  option_obj):
		InspyredAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.option_obj.multi_objective=True
		self.evo_strat=self.inspyred.ec.emo.NSGA2(self.rand)
		self.evo_strat.variator=[self.inspyred.ec.variators.gaussian_mutation, self.inspyred.ec.variators.blend_crossover]
		self.kwargs["mutation_rate"] = 0.25
		self.kwargs["num_elites"] = int(self.size_of_population/2)
		self.kwargs["gaussian_stdev"] = 0.5

class PAES_INSPYRED(InspyredAlgorithmBasis):
	"""
	Implements a custom version of ``Pareto Archived Evolution Strategies`` algorithm for minimization from the ``inspyred`` package.
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	.. seealso::

		Documentation of the options from 'inspyred':
			http://inspyred.github.io/reference.html#module-inspyred.ec

	"""
	def __init__(self, reader_obj,  option_obj):
		InspyredAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.option_obj.multi_objective=True
		self.kwargs["max_archive_size"] = 100,
		self.kwargs["num_grid_divisions"] = 4
		self.evo_strat=self.inspyred.ec.emo.PAES(self.rand)

class SA_INSPYRED(InspyredAlgorithmBasis):
	"""
	Implements the ``Simulated Annealing`` algorithm for minimization from the ``inspyred`` package.
	:param reader_obj: an instance of ``DATA`` object
	:param option_obj: an instance of ``optionHandler`` object
	.. seealso::
		Documentation of the Simulated Annealing from 'inspyred':
			http://inspyred.github.io/reference.html#replacers-survivor-replacement-methods


	"""
	def __init__(self, reader_obj,  option_obj):
		InspyredAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.evo_strat=self.inspyred.ec.SA(self.rand)
	

class IBEA_BLUEPYOPT(BluepyoptAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		BluepyoptAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.selector_name = "IBEA"


class NSGA2_BLUEPYOPT(BluepyoptAlgorithmBasis):
	def __init__(self, reader_obj,  option_obj):
		BluepyoptAlgorithmBasis.__init__(self, reader_obj,  option_obj)
		self.selector_name = "NSGA2"

class CMAES_CMAES(baseOptimizer):
	def __init__(self, reader_obj,  option_obj):
		baseOptimizer.__init__(self, reader_obj,  option_obj)
		self.size_of_population = self.algo_params.pop("size_of_population")
		self.number_of_generations = self.algo_params.pop("number_of_generations")
		self.number_of_cpu = int(self.algo_params.pop("number_of_cpu",1))
		if option_obj.starting_points:
			self.starting_points = [normalize(option_obj.starting_points, self)]
		else:
			self.starting_points = np.ones(len(self.boundaries[0]))*0.5
		"""if os.path.isfile(self.directory+"/checkpoint_cmaes.pickle"):
				with open(self.directory+"/checkpoint_cmaes.pickle", 'rb') as outfile:
					self.cmaoptimizer=pickle.load(outfile)
		else:"""
		from cmaes import CMA
		self.cmaoptimizer = CMA(mean=(self.starting_points), **self.algo_params, seed=self.seed, population_size=int(self.size_of_population), bounds=np.array([[0,1]]*len(self.boundaries[0])))
		
				
	def Optimize(self):
			"""
			Performs the optimization.
			"""
					
			with Pool(int(self.number_of_cpu)) as pool:
				for generation in range(int(self.number_of_generations-int(self.cmaoptimizer.generation))):
					"""with open(self.directory+"/checkpoint_cmaes.pickle", "wb") as outfile:
						pickle.dump(self.cmaoptimizer, outfile)"""
					print("Generation: {0}".format(self.cmaoptimizer.generation))
					solutions = []
					candidate = [self.cmaoptimizer.ask() for _ in range(self.cmaoptimizer.population_size)]
					fitness = pool.map(self.ffun,candidate)
					solutions=[[list(pop), fit[0]] for pop,fit in zip(candidate,fitness)]
					self.cmaoptimizer.tell(solutions)
					
					

					
