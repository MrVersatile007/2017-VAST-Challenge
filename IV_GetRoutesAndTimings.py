import csv
import pandas
import datetime


# CSV Input and output paths. Change these.
IN_CSV_PATH = "C:\\Users\\ryan_\\OneDrive\\Documents\\School\\Information Visualization\\Final Project\\" \
              "2017MC1Data\\Lekagul Sensor Data.csv"
OUT_CSV_PATH = "C:\\Users\\ryan_\\OneDrive\\Documents\\School\\Information Visualization\\Final Project\\" \
               "2017MC1Data\\Lekagul Sensor Routes.csv"


def main():
    # Read in data
    df = pandas.read_csv(IN_CSV_PATH)

    # Find delta time and time spent in park
    cars_in_park = {}
    delta_time = {}

    # Find routes
    route_idx = {}
    current_route_idx = 0
    route_step = {}

    df["time-in-park"] = ""
    df["delta-time"] = ""
    df["route-idx"] = ""
    df["route-step"] = ""

    for index, row in df.iterrows():
        if row["car-id"] not in cars_in_park.keys():
            current_time = datetime.datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
            cars_in_park[row["car-id"]] = current_time
            row["time-in-park"] = (current_time - current_time).total_seconds()

            route_idx[row["car-id"]] = current_route_idx
            route_step[route_idx[row["car-id"]]] = 0

            row["route-idx"] = route_idx[row["car-id"]]
            row["route-step"] = route_step[route_idx[row["car-id"]]]

            route_step[route_idx[row["car-id"]]] += 1
            current_route_idx += 1

        # Consider the end of a route when the vehicle hits an entrance or the ranger base
        elif (row["gate-name"][:-1] != "entrance") and (row["gate-name"] != "ranger-base"):
            current_time = datetime.datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
            row["time-in-park"] = (current_time - cars_in_park[row["car-id"]]).total_seconds()

            row["route-idx"] = route_idx[row["car-id"]]
            row["route-step"] = route_step[route_idx[row["car-id"]]]

            route_step[route_idx[row["car-id"]]] += 1

        else:
            current_time = datetime.datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
            row["time-in-park"] = (current_time - cars_in_park[row["car-id"]]).total_seconds()
            cars_in_park.pop(row["car-id"])

            row["route-idx"] = route_idx[row["car-id"]]
            row["route-step"] = route_step[route_idx[row["car-id"]]]

            route_step.pop(route_idx[row["car-id"]])
            route_idx.pop(row["car-id"])

        # Compute delta time
        if row["car-id"] not in delta_time.keys():
            current_time = datetime.datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
            delta_time[row["car-id"]] = current_time
            row["delta-time"] = (current_time - current_time).total_seconds()
        else:
            current_time = datetime.datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
            row["delta-time"] = (current_time - delta_time[row["car-id"]]).total_seconds()
            delta_time[row["car-id"]] = current_time

    # Drill down to unique routes
    routes = {}
    for index, row in df.iterrows():
        if row["route-idx"] not in routes.keys():
            routes[row["route-idx"]] = []
        routes[row["route-idx"]].append(row["gate-name"])

    unique_routes = {}
    route_matches = {}
    for key, value in routes.items():
        # Consider unique routes, regardless of direction
        if value not in unique_routes.values() and value.reverse() not in unique_routes.values():
            unique_routes[key] = value
            route_matches[key] = key
        else:
            if value in unique_routes.values():
                route_matches[key] = [i for i in unique_routes if unique_routes[i] == value][0]
            else:
                route_matches[key] = [i for i in unique_routes if unique_routes[i] == value.reverse()][0]

    for index, row in df.iterrows():
        row["route-idx"] = route_matches[row["route-idx"]]

    df.to_csv(OUT_CSV_PATH)


if __name__ == "__main__":
    main()
