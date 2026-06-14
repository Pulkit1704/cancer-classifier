from sklearn.svm import SVC 
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler 
import numpy as np 

class CancerClassifier(): 

    def __init__(self, pca_components: int): 
        self.scaler = None
        self.pca_decomposer = None
        self.svc = None
        self.pca_components = pca_components
        self.label_map = None 

    
    def fit(self, data: np.ndarray, targets: np.ndarray): 


        self.label_map = {idx: label for idx, label in enumerate(np.unique(targets))}

        string_num_map = {label: idx for idx, label in self.label_map.items()}

        targets = np.array([string_num_map[label] for label in targets])

        self.scaler = StandardScaler() 

        data = self.scaler.fit_transform(data) 

        self.pca_decomposer = PCA(n_components = self.pca_components) 

        decomposed_features = self.pca_decomposer.fit_transform(data) 

        self.svc = SVC(kernel = 'linear', probability = True) 

        self.svc.fit(decomposed_features, targets) 

        return 
    
    
    def predict(self, data: np.ndarray): 

        data = self.scaler.transform(data) 

        decomposed_features = self.pca_decomposer.transform(data) 

        predictions = self.svc.predict(decomposed_features) 

        predictions = np.array([self.label_map[id] for id in predictions])

        return predictions 
    
    
    def get_pca_decomposition(self, data: np.ndarray): 

        decomposed_data = self.pca_decomposer.transform(data) 

        return decomposed_data 
    
    
    def get_confidence_score(self, data: np.ndarray): 

        decomposed_data = self.get_pca_decomposition(data) 

        distances = self.svc.decision_function(decomposed_data) 

        absolute_dist = np.abs(distances)

        min_dist = np.min(absolute_dist) 
        max_dist = np.max(absolute_dist) 

        scaled_distances = (absolute_dist - min_dist) / (max_dist - min_dist)

        return np.round(scaled_distances, 2)
    
    
    def standardize_input(self, data: np.ndarray): 

        standardized_data = self.scaler.transform(data) 

        return standardized_data
