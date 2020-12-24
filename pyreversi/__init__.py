"""Python reversi"""
import pkg_resources

__version__: str = pkg_resources.get_distribution("pyreversi").version

del pkg_resources
