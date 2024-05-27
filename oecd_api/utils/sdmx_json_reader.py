import pandas as pd


class SdmxJsonReader:
    def __init__(self, json_data: dict):
        self.json_data = json_data

    def to_data_frame(self) -> pd.DataFrame:
        # Extracting the relevant data for the DataFrame
        series_data = self.json_data["data"]["dataSets"][0]["series"]
        dimensions = self.json_data["data"]["structures"][0]["dimensions"]

        # Mapping dimension IDs to their names
        dimension_names = {
            dim["id"]: [val["name"] for val in dim["values"]]
            for dim in dimensions["series"]
        }
        time_periods = {
            str(i): val["name"]
            for i, val in enumerate(dimensions["observation"][0]["values"])
        }

        # Creating a DataFrame from the series data
        data = []
        for series_key, series_info in series_data.items():
            series_indices = series_key.split(":")
            series_record = {
                dim["id"]: dimension_names[dim["id"]][int(index)]
                for dim, index in zip(dimensions["series"], series_indices)
            }
            for obs_key, obs_value in series_info["observations"].items():
                obs_record = series_record.copy()
                obs_record["TIME_PERIOD"] = time_periods[obs_key]
                obs_record["VALUE"] = obs_value[0]
                data.append(obs_record)

        return pd.DataFrame(data)
