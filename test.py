import pandas as pd
from sklearn import metrics

def list_to_file(lst, name):
	df = pd.DataFrame(lst)
	df.to_csv(f'{name}.csv')


ridge_kernels = metrics.pairwise.PAIRWISE_KERNEL_FUNCTIONS
ridge_kernels = ridge_kernels.keys()

list_to_file(ridge_kernels, 'model_errors')