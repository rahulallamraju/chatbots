from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Load CSV data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), 't1.csv')
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        print("Error: t1.csv file not found!")
        return None

class FinancialChatbot:
    def __init__(self, dataframe):
        self.df = dataframe
        
    def get_company_data(self, company, metric, year=None):
        """Get specific data for a company and metric"""
        if self.df is None:
            return None
            
        company_data = self.df[(self.df['Company'] == company) & 
                              (self.df['Metric'] == metric)]
        
        if company_data.empty:
            return None
            
        if year:
            if str(year) in company_data.columns:
                return company_data[str(year)].iloc[0]
        
        return company_data.iloc[0]
    
    def calculate_change(self, company, metric, year1, year2):
        """Calculate change between two years"""
        try:
            value1 = self.get_company_data(company, metric, year1)
            value2 = self.get_company_data(company, metric, year2)
            
            if value1 and value2:
                change = value2 - value1
                percentage = (change / value1) * 100
                return change, percentage
        except:
            return None, None
        return None, None
    
    def process_query(self, user_query):
        """Main chatbot logic"""
        if self.df is None:
            return "Sorry, I couldn't load the financial data. Please check if t1.csv exists."
            
        query = user_query.lower().strip()
        
        # Query 1: Total Revenue
        if any(keyword in query for keyword in ['total revenue', 'revenue']):
            if 'microsoft' in query:
                revenue_2024 = self.get_company_data('Microsoft', 'Total Revenue(in millions)', '2024')
                return f"Microsoft's total revenue in 2024 is ${revenue_2024:,} million."
            elif 'tesla' in query:
                revenue_2024 = self.get_company_data('Tesla', 'Total Revenue(in millions)', '2024')
                return f"Tesla's total revenue in 2024 is ${revenue_2024:,} million."
            elif 'apple' in query:
                revenue_2024 = self.get_company_data('Apple', 'Total Revenue(in millions)', '2024')
                return f"Apple's total revenue in 2024 is ${revenue_2024:,} million."
            else:
                ms_rev = self.get_company_data('Microsoft', 'Total Revenue(in millions)', '2024')
                tesla_rev = self.get_company_data('Tesla', 'Total Revenue(in millions)', '2024')
                apple_rev = self.get_company_data('Apple', 'Total Revenue(in millions)', '2024')
                return f"2024 Total Revenue: Microsoft: ${ms_rev:,}M, Tesla: ${tesla_rev:,}M, Apple: ${apple_rev:,}M"
        
        # Query 2: Net Income Changes
        elif any(keyword in query for keyword in ['net income', 'profit', 'earnings']):
            # Check for specific company first
            if 'microsoft' in query:
                if 'change' in query or 'growth' in query:
                    change, percentage = self.calculate_change('Microsoft', 'Net Income(in millions)', 2023, 2024)
                    if change is not None:
                        direction = "increased" if change > 0 else "decreased"
                        return f"Microsoft's net income {direction} by ${abs(change):,.0f}M ({percentage:+.1f}%) from 2023 to 2024."
                else:
                    income_2024 = self.get_company_data('Microsoft', 'Net Income(in millions)', '2024')
                    return f"Microsoft's net income in 2024 is ${income_2024:,} million."
            elif 'tesla' in query:
                if 'change' in query or 'growth' in query:
                    change, percentage = self.calculate_change('Tesla', 'Net Income(in millions)', 2023, 2024)
                    if change is not None:
                        direction = "increased" if change > 0 else "decreased"
                        return f"Tesla's net income {direction} by ${abs(change):,.0f}M ({percentage:+.1f}%) from 2023 to 2024."
                else:
                    income_2024 = self.get_company_data('Tesla', 'Net Income(in millions)', '2024')
                    return f"Tesla's net income in 2024 is ${income_2024:,} million."
            elif 'apple' in query:
                if 'change' in query or 'growth' in query:
                    change, percentage = self.calculate_change('Apple', 'Net Income(in millions)', 2023, 2024)
                    if change is not None:
                        direction = "increased" if change > 0 else "decreased"
                        return f"Apple's net income {direction} by ${abs(change):,.0f}M ({percentage:+.1f}%) from 2023 to 2024."
                else:
                    income_2024 = self.get_company_data('Apple', 'Net Income(in millions)', '2024')
                    return f"Apple's net income in 2024 is ${income_2024:,} million."
            # If no specific company mentioned, show all companies
            elif 'change' in query or 'growth' in query:
                results = []
                for company in ['Microsoft', 'Tesla', 'Apple']:
                    change, percentage = self.calculate_change(company, 'Net Income(in millions)', 2023, 2024)
                    if change is not None:
                        direction = "increased" if change > 0 else "decreased"
                        results.append(f"{company}: {direction} by ${abs(change):,.0f}M ({percentage:+.1f}%)")
                return "Net Income Changes (2023 to 2024): " + ", ".join(results)
            else:
                ms_income = self.get_company_data('Microsoft', 'Net Income(in millions)', '2024')
                tesla_income = self.get_company_data('Tesla', 'Net Income(in millions)', '2024')
                apple_income = self.get_company_data('Apple', 'Net Income(in millions)', '2024')
                return f"2024 Net Income: Microsoft: ${ms_income:,}M, Tesla: ${tesla_income:,}M, Apple: ${apple_income:,}M"
        
        # Query 3: Cash Flow Information
        elif any(keyword in query for keyword in ['cash flow', 'operating cash']):
            # Check for specific company first
            if 'microsoft' in query:
                if 'change' in query or 'growth' in query:
                    change, percentage = self.calculate_change('Microsoft', 'Operating Cash Flow(in millions)', 2023, 2024)
                    if change is not None:
                        direction = "increased" if change > 0 else "decreased"
                        return f"Microsoft's operating cash flow {direction} by ${abs(change):,.0f}M ({percentage:+.1f}%) from 2023 to 2024."
                else:
                    cash_flow = self.get_company_data('Microsoft', 'Operating Cash Flow(in millions)', '2024')
                    return f"Microsoft's operating cash flow in 2024 is ${cash_flow:,} million."
            elif 'tesla' in query:
                if 'change' in query or 'growth' in query:
                    change, percentage = self.calculate_change('Tesla', 'Operating Cash Flow(in millions)', 2023, 2024)
                    if change is not None:
                        direction = "increased" if change > 0 else "decreased"
                        return f"Tesla's operating cash flow {direction} by ${abs(change):,.0f}M ({percentage:+.1f}%) from 2023 to 2024."
                else:
                    cash_flow = self.get_company_data('Tesla', 'Operating Cash Flow(in millions)', '2024')
                    return f"Tesla's operating cash flow in 2024 is ${cash_flow:,} million."
            elif 'apple' in query:
                if 'change' in query or 'growth' in query:
                    change, percentage = self.calculate_change('Apple', 'Operating Cash Flow(in millions)', 2023, 2024)
                    if change is not None:
                        direction = "increased" if change > 0 else "decreased"
                        return f"Apple's operating cash flow {direction} by ${abs(change):,.0f}M ({percentage:+.1f}%) from 2023 to 2024."
                else:
                    cash_flow = self.get_company_data('Apple', 'Operating Cash Flow(in millions)', '2024')
                    return f"Apple's operating cash flow in 2024 is ${cash_flow:,} million."
            # If no specific company mentioned, show all companies
            elif 'change' in query or 'growth' in query:
                results = []
                for company in ['Microsoft', 'Tesla', 'Apple']:
                    change, percentage = self.calculate_change(company, 'Operating Cash Flow(in millions)', 2023, 2024)
                    if change is not None:
                        direction = "increased" if change > 0 else "decreased"
                        results.append(f"{company}: {direction} by ${abs(change):,.0f}M ({percentage:+.1f}%)")
                return "Operating Cash Flow Changes (2023 to 2024): " + ", ".join(results)
            else:
                results = []
                for company in ['Microsoft', 'Tesla', 'Apple']:
                    cash_flow = self.get_company_data(company, 'Operating Cash Flow(in millions)', '2024')
                    results.append(f"{company}: ${cash_flow:,}M")
                return "2024 Operating Cash Flow: " + ", ".join(results)
        
        # Query 4: Company Comparison
        elif 'compare' in query or 'comparison' in query:
            return """Company Comparison (2024):
            Revenue: Microsoft ($245,122M) > Tesla ($97,690M) > Apple ($7,700M)
            Net Income: Apple ($93,736M) > Microsoft ($88,136M) > Tesla ($7,153M)
            Cash Flow: Apple ($118,254M) > Microsoft ($118,548M) > Tesla ($14,923M)"""
        
        # Query 5: Financial Health
        elif any(keyword in query for keyword in ['financial health', 'assets', 'liabilities']):
            results = []
            for company in ['Microsoft', 'Tesla', 'Apple']:
                assets = self.get_company_data(company, 'Total Assets(in millions)', '2024')
                liabilities = self.get_company_data(company, 'Total Liabilities(in millions)', '2024')
                equity = assets - liabilities
                results.append(f"{company}: Assets ${assets:,}M, Equity ${equity:,}M")
            return "Financial Position (2024): " + "; ".join(results)
        
        # Default response
        else:
            return """I can help you with these financial queries:
            • "What is the total revenue?" - Get revenue information
            • "How has net income changed?" - See profit changes
            • "What is the operating cash flow?" - Cash flow data
            • "Compare the companies" - Side-by-side comparison
            • "What is the financial health?" - Assets and equity info
            
            You can also specify a company (Microsoft, Tesla, or Apple) in your question."""

# Initialize chatbot with data
df = load_data()
chatbot = FinancialChatbot(df)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    bot_response = chatbot.process_query(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    print("Starting Financial Analysis Chatbot...")
    print("Visit: http://127.0.0.1:5000")
    app.run(debug=True)