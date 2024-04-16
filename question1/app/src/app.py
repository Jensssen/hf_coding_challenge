import os
import re

import gradio as gr
from dotenv import load_dotenv

from answer_template import fill_answer
from inference import query_model
from seeking_alpah_api import SeekingAlphaAPI

load_dotenv()

sa_api = SeekingAlphaAPI(api_key=os.environ.get("SEEKING_ALPHA_API_KEY"),
                         api_host=os.environ.get("SEEKING_ALPHA_HOST"))


def stock_news_summary(symbol: str, article_count: int) -> str:
    """
    Queries Seeking Alpha api for latest articles about a public company. Then it uses a LLM to summarize each article.

    Args:
        symbol: Symbol of the company of interest such as aapl.
        article_count: Number of articles that shall be summarized.

    Returns:
        Returns the summarized articles as string.
    """
    if symbol:
        company_info = sa_api.get_company_info(symbol)
        article_info = []

        if company_info is not None:
            company_name = company_info['data'][0]['attributes']['companyName']
            latest_news = sa_api.get_latest_news(company_symbol=symbol, number_of_articles=article_count)
        else:
            return f"The company symbol that you have selected ({symbol}) does not seem to exist."

        for article in latest_news["data"]:
            detailed_article = sa_api.get_article_by_id(article["id"])
            source_url = detailed_article["data"]["links"]["canonical"]
            article_attributes = detailed_article["data"]["attributes"]
            published_on = article_attributes["publishOn"]
            title = article_attributes["title"]
            content = article_attributes["content"]
            cleaned_content = re.sub(r'<[^>]*>', '', content).strip()

            model_response = query_model(
                query=f"Please summarize the following article in TWO sentences! "
                      f"The summarization MUST contain the key information about {company_name}. "
                      f"Article: {cleaned_content}")

            generated_text = model_response[0]["generated_text"]
            article_info.append({
                "title": title,
                "source": source_url,
                "summary": generated_text,
                "date": published_on,
                "compression_rate": int((1 - len(generated_text.split()) / len(cleaned_content.split())) * 100)
            })

        final = fill_answer(article_info, company_name)
        return final
    else:
        return "No symbol provided!"


demo = gr.Interface(
    fn=stock_news_summary,
    inputs=["text", gr.Slider(2, 5, value=3, step=1, label="Count",
                              info="Nr. of articles that shall be summarized.")],
    outputs=["text"],
    examples=[["tsla"], ["aapl"], ["nvda"], ["msft"], ["amzn"], ["huggingface"]],
    title=f"Stock News Summarization",
    description="This application summarizes the top n latest News articles of any public company that is covered by "
                "[Seeking Alpha](https://seekingalpha.com/). Just enter the symbol of a publicly listed company and "
                "inform yourself quickly about whats is being reported right now!!",
)

demo.launch(server_name="0.0.0.0",
            server_port=8080)
