# model.py (финальная версия для Mesa 3.0+)

from mesa import Agent, Model
from mesa.datacollection import DataCollector

class PersonAgent(Agent):
    """Агент-физлицо с доходом и налоговой ставкой."""
    def __init__(self, model, initial_wealth):
        # Mesa 3.0+ автоматически управляет unique_id
        super().__init__(model)
        self.wealth = initial_wealth
        self.income = self.random.uniform(0.5, 1.5) * (initial_wealth or 1)

    def step(self):
        """На каждом шаге агент зарабатывает доход и платит налог."""
        tax_paid = self.income * self.model.tax_rate
        self.wealth += self.income - tax_paid
        self.model.government_revenue += tax_paid

class EconomicModel(Model):
    """Модель для симуляции базовых экономических взаимодействий (синтаксис Mesa 3.0+)."""
    def __init__(self, N, gdp, tax_rate=0.1):
        super().__init__() 
        
        self.num_agents = N
        self.tax_rate = tax_rate
        self.government_revenue = 0
        
        initial_wealth_per_capita = gdp / N if N > 0 else 0

        # Создание агентов и добавление их в модель
        for i in range(self.num_agents):
            a = PersonAgent(self, initial_wealth_per_capita)
            # ИСПРАВЛЕНИЕ: Используем self.agents.append() вместо self.add_agent()
            #self.agents.append(a) # 

        # DataCollector остается таким же
        self.datacollector = DataCollector(
            model_reporters={
                "TotalWealth": lambda m: sum(a.wealth for a in m.agents),
                "GovernmentRevenue": "government_revenue"
            }
        )
        self.datacollector.collect(self)

    def step(self):
        """Выполняет один шаг симуляции."""
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)