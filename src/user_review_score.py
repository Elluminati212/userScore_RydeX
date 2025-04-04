# import pymongo
# import csv
# import openai
# import os
# from datetime import datetime, timezone
# import pandas as pd
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Set up OpenAI API
# client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# # Connect to MongoDB
# mongo_uri = os.getenv('MONGO_URI')
# # mongo_client = pymongo.MongoClient(mongo_uri)
# mongo_client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=30000)
# db = mongo_client["RydeX_history"]
# ratings_collection = db['booking_histories']

# def analyze_review_sentiment(review_text):
#     """
#     Use OpenAI to analyze the sentiment of a review and user a score from 1-5
#     """
#     if not review_text or review_text.strip() == "":
#         return None
    
#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are an expert sentiment analyzer for driver reviews. Analyze the sentiment and return only a score from 1-5 where 1 is very negative and 5 is very positive."},
#                 {"role": "user", "content": f"Review: {review_text}. Score (1-5):"}
#             ],
#             temperature=0.3,
#             max_tokens=10
#         )
        
#         # Extract the score from response
#         score_text = response.choices[0].message.content.strip()
#         try:
#             # Try to extract just the number
#             score = int(score_text)
#             if 1 <= score <= 5:
#                 return score
#             else:
#                 return 3  # Default to neutral if outside range
#         except ValueError:
#             # If we can't get a clean integer, try to find the first number in the response
#             import re
#             match = re.search(r'\d', score_text)
#             if match and 1 <= int(match.group()) <= 5:
#                 return int(match.group())
#             return 3  # Default to neutral if parsing fails
            
#     except Exception as e:
#         print(f"Error analyzing review: {e}")
#         return None

# def get_todays_user_ratings():
#     """
#     Fetch only today's users ratings from MongoDB
#     """
#     # Get today's date in the correct timezone
#     today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
#     tomorrow = today.replace(day=today.day + 1)
    
#     # Query for ratings created today
#     ratings = list(ratings_collection.find({
#         "customerDetail": {"$exists": True}, #customerDetail
#         "createdAt": {
#             "$gte": today,
#             "$lt": tomorrow
#         }
#     }))
    
#     return ratings

# def process_ratings():
#     """
#     Process today's ratings, analyze reviews, and prepare data for CSV export
#     """
#     todays_ratings = get_todays_user_ratings()
#     results = []
    
#     for rating in todays_ratings:
#         # Extract driver ID
#         user_id = rating.get('customerDetail', {}).get('id')
#         if not user_id:
#             continue

#         # Extract rating and review
#         driver_rate = rating.get('driverRate')
#         driver_review = rating.get('driverReview', '')
#         created_at = rating.get('createdAt')
        
#         # Extract rating and review
#         user_rate = rating.get('userRate')
#         user_review = rating.get('userReview', '')
#         created_at = rating.get('createdAt')
        
#         # Get timestamp in readable format
#         if created_at:
#             if isinstance(created_at, str):
#                 try:
#                     created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
#                 except:
#                     try:
#                         created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%f%z")
#                     except:
#                         created_at = None
#             created_at_str = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "Unknown"
#         else:
#             created_at_str = "Unknown"
        
#         # Use OpenAI to analyze the review
#         review_score = analyze_review_sentiment(user_review) if user_review else None

#         # Add to results
#         results.append({
#             'user_id': user_id,
#             'driver_rating': driver_rate,
#             'sentiment_score': review_score,
#             'review_text': driver_review,
#             'created_at': created_at_str
#         })
    
#     return results

# def export_to_csv(data, filename="user_ratings_analysis.csv"):
#     """
#     Export the processed data to a CSV file
#     """
#     # Define CSV headers
#     headers = ['user_id', 'driver_rating', 'sentiment_score', 'review_text', 'created_at']
    
#     # Write to CSV
#     with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=headers)
#         writer.writeheader()
#         writer.writerows(data)
    
#     print(f"Today's data exported to {filename}")
    
# def main():
#     today_date = datetime.now().strftime("%Y-%m-%d")
#     print(f"Starting user rating analysis for today ({today_date})...")
    
#     results = process_ratings()
#     if not results:
#         print("No user ratings found for today.")
#         return
    
#     print(f"Processed {len(results)} ratings from today.")
#     export_to_csv(results)

# if __name__ == "__main__":
#     main()








from datetime import datetime
import pymongo
import openai
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

# Connect to MongoDB
mongo_uri = os.getenv('MONGO_URI')
client = pymongo.MongoClient(mongo_uri)
db = client["RydeX_history"]
ratings_collection = db['booking_histories']

# Fetch all user reviews and ratings from MongoDB
def get_driver_reviews_and_ratings():
    """
    Fetch all driver reviews and ratings from MongoDB.
    """
    pipeline = [
        # {
        #     '$unwind': {
        #         'path': '$rating',
        #         'preserveNullAndEmptyArrays': True  # Keep records even if rating is missing
        #     }
        # },
        {
            '$project': {
                'driverReview': '$rating.driverReview',
                'driverRate': '$rating.driverRate',
                'customerId': 1,
            }
        },
        # {
        #     "$match": {
        #         "date": datetime.now().strftime("%Y-%m-%d")
        #     }
        # }
    ]

    data = list(ratings_collection.aggregate(pipeline))

    if not data:
        print("No driver reviews found.")
        return []

    print(f"Fetched {len(data)} reviews.")
    return data

# Store reviews in DataFrame
def store_reviews_in_dataframe():
    """
    Store user reviews and ratings in a DataFrame and process the data.
    """
    reviews_data = get_driver_reviews_and_ratings()

    if not reviews_data:
        print("No data available to process.")
        return pd.DataFrame()  # Return empty DataFrame to prevent crashes

    df = pd.DataFrame(reviews_data)

    if 'driverRate' not in df:
        df['driverRate'] = None  # Add a placeholder column if missing

    # Calculate average rating safely
    average_rating = df['driverRate'].mean() if not df.empty else 0
    print(f"Average driver Rating: {average_rating:.2f}")

    return df

# Sentiment Analysis using OpenAI
def analyze_sentiment(df):
    """
    Analyze sentiment of user reviews using OpenAI.
    """
    if df.empty or 'driverReview' not in df:
        print("No reviews to analyze.")
        return df

    sentiment_scores = []

    for _, row in df.iterrows():
        driver_review = row['driverReview']
        if not driver_review or not isinstance(driver_review, str):
            sentiment_scores.append(None)  # Handle missing reviews
            continue

        prompt = f"""
        Analyze the following review and rate it on a scale of 0 to 5, where:
        0 = Extremely negative
        1 = Very negative
        2 = Somewhat negative
        3 = Neutral/Mixed
        4 = Positive
        5 = Very positive
        Provide only the numerical score.
        Review: {driver_review}
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a expert driver review analyzer for user. Respond only with a number between 0 and 5."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            score = float(response.choices[0].message.content.strip())
            sentiment_scores.append(max(0, min(5, score)))
        except Exception as e:
            print(f"Error calculating review score: {str(e)}")
            sentiment_scores.append(None)

    df['sentiment_score'] = sentiment_scores
    return df

# Export to CSV
def export_to_csv(df, filename="user_reviews_score.csv"):
    """
    Export the DataFrame to a CSV file.
    """
    if df.empty:
        print("No data to export.")
        return

    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")

# Execute functions
df_reviews = store_reviews_in_dataframe()
df_reviews = analyze_sentiment(df_reviews)
export_to_csv(df_reviews)
