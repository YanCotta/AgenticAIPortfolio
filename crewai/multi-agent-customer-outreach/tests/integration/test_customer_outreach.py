import unittest
from unittest.mock import patch
from src.main import create_agents, create_tasks, create_crew, create_tools
# from src.utils import pretty_print_result  # Removed import

class CustomerOutreachIntegrationTest(unittest.TestCase):

    @patch('src.main.create_agents')
    @patch('src.main.create_tasks')
    @patch('src.main.create_crew')
    def test_end_to_end_customer_outreach(self, mock_create_crew, mock_create_tasks, mock_create_agents):
        # Mock the agent creation
        mock_agents = (
            unittest.mock.Mock(role="Sales Representative"),
            unittest.mock.Mock(role="Lead Sales Representative")
        )
        mock_create_agents.return_value = mock_agents

        # Mock the task creation
        mock_tasks = (unittest.mock.Mock(), unittest.mock.Mock())
        mock_create_tasks.return_value = mock_tasks

        # Mock the crew creation and kickoff
        mock_crew = unittest.mock.Mock()
        mock_crew.kickoff.return_value = "Outreach completed successfully."
        mock_create_crew.return_value = mock_crew

        # Define input
        inputs = {
            "lead_name": "TestLead",
            "industry": "TestIndustry",
            "key_decision_maker": "TestName",
            "position": "TestPosition",
            "milestone": "TestMilestone"
        }

        # Call the main function (or a similar entry point)
        agents = create_agents(inputs)
        tools = create_tools()
        tasks = create_tasks(tools, agents)
        crew = create_crew(agents, tasks)
        result = crew.kickoff(inputs=inputs)

        # Assertions
        self.assertEqual(result, "Outreach completed successfully.")
        mock_create_agents.assert_called()
        mock_create_tasks.assert_called()
        mock_create_crew.assert_called()
        crew.kickoff.assert_called_with(inputs=inputs)

if __name__ == '__main__':
    unittest.main()
