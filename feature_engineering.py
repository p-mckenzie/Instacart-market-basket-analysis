#!/usr/bin/env python

# Import relevant packages, filter warnings
import pandas as pd
import numpy
import os
import pickle
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def user_computations(big_group):
    '''
    Takes a subset of the new dataframe created above (all rows for a given user_id), 
    computes relevant information for each unique product_id,
    and returns a dictionary with 
            keys: product_id 
            values: ['order_number', 'days_since_prod','days_since_aisle','days_since_department','order_aisle_displacement','orders_since_prod','avg_prod_disp','avg_aisle_disp','avg_dept_disp','prod_aisle_ratio','prod_dept_ratio', 'streak_length', 'target']
    Information about these engineered features can be found in the data dictionary.
    '''

    user_dict = {}
    for product_id, group in big_group.groupby('product_id'):
        #set up initial values to retain/update as we loop
        user_dict[product_id] = {
                            'order_number':max(group['order_number']),
                            'aisle_id':max(group['aisle_id']), 
                            'department_id':max(group['department_id']),
                            'days_since_prod':None,
                            'orders_since_prod':None,
                            'days_since_aisle':None,
                            'days_since_department':None,
                            'prod_ord_num':None, 
                            'aisle_ord_num':None,
                            'product_displacements':[],
                            'aisle_displacements':[],
                            'dept_displacements':[],
                            'prod_days':0, 
                            'aisle_days':0, 
                            'dept_days':0, 
                            'streak_length':0,
                            'prod_support':0.,
                            'aisle_support':0.,
                            'dept_support':0.,
                            'target':max(group['target'])
                                }
    
    order_num_max = max(group['order_number_max'])
    
    #iterate through orders, starting with most recent
    for order_number, group in big_group.groupby('order_number', sort=False):
        try:
            days = max(group['days_since_prior_order'])
        except:
            continue
        
        if 'train' in group['eval_set'].values or 'test' in group['eval_set'].values:
            #we're on the most recent order, just getting started in the loop
            
            for product_id in user_dict:
                user_dict[product_id]['prod_days']+=days
                user_dict[product_id]['aisle_days']+=days
                user_dict[product_id]['dept_days']+=days
                
            continue

        # get sets of products, aisles, and departments that occur in the order in consideration
        products = set(group['product_id'])
        aisles = set(group['aisle_id'])
        depts = set(group['department_id'])
        
        for product_id in user_dict:
            if product_id in products:
                #the current order contains the product! 
                user_dict[product_id]['prod_support'] += 1
                
                #append days since product to maintain average product displacement (in days)
                user_dict[product_id]['product_displacements'] += [user_dict[product_id]['prod_days']]
                
                # if this is the first time the product has been in the order
                if user_dict[product_id]['days_since_prod']==None:
                    #track the days/orders since prior product order
                    #AKA the number of days/orders between the test/train order and the user last ordering the product
                    user_dict[product_id]['days_since_prod'] = user_dict[product_id]['prod_days']
                    user_dict[product_id]['orders_since_prod'] = order_num_max-order_number
                    
                # check days since product - num orders
                if user_dict[product_id]['prod_ord_num']==None:
                    #track the orders since prior order, AKA the number of orders between the test/train order and the user last ordering the product
                    user_dict[product_id]['prod_ord_num'] = order_number

                # check for streak and update
                if order_num_max-order_number-1==user_dict[product_id]['streak_length']:
                    user_dict[product_id]['streak_length'] += 1

                #reset prod_days offset for next iteration
                user_dict[product_id]['prod_days'] = days
            else:
                #product was not in order, increment prod_days and continue to next product
                user_dict[product_id]['prod_days'] += days


            if user_dict[product_id]['aisle_id'] in aisles:
                #the current order contains the aisle! 
                user_dict[product_id]['aisle_support'] += 1
                
                # append days since aisle                                 
                user_dict[product_id]['aisle_displacements'] += [user_dict[product_id]['aisle_days']]
                
                # if this is the first time the aisle has been in the order
                if user_dict[product_id]['days_since_aisle']==None:
                    user_dict[product_id]['days_since_aisle'] = user_dict[product_id]['aisle_days']
                    
                # check days since product - num orders
                if user_dict[product_id]['aisle_ord_num']==None:
                    user_dict[product_id]['aisle_ord_num'] = order_number

                #reset aisle_days offset
                user_dict[product_id]['aisle_days'] = days
            else:
                user_dict[product_id]['aisle_days'] += days

            if user_dict[product_id]['department_id'] in depts:
                #the current order contains the department! 
                user_dict[product_id]['dept_support'] += 1

                # append days since dept
                user_dict[product_id]['dept_displacements'] += [user_dict[product_id]['dept_days']]
                
                # if this is the first time the department has been in the order
                if user_dict[product_id]['days_since_department']==None:
                    user_dict[product_id]['days_since_department'] = user_dict[product_id]['dept_days']

                #reset aisle_days offset
                user_dict[product_id]['dept_days'] = days
            else:
                user_dict[product_id]['dept_days'] += days
        
        #increment days, and loop again
        days = max(group['days_since_prior_order'])
        
    # take averages and reorganize/cleanup
    for product_id in user_dict:
        user_dict[product_id]['avg_prod_disp'] = round(numpy.nanmean(user_dict[product_id]['product_displacements']),2)
        user_dict[product_id]['avg_aisle_disp'] = round(numpy.nanmean(user_dict[product_id]['aisle_displacements']),2)
        user_dict[product_id]['avg_dept_disp'] = round(numpy.nanmean(user_dict[product_id]['dept_displacements']),2)
        
        user_dict[product_id]['order_aisle_displacement'] = int(abs(user_dict[product_id]['aisle_ord_num']-user_dict[product_id]['prod_ord_num'])) if user_dict[product_id]['aisle_ord_num']!=None and user_dict[product_id]['prod_ord_num']!=None else None
        user_dict[product_id]['order_aisle_displacement'] = round(numpy.nanmean(user_dict[product_id]['product_displacements']),2)
        user_dict[product_id]['order_aisle_displacement']
		
        user_dict[product_id] = {k: user_dict[product_id][k] for k in ['order_number', 'days_since_prod','days_since_aisle','days_since_department','order_aisle_displacement','orders_since_prod','avg_prod_disp','avg_aisle_disp','avg_dept_disp','prod_support', 'aisle_support', 'dept_support', 'streak_length', 'target']}
        
    return pd.DataFrame.from_dict(user_dict).T.reset_index().rename(columns={'index':'product_id'})

