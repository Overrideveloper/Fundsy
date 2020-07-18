from app.data.database import db
from app.data.repositories.customer_investment import CustomerInvestmentRepository
from app.server.cron.utils import calculate_daily_appreciation

customer_investment_repo = CustomerInvestmentRepository(db)

def customer_investment_appreciation():
    try:
        customer_investments = customer_investment_repo.get_all()
        
        for customer_investment in customer_investments:
            if customer_investment.amount > 0:
                id = customer_investment.id
                investment = customer_investment.investment
                amount = customer_investment.amount
                rate = investment.appreciation_amount
                duration = investment.appreciation_duration
                
                daily_appreciation = calculate_daily_appreciation(amount, rate, duration)
                customer_investment_repo.appreciate(id, daily_appreciation)
    except Exception as exc:
        print(exc)
