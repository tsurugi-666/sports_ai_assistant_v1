class LogicReasoningEngine:
    def __init__(self):
        # База фактов: {"fact_name": True/False}
        self.facts = {}
        # База правил: [(rule_name, logic_func, target_fact, explanation_text)]
        self.rules = []

    def set_fact(self, name: str, value: bool):
        self.facts[name] = value

    def add_rule(self, name: str, condition_fn, target_fact: str, explanation: str):
        self.rules.append({
            "name": name,
            "condition": condition_fn,
            "target": target_fact,
            "explanation": explanation
        })

    def infer(self):
        explanations = []
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                target = rule["target"]
                if self.facts.get(target) is not True:
                    if rule["condition"](self.facts):
                        self.facts[target] = True
                        explanations.append(f"Выведено [{target}]: {rule['explanation']}")
                        changed = True
        return explanations