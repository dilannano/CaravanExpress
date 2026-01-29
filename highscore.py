import json
import os
import getpass

class HighScoreManager:
    def __init__(self, filename="highscores.json"):
        # Get the current user's username to create separate score files
        try:
            username = getpass.getuser()
        except:
            username = "player"
        
        # Create a user-specific high score file
        self.filename = f"highscores_{username}.json"
        self.high_scores = self.load_scores()
    
    def load_scores(self):
        """Load high scores from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_scores(self):
        """Save high scores to file"""
        with open(self.filename, 'w') as f:
            json.dump(self.high_scores, f, indent=2)
    
    def add_score(self, score, distance):
        """Add a new score and return if it's a high score"""
        entry = {
            'score': score,
            'distance': distance
        }
        self.high_scores.append(entry)
        # Sort by score (descending)
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        # Keep only top 5
        self.high_scores = self.high_scores[:5]
        self.save_scores()
        
        # Return True if this score made it to top 5
        return entry in self.high_scores
    
    def get_top_scores(self, count=5):
        """Get top N scores"""
        return self.high_scores[:count]
    
    def is_high_score(self, score):
        """Check if a score would make it to the high score list"""
        if len(self.high_scores) < 5:
            return True
        return score > self.high_scores[-1]['score']
    
    def clear_scores(self):
        """Clear all high scores (reset)"""
        self.high_scores = []
        self.save_scores()
    
    def get_username(self):
        """Get the current username for display"""
        try:
            return getpass.getuser()
        except:
            return "Player"
