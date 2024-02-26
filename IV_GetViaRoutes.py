import csv
import pandas
import datetime


# CSV Input and output paths. Change these.
IN_CSV_PATH = "C:\\Users\\ryan_\\OneDrive\\Documents\\School\\Information Visualization\\Final Project\\" \
              "2017MC1Data\\Lekagul Sensor Data.csv"
OUT_CSV_PATH = "C:\\Users\\ryan_\\OneDrive\\Documents\\School\\Information Visualization\\Final Project\\" \
               "2017MC1Data\\Lekagul Via Routes.csv"


def main():
    # Read in data
    df = pandas.read_csv(IN_CSV_PATH)

    # Track cars in park and route IDs
    cars_in_park = {}
    unique_routes = []

    # Find Via
    out_df = pandas.DataFrame(
        columns=["route-idx", "step-idx", "car-id", "car-type", "timestamp", "position", "duration"]
    )

    for index, row in df.iterrows():
        if row["car-id"] not in cars_in_park.keys():
            current_time = datetime.datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
            cars_in_park[row["car-id"]] = (current_time, row["gate-name"])

            route = [cars_in_park[row["car-id"]][1], row["gate-name"]]
            if route in unique_routes:
                route_idx = unique_routes.index(route)
            elif route.reverse() in unique_routes:
                route_idx = unique_routes.index(route.reverse())
            else:
                route_idx = len(unique_routes)
                unique_routes.append(route)

            out_df.loc[len(out_df.index)] = [route_idx, 0, row["car-id"], row["car-type"], row["Timestamp"],
                                             cars_in_park[row["car-id"]][1],
                                             (current_time - current_time).total_seconds()]
            out_df.loc[len(out_df.index)] = [route_idx, 1, row["car-id"], row["car-type"], row["Timestamp"],
                                             row["gate-name"], (current_time - current_time).total_seconds()]

        else:
            current_time = datetime.datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")

            route = [cars_in_park[row["car-id"]][1], row["gate-name"]]
            if route in unique_routes:
                route_idx = unique_routes.index(route)
            elif route.reverse() in unique_routes:
                route_idx = unique_routes.index(route.reverse())
            else:
                route_idx = len(unique_routes)
                unique_routes.append(route)

            out_df.loc[len(out_df.index)] = [route_idx, 0, row["car-id"], row["car-type"], row["Timestamp"],
                                             cars_in_park[row["car-id"]][1],
                                             (current_time - cars_in_park[row["car-id"]][0]).total_seconds()]
            out_df.loc[len(out_df.index)] = [route_idx, 1, row["car-id"], row["car-type"], row["Timestamp"],
                                             row["gate-name"],
                                             (current_time - cars_in_park[row["car-id"]][0]).total_seconds()]

            if (row["gate-name"][:-1] != "entrance") and (row["gate-name"] != "ranger-base"):
                cars_in_park[row["car-id"]] = (current_time, row["gate-name"])
            else:
                cars_in_park.pop(row["car-id"])

    out_df.to_csv(OUT_CSV_PATH)


if __name__ == "__main__":
    main()
