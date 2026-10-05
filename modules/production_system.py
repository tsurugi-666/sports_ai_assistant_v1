class ProductionSystem:
    def __init__(self):
        self.rules = []

    def add_rule(self, conditions: list, action: str):
        # conditions: список имён признаков, которые должны быть True
        self.rules.append({"if": conditions, "then": action})

    def forward_chaining(self, active_facts: set) -> list:
        derived_actions = []
        working_facts = set(active_facts)
        
        added = True
        while added:
            added = False
            for rule in self.rules:
                if rule["then"] not in derived_actions:
                    # Проверяем, выполнено ли условие (Прямой вывод)
                    if all(cond in working_facts for cond in rule["if"]):
                        derived_actions.append(rule["then"])
                        working_facts.add(rule["then"])
                        added = True
        return derived_actions