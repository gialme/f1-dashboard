import fastf1
from fastf1.ergast import Ergast
import pandas as pd
from django.shortcuts import render
from datetime import datetime
import os

# Helper functions that enables fastf1 cache
def setup_fastf1_cache():
    """Enables fastf1 cache in the directory: './cache'"""
    cache_dir = './cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    if not fastf1.Cache.is_enabled():
        fastf1.Cache.enable_cache(cache_dir)

def dashboard_view(render_request):
    """
    This view fetches last F1 race data and creates a graph
    """
    setup_fastf1_cache()
    context = {
        'next_race': None,
        'driver_standings': [],
        'constructor_standings': [],
        'error_message': None,
    }
    try:
        # Fetch next race
        current_year = datetime.now().year
        schedule = fastf1.get_event_schedule(current_year, include_testing=False)
        # Convert to UTC timezone
        schedule['EventDate'] = pd.to_datetime(schedule['EventDate'], utc=True)
        
        # Filter past events using 'today', which also is timezone-aware
        today = pd.Timestamp.now(tz='UTC')
        future_events = schedule[schedule['EventDate'] > today].sort_values(by='EventDate')
        
        if not future_events.empty:
            next_race_info = future_events.iloc[0]
            race_date_utc = next_race_info['EventDate']

            # Format the date for the countdown
            context['next_race'] = {
                'name': next_race_info['EventName'],
                'location': next_race_info['Location'],
                'country': next_race_info['Country'],
                'race_date_str': race_date_utc.strftime('%d %B %Y %H:%M UTC'),
                'race_date_iso': race_date_utc.isoformat(),
            }
        else:
            # Season ended
            context['next_race'] = {
                'name': 'Season ended',
                'location': 'No race :(',
                'race_date_iso': None,
            }

        ergast = Ergast()
        # Load driver standings
        driver_standings_response = ergast.get_driver_standings(season=current_year)
        if driver_standings_response and driver_standings_response.content:
            df_drivers = driver_standings_response.content[0]
            # Driver full name
            df_drivers['driver'] = df_drivers['givenName'] + ' ' + df_drivers['familyName']
            # Pick latest constructor
            df_drivers['constructor'] = df_drivers['constructorNames'].str[-1]
            # Cast points to int
            df_drivers['points'] = pd.to_numeric(df_drivers['points']).astype(int)
            # Select useful columns
            context['driver_standings'] = df_drivers[['position', 'driver', 'constructor', 'points']].to_dict('records')

        # Load constructors standings
        constructor_standings_response = ergast.get_constructor_standings(season=current_year)
        if constructor_standings_response and constructor_standings_response.content:
            df_constructors = constructor_standings_response.content[0]
            df_constructors.rename(columns={'constructorName': 'constructor'}, inplace=True)
            df_constructors['points'] = pd.to_numeric(df_constructors['points']).astype(int)
            context['constructor_standings'] = df_constructors[['position', 'constructor', 'points']].to_dict('records')

    except Exception as e:
        context['error_message'] = f"Error while loading data: {e}"

    return render(render_request, 'dashboard/index.html', context)

