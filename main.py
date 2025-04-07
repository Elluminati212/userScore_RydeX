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
import re

app = FastAPI()

# MongoDB connection
MONGO_URI = "mongodb+srv://vpatel179:LqpC2zz4rO7pmtkR@cluster0.ejksq.mongodb.net/"
DB_NAME = "WriteSCORE"

RYDEX_MONGO_URI = "mongodb+srv://read_access:g4WJ9ZstQzwsa3lm@hyzedeveloper.rfju1.mongodb.net/RydeX_history?retryWrites=true&w=majority"
RYDEX_DB_NAME = "RydeX"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["userScore"]

rydex_client = MongoClient(RYDEX_MONGO_URI)
rydex_db = rydex_client[RYDEX_DB_NAME]
customer_collection = rydex_db["customers"]

@app.get("/user_score")
async def get_customer_score(
    customerId: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    final_score: Optional[float] = Query(None),
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    searchKey: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10),
):
    try:
        query = {}

        # Optional search with regex on the customers collection
        if searchKey:
            search_regex = {"$regex": re.escape(searchKey), "$options": "i"}
            matched_customers = list(customer_collection.find({
                "$or": [
                    {"firstName": search_regex},
                    {"lastName": search_regex},
                    {"phone": search_regex},
                    {"email": search_regex},
                    {"searchKey": search_regex}
                ]
            }, {"_id": 0, "customerId": 1}))

            matched_ids = [customer["customerId"] for customer in matched_customers if "customerId" in customer]
            if matched_ids:
                query["customerId"] = {"$in": matched_ids}
            else:
                return {
                    "page": page,
                    "limit": limit,
                    "count": 0,
                    "data": []
                }

        if customerId is not None:
            query["customerId"] = customerId
        if date is not None:
            query["Date"] = date
        if final_score is not None:
            query["final_score"] = final_score
        if name is not None:
            query["name"] = name
        if email is not None:
            query["email"] = email
        if phone is not None:
            query["phone"] = phone

        skip = (page - 1) * limit
        users_scores = list(collection.find(query, {"_id": 0}).skip(skip).limit(limit))

        return {
            "page": page,
            "limit": limit,
            "count": len(users_scores),
            "data": sanitize_data(users_scores)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def sanitize_data(data):
    for record in data:
        for key, value in record.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                record[key] = None
    return data

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5560, reload=True)
