from string import Template
from typing import Dict, List

SUMMARY_BLOCK = """
$idx. 
TITLE: $title 
DATE: $date
SUMMARY: $summary
ARTICLE COMPRESSION RATE: $article_compression_rate%
SOURCE: $source
"""


def fill_answer(article_info: List[Dict[str, str]], company_name: str) -> str:
    """
    Construct final answer string using a string template.

    Args:
        article_info: List of article info as dict.
        company_name: Name of the Company of interest.

    Returns:

    """
    final_answer = f"""Here are the top {len(article_info)} articles about {company_name}: \n"""

    for idx, info in enumerate(article_info):
        t = Template(SUMMARY_BLOCK)

        filled_in_summary_block = t.substitute(idx=f"{idx + 1}", title=info["title"], date=info["date"],
                                               summary=info["summary"],
                                               article_compression_rate=info["compression_rate"],
                                               source=info["source"])
        final_answer += filled_in_summary_block + "\n"

    return final_answer
