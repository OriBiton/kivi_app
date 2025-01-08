import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from db import get_training_summary, get_training_dates

# קבלת הנתונים מה-DB
def get_summary_data(username):
    data = get_training_summary(username)
    df = pd.DataFrame(data, columns=["Muscle Group", "Count"])
    return df

def get_dates_data(username):
    data = get_training_dates(username)
    df = pd.DataFrame(data, columns=["Date", "Muscle Group"])
    return df

# יצירת האפליקציה עם Dash
def create_dash_app(username):
    summary_df = get_summary_data(username)
    dates_df = get_dates_data(username)

    # גרף ראשון - סיכום לפי קבוצות שרירים
    fig_summary = px.bar(summary_df, x="Muscle Group", y="Count", title="Training Summary")

    # גרף שני - אימונים לפי ימים
    fig_dates = px.histogram(dates_df, x="Date", title="Training Days")

    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1(f"Hello, {username}! Your Training Dashboard"),
        dcc.Graph(figure=fig_summary),
        dcc.Graph(figure=fig_dates)
    ])

    return app

if __name__ == '__main__':
    username = "testuser"  # החלף בשם המשתמש הדינמי שלך
    app = create_dash_app(username)
    app.run_server(debug=True)
