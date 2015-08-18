'''
Created on 22 Jan 2013

.. codeauthor:: jhkwakkel <j.h.kwakkel (at) tudelft (dot) nl>
'''
from __future__ import (absolute_import, print_function, division,
                        unicode_literals)

import abc
from threading import Lock

import numpy as np

from . import ema_logging
from .ema_exceptions import EMAError
from .ema_logging import info, debug
from .uncertainties import CategoricalUncertainty,\
                                       ParameterUncertainty,\
                                       INTEGER

__all__ = ['AbstractCallback',
           'DefaultCallback']

class AbstractCallback(object):
    '''
    Base class from which different call back classes can be derived.
    Callback is responsible for storing the results of the runs.
    
    '''
    __metaclass__ = abc.ABCMeta
    
    
    i = 0
    reporting_interval = 100
    results = []
    
    def __init__(self, 
                 uncertainties, 
                 outcomes,
                 nr_experiments,
                 reporting_interval=100):
        '''
        
        Parameters
        ----------
        uncs : list
                a list of the uncertainties over which the experiments 
                are being run.
        outcomes : list
                   a list of outcomes
        nr_experiments : int
                         the total number of experiments to be executed
        reporting_interval : int 
                             the interval at which to provide
                             progress information via logging.
        
                
        '''
        self.reporting_interval = reporting_interval
            
    @abc.abstractmethod
    def __call__(self, case_id, case, policy, name, result):
        '''
        Method responsible for storing results. The implementation in this
        class only keeps track of how many runs have been completed and 
        logging this. 
        
        Parameters
        ----------
        case_id: int
                 the job id
        case: dict
              the case to be stored
        policy: str 
                the name of the policy being used
        name: str
              the name of the model being used
        result: dict
                the result dict
        
        '''
        
        self.i+=1
        debug(str(self.i)+" cases completed")
        
        if self.i % self.reporting_interval == 0:
            info(str(self.i)+" cases completed")

    @abc.abstractmethod
    def get_results(self):
        """
        method for retrieving the results. Called after all experiments have 
        been completed
        """

        
class DefaultCallback(AbstractCallback):
    """ 
    default callback system
    callback can be used in performExperiments as a means for specifying 
    the way in which the results should be handled. If no callback is 
    specified, this default implementation is used. This one can be 
    overwritten or replaced with a callback of your own design. For 
    example if you prefer to store the result in a database or write 
    them to a text file
    """
    
    i = 0
    cases = None 
    results = {}
    
    shape_error_msg = "can only save up to 2d arrays, this array is {}d"
    
    def __init__(self, 
                 uncs, 
                 outcomes, 
                 nr_experiments, 
                 reporting_interval=100):
        '''
        
        
        Parameters
        ----------
        uncs : list
                a list of the uncertainties over which the experiments 
                are being run.
        outcomes : list
                   a list of outcomes
        nr_experiments : int
                         the total number of experiments to be executed
        reporting_interval : int 
                             the interval at which to provide
                             progress information via logging.
        
        '''
        super(DefaultCallback, self).__init__(uncs, 
                                              outcomes, 
                                              nr_experiments, 
                                              reporting_interval)
        self.i = 0
        self.cases = None
        self.results = {}
        self.lock = Lock()
        
        self.outcomes = outcomes

        #determine data types of uncertainties
        self.dtypes = []
        self.uncertainties = []
        
        for uncertainty in uncs:
            name = uncertainty.name
            self.uncertainties.append(name)
            dataType = float
            
            if isinstance(uncertainty, CategoricalUncertainty):
                dataType = object
            elif isinstance(uncertainty, ParameterUncertainty) and\
                          uncertainty.dist==INTEGER:
                dataType = int
            self.dtypes.append((name, dataType))
        self.dtypes.append((str('model'), object))
        self.dtypes.append((str('policy'), object))
        
        self.cases = np.empty((nr_experiments,), dtype=self.dtypes)
        self.cases[:] = np.NAN
        self.nr_experiments = nr_experiments

    def _store_case(self, case_id, case, model, policy):
        case = [case.get(key) for key in self.uncertainties]
        case.append(model)
        case.append(policy)
        case = tuple(case)
        self.cases[case_id] = case
            
    def _store_result(self, case_id, result):
        for outcome in self.outcomes:
            debug("storing {}".format(outcome))
            
            try:
                outcome_res = result[outcome]
            except KeyError:
                ema_logging.debug("%s not specified as outcome in msi" % outcome)
            else:
                try:
                    self.results[outcome][case_id, ] = outcome_res
                except KeyError: 
                    shape = np.asarray(outcome_res).shape
                    
                    if len(shape)>2:
                        raise EMAError(self.shape_error_msg.format(len(shape)))
                    
                    shape = list(shape)
                    shape.insert(0, self.nr_experiments)
                    
                    self.results[outcome] = np.empty(shape)
                    self.results[outcome][:] = np.NAN
                    self.results[outcome][case_id, ] = outcome_res
    
    def __call__(self, case_id, case, policy, name, result ):
        '''
        Method responsible for storing results. This method calls 
        :meth:`super` first, thus utilizing the logging provided there
        
        
        Parameters
        ----------
        case_id: int
                 the job id
        case: dict
              the case to be stored
        policy: str 
                the name of the policy being used
        name: str
              the name of the model being used
        result: dict
                the result dict
        
        '''
        super(DefaultCallback, self).__call__(case_id, case, policy, name, result)

        self.lock.acquire()
                           
        #store the case
        self._store_case(case_id, case, name, policy.get('name'), )
        
        #store results
        self._store_result(case_id, result)
        
        self.lock.release()
        
    def get_results(self):
        return self.cases, self.results