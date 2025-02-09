import matplotlib.pyplot as plt
import pandas as pd
from typing import List
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Task(BaseModel):
    task_name: str
    start_date: str
    end_date: str
    resource: str

class ProjectDashboard:
    def __init__(self, project_name: str, tasks: List[Task]):
        self.project_name = project_name
        self.tasks = tasks
        self.app = FastAPI()

    def generate_gantt_chart(self, output_path: str = "gantt_chart.png"):
        """
        Generates a static Gantt chart image using matplotlib.
        Args:
            output_path (str): The file path to save the Gantt chart image.
        """
        df = pd.DataFrame([task.dict() for task in self.tasks])
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        
        fig, ax = plt.subplots(1, figsize=(12, 6))
        
        for i, task in df.iterrows():
            ax.barh(task['task_name'], (task['end_date'] - task['start_date']).days, left=task['start_date'], color='skyblue')
        
        ax.set_xlabel("Date")
        ax.set_ylabel("Task")
        ax.set_title(f"Gantt Chart for {self.project_name}")
        
        plt.savefig(output_path)
        plt.close()
        print(f"Gantt chart saved to {output_path}")

    def create_rest_endpoint(self):
        """
        Offers a REST endpoint for external data consumption using FastAPI.
        """
        app = self.app
        project_name = self.project_name
        tasks = self.tasks

        @app.get("/project_data")
        async def get_project_data():
            """
            Returns project data as a JSON response.
            """
            return {"project_name": project_name, "tasks": tasks}

        @app.get("/gantt_chart")
        async def get_gantt_chart():
            """
            Returns the Gantt chart image.
            """
            self.generate_gantt_chart()
            return FileResponse("gantt_chart.png", media_type="image/png")

        return app

if __name__ == "__main__":
    # Example Usage
    tasks = [
        Task(task_name="Task 1", start_date="2024-01-01", end_date="2024-01-15", resource="John"),
        Task(task_name="Task 2", start_date="2024-01-10", end_date="2024-01-25", resource="Jane"),
        Task(task_name="Task 3", start_date="2024-01-20", end_date="2024-02-10", resource="Bob"),
    ]
    
    dashboard = ProjectDashboard(project_name="Sample Project", tasks=tasks)
    app = dashboard.create_rest_endpoint()

    # To run this example, you'll need to install uvicorn: pip install uvicorn
    # Then, run the app using: uvicorn project_dashboard:app --reload
