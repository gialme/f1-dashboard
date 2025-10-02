import fastf1
import pandas as pd
from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from datetime import datetime
import os
import matplotlib

matplotlib.use('Agg')

def dashboard_view(render_request):
    """
    This view fetches last F1 race data and creates a graph
    """
    plot_url = None
    results_df = pd.DataFrame()
    error_message = None
    event_name = "Dashboard F1"

    try:
        # Enable cache in order to speed up data loading
        # Cache is stored in the project root
        cache_dir = './cache'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            
        fastf1.Cache.enable_cache(cache_dir)

        # Fetch last disputed race
        current_year = datetime.now().year
        schedule = fastf1.get_event_schedule(current_year, include_testing=False)
        # Convert to UTC timezone
        schedule['EventDate'] = pd.to_datetime(schedule['EventDate'], utc=True)
        
        # Filter past events using 'today', which also is timezone-aware
        today = pd.Timestamp.now(tz='UTC')
        past_events = schedule[schedule['EventDate'] < today]
        
        if not past_events.empty:
            latest_event = past_events.iloc[-1]
            event_name = f"{latest_event['EventName']} {current_year}"
            
            # Load race session
            session = fastf1.get_session(current_year, latest_event['RoundNumber'], 'R')
            session.load(laps=True, telemetry=True, weather=False)

            # Select columns from the result
            results = session.results
            if not results.empty:
                results_df = results[[
                    'Position', 'Abbreviation', 'TeamName', 
                    'Time', 'Status', 'Points'
                ]].copy()
                
                # Convert 'Position' values in integers
                results_df['Position'] = results_df['Position'].astype(int)

                # Format Timedelta values for better readability
                # from "0 days 01:34:56.789000" to "01:34:56.789000"
                results_df['Time'] = results_df['Time'].apply(
                    lambda t: str(t)[7:-3] if pd.notnull(t) else 'N/A'
                )
                # Rename columns for better readability
                results_df.rename(columns={
                    'Abbreviation': 'Driver',
                    'TeamName': 'Team'
                }, inplace=True)

            # --- Telemetry graph ---
            # Pick first 3 drivers and compare their fastest lap
            laps = session.laps
            top_3_drivers = results.head(3)['Abbreviation'].tolist()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_alpha(0.0)
            ax.set_facecolor('#1f2937') # Dark background
            
            # Pick 3 colors
            colors = ['#4F709C', '#F24C3D', '#A1C398']
            
            for i, driver in enumerate(top_3_drivers):
                fastest_lap = laps.pick_driver(driver).pick_fastest()
                if fastest_lap is not None and isinstance(fastest_lap, pd.Series):
                    telemetry = fastest_lap.get_car_data().add_distance()
                    if not telemetry.empty:
                        ax.plot(
                            telemetry['Distance'], 
                            telemetry['Speed'], 
                            label=driver,
                            color=colors[i]
                        )

            # Graph style
            ax.set_title(f"Fastest lap speed comparison - {session.event['EventName']}", color='white')
            ax.set_xlabel("Distance (m)", color='white')
            ax.set_ylabel("Speed (Km/h)", color='white')
            ax.legend()
            ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
            plt.xticks(rotation=45, color='white')
            plt.yticks(color='white')
            plt.tight_layout()

            # Convert graph to base64 image
            buf = io.BytesIO()
            fig.savefig(buf, format='png', transparent=True)
            buf.seek(0)
            string = base64.b64encode(buf.read())
            plot_url = urllib.parse.quote(string)
        else:
            error_message = "No events found for the current season."

    except Exception as e:
        error_message = f"Error while loading data: {e}"

    # Context to send to the template
    context = {
        'results': results_df.to_dict('records') if not results_df.empty else [],
        'plot_url': plot_url,
        'error_message': error_message,
        'event_name': event_name,
    }

    return render(render_request, 'dashboard/index.html', context)

