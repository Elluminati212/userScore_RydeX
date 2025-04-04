# #here if canceletion_charge their i want that detail from booking_invoice_histories:object ->actual->title cancellationPrice, then if title is tipPrice or surgePrice i want increse score also in booking_invoice_histories: object-> actual get distrance based on this also increse points


# from pymongo import MongoClient
# from dotenv import load_dotenv
# from datetime import datetime, timedelta
# import pandas as pd

# today = datetime.today().date()

# load_dotenv()

# client = MongoClient("mongodb+srv://read_access:g4WJ9ZstQzwsa3lm@hyzedeveloper.rfju1.mongodb.net/RydeX_history?retryWrites=true&w=majority")
# db = client["RydeX_history"]
# collection = db["booking_invoice_histories"]


# class UserScoring:
#     def calculate_performance_score(self, booking_invoice_histories):
#         """Calculate performance score based on user metrics"""
        
#         # Safely extract values using nested get() calls
#         actual = booking_invoice_histories.get("actual", {"distance": 0, "time": 0, "waitingTime": 0, "stopWaitingTime": 0, "directionPath": "", "isMinFareApplied": False, "charges": []})
        
#         charges = [charge for charge in actual.get("charges", []) if charge.get("title") in ["bookingFee", "distancePrice", "surgePrice", "cancellationPrice"]]
#         print(charges)

#         # Extract specific metrics
#         tipPrice = sum(charge.get("price", 0) for charge in charges if charge.get("title") == "tipPrice")
#         surgePrice = sum(charge.get("price", 0) for charge in charges if charge.get("title") == "surgePrice")
#         cancellationPrice = sum(charge.get("price", 0) for charge in charges if charge.get("title") == "cancellationPrice")
#         distance = actual.get("distance", 0)
#         promoDetails = booking_invoice_histories.get("promoDetails", 0) if booking_invoice_histories.get("id") else 0

#         # Avoid division by zero and set minimum values
#         max_values = {
#             "tipPrice": max(tipPrice, 1),
#             "cancelPaid": max(cancellationPrice, 1),
#             "promoDetails": max(promoDetails, 1),
#             "surgePrice": max(surgePrice, 1),
#             "distance": max(distance, 1)
#         }

#         # Calculate scores with adjusted weights and bonuses
#         scores = {
#             "tips_score": min((tipPrice / max_values["tipPrice"]) * self.performance_weights["tips_score"] * 100 * 
#                             (1.2 if tipPrice > 0 else 1), 20),  # 20% bonus for giving tips
            
#             "promo_score": min((promoDetails / max_values["promoDetails"]) * self.performance_weights["promo_score"] * 100, 40),
            
#             "surge_price_score": min((surgePrice / max_values["surgePrice"]) * self.performance_weights["surge_price_score"] * 100 * 
#                                     (1.1 if surgePrice > 0 else 1), 20),  # 10% bonus for surge pricing 


#             "canceleltion_paid_score": min((1 - cancellationPrice / max_values["cancelPaid"]) * self.performance_weights["canceleltion_paid_score"] * 100, 20),
#             "distrance_score": min((distance / max_values["distance"]) * self.performance_weights["distrance_score"] * 100, 20),
#         }

#         # return scores
#         print("Scores:")
#         for key, value in scores.items():
#                 print(f"{key}: {value}")

#         return sum(scores.values()), scores

#     def get_combined_category(self, score):
#             """Get performance category based on combined score"""
#             if score >= 80:
#                 return "Outstanding"
#             elif score >= 70:
#                 return "Excellent"
#             elif score >= 60:
#                 return "Very Good"
#             elif score >= 50:
#                 return "Good"
#             elif score >= 40:
#                 return "Average"
#             elif score >= 30:
#                 return "Below Average"
#             else:
#                 return "Needs Improvement"

#     #store this scores and complete def main() function and call the function
# def main():
#         # Get today's date in the correct timezone
#         today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
#         tomorrow = today.replace(day=today.day + 1)

