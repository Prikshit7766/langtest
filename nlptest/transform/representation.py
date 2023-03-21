

from abc import ABC, abstractmethod
from typing import List
import pandas as pd
from nlptest.utils.custom_types import Sample, MinScoreOutput
from .utils import default_label_representation ,default_ehtnicity_representation,default_economic_country_representation,  default_religion_representation, get_label_representation_dict, get_country_economic_representation_dict, get_religion_name_representation_dict, get_ethnicity_representation_dict, get_entity_representation_proportions

class BaseRepresentation(ABC):

    """
    Abstract base class for implementing representation measures.

    Attributes:
        alias_name (str): A name or list of names that identify the representation measure.

    Methods:
        transform(data: List[Sample]) -> Any: Transforms the input data into an output based on the implemented representation measure.
    """

    @staticmethod
    @abstractmethod
    def transform(self):

        """
        Abstract method that implements the representation measure.

        Args:
            data (List[Sample]): The input data to be transformed.

        Returns:
            Any: The transformed data based on the implemented representation measure.
        """

        return NotImplementedError
    
    alias_name = None


class GenderRepresentation(BaseRepresentation):

    alias_name = [
        "min_gender_representation_count",
        "min_gender_representation_proportion"
    ]
    
    def transform(data: List[Sample]):
        return super().transform()

class EthnicityRepresentation(BaseRepresentation):
    
    alias_name = [
        "min_ethnicity_name_representation_count",
        "min_ethnicity_name_representation_proportion"
    ]
    
    

    def transform(test,data,params):
        sample_list = []
          
        if test=="min_ethnicity_name_representation_count":
            if not params:
                expected_representation = {"black": 10, "asian": 10, "white": 10, "native_american": 10, "hispanic": 10, "inter_racial": 10}
            
            else:
                if isinstance(params['min_count'], dict):
                        expected_representation = params['min_count']

                elif isinstance(params['min_count'], int):
                       expected_representation = {key: params['min_count'] for key in default_ehtnicity_representation}
                
            
            entity_representation= get_ethnicity_representation_dict(data)
               
            actual_representation = {**default_ehtnicity_representation, **entity_representation}
            
            for key, value in expected_representation.items():
                sample = Sample(
                    original = "-",
                    category = "representation",
                    test_type = "min_ethnicity_name_representation_count",
                    test_case = key,
                    expected_results = MinScoreOutput(score=value) ,
                    actual_results = MinScoreOutput(score=actual_representation[key]),
                    state = "done"
                )
                sample_list.append(sample)
                
        if test=="min_ethnicity_name_representation_proportion": 
              if not params:
                    expected_representation = {"black": 0.13, "asian": 0.13, "white": 0.13, "native_american": 0.13, "hispanic": 0.13, "inter_racial": 0.13}
                    
              
              else:
                if isinstance(params['min_proportion'], dict):
                        expected_representation = params['min_proportion']
                        
                        if sum(expected_representation.values()) > 1:
                            print(f"\nSum of proportions cannot be greater than 1. So min_ethnicity_name_representation_proportion test cannot run \n")
                            raise ValueError()

                elif isinstance(params['min_proportion'], float):
                       expected_representation = {key: params['min_proportion'] for key in default_ehtnicity_representation} 
                       if sum(expected_representation.values()) > 1:
                            print(f"\nSum of proportions cannot be greater than 1. So min_ethnicity_name_representation_proportion test cannot run \n")
                            raise ValueError()
                    
              
              entity_representation= get_ethnicity_representation_dict(data)
              entity_representation_proportion = get_entity_representation_proportions(entity_representation)
              actual_representation = {**default_ehtnicity_representation, **entity_representation_proportion}
              for key, value in expected_representation.items():

                    sample = Sample(
                        original = "-",
                        category = "representation",
                        test_type = "min_ethnicity_name_representation_proportion",
                        test_case = key,
                        expected_results = MinScoreOutput(score=value),
                        actual_results = MinScoreOutput(score=actual_representation[key]),
                        state = "done"
                    )
                    sample_list.append(sample)
                
        return sample_list
           
