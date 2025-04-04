import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Dropout # type: ignore
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# Load datasets
ratings_df = pd.read_csv('user_reviews_score.csv')
user_df = pd.read_csv('user_daily_calculater.csv')

# Preprocessing ratings data
ratings_df['created_at'] = pd.to_datetime(ratings_df['created_at'])
ratings_df['month'] = ratings_df['created_at'].dt.month
ratings_df['year'] = ratings_df['created_at'].dt.year

# Aggregate ratings by driver and month
ratings_agg = ratings_df.groupby(['driverId', 'year', 'month']).agg({
    'user_rating': 'mean',
    'sentiment_score': 'mean',
    'review_text': 'count'
}).reset_index()
ratings_agg.rename(columns={'review_text': 'review_count'}, inplace=True)

# Create a date column for merging
ratings_agg['date'] = pd.to_datetime(ratings_agg['year'].astype(str) + '-' + ratings_agg['month'].astype(str) + '-01')
ratings_agg.drop(['year', 'month'], axis=1, inplace=True)