#         # Query for ratings created today
#         ratings = list(collection.find({
#             "customerDetail": {"$exists": True},
#             "createdAt": {
#                 "$gte": today - timedelta(days=10),
#                 "$lt": tomorrow
#             }
#         }))

#         # Create a DataFrame from the MongoDB data
#         df = pd.DataFrame(ratings)

#         # Initialize the UserScoring class
#         user_scoring = UserScoring()

#         # Calculate the performance score for each user
#         if not df.empty:
#             df["performance_score"] = df.apply(lambda x: user_scoring.calculate_performance_score(x)[0], axis=1)

#         # Check if the column exists before trying to access it
#         if "performance_score" in df.columns:
#             # Get the combined category for each user
#             df["performance_category"] = df["performance_score"].apply(lambda x: user_scoring.get_combined_category(x))

#         # Save the results to a CSV file
#         df.to_csv("user_performance_scores.csv", index=False)

# if __name__ == "__main__":
#     main()



import pandas as pd
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
import tensorflow as tf
import os


# Load the .env file
load_dotenv()

# Connect to the MongoDB database
client = MongoClient("mongodb+srv://read_access:g4WJ9ZstQzwsa3lm@hyzedeveloper.rfju1.mongodb.net/RydeX_history?retryWrites=true&w=majority")
db = client["RydeX_history"]
collection = db["booking_invoice_histories"]

# Query the database for booking invoice histories
booking_invoice_histories = list(collection.find({}))

# Create a DataFrame from the MongoDB data
df = pd.DataFrame(booking_invoice_histories)

# check if there is any of this surgePrice or tipPrice or cancellationPrice in actual->charges->title

df["has_surge_price"] = df.apply(lambda x: any(charge["title"] == "surgePrice" for charge in x["actual"].get("charges", [])), axis=1)
df["has_tip_price"] = df.apply(lambda x: any(charge["title"] == "tipPrice" for charge in x["actual"].get("charges", [])), axis=1)
df["has_cancellation_price"] = df.apply(lambda x: any(charge["title"] == "cancellationPrice" for charge in x["actual"].get("charges", [])), axis=1)

print(df[["customerId","has_surge_price", "has_tip_price", "has_cancellation_price"]])

# add this score to user_daily_scores.csv
df.to_csv("user_daily_scores.csv", index=False)

# use neural network to do the calculation of has_surge_price or has_tip_price or has_cancellation_price is true and same user complete next trip then increase score of user

# Create a neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation="relu", input_shape=(3,)),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Train the model
df["has_next_trip"] = False
model.fit(df[["has_surge_price", "has_tip_price", "has_cancellation_price"]], df["has_next_trip"], epochs=10)

# Make predictions
predictions = model.predict(df[["has_surge_price", "has_tip_price", "has_cancellation_price"]])

# Increase score of user if has_surge_price or has_tip_price or has_cancellation_price is true and same user complete next trip
df["score"] = np.where(predictions > 0.5, 10, 0)

# Save the data
df.to_csv("user_daily_scores.csv", index=False)






# # Get the latest trip for each user
# latest_trips = df.groupby("customerId")["created_at"].max().reset_index()
# latest_trips = latest_trips.merge(df, on=["customerId", "created_at"], how="left")

# # Check if has_surge_price or has_tip_price or has_cancellation_price is true and same user complete next trip
# latest_trips["has_next_trip"] = latest_trips.groupby("customerId")["created_at"].shift(-1) > latest_trips["created_at"]

# # Increase score of user if has_surge_price or has_tip_price or has_cancellation_price is true and same user complete next trip
# latest_trips["score"] = np.where((latest_trips["has_surge_price"] | latest_trips["has_tip_price"] | latest_trips["has_cancellation_price"]) & latest_trips["has_next_trip"], 10, 0)

# # Save the data
# latest_trips.to_csv("user_daily_scores.csv", index=False)
















