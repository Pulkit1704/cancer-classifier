# A classifier to predict breast cancer samples based on gene expression data. 

A support vector machine classifier to classify samples as cancerous or non-cancerous. The dataset used is GSE45827. It is a microarray sequencing dataset with over 150 patient samples and expression profiles for over 26,000 genes. 
The work flow is as follows: 

* Loading and cleaning the data 
* replacing the microarray tags with gene names using the sequencing platform specific SOFT map. 
* Extraction of class labels from the file metadata.
* SMOTE the dataset to balance the classes. 
* Identifying the principle componenets to reduce the dimensionality of the dataset. 
* building and training the support vector classifier. 


### Libraries used
---

* Pandas 
* Numpy 
* Matplotlib 
* Seaborn 
* Scikit-learn 
* Imbalanced-learn 
* Plotly 


### Overview 
The project aims to build a classifier to predict if the sample is cancerous or non-cancerous based on the gene expression of the sample. The raw data contains over 26,000 genes which is over 26,000 dimensions. The dataset contains around 150 samples divided into two classes: Breast Cancerous or Normal. 

After loading and cleaning the data, the class imbalance was addressed by SMOTE technique (Synthetic Minority Oversampling Technique). It works by clustering the data using KNN and then randomly sampling points around the minority cluster to augment the minority class with more samples. After SMOTE, the sample size was increased to 260 with 130 samples for each class. 

Next PCA was done to address the high dimensionality of the dataset. First three principle components were enough to explain more than 50% of the variance in the data hence the dimensionality of the dataset was reduced from 26,000 to 3 dimensions. 

The following plots shows the three principle components 

![](./output_plots/pca%20plot.png)


The two clusters are clearly visible with their respective labels. 

the SVM hyperplane is depicted below: 
![](./output_plots/hyperplant%20plot.png)