def generate_new_df():
	'''
	Merges the competition-provided datasets (orders, order_products__train, and order_products__prior)
	and saves instacart_merged_new.csv.
	'''
	#check if file already exists
	filename = 'instacart_merged_new.csv'
	if os.path.isfile(filename):
		return
			
	# read in data
	orders = pd.read_csv('orders.csv')
	train = pd.read_csv('order_products__train.csv')
	prior = pd.read_csv('order_products__prior.csv')

	#merge with orders
	train = train.merge(orders, on='order_id', how='left')
	prior = prior.merge(orders, on='order_id', how='left')

	#make new dataframe
	new = train.append(prior, ignore_index=True)

	del train
	del prior

	#get unique set of user, product combinations, where the user_id is in the test set (unknowns to predict)
	unique = new[new['user_id'].isin(orders[orders['eval_set']=='test']['user_id'])].drop_duplicates(['user_id', 'product_id'])[['user_id', 'product_id']]
	#merge with orders
	unique = unique.merge(orders[orders['eval_set']=='test'], on='user_id', how='left')

	del orders

	#append to new dataframe
	new = new.append(unique, ignore_index=True)

	#select a few relevant columns and re-arrange
	new = new[['order_id', 'product_id', 'user_id', 'order_number', 'add_to_cart_order', 'reordered', 'days_since_prior_order', 'eval_set', 'order_dow', 'order_hour_of_day']]

	#self-join to get each user's maximum number of orders (including the train/test orders)
	new = new.join(new.groupby('user_id')['order_number'].max(), on='user_id', how='left', rsuffix='_max')

	#self-join to get each order's number of items (meaningless for the train/test orders)
	new = new.join(new.groupby('order_id')['add_to_cart_order'].max(), on='order_id', how='left', rsuffix='_max')
	new.rename(columns={'add_to_cart_order_max':'ord_size'}, inplace=True)

	#merge with products to get aisle_id and department_id
	products = pd.read_csv('products.csv')
	new = new.merge(products[['product_id', 'aisle_id', 'department_id']], left_on='product_id', right_on='product_id', how='left')
	del products

	# create target, based on which order the product was in
	new['target'] = 0
	new.loc[new['eval_set'] == 'train', 'target'] = 1
	new.loc[new['eval_set'] == 'test', 'target'] = 2

	#sort to get newest orders first
	new.sort_values(['target', 'order_number'], ascending=[False, False], inplace=True)

	# remove values where the product is FIRST ordered by the user in the train set
	# we're only predicting re-orders, so no use training with products that have no history with that user
	new = new[~((new['target']==1) & (new['reordered']==0))]

	#save
	new.to_csv('instacart_merged_new.csv')
	
	
