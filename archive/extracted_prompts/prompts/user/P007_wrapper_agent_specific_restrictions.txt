SOURCE: Improving Testing Prompt.pdf, Pages 16-20
TYPE: User Prompt (VERBATIM EXTRACT)
================================================================================

I want you to build be an agent for this task only prompt as a wrapper for this to give them speciﬁc 
restriction or roles like we did for the previous agents
# Role & Goal
You are an expert Java Spring Boot and PostGIS developer. We are upgrading the "ZonePilot" 
backend from a passive location logger to a stateful, predictive ﬂeet routing engine.
# Context & Architectural Decisions
We use pgRouting (pgr_dijkstra) on an OSM-derived table (blr_2po_4pgr) for Bangalore. 
* **Routing Cost:** We will use pre-calculated time (cost_time_sec) rather than distance.
* **API Timing:** Google Routes API integration for predictive time calculation will be 
Synchronous during route generation.
* **Deviation Logic:** We must distinguish between temporary GPS glitches and actual wrong 
turns before recalculating.
* **Curfew Optimization:** If avoiding a curfew makes the route slower than just waiting out the 
curfew, we assign the original route with a "Wait State".
# Implementation Tasks
Please implement the following epics sequentially. Ask for clariﬁcation if any PostGIS queries or 
Spring Data architectures are ambiguous.
## Epic 1: Pre-calculated Time-Based Routing Proﬁle
Update the pgRouting logic to favor *faster* routes, not just shorter ones.
1. Create a Flyway migration to add a cost_time_sec column to blr_2po_4pgr.
2. Write a SQL script in the migration to populate this column: calculate travel time based on OSM 
maxspeed tags. If maxspeed is missing, apply fallback speeds based on the highway tag (e.g., 
primary=60, residential=30).
3. Update RoadNetworkRepository.java so pgr_dijkstra uses cost_time_sec as the edge weight 
instead of length_m.
## Epic 2: Smarter Map-Snapped Simulation (With Glitches & Wrong Turns)
Replace hardcoded straight-line simulation paths with dynamic, pgRouting-backed paths.
1. Update SimulationService to generate a route between two random coordinate points within the 
Bangalore bounding box.
================================================================================
PAGE 17
================================================================================
2. Use PostGIS ST_LineInterpolatePoint and ST_LineMerge to generate highly accurate simulation 
ticks (waypoints) directly on the road geometry.
3. Implement a dual "Deviation Injector" during the tick loop:
   * **GPS Glitch (10% chance):** Temporarily jump the coordinate 50m away and ﬂip the azimuth, 
but snap back to the correct path on the next tick.
   * **Wrong Turn (5% chance):** Pathﬁnd down the wrong OSM edge for 3-4 consecutive ticks to 
trigger a legitimate oﬀ-route event.
## Epic 3: Stateful Journey & GPS Glitch Tolerance
Vehicles must know their active route and tolerate bad telemetry without aggressively rerouting.
1. Add active_dispatch_route_id to the vehicle table.
2. In PositionTrackingService, calculate ST_Distance between the GPS point and the active route's 
geometry.
3. **Map-Matching Logic:** If the vehicle is close to the route (< 30m) but the GPS heading is 
backwards, assume it's a GPS glitch and snap it to the route's forward trajectory. 
4. **Reroute Trigger:** Only trigger BreachService.computeReroute() if the vehicle is strictly oﬀ-
route (> 50m deviation) for **two consecutive position pings** (to ﬁlter out the temporary GPS 
glitches).
## Epic 4: Predictive Compliance & Wait-Time Optimization (Google Routes API)
Implement synchronous, forward-looking compliance when the user requests a route.
1. Integrate the Google Routes API (computeRoutes endpoint) as a new TimePredictionService.
2. Post-pgRouting, prune the geometry to a max of 25 waypoints (Start + End + Zone Entry Points + 
Major Intersections). 
3. Call Google Routes API synchronously. Set via: true on intermediate points and 
routingPreference to TRAFFIC_AWARE.
4. Parse the leg durations to predict exact arrival times at restricted zones. 
5. **Curfew Logic:** If a zone curfew is hit, calculate an alternative route avoiding the zone. 
6. **Wait State Comparison:** Compare Duration(Alternate_Route) against 
Duration(Original_Route) + Wait_Time_Until_Curfew_Ends. If the alternate route takes longer than 
waiting, return the Original Route but ﬂag it with a required Wait Time instruction.
# Output Instructions
Start with Epic 1. Provide the exact Flyway SQL migration script and the updated 
RoadNetworkRepository.java code.