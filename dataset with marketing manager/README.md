# challenge-dataset
This dataset contains JSON files describing synthetic driver profiles, calendar events, historical EV telemetry, and realistic trip simulations generated for the ENT-icipate proactive in-car assistant.

The dataset is designed to model driver behavior, daily habits, vehicle energy consumption, and route-specific patterns, similarly to how SUMO-based EV datasets represent simulated trips and influencing factors.

The dataset includes the following files:

-calendar_events_fake.json

-drivers_dataset.json

-historical_trips_full.json

-trips_final_realistic.json

Executing the notebooks you will obtain 2 new files:

-drivers_with_style.json (generated via kmeans)

-drivers_with_style_and_habits.json (enriched with calendar dataset)

# 1. calendar_events_fake.json

Contains synthetic calendar events for each driver 2 weeks-based. These events model weekly routines such as work shifts, hobbies, leisure activities, charging stops, or sports sessions.
Each entry represents one event:

-event_id: unique event identifier

-driver_id: ID linking the event to a driver

-title: human-readable event description

-category: event type (work, leisure, hobby, charging, health, etc.)

-start_time / end_time: timestamps in ISO 8601 format

-location_name: location name

-location.lat / location.lon: location coordinates

# 2. drivers_dataset.json
   
Stores driver profiles focused on preferences (music, drinks, hobbies), as well as known favorite places in their routine.
For each driver:

-driver_id: unique driver identifier

-preferences that include favourite music type, hobbies and also favourite places

For the driverID=7 there is also a role field (marketing manager) that is our case study

# 3. historical_trips_full.json
Contains detailed EV telemetry logs representing historical driving data.
The dataset includes second-by-second vehicle states such as speed, acceleration, battery percentage, simulated battery usage, and inferred energy metrics.
It include:

-trip_id: Unique identifier of the trip.

-driver_id: Driver identifier

-a list of telemetry data

Regarding telemetry data:

-timestamp: in the format: YYYY-MM-DDTHH:MM:SS, e.g. "2025-11-26T08:03:00".

-location: Vehicle GPS position at this time step in lat and long

-speed_kmh

-acceleration_mps2 (in m/s²).
Positive values: accelerating
Negative values: decelerating
Near zero: cruising

-braking (boolean): Indicates whether the vehicle is actively braking in this time step.
This is derived from the acceleration profile and can be used to detect aggressive vs smooth driving behavior.

-road_type, like city or highway

-battery_level_%: Real (or ground-truth) state of charge (SoC) of the battery in percent at this time step.

-distance_to_destination_km: Remaining distance to the (scenario) destination in kilometers.
This value decreases along the trip and can be used to model:
range anxiety
whether the current SoC is sufficient to complete the trip
whether an intermediate charging stop might be needed

-battery_level_sim_% (not important)

-energy_consumption_kWh: Energy consumed during this time step in kWh.
For the first telemetry record of a trip, this value is usually null (no previous step to compare).
For subsequent records, it represents the energy used between the previous timestamp and the current one.

-energy_consumption_Wh_per_km: Step-level energy consumption normalized per distance in Wh/km.
It indicates how efficient the vehicle was during this segment and is compatible with typical EV consumption metrics.
null for the first sample (or whenever the segment distance is undefined).
For later steps, it is computed based on the energy consumed and the distance covered between consecutive telemetry points.

# 4. trips_final_realistic.json
Contains complete realistic scenario trips (e.g., Turin → Piacenza), each with a full stream of telemetry.
These trips simulate real-world usage conditions and serve as evaluation scenarios for the proactive assistant.
For each trip:

-trip_id

-driver_id

-start_location

-destination

-estimated_distance_km

-telemetry: identical structure to historical_trips_full.json
This can be used as test dataset to test the multiagent system

There will be create 2 new datasets:

# 5. drivers_with_style.json
This file extends the baseline driver profiles by adding driving_style (eco, normal, aggressive) and baseline_whkm (baseline energy consumption).
These values were generated using:

K-Means clustering on historical trip features (using k=3)

Features such as: acceleration patterns, speed variance, braking frequency, Wh/km averages

# 6. drivers_with_style_and_habits.json
It populate the previous dataset with habits, using calendar_events_fake.json file
Each driver may contain:

-recurring_events: inferred habitual events

-day_of_week

-time_range

-category (work, hobby, health, leisure…)

-location_name

-coordinates of the location

-occurrences: count of repeated events used for habit confidence (only stored events with occurances>2)
