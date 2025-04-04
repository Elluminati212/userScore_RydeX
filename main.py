from fastapi import FastAPI, HTTPException, Header, Depends, Query
from pymongo import MongoClient
from bson.json_util import dumps, loads
import requests
import uvicorn
import os
import math
import pandas as pd
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import HTMLResponse

app = FastAPI()

    
# MongoDB connection
MONGO_URI = "mongodb+srv://vpatel179:LqpC2zz4rO7pmtkR@cluster0.ejksq.mongodb.net/"  # WriteDB MongoDB URI
DB_NAME = "WriteSCORE"  # Database name

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["userScore"]


@app.get("/provider_score")
async def get_provider_score(
    # auth: None = Depends(authenticate_request),
    user_id: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    final_score: Optional[float] = Query(None),
    # name: Optional[str] = Query(None),
    # email: Optional[str] = Query(None),
    # phone: Optional[str] = Query(None),
    # performance_score: Optional[float] = Query(None),
    # review_score: Optional[float] = Query(None),
    # review_score_percentage: Optional[float] = Query(None),
    # rating_score: Optional[float] = Query(None),
    # acceptance_score: Optional[float] = Query(None),
    # activation_score: Optional[float] = Query(None),
    # completion_score: Optional[float] = Query(None),
    # rejection_score: Optional[float] = Query(None),
    # cancellation_score: Optional[float] = Query(None),
    # reliability_score: Optional[float] = Query(None),
    # missed_request_score: Optional[float] = Query(None),
    # combined_score: Optional[float] = Query(None),
    # category: Optional[int] = Query(None),
    # rank: Optional[int] = Query(None),
    # percentile: Optional[float] = Query(None),
):
    try:
        query = {}

        if user_id is not None:
            query["user_id"] = user_id
        if date is not None:
            query["Date"] = date
        if final_score is not None:
            query["email"] = final_score
        # if phone is not None:
        #     query["phone"] = phone
        # if performance_score is not None:
        #     query["performance_score"] = performance_score
        # if review_score is not None:
        #     query["review_score"] = review_score
        # if review_score_percentage is not None:
        #     query["review_score_percentage"] = review_score_percentage
        # if rating_score is not None:
        #     query["rating_score"] = rating_score
        # if acceptance_score is not None:
        #     query["acceptance_score"] = acceptance_score
        # if activation_score is not None:
        #     query["activation_score"] = activation_score
        # if completion_score is not None:
        #     query["completion_score"] = completion_score
        # if rejection_score is not None:
        #     query["rejection_score"] = rejection_score
        # if cancellation_score is not None:
        #     query["cancellation_score"] = cancellation_score
        # if reliability_score is not None:
        #     query["reliability_score"] = reliability_score
        # if missed_request_score is not None:
        #     query["missed_request_score"] = missed_request_score
        # if combined_score is not None:
        #     query["combined_score"] = combined_score
        # if category is not None:
        #     query["category"] = category
        # if rank is not None:
        #     query["rank"] = rank
        # if percentile is not None:
        #     query["percentile"] = percentile

        users_scores = list(collection.find(query, {"_id": 0}))
        return sanitize_data(users_scores)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def sanitize_data(data):
    for record in data:
        for key, value in record.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                record[key] = None  # Replace invalid float with None
    return data


@app.get("/provider_score_card")
async def get_provider_score_card():
    try:
        # Load CSV files
        ratings_df = pd.read_csv('user_reviews_score.csv')
        user_df = pd.read_csv('user_daily_calculater.csv')

        # Merge all dataframes on driver_id and date
        merged_df = pd.merge(merged_df, ratings_df, on=['customerId'], how='outer')
        merged_df = pd.merge(merged_df, user_df, on=['customerId'], how='outer')

        # Convert to JSON and return
        return sanitize_data(merged_df.to_dict(orient='records'))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")


@app.get("/provider_score")
async def get_provider_score_card():
    try:
        # Load CSV files
        final_df = pd.read_csv('final_score.csv')

        #  dataframe of final_score.csv
        df = final_df
        return sanitize_data(df.to_dict(orient='records'))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

