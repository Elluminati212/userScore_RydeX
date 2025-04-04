# I have multiple db in mongodb and i want to use the same code to get the data from different db.
# Use the db name RydeX and RydeX_history and also use the collection name booking_histories"] from RydeX and booking_histories from RydeX_history db




from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

today = datetime.today().date()

load_dotenv()

client = MongoClient("mongodb+srv://read_access:g4WJ9ZstQzwsa3lm@hyzedeveloper.rfju1.mongodb.net/RydeX_history?retryWrites=true&w=majority")
db = client["RydeX"]
collection = db["customers"]

class UserScoring:
    def __init__(self, df_users):
        self.df_users = df_users
        self.db = client["RydeX"]
        self.performance_weights = {
            "acceptance_score": 0.2,
            "credit_score": 0.4,
            "distrance_score": 0.2,
            "canceleltion_score": 0.2,
        }

    
    def calculate_performance_score(self ,booking_histories):
        """Calculate performance score based on user metrics"""
   
        # Get values with proper defaults
        accepted = ["booking_histories"].get("accepted", 0)
        credit = ["booking_histories"].get("credit", 0)
        distance = ["booking_histories"].get("distance", 0)
        cancelled = ["booking_histories"].get("cancelled", 0)
        
        # Avoid division by zero
        max_accepted = max(accepted, 1)
        max_cancelled = max(cancelled, 1)
        max_credit = max(credit, 1)
        max_distance = max(distance, 1)

        # Maximum values for normalization
        max_values = {
            "accepted": max_accepted,
            "rejected": max_cancelled,
            "credit": max_credit,
            "distance": max_distance,
        }
        
        # Calculate scores with bounds
        scores = {
            "acceptance_score": min((accepted / max_values["accepted"]) * self.performance_weights["acceptance_score"] * 100, 20),
            "credit_score": min((credit / max_values["credit"]) * self.performance_weights["credit_score"] * 100, 40),
            "distance_score": min((distance / max_values["distance"]) * self.performance_weights["distance_score"] * 100, 20),
            "cancellation_score": min((1 - cancelled / max_values["rejected"]) * self.performance_weights["cancellation_score"] * 100, 20),
        }  
        
        return sum(scores.values()), scores
    
    def get_combined_category(self, score):
        """Get performance category based on combined score"""
        if score >= 80:
            return "Outstanding"
        elif score >= 70:
            return "Excellent"
        elif score >= 60:
            return "Very Good"
        elif score >= 50:
            return "Good"
        elif score >= 40:
            return "Average"
        elif score >= 30:
            return "Below Average"
        else:
            return "Needs Improvement"
        
    def calculate_scores(self):
        """Calculate scores for all users"""
        scores = []

        # Group by userId to get aggregated metrics per user
        grouped = self.df_users.groupby('userId')
        total_users = len(grouped)

        for idx, (user_id, group) in enumerate(grouped, 1):
            print(f"Processing users {idx}/{total_users}: {user_id}")

            # Aggregate metrics for this user
            user_analytics = {
                'userId': user_id,
                'credit': group['credit'].sum() if 'credit' in group.columns else 0,
                'distance': group['distance'].sum() if 'distance' in group.columns else 0,
                'bookingStates': {
                    'accepted': group['bookingStates.accepted'].sum() if 'bookingStates.accepted' in group.columns else 0,
                    'completed': group['bookingStates.completed'].sum() if 'bookingStates.completed' in group.columns else 0,
                    'rejected': group['bookingStates.rejected'].sum() if 'bookingStates.rejected' in group.columns else 0,
                    'cancelled': group['bookingStates.cancelled'].sum() if 'bookingStates.cancelled' in group.columns else 0,
                    'notAnswered': group['bookingStates.notAnswered'].sum() if 'bookingStates.notAnswered' in group.columns else 0,
                }
            }

            performance_score, detailed_scores = self.calculate_performance_score(user_analytics)
            scores.append({
                "userId": user_id,
                "category": self.get_combined_category(performance_score),
                "overall_score": round(performance_score, 2),
                **detailed_scores
            })

        return scores
def main(df_users):
    if len(df_users) == 0:
        print("No data available for today")
        return
    
    # Flatten nested bookingStates for better DataFrame handling
    if 'bookingStates' in df_users.columns:
        for state in ['accepted', 'completed', 'rejected', 'cancelled', 'notAnswered']:
            df_users[f'bookingStates.{state}'] = df_users['bookingStates'].apply(
                lambda x: x.get(state, 0) if isinstance(x, dict) else 0
            )
    
    # Initialize userScoring with the dataframe
    user_scoring = UserScoring(df_users)
    
    # Calculate scores for all users
    scores = user_scoring.calculate_scores()
    
    if not scores:
        print("No scores calculated")
        return
    
    # Print the scores
    print("Calculated Scores:")
    for score in scores:
        print(score)

    # Save the calculated scores to a CSV file
    try:
        output_filename = f"user_daily_scores.csv"
        pd.DataFrame(scores).to_csv(output_filename, index=False)
        print(f"Successfully saved scores to {output_filename}")
        return True
    except Exception as e:
        print(f"Error saving to CSV: {str(e)}")
        return False

if __name__ == "__main__":
    main(pd.DataFrame())
