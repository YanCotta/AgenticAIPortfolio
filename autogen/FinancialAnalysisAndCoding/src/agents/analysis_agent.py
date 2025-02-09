"""
Module for implementing an analysis agent with a plugin system for incorporating additional factors.
"""

import os
import importlib
from typing import List, Dict, Callable
from autogen import AssistantAgent
from MultiAgentFinancialAnalysis.logger import get_logger

logger = get_logger(__name__)

class AnalysisAgent(AssistantAgent):
    """
    An agent that performs advanced stock analysis using a plugin system.
    """

    def __init__(self, name: str, llm_config: Dict, plugins: List[str] = None, **kwargs):
        """
        Initializes the AnalysisAgent.

        Args:
            name (str): The name of the agent.
            llm_config (Dict): The language model configuration.
            plugins (List[str], optional): A list of plugin module names to load. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the AssistantAgent.
        """
        super().__init__(name=name, llm_config=llm_config, **kwargs)
        self.plugins = []
        if plugins:
            self.load_plugins(plugins)

    def load_plugins(self, plugin_names: List[str]):
        """
        Loads the specified plugins.

        Args:
            plugin_names (List[str]): A list of plugin module names to load.
        """
        for plugin_name in plugin_names:
            try:
                module = importlib.import_module(f"MultiAgentFinancialAnalysis.src.plugins.{plugin_name}")
                plugin_class = getattr(module, plugin_name.capitalize())  # Assuming class name is capitalized
                plugin = plugin_class()
                self.plugins.append(plugin)
                logger.info(f"Plugin '{plugin_name}' loaded successfully.")
            except ImportError as e:
                logger.error(f"Error importing plugin '{plugin_name}': {e}")
            except AttributeError as e:
                logger.error(f"Error loading plugin class from '{plugin_name}': {e}")
            except Exception as e:
                logger.error(f"Error loading plugin '{plugin_name}': {e}")

    def analyze_stock(self, stock_symbol: str) -> str:
        """
        Analyzes the given stock symbol using the loaded plugins.

        Args:
            stock_symbol (str): The stock symbol to analyze.

        Returns:
            str: A string containing the analysis results.
        """
        results = []
        for plugin in self.plugins:
            try:
                result = plugin.analyze(stock_symbol)
                results.append(result)
            except Exception as e:
                logger.error(f"Error running plugin '{plugin.__class__.__name__}': {e}")
        return "\n".join(results)

# Example Plugin Interface (Abstract Base Class)
class PluginInterface:
    """
    An interface for creating analysis plugins.
    """
    def analyze(self, stock_symbol: str) -> str:
        """
        Analyzes the given stock symbol.

        Args:
            stock_symbol (str): The stock symbol to analyze.

        Returns:
            str: A string containing the analysis results.
        """
        raise NotImplementedError("Subclasses must implement the analyze method.")
