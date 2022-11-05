import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from scipy import sparse
from collections import Counter

def foodrecommendation():

    lmbda = 0.0002
    df = pd.read_csv("new_reviews.csv")
    train_df = df[["ProductId", "UserId", "Score"]]
    train_df.head()

    n_users = len(pd.unique(df["UserId"]))
    n_foods = len(pd.unique(df["ProductId"]))

    print("Number of ratings : ", len(np.array(df["UserId"])))
    print("Number of users : ", n_users)
    print("Number of products : ", n_foods)

    def create_embeddings(n, K):
        return 11 * np.random.random((n, K)) / K

    def create_sparse_matrix(df, rows, cols, column_name="Score"):
        return sparse.csc_matrix((df[column_name].values, (df['UserId'].values, df['ProductId'].values)),
                                 shape=(rows, cols))

    def encode_column(column):
        """ Encodes a pandas column with continous IDs"""
        keys = column.unique()
        key_to_id = {key: idx for idx, key in enumerate(keys)}
        return key_to_id, np.array([key_to_id[x] for x in column]), len(keys)

    def encode_df(food_df):
        """Encodes rating data with continuous user and food ids"""

        food_ids, food_df['ProductId'], num_foods = encode_column(food_df['ProductId'])
        user_ids, food_df['UserId'], num_users = encode_column(food_df['UserId'])
        return food_df, num_users, num_foods, user_ids, food_ids

    food_df, num_users, num_foods, user_ids, food_ids = encode_df(train_df)

    print("Number of users :", num_users)
    print("Number of food :", num_foods)
    food_df.head()

    Y = create_sparse_matrix(food_df, num_users, num_foods)

    def predict(df, emb_user, emb_food):
        """ This function computes df["prediction"] without doing (U*V^T).

        Computes df["prediction"] by using elementwise multiplication of the corresponding embeddings and then
        sum to get the prediction u_i*v_j. This avoids creating the dense matrix U*V^T.
        """
        df['prediction'] = np.sum(np.multiply(emb_food[df['ProductId']], emb_user[df['UserId']]), axis=1)
        return df

    def cost(df, emb_user, emb_food):
        """ Computes mean square error"""
        Y = create_sparse_matrix(df, emb_user.shape[0], emb_food.shape[0])
        predicted = create_sparse_matrix(predict(df, emb_user, emb_food), emb_user.shape[0], emb_food.shape[0],
                                         'prediction')
        return np.sum((Y - predicted).power(2)) / df.shape[0]

    def gradient(df, emb_user, emb_food):
        Y = create_sparse_matrix(df, emb_user.shape[0], emb_food.shape[0])
        predicted = create_sparse_matrix(predict(df, emb_user, emb_food), emb_user.shape[0], emb_food.shape[0],
                                         'prediction')
        delta = (Y - predicted)
        grad_user = (-2 / df.shape[0]) * (delta * emb_food) + 2 * lmbda * emb_user
        grad_anime = (-2 / df.shape[0]) * (delta.T * emb_user) + 2 * lmbda * emb_food
        return grad_user, grad_anime

    def gradient_descent(df, emb_user, emb_food, iterations=2000, learning_rate=0.01, df_val=None):
        Y = create_sparse_matrix(df, emb_user.shape[0], emb_food.shape[0])
        beta = 0.9
        grad_user, grad_food = gradient(df, emb_user, emb_food)
        v_user = grad_user
        v_food = grad_food
        for i in range(iterations):
            grad_user, grad_food = gradient(df, emb_user, emb_food)
            v_user = beta * v_user + (1 - beta) * grad_user
            v_food = beta * v_food + (1 - beta) * grad_food
            emb_user = emb_user - learning_rate * v_user
            emb_food = emb_food - learning_rate * v_food
            if (not (i + 1) % 50):
                print("\niteration", i + 1, ":")
                print("train mse:", cost(df, emb_user, emb_food))
                if df_val is not None:
                    print("validation mse:", cost(df_val, emb_user, emb_food))
        return emb_user, emb_food

    emb_user = create_embeddings(num_users, 5)
    emb_food = create_embeddings(num_foods, 5)
    print("iteration", 0, ":")
    print("train mse:", cost(food_df, emb_user, emb_food))
    emb_user, emb_food = gradient_descent(food_df, emb_user, emb_food, iterations=200, learning_rate=0.1)

    return emb_user, emb_food , user_ids, food_ids