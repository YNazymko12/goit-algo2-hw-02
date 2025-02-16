from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Перетворюємо вхідні дані на об'єкти PrintJob
    jobs = [PrintJob(**job) for job in print_jobs]
    jobs.sort(key=lambda x: (x.priority, x.print_time))  # Сортуємо за пріоритетом, потім за часом друку
    
    print_order = []
    total_time = 0
    
    while jobs:
        batch = []
        batch_volume = 0
        batch_time = 0
        
        for job in jobs[:]:  # Копіюємо список, щоб змінювати вихідний
            if batch_volume + job.volume <= constraints["max_volume"] and len(batch) < constraints["max_items"]:
                batch.append(job)
                batch_volume += job.volume
                batch_time = max(batch_time, job.print_time)
                jobs.remove(job)
        
        print_order.extend(job.id for job in batch)
        total_time += batch_time
    
    return {
        "print_order": print_order,
        "total_time": total_time
    }

if __name__ == "__main__":
    constraints = {
        "max_volume": 300,
        "max_items": 2
    }
    
    test_cases = [
    ([
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ], "однаковий пріоритет"),

    ([
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ], "різні пріоритети"),

    ([
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ], "перевищення обмежень")
]
    
    for test, description in test_cases:
        print(f"\nТест ({description}):")
        result = optimize_printing(test, constraints)
        print(f"Порядок друку: {result['print_order']}")
        print(f"Загальний час: {result['total_time']} хвилин")
