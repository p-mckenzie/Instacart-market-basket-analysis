# Instacart Market Basket Analysis

A feature engineering approach by Paige McKenzie.

See my [blog post](https://p-mckenzie.github.io/2017/12/12/instacart-part-2/ "Instacart Part 2 - Modeling") concerning this project.

Overview
======
The Instacart Market Basket Analysis was a competition hosted on [Kaggle](https://www.kaggle.com/c/instacart-market-basket-analysis "Kaggle's Instacart Market Basket Analysis") which ended on August 14, 2017, that challenged data scientists to use a set of various users' order histories to predict what set of products a given user will re-order, the next time they place an order through Instacart.

My approach was feature engineering (feature_engineering.py), followed by various models including GBM, MLP, and lightGBM (analysis.ipynb).

The feature engineering script takes the data files provided by the competition and generates a set of predictive variables for each unique user-product pair in the prior orders (those before the train/test order). The target for each unique user-product pair where the user is in the training set is 1 if the user orders the product in their train order (most recent order in the dataset), and 0 if the user does not. The target for each unique user-product pair where the user is in the test set is unknown, though designated as 2 in the files. 


The data dictionary (also available as an Excel workbook) is as follows: 

|Attribute	|  Description	|
|-----:|:-----|
|product_id|Unique row identifier|
|user_id|Unique row identifier|
|order_id|Used for grouping predictions in test set|
|target|That which we are predicting (whether the product appeared in the user's most recent order or not)|
|avg_order_size|The average number of products in all the user's orders|
|prev_ord_size|The number of products in the user's previous order|
|avg_days_between_order|The average number of days between the user's orders|
|reordered_usr_avg|The average of 'reordered' across all of the user's entries in the dataset|
|num_orders_placed|The number of orders the user has placed|
|overall_avg_prod_disp|Average of usr_avg_prod_disp, across all users|
|overall_avg_aisle_disp|Average of usr_avg_aisle_disp, across all users|
|perc_aisle_support|The percentage of the user's orders which have something from the aisle|
|overall_avg_dept_disp|Average of usr_avg_dept_disp, across all users|
|perc_dept_support|The percentage of the user's orders which have something from the department|
|perc_prod_support|The percentage of the user's orders which contain the product|
|avg_ord_pos|average position of the product in the user's orders (normalized)|
|days_since_aisle|Number of days since the user has ordered from the product's aisle|
|days_since_department|Number of days since the user has ordered from the product's department|
|days_since_prod|Number of days since the user has ordered the product|
|order_aisle_displacement|Number of orders between the user placing an order from the aisle and the user ordering the product|
|orders_since_prod|Number of orders since the user last ordered the product|
|prod_aisle_ratio|ratio of how many orders had the product/how many orders had the aisle|
|prod_dept_ratio|ratio of how many orders had the product/how many orders had the department|
|usr_avg_aisle_disp|average number of days between the user ordering items from the product's aisle|
|usr_avg_dept_disp|average number of days between the user ordering items from the product's department|
|usr_avg_prod_disp|average number of days between the user ordering the product|
|streak_length|The number of consecutive orders (from most recent) the user has placed, which contain the product|
|prod_due_overall_perc|days_since_prod/overall_avg_prod_disp|
|prod_due_user_perc|days_since_prod/usr_avg_prod_disp|
|aisle_due_overall_perc|days_since_aisle/overall_avg_prod_disp|
|aisle_due_user_perc|days_since_aisle/usr_avg_prod_disp|
|dept_due_overall_perc|days_since_department/overall_avg_prod_disp|
|dept_due_user_perc|days_since_department/usr_avg_prod_disp|
|reorder_custom|Whether the product had been in the user's most recent order|


Usage
======
Feature_engineering.py
--------
Download feature_engineering.py, and place in a folder with the following files:
1. orders.csv
2. order_products__train.csv
3. order_products__prior.csv

These can be found and downloaded from the [Kaggle competition page](https://www.kaggle.com/c/instacart-market-basket-analysis/data "Data from Instacart Market Basket Analysis") as of 12/11/17. In accordance with competition rules, no datasets are included in this repository.

Execute the script, and allow for 6-7 hours of runtime. The script saves intermediate steps, and can be terminated and restarted in the middle with minimal loss of progress.

Note that, to accomplish this flexibility, several intermediate files will be saved. If you would NOT like these files to be removed when the script finishes, you will need to use standard input to direct the script to 'save' the files when the script starts. Otherwise, they will be removed.

analysis.ipynb
--------
Download analysis.ipynb, and place in a folder with the following files:
1. x_train.csv
2. x_test.csv

Both of which are generated by feature_engineering.py (see above). The Jupyter Notebook interface is recommended. Run models as you see fit, with the option to save kaggle-submission-ready CSV files. 


Requirements
======
Both scripts require Python, relying primarily on the pandas library. The analysis also requires lightGBM, sklearn, and XGBoost.

Credits
======
1. Thanks to Akulov Yaroslav's [Kaggle discussion post](https://www.kaggle.com/c/instacart-market-basket-analysis/discussion/38112 "Kaggle's Instacart discussion post #38112") detailing his feature engineering approach.
2. Part of this approach was used in a group project for MIS 382N in the Fall of 2017, but all code contained herein is my own independent work.

License
======
Copyright 2017 Paige McKenzie

In accordance with competition rules, the code contained herein is posted under the MIT License, designating it to be free to use or modify, providing the above copyright is included in all copies or substantial portions of the software.
