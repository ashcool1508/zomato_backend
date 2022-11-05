import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from scipy import sparse
from collections import Counter

lmbda = 0.0002
df = pd.read_csv("C:/Users/ashwa/Downloads/zomato/zomato_backend/new_reviews.csv")
df = df[["ProductId", "UserId", "Score"]]

def create_embeddings(n, k):
    return 11*np.random.random((n, k)) / k

def create_sparse_matrix(df, rows, cols, column_name="Score"):
    return sparse.csc_matrix((df[column_name].values,(df['UserId'].values, df['ProductId'].values)),shape=(rows, cols))

def encode_column(column):
    keys = column.unique()
    key_to_id = {key:idx for idx,key in enumerate(keys)}
    return key_to_id, np.array([key_to_id[x] for x in column]), len(keys)

def encode_df(df):
    food_ids, df['ProductId'], num_foods = encode_column(df['ProductId'])
    user_ids, df['UserId'], num_users = encode_column(df['UserId'])
    return df, num_users, num_foods, user_ids, food_ids

train_df, num_users, num_foods, user_ids, food_ids = encode_df(df)
Y = create_sparse_matrix(train_df, num_users, num_foods)

def predict(df, emb_user, emb_food):
    df['prediction'] = np.sum(np.multiply(emb_food[df['ProductId']],emb_user[df['UserId']]), axis=1)
    return df

def cost(df, emb_user, emb_food):
    Y = create_sparse_matrix(df, emb_user.shape[0], emb_food.shape[0])
    predicted = create_sparse_matrix(predict(df, emb_user, emb_food), emb_user.shape[0], emb_food.shape[0], 'prediction')
    return np.sum((Y-predicted).power(2))/df.shape[0]

def gradient(df, emb_user, emb_food):
    Y = create_sparse_matrix(df, emb_user.shape[0], emb_food.shape[0])
    predicted = create_sparse_matrix(predict(df, emb_user, emb_food), emb_user.shape[0], emb_food.shape[0], 'prediction')
    delta =(Y-predicted)
    grad_user = (-2/df.shape[0])*(delta*emb_food) + 2*lmbda*emb_user
    grad_anime = (-2/df.shape[0])*(delta.T*emb_user) + 2*lmbda*emb_food
    return grad_user, grad_anime

def gradient_descent(df, emb_user, emb_food, iterations=2000, learning_rate=0.01, df_val=None):
    Y = create_sparse_matrix(df, emb_user.shape[0], emb_food.shape[0])
    beta = 0.9
    grad_user, grad_food = gradient(df, emb_user, emb_food)
    v_user = grad_user
    v_food = grad_food
    for i in range(iterations):
        grad_user, grad_food = gradient(df, emb_user, emb_food)
        v_user = beta*v_user + (1-beta)*grad_user
        v_food = beta*v_food + (1-beta)*grad_food
        emb_user = emb_user - learning_rate*v_user
        emb_food = emb_food - learning_rate*v_food
        if(not (i+1)%50):
            print("\niteration", i+1, ":")
            print("train mse:",  cost(df, emb_user, emb_food))
            if df_val is not None:
                print("validation mse:",  cost(df_val, emb_user, emb_food))
    return emb_user, emb_food

emb_user = create_embeddings(num_users, 5)
emb_food = create_embeddings(num_foods, 5)
print("iteration", 0, ":")
print("train mse:",  cost(train_df, emb_user, emb_food))
emb_user, emb_food = gradient_descent(train_df, emb_user, emb_food, iterations=200, learning_rate=0.1)

def get_recommandation(user_id, emb_user, emb_food, num_recommadations):
  ratings_predicted = np.matmul(np.reshape(emb_user[user_ids[list(user_ids.keys())
      [list(user_ids.values()).index(user_id)]]], (1, 5)), np.transpose(emb_food))
  recommanded_index = ratings_predicted[0].argsort()[-num_recommadations:][::-1]
  for i in range(5):
    recommanded_index[i] = food_ids[recommanded_index[i]]
  return recommanded_index

for i in range(5):
  print(get_recommandation(i, emb_user, emb_food, 10))