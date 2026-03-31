"""
🏏 CRICKET DATA FETCHER - Real Live Match Data
Fetches real cricket data from free APIs
No authentication needed!
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import sqlite3
from cachetools import TTLCache
import os

class CricketDataFetcher:
    """Fetch real cricket data from free APIs"""
    
    def __init__(self):
        # Real API endpoints (Free)
        self.apis = {
            'cricketapi': 'https://api.cricketapi.dev/matches',
            'esportapi': 'https://api.esportapi.in/matches',
            'rapidapi': 'https://cricketapi.p.rapidapi.com/matches'
        }
        
        # Cache to store data (5 minute TTL)
        self.cache = TTLCache(maxsize=100, ttl=300)
        self.db_path = 'cricket_data.db'
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for offline support"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Matches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id TEXT PRIMARY KEY,
                team1 TEXT,
                team2 TEXT,
                venue TEXT,
                date TEXT,
                format TEXT,
                status TEXT,
                score_team1 INTEGER,
                score_team2 INTEGER,
                wickets_team1 INTEGER,
                wickets_team2 INTEGER,
                overs_completed REAL,
                live_data TEXT,
                prediction_team1 REAL,
                prediction_team2 REAL,
                created_at TIMESTAMP
            )
        ''')
        
        # Players table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id TEXT PRIMARY KEY,
                name TEXT,
                team TEXT,
                role TEXT,
                batting_avg REAL,
                bowling_avg REAL,
                recent_form REAL,
                ipl_points INTEGER,
                market_price REAL
            )
        ''')
        
        # News table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                image_url TEXT,
                source TEXT,
                published_at TIMESTAMP,
                match_id TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_live_matches(self):
        """Get real live matches"""
        try:
            # Try primary API first
            response = requests.get(
                'https://api.cricketapi.dev/matches',
                timeout=5
            )
            
            if response.status_code == 200:
                matches = response.json()
                
                # Format the data
                formatted_matches = []
                for match in matches.get('data', [])[:10]:  # Get top 10
                    formatted_matches.append({
                        'id': match.get('id'),
                        'team1': match.get('team1', {}).get('name'),
                        'team2': match.get('team2', {}).get('name'),
                        'venue': match.get('venue', 'TBA'),
                        'format': match.get('format', 'T20'),
                        'status': match.get('status', 'scheduled'),
                        'date': match.get('date'),
                        'score_team1': match.get('score', {}).get('team1', 0),
                        'score_team2': match.get('score', {}).get('team2', 0),
                    })
                
                return formatted_matches
        except Exception as e:
            print(f"⚠️ API Error: {e}")
        
        # Fallback: Return cached data
        return self.get_cached_matches()
    
    def get_match_details(self, match_id):
        """Get detailed match information"""
        try:
            response = requests.get(
                f'https://api.cricketapi.dev/matches/{match_id}',
                timeout=5
            )
            
            if response.status_code == 200:
                match = response.json()
                
                return {
                    'id': match.get('id'),
                    'team1': match.get('team1', {}).get('name'),
                    'team2': match.get('team2', {}).get('name'),
                    'venue': match.get('venue'),
                    'date': match.get('date'),
                    'format': match.get('format'),
                    'status': match.get('status'),
                    'commentary': match.get('commentary', []),
                    'scorecard': match.get('scorecard'),
                    'squad_team1': match.get('team1', {}).get('squad', []),
                    'squad_team2': match.get('team2', {}).get('squad', []),
                }
        except Exception as e:
            print(f"Error fetching match details: {e}")
        
        return None
    
    def get_players(self, team_id=None):
        """Get player data"""
        try:
            response = requests.get(
                'https://api.cricketapi.dev/players',
                timeout=5
            )
            
            if response.status_code == 200:
                players = response.json().get('data', [])
                
                if team_id:
                    players = [p for p in players if p.get('team_id') == team_id]
                
                formatted_players = []
                for player in players[:30]:
                    formatted_players.append({
                        'id': player.get('id'),
                        'name': player.get('name'),
                        'team': player.get('team'),
                        'role': player.get('role'),
                        'batting_avg': player.get('stats', {}).get('batting_avg', 0),
                        'bowling_avg': player.get('stats', {}).get('bowling_avg', 0),
                        'recent_form': player.get('recent_form', 0.5),
                        'image_url': player.get('image_url'),
                        'jersey_no': player.get('jersey_no'),
                        'price': player.get('market_price', 100),
                    })
                
                return formatted_players
        except Exception as e:
            print(f"Error fetching players: {e}")
        
        return self.get_cached_players()
    
    def get_cricket_news(self):
        """Get cricket news from free sources"""
        try:
            # Try ESPN Cricket News RSS
            response = requests.get(
                'https://www.espncricinfo.com/feeds/site/recent_news',
                timeout=5,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if response.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                
                news_items = []
                for item in root.findall('item')[:10]:
                    title = item.find('title')
                    desc = item.find('description')
                    pub_date = item.find('pubDate')
                    
                    if title is not None:
                        news_items.append({
                            'id': title.text[:50].replace(' ', '_'),
                            'title': title.text,
                            'description': desc.text if desc is not None else '',
                            'published_at': pub_date.text if pub_date is not None else '',
                            'source': 'ESPN Cricinfo'
                        })
                
                return news_items
        except Exception as e:
            print(f"Error fetching news: {e}")
        
        return []
    
    def get_cached_matches(self):
        """Get matches from local database (offline support)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM matches 
                ORDER BY date DESC 
                LIMIT 10
            ''')
            
            matches = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': m[0],
                    'team1': m[1],
                    'team2': m[2],
                    'venue': m[3],
                    'date': m[4],
                    'format': m[5],
                    'status': m[6],
                    'score_team1': m[7],
                    'score_team2': m[8],
                }
                for m in matches
            ]
        except Exception as e:
            print(f"Error getting cached data: {e}")
            return []
    
    def get_cached_players(self):
        """Get players from cache (offline support)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM players LIMIT 50')
            players = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': p[0],
                    'name': p[1],
                    'team': p[2],
                    'role': p[3],
                    'batting_avg': p[4],
                    'bowling_avg': p[5],
                    'recent_form': p[6],
                    'ipl_points': p[7],
                    'price': p[8],
                }
                for p in players
            ]
        except Exception as e:
            print(f"Error getting cached players: {e}")
            return []
    
    def cache_match_data(self, match_id, match_data):
        """Cache match data locally for offline use"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO matches 
                (id, team1, team2, venue, date, format, status, score_team1, score_team2, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                match_id,
                match_data.get('team1'),
                match_data.get('team2'),
                match_data.get('venue'),
                match_data.get('date'),
                match_data.get('format'),
                match_data.get('status'),
                match_data.get('score_team1', 0),
                match_data.get('score_team2', 0),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            print(f"✅ Cached match: {match_id}")
        except Exception as e:
            print(f"Error caching data: {e}")
    
    def sync_data(self):
        """Sync all data for offline use"""
        print("🔄 Syncing cricket data...")
        
        # Fetch and cache matches
        matches = self.get_live_matches()
        for match in matches:
            self.cache_match_data(match['id'], match)
        
        # Fetch and cache players
        players = self.get_players()
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for player in players:
                cursor.execute('''
                    INSERT OR REPLACE INTO players
                    (id, name, team, role, batting_avg, bowling_avg, recent_form, market_price)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    player.get('id'),
                    player.get('name'),
                    player.get('team'),
                    player.get('role'),
                    player.get('batting_avg'),
                    player.get('bowling_avg'),
                    player.get('recent_form'),
                    player.get('price')
                ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error caching players: {e}")
        
        print("✅ Sync complete!")

# Test the fetcher
if __name__ == "__main__":
    fetcher = CricketDataFetcher()
    
    print("🏏 Cricket Data Fetcher\n")
    
    print("📊 Live Matches:")
    matches = fetcher.get_live_matches()
    for match in matches[:5]:
        print(f"  {match['team1']} vs {match['team2']} - {match['status']}")
    
    print("\n🏆 Players:")
    players = fetcher.get_players()
    for player in players[:5]:
        print(f"  {player['name']} ({player['team']}) - {player['role']}")
    
    print("\n📰 Cricket News:")
    news = fetcher.get_cricket_news()
    for article in news[:3]:
        print(f"  {article['title'][:60]}...")
    
    print("\n💾 Syncing data for offline...")
    fetcher.sync_data()
