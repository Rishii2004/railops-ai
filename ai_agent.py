"""Gemini tool-calling assistant grounded in already validated inspection records."""
import os
import pandas as pd


def ask_agent(df: pd.DataFrame, question: str, api_key: str) -> str:
    if not api_key:
        raise ValueError('A Gemini API key is required to use the AI assistant.')
    if not question.strip():
        raise ValueError('Enter a question first.')
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError('Install dependencies: python -m pip install -r requirements.txt') from exc

    def get_inspection_summary() -> dict:
        """Return verified counts of railcars by inspection scheduling status."""
        counts = df['inspection_status'].value_counts()
        return {
            'total_railcars': int(len(df)),
            'overdue': int(counts.get('Overdue', 0)),
            'due_soon_14_days': int(counts.get('Due Soon', 0)),
            'on_track': int(counts.get('On Track', 0)),
        }

    def get_priority_railcars(limit: int = 5) -> dict:
        """Get the most overdue railcars, ordered by days remaining (most overdue first).

        Args:
            limit: Number of records to return, between 1 and 20.
        """
        limit = max(1, min(int(limit), 20))
        overdue = df.loc[df['inspection_status'].eq('Overdue')].nsmallest(limit, 'days_remaining')
        return {'records': [
            {'railcar_id': str(row.railcar_id),
             'days_overdue': int(-row.days_remaining),
             'next_inspection': row.next_inspection.strftime('%Y-%m-%d')}
            for row in overdue.itertuples()
        ]}

    

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=20000)
    )


    response = client.models.generate_content(
        model=os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'),
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=(
                'You are a demo inspection scheduling analyst. Use the provided Python tools '
                'to answer numerical or record-specific questions. Never invent railcar data. '
                'Do not claim inspection scheduling status determines mechanical safety. '
                'This is synthetic portfolio data. Be concise.'
            ),
            tools=[get_inspection_summary, get_priority_railcars],
            temperature=0.1,
        ),
    )
    if not response.text:
        raise RuntimeError('The model returned no text. Please try again.')
    return response.text
