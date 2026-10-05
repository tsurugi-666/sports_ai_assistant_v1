import msvcrt
from expert_system import FitnessExpertSystem

# Цветовые ANSI коды для консоли
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main():
    ai = FitnessExpertSystem()
    print(CYAN + BOLD + "=" * 65 + RESET)
    print(GREEN + BOLD + " 🚀  ИИ-ПОМОЩНИК ПО ПОДБОРУ ТРЕНИРОВОК И СПОРТИВНЫХ УПРАЖНЕНИЙ  🚀 " + RESET)
    print(CYAN + BOLD + "=" * 65 + RESET)

    # 1. Ввод данных
    print(YELLOW + BOLD + "\n[Шаг 1] Введите параметры пользователя:" + RESET)
    weight = float(input(" ⚖️  Ваш вес (в кг): "))
    level = int(input(" 📊 Ваш уровень (0 - Новичок, 1 - Средний, 2 - Профи): "))
    location = int(input(" 🏠 Локация (0 - Дом, 1 - Тренажерный зал): "))
    goal = int(input(" 🎯 Главная цель (0 - Похудение, 1 - Набор массы, 2 - Выносливость): "))
    injuries = input(" ⚠️ Есть ли травмы/ограничения? (да/нет): ").strip().lower() == "да"

    print("\n" + CYAN + BOLD + "=" * 65 + RESET)
    print(MAGENTA + BOLD + "                     ✨ РЕЗУЛЬТАТЫ АНАЛИЗА ИИ ✨                    " + RESET)
    print(CYAN + BOLD + "=" * 65 + RESET)

    # 2. Нейронная сеть
    rec_category = ai.predict_category(level, location, goal)
    print(f"\n🧠 {BOLD}[Нейронная сеть]:{RESET} Рекомендуемый тип -> {GREEN}{BOLD}{rec_category}{RESET}")

    # 3. Логический вывод (AND, OR, NOT)
    ai.logic.set_fact("is_beginner", level == 0)
    ai.logic.set_fact("has_injuries", injuries)
    explanations = ai.logic.infer()

    print(f"\n📋 {BOLD}[Рекомендации по безопасности и режиму]:{RESET}")
    if explanations:
        for exp in explanations:
            clean_exp = exp.split("]: ")[-1] if "]: " in exp else exp
            print(f"  {RED}• {clean_exp}{RESET}")
    else:
        print(f"  {GREEN}• Ограничений не выявлено. Можете выполнять стандартную нагрузку.{RESET}")

    # 4. Продукционный вывод (Тренировки и Питание)
    facts_set = set()
    facts_set.add("home" if location == 0 else "gym")
    if goal == 0:
        facts_set.add("weight_loss")
    elif goal == 1:
        facts_set.add("muscle_gain")
    else:
        facts_set.add("stamina")

    prod_res = ai.prod.forward_chaining(facts_set)
    nutrition_res = ai.calculate_nutrition(weight, goal)

    print(f"\n🏋️‍♂️ {BOLD}[Подробная программа тренировок]:{RESET}")
    if prod_res:
        for res in prod_res:
            if res.startswith("ТРЕНИРОВКА:"):
                clean_tr = res.replace('ТРЕНИРОВКА: ', '')
                print(f"{YELLOW}{clean_tr}{RESET}")

    print(f"\n🥗 {BOLD}[Индивидуальные рекомендации по Питанию]:{RESET}")
    print(f"  {GREEN}{nutrition_res}{RESET}")

    # 5. База знаний
    print(f"\n📚 {BOLD}[Справка из Базы Знаний]:{RESET}")

    relation_translations = {
        "targets": "тренирует",
        "requires": "требует"
    }

    sem_relations = ai.sem_net.get_related_objects("Отжимания")
    formatted_relations = ", ".join([
        f"{relation_translations.get(rel, rel)} {target}"
        for rel, target in sem_relations
    ])

    print(f"  • {CYAN}Семантическая сеть ('Отжимания'):{RESET} {formatted_relations}")

    frame_pushups = ai.kb_frames.find_frame("Отжимания")
    if frame_pushups:
        print(
            f"  • {CYAN}Фрейм 'Отжимания':{RESET} Наследует тип '{frame_pushups.get_slot('тип')}', инвентарь '{frame_pushups.get_slot('инвентарь')}'")

    print("\n" + CYAN + BOLD + "=" * 65 + RESET)


if __name__ == "__main__":
    main()
    print("\n" + "=" * 50)
    print("Нажмите ESC для выхода из программы...")

    while True:
        # Проверяем, нажата ли клавиша
        if msvcrt.kbhit():
            # Читаем символ нажатой клавиши
            key = msvcrt.getch()
            # Код клавиши Esc — b'\x1b'
            if key == b'\x1b':
                break