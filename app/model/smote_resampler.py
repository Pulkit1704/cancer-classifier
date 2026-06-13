from imblearn.over_sampling import SMOTE 
import logging 

class Resampler(): 

  def __init__(self):
    
    self.resampler = SMOTE(sampling_strategy='auto')

  
  def resample(self, input_features,target_variables): 

    resampled_input, resampled_target = self.resampler.fit_resample(input_features, 
                                                                    target_variables)
    
    return resampled_input, resampled_target 

