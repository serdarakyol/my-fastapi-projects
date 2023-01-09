from pandas import DataFrame
from numpy import zeros, where, argmax, int8, empty
from numpy.core.defchararray import find
from numpy.random import choice

from collections import Counter

from api.utils.utils_cf import calculate_similarity_parallel

class Recommendation:
    def __init__(self, cf_matrix:DataFrame, products_info:list) -> None:
        self.cf_matrix = cf_matrix
        self.products_info = products_info

    def find_products_by_id(self, recommended_product_ids:list):
        """
        Finds product information based via product id

        Return: Recommended product information
        """

        # create empty array and store in same order
        product_ids = empty(len(self.products_info), dtype='S18')
        for index, id in enumerate(self.products_info):
            product_ids[index] = id['productid']


        for idx, rec_item in enumerate(recommended_product_ids):
            # find string
            is_in = find(product_ids.astype(str), rec_item) # if there is not string return -1 else 0
            index = where(is_in == 0)[0][0]
            # replace product and if all product info
            recommended_product_ids[idx] = self.products_info[index]
        
        return recommended_product_ids

    def recommend(self, items:list, n_item:int) -> list:
        """
        Recommends new products based on similar sessions

        Return: Recommended product information
        """
        cf_products = self.cf_matrix.columns
        cf_column_len:int = cf_products.shape[0]

        # create current cart
        current_cart = zeros(shape=cf_column_len, dtype=int8)
        for item in items:
            indices = where(cf_products == item)
            current_cart[indices] = 1
        
        # convert pandas df to numpy array
        data_matrix = self.cf_matrix.to_numpy(dtype=int8)

        # store scores (dtype is np.float64)
        scores = calculate_similarity_parallel(
            multiple_item=data_matrix,
            single_item=current_cart
        )

        # find the most n similar items
        similar_items = []
        while len(similar_items) <= n_item:
            idx = argmax(scores)
            if current_cart != self.cf_matrix.index.to_numpy():
                # find similar sessions
                item_indexes = where(self.cf_matrix.iloc[idx].values == 1)
                similar_session_items = cf_products[item_indexes]

                # store all of the products from similar sessions
                for item in similar_session_items:
                    if item not in items:
                        similar_items.append(item) 
                scores[idx] = 0

            else:
                scores[idx] = 0

        # find frequency of similar item based onn similar sessions 
        likely_items = Counter(similar_items).most_common(n_item)
        del similar_items

        # recommend if item not in cart
        product_ids = []
        for recommend_item in likely_items:
            if recommend_item[0] not in items:
                product_ids.append(recommend_item[0])
        
        # if there are not any similar item, randomly recommend
        if len(product_ids) == 0:
            product_ids = cf_products[choice(cf_column_len, size=n_item, replace=False)].to_list()

        # find product details via product id
        recommended_items = self.find_products_by_id(product_ids)

        return recommended_items