class LabelRepresentation(BaseRepresentation):
    
    alias_name = [
        "min_label_representation_count",
        "min_label_representation_proportion"
    ]
    
    
    def transform(test,data,params):
        sample_list = []
 
        if test=="min_label_representation_count":
        
            if not params:
                expected_representation = {'O': 10, 'LOC': 10, 'PER': 10, 'MISC': 10, 'ORG': 10}
                
            else:
                if isinstance(params['min_count'], dict):
                        expected_representation = params['min_count']

                elif isinstance(params['min_count'], int):
                       expected_representation = {key: params['min_count'] for key in default_label_representation}
           
            
            entity_representation= get_label_representation_dict(data)
               
            actual_representation = {**default_label_representation, **entity_representation}

            for key, value in expected_representation.items():
                sample = Sample(
                    original = "-",
                    category = "representation",
                    test_type = "min_label_representation_count",
                    test_case = key,
                    expected_results = MinScoreOutput(score=value) ,
                    actual_results = MinScoreOutput(score=actual_representation[key]),
                    state = "done"
                )
                sample_list.append(sample)
                
                
        if test=="min_label_representation_proportion": 
              if not params:
                    expected_representation = {'O': 0.16, 'LOC': 0.16, 'PER': 0.16, 'MISC': 0.16, 'ORG': 0.16}
              
              else:
                if isinstance(params['min_proportion'], dict):
                        expected_representation = params['min_proportion']
                        
                        if sum(expected_representation.values()) > 1:
                            print(f"\nSum of proportions cannot be greater than 1. So min_label_representation_proportion test cannot run \n")
                            raise ValueError()

                elif isinstance(params['min_proportion'], float):
                       expected_representation = {key: params['min_proportion'] for key in default_label_representation} 
                       if sum(expected_representation.values()) > 1:
                            print(f"\nSum of proportions cannot be greater than 1. So min_label_representation_proportion test cannot run \n")
                            raise ValueError()
              

              entity_representation= get_label_representation_dict(data)

              entity_representation_proportion = get_entity_representation_proportions(entity_representation)
              actual_representation = {**default_label_representation, **entity_representation_proportion}
              for key, value in expected_representation.items():

                    sample = Sample(
                        original = "-",
                        category = "representation",
                        test_type = "min_label_representation_proportion",
                        test_case = key,
                        expected_results = MinScoreOutput(score=value),
                        actual_results = MinScoreOutput(score=actual_representation[key]),
                        state = "done"
                    )
                    sample_list.append(sample)
                
        return sample_list
    

class ReligionRepresentation(BaseRepresentation):
    
    alias_name = [
        "min_religion_name_representation_count",
        "min_religion_name_representation_proportion"
    ]
    

    def transform(test,data,params):
        sample_list = []
        
        if test=="min_religion_name_representation_count":
            if not params:
                expected_representation = {'muslim': 5, 'hindu':5, 'sikh':5, 'christian':5, 'jain':5, 'buddhist':5, 'parsi':5}
                
            else:
                if isinstance(params['min_count'], dict):
                        expected_representation = params['min_count']

                elif isinstance(params['min_count'], int):
                       expected_representation = {key: params['min_count'] for key in default_religion_representation}
            
             
            entity_representation= get_religion_name_representation_dict(data)
               
            actual_representation = {**default_religion_representation, **entity_representation}

       
            for key, value in expected_representation.items():
                sample = Sample(
                    original = "-",
                    category = "representation",
                    test_type = "min_religion_name_representation_count",
                    test_case = key,
                    expected_results = MinScoreOutput(score=value) ,
                    actual_results = MinScoreOutput(score=actual_representation[key]),
                    state = "done"
                )
                sample_list.append(sample)
                
        if test=="min_religion_name_representation_proportion": 
              if not params:
                    expected_representation = {'muslim': 0.11, 'hindu':0.11, 'sikh':0.11, 'christian':0.11, 'jain':0.11, 'buddhist':0.11, 'parsi':0.11}
              
              else:
                    if isinstance(params['min_proportion'], dict):
                        expected_representation = params['min_proportion']
                        
                        if sum(expected_representation.values()) > 1:
                            print(f"\nSum of proportions cannot be greater than 1. So min_religion_name_representation_proportion test cannot run \n")
                            raise ValueError()
                   
                    elif isinstance(params['min_proportion'], float):
                       expected_representation = {key: params['min_proportion'] for key in default_religion_representation} 
                       if sum(expected_representation.values()) > 1:
                            print(f"\nSum of proportions cannot be greater than 1. So min_religion_name_representation_proportion test cannot run \n")
                            raise ValueError()

              
              entity_representation= get_religion_name_representation_dict(data)
              entity_representation_proportion = get_entity_representation_proportions(entity_representation)       
              actual_representation = {**default_religion_representation, **entity_representation_proportion}
              for key, value in expected_representation.items():

                    sample = Sample(
                        original = "-",
                        category = "representation",
                        test_type = "min_religion_name_representation_proportion",
                        test_case = key,
                        expected_results = MinScoreOutput(score=value),
                        actual_results = MinScoreOutput(score=actual_representation[key]),
                        state = "done"
                    )
                    sample_list.append(sample)
                
        return sample_list

