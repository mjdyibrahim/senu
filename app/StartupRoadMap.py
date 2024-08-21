# StartupRoadMap.py

class StartupRoadMap:
    """
    A class to define and manage the roadmap of a startup based on its stage and funding.
    """
    
    def __init__(self):
        """
        Initializes the roadmap with predefined stages and their criteria.
        """
        self.stages = {
            "Pre-Seed": {
                "description": "Initial phase where the startup is working on their prototype or MVP.",
                "criteria": {
                    "revenue": 0,
                    "funding": (0, 50000),
                    "market_fit": False
                }
            },
            "Seed": {
                "description": "Phase where the startup has a working prototype and is seeking initial funding to scale.",
                "criteria": {
                    "revenue": (0, 100000),
                    "funding": (50000, 500000),
                    "market_fit": True
                }
            },
            "Series A": {
                "description": "Phase where the startup is looking to scale significantly and expand its market presence.",
                "criteria": {
                    "revenue": (100000, 2000000),
                    "funding": (500000, 5000000),
                    "market_fit": True
                }
            }
            # Add more stages as needed
        }
    
    def determine_stage(self, revenue, funding, market_fit):
        """
        Determines the startup stage based on provided metrics.
        
        Parameters:
        revenue (float): Current revenue of the startup.
        funding (float): Amount of funding raised.
        market_fit (bool): Whether the startup has achieved product-market fit.

        Returns:
        str: The stage of the startup.
        """
        for stage, criteria in self.stages.items():
            if (criteria["criteria"]["revenue"][0] <= revenue <= criteria["criteria"]["revenue"][1] and
                criteria["criteria"]["funding"][0] <= funding <= criteria["criteria"]["funding"][1] and
                market_fit == criteria["criteria"]["market_fit"]):
                return stage
        return "Unknown Stage"
    
    def get_stage_description(self, stage):
        """
        Provides a description for a given stage.
        
        Parameters:
        stage (str): The stage of the startup.

        Returns:
        str: The description of the stage.
        """
        return self.stages.get(stage, {}).get("description", "No description available.")

# Example usage
if __name__ == "__main__":
    roadmap = StartupRoadMap()
    stage = roadmap.determine_stage(50000, 100000, True)
    print(f"Stage: {stage}")
    print(f"Description: {roadmap.get_stage_description(stage)}")
