import warnings
import pandas as pd
import pickle
from modules.semantic_net import SemanticNetwork
from modules.logic_reasoning import LogicReasoningEngine
from modules.production_system import ProductionSystem
from modules.frame_system import Frame, FrameKnowledgeBase

warnings.filterwarnings("ignore", category=UserWarning)


class FitnessExpertSystem:
    def __init__(self):
        self.init_semantic_net()
        self.init_frames()
        self.init_logic()
        self.init_production()

        try:
            with open("data/ml_model.pkl", "rb") as f:
                self.ml_model = pickle.load(f)
            with open("data/nn_model.pkl", "rb") as f:
                self.nn_model = pickle.load(f)
        except FileNotFoundError:
            self.ml_model = None
            self.nn_model = None

    def init_semantic_net(self):
        self.sem_net = SemanticNetwork()
        self.sem_net.add_edge("Отжимания", "targets", "Грудные мышцы и Трицепс")
        self.sem_net.add_edge("Приседания", "targets", "Квадрицепс и Ягодичные мышцы")
        self.sem_net.add_edge("Подтягивания", "targets", "Широчайшие мышцы и Бицепс")
        self.sem_net.add_edge("Планка", "targets", "Мышцы кора и Пресс")
        self.sem_net.add_edge("Становая тяга", "targets", "Бицепс бедра и Спина")

    def init_frames(self):
        self.kb_frames = FrameKnowledgeBase()

        base_exercise = Frame("БазовоеУпражнение")
        base_exercise.set_slot("тип", "Физическая нагрузка")
        base_exercise.set_slot("сложность", "Регулируемая")
        self.kb_frames.add_frame(base_exercise)

        pushups = Frame("Отжимания", parent=base_exercise)
        pushups.set_slot("инвентарь", "Собственный вес")
        pushups.set_slot("целевая_группа", "Верх тела")
        self.kb_frames.add_frame(pushups)

    def init_logic(self):
        self.logic = LogicReasoningEngine()

        self.logic.add_rule(
            "rule_beginner_safe",
            lambda f: f.get("is_beginner", False) and not f.get("has_injuries", False),
            "Адаптационный режим",
            "Рекомендуется начать с 2-3 тренировок в неделю с акцентом на правильную технику."
        )
        self.logic.add_rule(
            "rule_injury_limit",
            lambda f: f.get("has_injuries", True),
            "Ограничение по нагрузке",
            "Исключить осевые нагрузки на позвоночник и резкие прыжки! Работа только с умеренным весом."
        )

    def init_production(self):
        self.prod = ProductionSystem()

        # --- Подробные программы тренировок с техникой ---
        self.prod.add_rule(
            ["home", "weight_loss"],
            "ТРЕНИРОВКА: Домашний HIIT (45 сек работа / 15 сек отдых, 4 круга):\n"
            "    1. Джампинг Джек (активный прыжок с разведением рук и ног)\n"
            "    2. Приседания с выпрыгиванием (спина прямая, мягкая посадка на носки)\n"
            "    3. Отжимания от пола или колен (локти под 45 градусов к корпусу)\n"
            "    4. Планка на локтях (корпус в одну линию, пресс напряжен)"
        )
        self.prod.add_rule(
            ["home", "muscle_gain"],
            "ТРЕНИРОВКА: Домашний Силовой Комплекс:\n"
            "    1. Отжимания с паузой внизу 2 сек (4 подхода x 10-12 раз)\n"
            "    2. Болгарские выпады на стуле (4 подхода x 10 раз на каждую ногу)\n"
            "    3. Подтягивания / Австралийские подтягивания на столе (4 подхода x 8-10 раз)\n"
            "    4. Скручивания на пресс (3 подхода x 20 раз)"
        )
        self.prod.add_rule(
            ["home", "stamina"],
            "ТРЕНИРОВКА: Домашний Функционал (5 кругов без отдыха):\n"
            "    1. Берпи — 12 раз (упор присев, отжимание, прыжок вверх с хлопком)\n"
            "    2. Скалолаз (Mountain Climbers) — 40 сек (быстрый поднос коленей к груди)\n"
            "    3. Приседания — 20 раз\n"
            "    4. Планка с касанием плеч — 30 сек"
        )
        self.prod.add_rule(
            ["gym", "weight_loss"],
            "ТРЕНИРОВКА: Зал (Жиросжигание + Тонус):\n"
            "    • Блок 1: Интервальный бег / эллипс — 15 минут\n"
            "    • Блок 2 (Суперсет 4х15): Жим ногами в тренажере + Тяга верхнего блока к груди\n"
            "    • Блок 3 (Суперсет 4х15): Выпады с гантелями + Сгибания рук на пресс\n"
            "    • Блок 4: Заминка (ходьба в горку 10 мин)"
        )
        self.prod.add_rule(
            ["gym", "muscle_gain"],
            "ТРЕНИРОВКА: Тренажерный зал (Классический 3-дневный Сплит):\n"
            "    📌 День 1 (Грудь + Трицепс):\n"
            "       - Жим штанги лежа: 4 подхода x 8-10 раз (лопатки сведены, упор стопами)\n"
            "       - Жим гантелей на наклонной скамье: 3 подхода x 10-12 раз\n"
            "       - Отжимания на брусьях / Разгибание рук на блоке: 4 подхода x 12 раз\n"
            "    📌 День 2 (Спина + Бицепс):\n"
            "       - Подтягивания широким хватом: 4 подхода x 8-10 раз\n"
            "       - Тяга штанги в наклоне: 4 подхода x 10 раз (спина прогнута, тяга к поясу)\n"
            "       - Подъем штанги на бицепс: 3 подхода x 12 раз\n"
            "    📌 День 3 (Ноги + Плечи):\n"
            "       - Приседания со штангой: 4 подхода x 8-10 раз (колени смотрят на носки)\n"
            "       - Жим гантелей сидя вверх: 4 подхода x 10 раз\n"
            "       - Махи гантелями в стороны: 3 подхода x 15 раз"
        )
        self.prod.add_rule(
            ["gym", "stamina"],
            "ТРЕНИРОВКА: Зал (Кроссфит / Выносливость):\n"
            "    1. Гребной тренажер — 500 метров (мощный толчок ногами)\n"
            "    2. Махи гирей двух рук перед собой — 20 раз\n"
            "    3. Прыжки на тумбу (Box Jumps) — 15 раз\n"
            "    4. Броски медбола в стену (Wall Balls) — 15 раз (4-5 кругов на время)"
        )

    def calculate_nutrition(self, weight: float, goal: int) -> str:
        """Динамический расчет калорий и БЖУ под вес пользователя"""
        base_kcal = weight * 32

        if goal == 0:  # Похудение
            target_kcal = int(base_kcal * 0.82)
            protein = int(weight * 2.0)
            fats = int(weight * 0.9)
            carbs = int((target_kcal - (protein * 4 + fats * 9)) / 4)
            return (f"Дефицит калорий под вес {weight} кг -> ~{target_kcal} ккал/день.\n"
                    f"    📊 БЖУ: Белки {protein}г | Жиры {fats}г | Углеводы {carbs}г\n"
                    f"    🥗 Рацион: куриная грудка, яйца, нежирный творог, свежие овощи, гречка.")

        elif goal == 1:  # Набор массы
            target_kcal = int(base_kcal * 1.15)
            protein = int(weight * 2.1)
            fats = int(weight * 1.0)
            carbs = int((target_kcal - (protein * 4 + fats * 9)) / 4)
            return (f"Профицит калорий под вес {weight} кг -> ~{target_kcal} ккал/день.\n"
                    f"    📊 БЖУ: Белки {protein}г | Жиры {fats}г | Углеводы {carbs}г\n"
                    f"    🥩 Рацион: говядина, курица, рис, макароны тв. сортов, арахисовая паста, бананы.")

        else:  # Выносливость
            target_kcal = int(base_kcal)
            protein = int(weight * 1.6)
            fats = int(weight * 1.0)
            carbs = int((target_kcal - (protein * 4 + fats * 9)) / 4)
            return (f"Баланс энергии под вес {weight} кг -> ~{target_kcal} ккал/день.\n"
                    f"    📊 БЖУ: Белки {protein}г | Жиры {fats}г | Углеводы {carbs}г\n"
                    f"    🍌 Рацион: овсянка, бананы, рыбы, сухофрукты, обильное питьё (2.5+ л воды).")

    def predict_category(self, level, location, goal):
        if self.nn_model:
            X_input = pd.DataFrame([[level, location, goal]], columns=["level", "location", "goal"])
            res = self.nn_model.predict(X_input)[0]
            cats = {
                0: "Домашнее Кардио и HIIT 🏃‍♂️",
                1: "Классический Силовой Тренинг 🏋️‍♂️",
                2: "Калистеника (Собственный вес) 🤸‍♂️",
                3: "Функциональный Фитнес и Выносливость ⚡"
            }
            return cats.get(res, "Не определено")
        return "Модель не обучена"