class CountryEconomicRepresentation(BaseRepresentation):
    
    alias_name = [
        "min_country_economic_representation_count",
        "min_country_economic_representation_proportion"
    ]
    

    def transform(test,data,params):
        sample_list = []
        
        if test=="min_country_economic_representation_count":
            if not params:
                expected_representation = {'high_income': 10,'low_income': 10,'lower_middle_income': 10,'upper_middle_income': 10}
            
            else:
                if isinstance(params['min_count'], dict):
                        expected_representation = params['min_count']

                elif isinstance(params['min_count'], int):
                       expected_representation = {key: params['min_count'] for key in default_economic_country_representation}
                        
            entity_representation= get_country_economic_representation_dict(data)
               
            actual_representation = {**default_economic_country_representation, **entity_representation}

            for key, value in expected_representation.items():
                sample = Sample(
                    original = "-",
                    category = "representation",
                    test_type = "min_country_economic_representation_count",
                    test_case = key,
                    expected_results = MinScoreOutput(score=value) ,
                    actual_results = MinScoreOutput(score=actual_representation[key]),
                    state = "done"
                )
                sample_list.append(sample)
                
                
        if test=="min_country_economic_representation_proportion": 
              if not params:
                    expected_representation = {'high_income': 0.20,'low_income': 0.20,'lower_middle_income': 0.20,'upper_middle_income': 0.20}        
              
              else:
                    if isinstance(params['min_proportion'], dict):
                        expected_representation = params['min_proportion']
                        
                        if sum(expected_representation.values()) > 1:
                            print(f"\nSum of proportions cannot be greater than 1. So min_country_economic_representation_proportion test cannot run \n")
                            raise ValueError()
                   
                    elif isinstance(params['min_proportion'], float):
                       expected_representation = {key: params['min_proportion'] for key in default_economic_country_representation} 
                       if sum(expected_representation.values()) > 1:
                            print(f"\nSum of proportions cannot be greater than 1. So min_country_economic_representation_proportion test cannot run \n")
                            raise ValueError()
                

        
              entity_representation= get_country_economic_representation_dict(data)
              entity_representation_proportion = get_entity_representation_proportions(entity_representation)
              actual_representation = {**default_economic_country_representation, **entity_representation_proportion}
              for key, value in expected_representation.items():

                    sample = Sample(
                        original = "-",
                        category = "representation",
                        test_type = "min_country_economic_representation_proportion",
                        test_case = key,
                        expected_results = MinScoreOutput(score=value),
                        actual_results = MinScoreOutput(score=actual_representation[key]),
                        state = "done"
                    )
                    sample_list.append(sample)
                
        return sample_list