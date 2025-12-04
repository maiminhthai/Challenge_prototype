import csv
import random
from datetime import datetime, timedelta

def generate_random_time(base_hour, error_minutes=30):
    """Generates a time string HH:MM with a random error."""
    base_time = datetime(2000, 1, 1, base_hour, 0)
    # Random error between -error_minutes and error_minutes
    error = random.randint(-error_minutes, error_minutes)
    
    actual_time = base_time + timedelta(minutes=error)
    return actual_time.strftime("%H:%M")

def generate_random_trip(date_obj):
    """Generates a random trip sequence for a day."""
    locations = ["Mall", "Park", "Restaurant", "Friend's House", "Cinema", "Grocery Store", "Dry Cleaners"]
    num_trips = random.randint(1, 3)
    trips = []
    
    current_hour = random.randint(8, 18)
    current_loc = "Home"
    
    for _ in range(num_trips):
        dest = random.choice(locations)
        while dest == current_loc:
            dest = random.choice(locations)
            
        start_hour = current_hour
        duration = random.randint(1, 3)
        arrival_hour = start_hour + 1 # simplistic travel time
        
        # Format times
        start_time_str = f"{start_hour:02d}:{random.randint(0, 59):02d}"
        # Ensure arrival is after start
        arrival_time_str = f"{arrival_hour:02d}:{random.randint(0, 59):02d}"
        
        trips.append({
            "Date": date_obj.strftime("%Y-%m-%d"),
            "Day": date_obj.strftime("%A"),
            "Start Time": start_time_str,
            "Arrival Time": arrival_time_str,
            "Starting Location": current_loc,
            "Arrival Location": dest
        })
        
        current_loc = dest
        current_hour = arrival_hour + duration
        if current_hour >= 23:
            break
            
    # Return home
    if current_loc != "Home":
        start_hour = current_hour
        arrival_hour = start_hour + 1
        if arrival_hour > 23: arrival_hour = 23
        
        trips.append({
            "Date": date_obj.strftime("%Y-%m-%d"),
            "Day": date_obj.strftime("%A"),
            "Start Time": f"{start_hour:02d}:{random.randint(0, 59):02d}",
            "Arrival Time": f"{arrival_hour:02d}:{random.randint(0, 59):02d}",
            "Starting Location": current_loc,
            "Arrival Location": "Home"
        })
        
    return trips

def main():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 3, 31) # 3 months of data
    
    fieldnames = ["Date", "Day", "Start Time", "Arrival Time", "Starting Location", "Arrival Location"]
    rows = []
    
    current_date = start_date
    while current_date <= end_date:
        day_of_week = current_date.weekday() # 0=Mon, 6=Sun
        is_weekend = day_of_week >= 5
        
        daily_trips = []
        
        if not is_weekend:
            # Weekday
            if random.random() < 0.90:
                # Standard Routine
                # 1. Home (8:00) -> Work (9:00)
                t1_start = generate_random_time(8)
                t1_end = generate_random_time(9)
                daily_trips.append({
                    "Date": current_date.strftime("%Y-%m-%d"),
                    "Day": current_date.strftime("%A"),
                    "Start Time": t1_start,
                    "Arrival Time": t1_end,
                    "Starting Location": "Home",
                    "Arrival Location": "Work"
                })
                
                # 2. Work (17:00) -> Gym (18:00)
                t2_start = generate_random_time(17)
                t2_end = generate_random_time(18)
                daily_trips.append({
                    "Date": current_date.strftime("%Y-%m-%d"),
                    "Day": current_date.strftime("%A"),
                    "Start Time": t2_start,
                    "Arrival Time": t2_end,
                    "Starting Location": "Work",
                    "Arrival Location": "Gym"
                })
                
                # 3. Gym (19:00) -> Home (19:30)
                t3_start = generate_random_time(19)
                t3_end = generate_random_time(19, error_minutes=30) # 19:30 target, so base 19:30?
                # Prompt: "At 19 he goes... He arrives home at 19:30."
                # Let's use base 19 for start, base 19:30 for end.
                # My helper takes hour. I'll adjust manually.
                
                # Start 19:00 + 0-30m
                t3_s_dt = datetime(2000,1,1,19,0) + timedelta(minutes=random.randint(0,30))
                t3_start = t3_s_dt.strftime("%H:%M")
                
                # End 19:30 + 0-30m
                t3_e_dt = datetime(2000,1,1,19,30) + timedelta(minutes=random.randint(0,30))
                t3_end = t3_e_dt.strftime("%H:%M")
                
                daily_trips.append({
                    "Date": current_date.strftime("%Y-%m-%d"),
                    "Day": current_date.strftime("%A"),
                    "Start Time": t3_start,
                    "Arrival Time": t3_end,
                    "Starting Location": "Gym",
                    "Arrival Location": "Home"
                })
                
            else:
                # 10% Random
                daily_trips = generate_random_trip(current_date)
        else:
            # Weekend
            if random.random() < 0.5:
                # Go somewhere
                daily_trips = generate_random_trip(current_date)
            else:
                # Stay home (no trips)
                pass
                
        rows.extend(daily_trips)
        current_date += timedelta(days=1)
        
    # Write to CSV
    filename = "travel_log.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Successfully generated {filename} with {len(rows)} trips.")

if __name__ == "__main__":
    main()
