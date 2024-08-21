# StartupEcosystem.py

class StartupEcosystem:
    """
    A class to manage and list different types of support organizations for startups.
    """
    
    def __init__(self):
        """
        Initializes the ecosystem with categories and sample organizations.
        """
        self.categories = {
            "Funders": [
                {"name": "Venture Capital Firm A", "description": "Provides seed funding to early-stage startups."},
                {"name": "Angel Investor B", "description": "Offers investment and mentorship to pre-seed startups."}
            ],
            "Consultants": [
                {"name": "Consulting Firm C", "description": "Specializes in business strategy and planning."},
                {"name": "Startup Mentor D", "description": "Provides one-on-one mentorship and advice."}
            ],
            "Coaches": [
                {"name": "Business Coach E", "description": "Helps with leadership and team development."},
                {"name": "Growth Coach F", "description": "Focuses on scaling and business growth strategies."}
            ],
            "Service Providers": [
                {"name": "Legal Services G", "description": "Offers legal assistance and company registration services."},
                {"name": "Accounting Firm H", "description": "Provides bookkeeping and financial advice."}
            ],
            "Business Associations": [
                {"name": "Startup Network I", "description": "A network of startup founders and entrepreneurs."},
                {"name": "Industry Association J", "description": "Supports startups in the technology sector."}
            ],
            "Business Events": [
                {"name": "Startup Expo K", "description": "An event showcasing innovative startups and networking opportunities."},
                {"name": "Pitch Competition L", "description": "A competition for startups to pitch their ideas to investors."}
            ]
        }
    
    def list_organizations(self, category):
        """
        Lists organizations under a specific category.
        
        Parameters:
        category (str): The category of organizations.

        Returns:
        list: A list of organizations in the specified category.
        """
        return self.categories.get(category, [])
    
    def get_category_description(self, category):
        """
        Provides a description for a given category.
        
        Parameters:
        category (str): The category of organizations.

        Returns:
        str: The description of the category.
        """
        return f"List of organizations under '{category}' category."

# Example usage
if __name__ == "__main__":
    ecosystem = StartupEcosystem()
    for category in ecosystem.categories.keys():
        print(f"Category: {category}")
        for org in ecosystem.list_organizations(category):
            print(f"  Name: {org['name']}, Description: {org['description']}")
