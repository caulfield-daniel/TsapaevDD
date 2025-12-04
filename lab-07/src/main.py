from modules.analysis import run_comprehensive_analysis

if __name__ == "__main__":
    # Характеристики ПК
    pc_info = """
    Характеристики ПК для тестирования:
    - Процессор: AMD Ryzen 7 5800H 3.20GHz
    - Оперативная память: 16 GB DDR4
    - ОС: Windows 11
    - Python: 3.12.10
    """
    print(pc_info)

    run_comprehensive_analysis()
