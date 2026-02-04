# test_api.py
import requests
import json

BASE_URL = "http://localhost:8000/api"


def test_api():
    print("Тестирование API...")

    # 1. Создаем товары
    items = [
        {"name": "Ноутбук Dell XPS 15", "quantity": 50, "price": 150000.00},
        {"name": "Мышь беспроводная", "quantity": 200, "price": 2500.00},
    ]

    item_ids = []
    for item in items:
        response = requests.post(f"{BASE_URL}/nomenclature", json=item)
        if response.status_code == 201:
            item_data = response.json()
            item_ids.append(item_data["id"])
            print(f"Создан товар: {item_data['name']} (ID: {item_data['id']})")

    # 2. Создаем заказ
    order_response = requests.post(f"{BASE_URL}/orders", json={"client_id": 1})
    if order_response.status_code == 201:
        order_data = order_response.json()
        order_id = order_data["id"]
        print(f"Создан заказ: ID {order_id}")

    # 3. Добавляем товары в заказ
    if item_ids and order_id:
        for item_id in item_ids:
            add_item_data = {
                "order_id": order_id,
                "nomenclature_id": item_id,
                "quantity": 2
            }
            response = requests.post(f"{BASE_URL}/orders/add-item", json=add_item_data)
            if response.status_code == 200:
                result = response.json()
                print(f"Добавлен товар: {result}")

    print("\nТестирование завершено!")


if __name__ == "__main__":
    test_api()