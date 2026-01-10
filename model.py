import mesa
import random

class Household(mesa.Agent):
    """Агент-домохозяйство."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.savings = 100  # Начальные сбережения

    def step(self):
        # На шаге домохозяйство платит налог, если получает зарплату
        pass

class Firm(mesa.Agent):
    """Агент-фирма."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.savings = 1000  # Начальный капитал

    def step(self):
        # Выплатить зарплату одному случайному домохозяйству
        if self.model.num_households > 0:
            household = random.choice(self.model.get_households())
            payment = self.model.firm_salary
            self.savings -= payment
            household.savings += payment
            # Домохозяйство платит налог
            tax = payment * self.model.tax_rate
            household.savings -= tax
            self.model.government.budget += tax

class Government(mesa.Agent):
    """Агент-правительство."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.budget = 10000  # Начальный бюджет

    def step(self):
        # Потратить часть бюджета на поддержку фирм
        if self.model.num_firms > 0:
            spending = self.budget * self.model.gov_spending_ratio
            self.budget -= spending
            per_firm_subsidy = spending / self.model.num_firms
            for firm in self.model.get_firms():
                firm.savings += per_firm_subsidy

def get_total_savings(model):
    """Функция для DataCollector: собирает общие сбережения домохозяйств."""
    return sum([a.savings for a in model.schedule.agents if isinstance(a, Household)])

def get_total_firm_capital(model):
    """Функция для DataCollector: собирает общий капитал фирм."""
    return sum([a.savings for a in model.schedule.agents if isinstance(a, Firm)])

def get_gov_budget(model):
    """Функция для DataCollector: собирает бюджет правительства."""
    return model.government.budget

class EconomicModel(mesa.Model):
    """Основной класс модели."""
    def __init__(self, N_households=10, N_firms=3, tax_rate=0.2, firm_salary=50, gov_spending_ratio=0.1):
        super().__init__()
        self.num_households = N_households
        self.num_firms = N_firms
        self.tax_rate = tax_rate
        self.firm_salary = firm_salary
        self.gov_spending_ratio = gov_spending_ratio

        self.schedule = mesa.time.RandomActivation(self)
        self.government = Government(0, self) # Правительство имеет id 0

        # Создание агентов-домохозяйств
        for i in range(self.num_households):
            h = Household(i + 1, self)
            self.schedule.add(h)

        # Создание агентов-фирм
        for i in range(self.num_firms):
            f = Firm(i + 1 + self.num_households, self)
            self.schedule.add(f)
            
        # Правительство добавляется в шедулер, чтобы его метод step() тоже вызывался
        self.schedule.add(self.government)

        # Сборщик данных для отслеживания показателей
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Total Savings": get_total_savings,
                "Total Firm Capital": get_total_firm_capital,
                "Government Budget": get_gov_budget,
            }
        )
        
    def get_households(self):
        return [agent for agent in self.schedule.agents if isinstance(agent, Household)]

    def get_firms(self):
        return [agent for agent in self.schedule.agents if isinstance(agent, Firm)]

    def step(self):
        """Выполняет один шаг симуляции."""
        self.datacollector.collect(self)
        self.schedule.step()

