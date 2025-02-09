import pandas as pd
from typing import List, Dict

class HistoryService:
    def __init__(self, data_source: str):
        """
        Initializes the HistoryService with a data source (e.g., a database connection string or file path).
        Args:
            data_source (str): The source of historical data.
        """
        self.data_source = data_source
        self.historical_data = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        """
        Loads historical data from the specified data source.
        Returns:
            pd.DataFrame: A DataFrame containing the historical data.
        """
        # Placeholder for data loading logic (e.g., from CSV, database)
        print(f"Loading historical data from {self.data_source}...")
        # Example: loading from a CSV file
        try:
            data = pd.read_csv(self.data_source)
            return data
        except FileNotFoundError:
            print("Historical data file not found. Initializing with an empty DataFrame.")
            return pd.DataFrame()

    def collect_velocity(self) -> float:
        """
        Calculates the average velocity (tasks completed per unit time) from historical data.
        Returns:
            float: The average velocity.
        """
        if self.historical_data.empty:
            return 0.0
        # Placeholder for velocity calculation logic
        print("Calculating velocity...")
        # Example: assuming 'completion_date' and 'start_date' columns exist
        self.historical_data['completion_date'] = pd.to_datetime(self.historical_data['completion_date'])
        self.historical_data['start_date'] = pd.to_datetime(self.historical_data['start_date'])
        self.historical_data['cycle_time'] = (self.historical_data['completion_date'] - self.historical_data['start_date']).dt.days
        velocity = len(self.historical_data) / self.historical_data['cycle_time'].mean()
        return velocity

    def collect_cycle_times(self) -> List[float]:
        """
        Collects cycle times for completed tasks from historical data.
        Returns:
            List[float]: A list of cycle times.
        """
        if self.historical_data.empty:
            return []
        # Placeholder for cycle time collection logic
        print("Collecting cycle times...")
        # Example: assuming 'completion_date' and 'start_date' columns exist
        self.historical_data['completion_date'] = pd.to_datetime(self.historical_data['completion_date'])
        self.historical_data['start_date'] = pd.to_datetime(self.historical_data['start_date'])
        cycle_times = (self.historical_data['completion_date'] - self.historical_data['start_date']).dt.days.tolist()
        return cycle_times

    def collect_costing_data(self) -> Dict[str, float]:
        """
        Collects costing data for completed tasks from historical data.
        Returns:
            Dict[str, float]: A dictionary of costing data (e.g., average cost per task).
        """
        if self.historical_data.empty:
            return {}
        # Placeholder for costing data collection logic
        print("Collecting costing data...")
        # Example: assuming 'cost' column exists
        average_cost = self.historical_data['cost'].mean()
        return {"average_cost_per_task": average_cost}

    def detect_anomalies(self, data: pd.Series, threshold: float = 3.0) -> List[int]:
        """
        Detects anomalies in the given data using the Z-score method.
        Args:
            data (pd.Series): The data to detect anomalies in.
            threshold (float): The Z-score threshold for anomaly detection.
        Returns:
            List[int]: A list of indices where anomalies were detected.
        """
        if data.empty:
            return []
        # Placeholder for anomaly detection logic
        print("Detecting anomalies...")
        mean = data.mean()
        std = data.std()
        z_scores = abs((data - mean) / std)
        anomalies = z_scores[z_scores > threshold].index.tolist()
        return anomalies

    def flag_potential_risks(self) -> List[str]:
        """
        Flags potential risks based on thresholds and anomaly detection.
        Returns:
            List[str]: A list of potential risks.
        """
        risks = []
        velocity = self.collect_velocity()
        if velocity < 1.0:  # Example threshold
            risks.append("Low velocity detected. Project may be behind schedule.")
        
        cycle_times = self.collect_cycle_times()
        if cycle_times:
            cycle_times_series = pd.Series(cycle_times)
            anomalies = self.detect_anomalies(cycle_times_series)
            if anomalies:
                risks.append(f"Anomalous cycle times detected for tasks at indices: {anomalies}")
        
        costing_data = self.collect_costing_data()
        if costing_data and costing_data.get("average_cost_per_task", 0) > 10000:  # Example threshold
            risks.append("High average cost per task detected. Project may be over budget.")
        
        return risks

if __name__ == "__main__":
    # Example Usage
    history_service = HistoryService(data_source="historical_data.csv")  # Replace with your data source
    
    # Create a dummy historical_data.csv for testing
    dummy_data = pd.DataFrame({
        'task_name': ['Task A', 'Task B', 'Task C', 'Task D', 'Task E'],
        'start_date': ['2024-01-01', '2024-01-05', '2024-01-10', '2024-01-15', '2024-01-20'],
        'completion_date': ['2024-01-04', '2024-01-12', '2024-01-15', '2024-01-22', '2024-02-05'],
        'cost': [1000, 1500, 1200, 1800, 5000]
    })
    dummy_data.to_csv("historical_data.csv", index=False)
    
    velocity = history_service.collect_velocity()
    print(f"Average Velocity: {velocity}")
    
    cycle_times = history_service.collect_cycle_times()
    print(f"Cycle Times: {cycle_times}")
    
    costing_data = history_service.collect_costing_data()
    print(f"Costing Data: {costing_data}")
    
    risks = history_service.flag_potential_risks()
    print(f"Potential Risks: {risks}")