def chunkify(lst,n):
    return [lst[i::n] for i in range(n)]
	
def make_chunks():
	'''
	Saves a pickle file, a list with 50 sublists, containing an approximately equal number of user_ids
	from instacart_merged_new (generated by generate_new_df()).
	'''
	#check if file already exists
	filename = 'chunks'
	if os.path.isfile(filename):
		return
		
	print("Now making chunks.", datetime.now().strftime("%X, %x"), "\n")

	new = pd.read_csv('instacart_merged_new.csv', index_col=0)

	chunks = chunkify(list(new['user_id'].unique()), 50)
	with open('chunks', 'wb') as fp:
		pickle.dump(chunks, fp)
		

def do_computations():
	'''
	Loops through the 50 user_id chunks (from make_chunks()), applying the user_computations function and
	saving a csv.
	'''
	if not os.path.exists('Chunk_partitions'):
		os.makedirs('Chunk_partitions')
		print("Chunk_partitions directory created.\n")
	
	with open ('chunks', 'rb') as fp:
		chunks = pickle.load(fp)
	
	print("Checking for user-product computations at", datetime.now().strftime("%X, %x"), "\n")

	for i in range(len(chunks)):
		filename = 'Chunk_partitions/chunk_{}.csv'.format(i)
		if os.path.isfile(filename):
			continue
		
		#read in data
		new = pd.read_csv('instacart_merged_new.csv', index_col=0)
		#filter by user_id
		new = new[new['user_id'].isin(chunks[i])]

		#apply the function
		joined = new.groupby('user_id').apply(user_computations)
		joined = joined.reset_index().drop('level_1', axis=1)

		#write to csv
		joined.to_csv(filename)

		#print status and repeat
		print("- completed chunk", i, "out of 49 at", datetime.now().strftime("%X, %x"))
	print()

def merge_chunks():
	'''
	Merge the files formed by do_computations() into a single file.
	'''
	filename = 'joined_current.csv'
	if os.path.isfile(filename):
		return
	print("Now merging the files into", filename, "at", datetime.now().strftime("%X, %x"), "\n")
	
	for i in range (0, 50):
		try:
			current = current.append(pd.read_csv('Chunk_partitions/chunk_{}.csv'.format(i), index_col=0), ignore_index=True)
		except:
			current = pd.read_csv('Chunk_partitions/chunk_{}.csv'.format(i), index_col=0)
	
	current.to_csv(filename)
		
def is_organic(text):
    if 'organic' in text.lower():
        return 1
    return 0

