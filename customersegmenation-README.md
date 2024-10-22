### Prerequisite
Have Ray installed on local machine
### Note
OnlineRetail.xlsx contains sample data for your experiment
### Execute
pip install "ray[all]" openpyxl scikit-learn

1. Run Ray cluster - ray start --head --port=6379 --dashboard-host=0.0.0.0
2. In another terminal, type: python3 customersegmentation.py
3. Type http://localhost:8265 to access Ray dashboard. Click on the header node, observe the workers working on the partitions.
