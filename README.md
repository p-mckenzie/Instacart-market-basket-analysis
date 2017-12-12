# Instacart Market Basket Analysis

A feature engineering approach by Paige McKenzie.


Overview
======
The Instacart Market Basket Analysis was a competition hosted on [Kaggle](https://www.kaggle.com/c/instacart-market-basket-analysis "Kaggle's Instacart Market Basket Analysis") which ended on August 14, 2017, that challenged data scientists to use a set of various users' order histories to predict what set of products a given user will re-order, the next time they place an order through Instacart.

My approach was feature engineering (feature_engineering.py), followed by various models including GBM, MLP, and lightGBM (analysis.ipynb).

The feature engineering script takes the data files provided by the competition and generates a set of predictive variables for each unique user-product pair in the prior orders (those before the train/test order). The target for each unique user-product pair where the user is in the training set is 1 if the user orders the product in their train order (most recent order in the dataset), and 0 if the user does not. The target for each unique user-product pair where the user is in the test set is unknown, though designated as 2 in the files. 


The data dictionary (also available as an Excel workbook) is as follows: 

|Attribute	| Level	| Description	|Type |
|-----:|-----:|:-----|:-----|
|product_id|1|Unique row identifier|||
|user_id|1|Unique row identifier|||
|order_id|1|Used for grouping predictions in test set|||
|target|1|That which we are predicting (whether the product appeared in the user's most recent order or not)|Category|
|avg_days_between_order|2 - User|The average number of days between the user's orders|Continuous|
|avg_order_size|2 - User|The average number of products in all the user's orders|Continuous|
|reordered_usr_avg|2 - User|The average of 'reordered' across all of the user's entries in the dataset|Continuous|
|num_orders_placed|2 - Use|The number of orders the user has placed|Continuous|
|aisle_id|3 - Product|The aisle the product is in|Category|
|department_id|3 - Product|The department the product is in|Category|
|organic|3 - Product|Whether the product's name indicates it is organic (1 if true)|Category|
|overall_avg_prod_disp|3 - Product|Average of usr_avg_prod_disp, across all users|Continuous|
|overall_avg_aisle_disp|4 - Aisle|Average of usr_avg_aisle_disp, across all users|Continuous|
|perc_aisle_support|4a - User/aisle|The percentage of the user's orders which have something from the aisle|Continuous|
|overall_avg_dept_disp|5 - Department|Average of usr_avg_dept_disp, across all users|Continuous|
|perc_dept_support|5a - User/dept|The percentage of the user's orders which have something from the department|Continuous|
|order_dow|6 - Order|The day of week the order was placed|Category|
|order_hour_of_day|6 - Order|The hour of day the order was placed|Category|
|perc_prod_support|7 - User/product|The percentage of the user's orders which contain the product|Continuous|
|avg_ord_pos|7 - User/product|average position of the product in the user's orders (normalized)|Continuous|
|days_since_aisle|7 - User/product|Number of days since the user has ordered from the product's aisle|Continuous|
|days_since_department|7 - User/product|Number of days since the user has ordered from the product's department|Continuous|
|days_since_prod|7 - User/product|Number of days since the user has ordered the product|Continuous|
|order_aisle_displacement|7 - User/product|Number of orders between the user placing an order from the aisle and the user ordering the product|Continuous|
|orders_since_prod|7 - User/product|Number of orders since the user last ordered the product|Continuous|
|prod_aisle_ratio|7 - User/product|ratio of how many orders had the product/how many orders had the aisle|Continuous|
|prod_dept_ratio|7 - User/product|ratio of how many orders had the product/how many orders had the department|Continuous|
|usr_avg_aisle_disp|7 - User/product|average number of days between the user ordering items from the product's aisle|Continuous|
|usr_avg_dept_disp|7 - User/product|average number of days between the user ordering items from the product's department|Continuous|
|usr_avg_prod_disp|7 - User/product|average number of days between the user ordering the product|Continuous|
|streak_length|7 - User/product|The number of consecutive orders (from most recent) the user has placed, which contain the product|Continuous|
|prod_due_overall_perc|7 - User/product|days_since_prod/overall_avg_prod_disp|Continuous|
|prod_due_user_perc|7 - User/product|days_since_prod/usr_avg_prod_disp|Continuous|
|aisle_due_overall_perc|7 - User/product|days_since_aisle/overall_avg_prod_disp|Continuous|
|aisle_due_user_perc|7 - User/product|days_since_aisle/usr_avg_prod_disp|Continuous|
|dept_due_overall_perc|7 - User/product|days_since_department/overall_avg_prod_disp|Continuous|
|dept_due_user_perc|7 - User/product|days_since_department/usr_avg_prod_disp|Continuous|



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
