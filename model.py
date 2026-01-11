# model.py (версия для Mesa 3.0+)

from mesa import Agent, Model
from mesa.datacollection import DataCollector

class PersonAgent(Agent):
    """Агент-физлицо с доходом и налоговой ставкой."""
    def __init__(self, unique_id, model, initial_wealth):
        super().__init__(unique_id, model)
        self.wealth = initial_wealth
        # Доход агента на каждом шаге
        self.income = self.random.uniform(0.5, 1.5) * (initial_wealth or 1)

    def step(self):
        """
        На каждом шаге агент зарабатывает доход и платит налог.
        Этот метод будет вызван командой model.agents.shuffle_do("step").
        """
        tax_paid = self.income * self.model.tax_rate
        self.wealth += self.income - tax_paid
        self.model.government_revenue += tax_paid

class EconomicModel(Model):
    """Модель для симуляции базовых экономических взаимодействий (синтаксис Mesa 3.0+)."""
    def __init__(self, N, gdp, tax_rate=0.1):
        # super().__init__() автоматически создает self.agents
        super().__init__() 
        
        self.num_agents = N
        self.tax_rate = tax_rate
        self.government_revenue = 0
        
        # Рассчитываем начальное богатство на душу населения
        initial_wealth_per_capita = gdp / N if N > 0 else 0

        # Создание агентов и добавление их в модель
        for i in range(self.num_agents):
            # Создаем агента
            a = PersonAgent(i, self, initial_wealth_per_capita) # <--- ИСПРАВЛЕНО
            # Добавляем агента в AgentSet модели (вместо self.schedule.add)
            self.add_agent(a)

        # DataCollector остается таким же
        self.datacollector = DataCollector(
            model_reporters={
                "TotalWealth": lambda m: sum(a.wealth for a in m.agents),
                "GovernmentRevenue": "government_revenue"
            }
        )
        # Первичный сбор данных в момент инициализации
        self.datacollector.collect(self)

    def step(self):
        """Выполняет один шаг симуляции."""
        # Вместо self.schedule.step() используем новый синтаксис.
        # shuffle_do("step") - это аналог RandomActivation.
        # Он вызывает метод "step" у всех агентов в случайном порядке.
        self.agents.shuffle_do("step")
        
        # Сбор данных после каждого шага
        self.datacollector.collect(self)