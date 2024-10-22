import ray
import pandas as pd
from sklearn.cluster import KMeans
import openpyxl

# Initialize Ray
ray.init(address="auto")

# Load the customer data from an Excel file into a Pandas DataFrame (Sample data taken from Keras website)
customer_data = pd.read_excel("/users/praghavs/Downloads/OnlineRetail.xlsx")

# Define a function to perform customer segmentation on a data partition
@ray.remote
def segment_customers(data_partition):
    # Perform customer segmentation using K-Means clustering
    kmeans = KMeans(n_clusters=5, random_state=42)
    cluster_labels = kmeans.fit_predict(data_partition[["Quantity", "UnitPrice"]])
    
    # Add cluster labels to the data partition
    data_partition["Cluster"] = cluster_labels
    
    return data_partition

# Partition the customer data into smaller chunks
num_partitions = 10
partitioned_data = [customer_data.iloc[i::num_partitions] for i in range(num_partitions)]

# Distribute the segmentation tasks across the Ray cluster
segmentation_tasks = [segment_customers.remote(partition) for partition in partitioned_data]

# Collect the results from the segmentation tasks
segmented_partitions = ray.get(segmentation_tasks)

# Concatenate the segmented partitions into a single DataFrame
segmented_data = pd.concat(segmented_partitions, ignore_index=True)

# Write the segmented customer data to an Excel file
with pd.ExcelWriter("/users/praghavs/Downloads/segmented_customers.xlsx", engine="openpyxl") as writer:
    segmented_data.to_excel(writer, index=False)

print("Segmented customer data has been written to 'segmented_customers.xlsx'")