def last_merges():
	'''
	Joins instacart_merged_new.csv with the user computations done previously, and saves
	x_train and x_test.
	'''
	filename = ['x_test.csv', 'x_train.csv']
	if os.path.isfile(filename[0]) or os.path.isfile(filename[1]):
		return
	print("Now computing", filename[0], "and", filename[1], "at", datetime.now().strftime("%X, %x"), "\n")
	
	new = pd.read_csv('instacart_merged_new.csv', index_col=0)
	
	new.sort_values(['target', 'order_number'], ascending=[False, False], inplace=True)

	#Drop duplicate user_id, product_id pairs to get the necessary number of X sets (rows)
	final = new.groupby(['user_id', 'product_id']).first().reset_index()

	# drop all entries in 'new' from the train set (no peeking at the future!)
	new = new[new['eval_set']=='prior']

	#get user-based values, reordered average and jaccard similarity index
	user_only = pd.DataFrame(new.groupby('user_id')['reordered'].mean()).reset_index()
	#user_only['jacc'] = user_only['user_id'].map(get_jaccard_index)
	user_only.columns = ['user_id', 'reordered_usr_avg']#,'user_jacc']
	
	final = final.merge(user_only, on='user_id', how='left')
	del user_only
	
	# get ratio for average order position
	user_product = new.groupby(['user_id', 'product_id'])[['add_to_cart_order', 'ord_size']].sum().reset_index()
	user_product= user_product.astype(float)
	user_product['avg_ord_pos'] = user_product['add_to_cart_order']/user_product['ord_size']
	user_product['avg_ord_pos'] = user_product['avg_ord_pos'].round(2)
	
	#merge final with user_product
	final = final.merge(user_product[['user_id', 'product_id', 'avg_ord_pos']], on=['user_id', 'product_id'], how='left')
	del user_product
	
	# self-merge for average days between order, average order size
	final = final.merge(new.drop_duplicates('order_id').groupby('user_id')['days_since_prior_order'].mean().reset_index().rename(columns={'days_since_prior_order':'avg_days_between_orders'}), how='left', on='user_id')
	final = final.merge(new.drop_duplicates('order_id').groupby('user_id')['ord_size'].mean().reset_index().rename(columns={'ord_size':'avg_order_size'}), how='left', on='user_id')
	del new
	
	#merge with computations
	current = pd.read_csv('joined_current.csv', index_col=0)
	final = final.merge(current, on=['user_id', 'product_id', 'order_number'], how='left')
	del current
	
	final.rename(columns={'avg_prod_disp':'usr_avg_prod_disp', 'avg_aisle_disp':'usr_avg_aisle_disp',
                  'avg_dept_disp':'usr_avg_dept_disp'}, inplace=True)
	
	# overall averages - grouped by product, aisle, and department
	final = final.merge(final.drop_duplicates(['user_id', 'product_id']).groupby('product_id')['usr_avg_prod_disp'].mean().reset_index().rename(columns={'usr_avg_prod_disp':'overall_avg_prod_disp'}), on='product_id', how='left')
	final = final.merge(final.drop_duplicates(['user_id', 'aisle_id']).groupby('aisle_id')['usr_avg_aisle_disp'].mean().reset_index().rename(columns={'usr_avg_aisle_disp':'overall_avg_aisle_disp'}), on='aisle_id', how='left')
	final = final.merge(final.drop_duplicates(['user_id', 'department_id']).groupby('department_id')['usr_avg_dept_disp'].mean().reset_index().rename(columns={'usr_avg_dept_disp':'overall_avg_dept_disp'}), on='department_id', how='left')
	
	del final['target_y']
	final.rename(columns={'order_number_max':'num_orders_placed','target_x':'target'}, inplace=True)
	
	#take a few ratios	
	final['perc_prod_support'] = final['prod_support']/final['num_orders_placed']
	final['perc_aisle_support'] = final['aisle_support']/final['num_orders_placed']
	final['perc_dept_support'] = final['dept_support']/final['num_orders_placed']
	
	final['prod_due_overall_perc'] = final['days_since_prod']/final['overall_avg_prod_disp']
	final['prod_due_user_perc'] = final['days_since_prod']/final['usr_avg_prod_disp']

	final['aisle_due_overall_perc'] = final['days_since_aisle']/final['overall_avg_aisle_disp']
	final['aisle_due_user_perc'] = final['days_since_aisle']/final['usr_avg_aisle_disp']

	final['dept_due_overall_perc'] = final['days_since_department']/final['overall_avg_dept_disp']
	final['dept_due_user_perc'] = final['days_since_department']/final['usr_avg_dept_disp']
	
	final['prod_aisle_ratio'] = final['prod_support']/final['aisle_support']
	final['prod_dept_ratio'] = final['prod_support']/final['dept_support']
	
	#clean up those decimals
	final['avg_days_between_orders'] = final['avg_days_between_orders'].round(2)
	final['avg_order_size'] = final['avg_order_size'].round(2)

	final['perc_prod_support'] = final['perc_prod_support'].round(3)
	final['perc_aisle_support'] = final['perc_aisle_support'].round(3)
	final['perc_dept_support'] = final['perc_dept_support'].round(3)
	final['reordered_usr_avg'] = final['reordered_usr_avg'].round(3)

	final['prod_due_overall_perc'] = final['perc_aisle_support'].round(3)
	final['prod_due_user_perc'] = final['perc_dept_support'].round(3)
	final['aisle_due_overall_perc'] = final['reordered_usr_avg'].round(3)
	final['aisle_due_user_perc'] = final['perc_aisle_support'].round(3)
	final['dept_due_overall_perc'] = final['perc_dept_support'].round(3)
	final['dept_due_user_perc'] = final['reordered_usr_avg'].round(3)
	
	final['prod_aisle_ratio'] = final['prod_aisle_ratio'].round(3)
	final['prod_dept_ratio'] = final['prod_dept_ratio'].round(3)
	
	#get 'organic' flag
	products = pd.read_csv('products.csv')
	products['organic'] = products['product_name'].apply(is_organic)

	final = final.merge(products[['product_id', 'organic']], how='left', on='product_id')
	del products
	
	#select relevant columns

	final = final[['user_id', 'product_id', 'target',
	'aisle_id',
	'department_id',
	'avg_days_between_orders',
	'avg_order_size',
	'num_orders_placed',
	'reordered_usr_avg',
	'organic',
	'overall_avg_prod_disp',
	'overall_avg_aisle_disp',
	'perc_aisle_support',
	'overall_avg_dept_disp',
	'perc_dept_support',
	'order_dow',
	'order_hour_of_day',
	'avg_ord_pos',
	'days_since_aisle',
	'days_since_department',
	'days_since_prod',
	'order_aisle_displacement',
	'orders_since_prod',
	'perc_prod_support',
	'prod_aisle_ratio',
	'prod_dept_ratio',
	'streak_length',
	'usr_avg_aisle_disp',
	'usr_avg_dept_disp',
	'usr_avg_prod_disp',
	'prod_due_overall_perc',
	'prod_due_user_perc',
	'aisle_due_overall_perc',
	'aisle_due_user_perc',
	'dept_due_overall_perc',
	'dept_due_user_perc'
				  ]]
	
	final[final['target']==2].to_csv('x_test.csv')
	final[final['target']!=2].to_csv('x_train.csv')
	print(final['target'].value_counts())
	
def cleanup():
	import shutil
	
	try:
		shutil.rmtree('Chunk_partitions')
	except:
		pass
	
	try:
		os.remove('instacart_merged_new.csv')
	except:
		pass
	
	try:
		os.remove('joined_current.csv')
	except:
		pass
		
	try:
		os.remove('chunks')
	except:
		pass
	print("Intermediary files cleared.\n")
	
clean = input("During the computations, several files will be saved.\nIf you would NOT like these to be cleaned after the computations are completed, enter 'save', else hit enter: ")
if clean=='save':
	print("Files will be left as created.\n")
else:
	print("Files will be removed after completion.\n")

print("Computations started at", datetime.now().strftime("%X, %x"), "\n")
generate_new_df()

make_chunks()

do_computations()

merge_chunks()

last_merges()

if clean=='save':
	print("Cleanup skipped.\n")
else:
	cleanup()


print("Finished at", datetime.now().strftime("%X, %x"))