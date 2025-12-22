import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta
import random
import json
from tqdm import tqdm

SCENARIO_CONFIG = {
    'n_users': 50000,
    'simulation_days': 180,
    'start_date': '2025-01-01',

    'prime_users_ratio': 0.30,

    'tutorial_start_rate': 0.90,
    'first_deathmatch_rate': 0.60,
    'first_premier_rate': 0.15,

    'case_drop_chance': 0.10,
    'inspect_case_rate': 0.40,
    'click_buy_key_rate': 0.05,
    'payment_success_rate': 0.95,

    'match_accept_rate': 0.95,
    'match_finish_rate': 0.75,

    'price_key': 2.50,
    'price_prime': 15.00,
    'price_operation': 10.00
}

print("Запуск генерации данных для Counter-Strike 2...")

print("Шаг 1/4: Генерация профилей игроков...")

np.random.seed(42)
random.seed(42)

user_ids = [str(uuid.uuid4()) for _ in range(SCENARIO_CONFIG['n_users'])]
start_dt = datetime.strptime(SCENARIO_CONFIG['start_date'], '%Y-%m-%d')

countries = ['RU', 'US', 'BR', 'DE', 'PL', 'CN', 'TR']
segments = ['Achiever', 'Killer', 'Socializer', 'Explorer']

df_players = pd.DataFrame({
    'user_id': user_ids,
    'install_date': [start_dt.date() + timedelta(days=np.random.randint(0, 60)) for _ in
                     range(SCENARIO_CONFIG['n_users'])],
    'country': np.random.choice(countries, SCENARIO_CONFIG['n_users'], p=[0.25, 0.15, 0.15, 0.10, 0.10, 0.15, 0.10]),
    'segment': np.random.choice(segments, SCENARIO_CONFIG['n_users'], p=[0.3, 0.3, 0.2, 0.2]),

    # CS2 Специфика
    'has_prime': np.random.choice([True, False], SCENARIO_CONFIG['n_users'],
                                  p=[SCENARIO_CONFIG['prime_users_ratio'], 1 - SCENARIO_CONFIG['prime_users_ratio']]),
    'trust_factor': np.random.choice(['Green', 'Yellow', 'Red'], SCENARIO_CONFIG['n_users'], p=[0.7, 0.2, 0.1]),
    'rank_elo': 0
})

print("Шаг 2/4: Симуляция игровых сессий и воронок...")

all_events = []
all_transactions = []
all_matches = []

for idx, user in tqdm(df_players.iterrows(), total=df_players.shape[0]):

    if user['has_prime']:
        lifespan = int(np.random.gamma(30, 5))
    else:
        lifespan = int(np.random.lognormal(2, 0.8))

    user_install_dt = datetime.combine(user['install_date'], datetime.min.time())

    onboarding_stage = 0

    for day in range(lifespan):
        current_date = user_install_dt + timedelta(days=day)
        if (current_date - start_dt).days > SCENARIO_CONFIG['simulation_days']:
            break

        play_prob = 1.0 if day == 0 else 0.8 / (1 + 0.1 * day)
        if random.random() > play_prob:
            continue

        session_id = str(uuid.uuid4())
        ts = current_date + timedelta(hours=random.randint(12, 23), minutes=random.randint(0, 59))

        if day == 0:
            all_events.append({'user_id': user['user_id'], 'event_name': 'app_start', 'timestamp': ts})

            if random.random() < SCENARIO_CONFIG['tutorial_start_rate']:
                ts += timedelta(minutes=15)
                all_events.append({'user_id': user['user_id'], 'event_name': 'tutorial_complete', 'timestamp': ts})
                onboarding_stage = 1

                if random.random() < SCENARIO_CONFIG['first_deathmatch_rate']:
                    ts += timedelta(minutes=5)
                    all_events.append({'user_id': user['user_id'], 'event_name': 'match_started', 'timestamp': ts,
                                       'properties': {'mode': 'deathmatch'}})
                    onboarding_stage = 2

                    premier_chance = SCENARIO_CONFIG['first_premier_rate']
                    if not user['has_prime']: premier_chance *= 0.1

                    if random.random() < premier_chance:
                        ts += timedelta(minutes=20)
                        all_events.append({'user_id': user['user_id'], 'event_name': 'match_started', 'timestamp': ts,
                                           'properties': {'mode': 'premier'}})
                        onboarding_stage = 3
            continue


        matches_count = np.random.poisson(2)

        for m in range(matches_count):
            ts += timedelta(minutes=2)
            all_events.append({'user_id': user['user_id'], 'event_name': 'match_search', 'timestamp': ts})

            if random.random() < SCENARIO_CONFIG['match_accept_rate']:
                ts += timedelta(seconds=30)
                all_events.append({'user_id': user['user_id'], 'event_name': 'match_accept', 'timestamp': ts})

                is_finished = random.random() < SCENARIO_CONFIG['match_finish_rate']
                match_duration = random.randint(15, 45)  # минут

                ts += timedelta(minutes=match_duration)
                match_res = 'finished' if is_finished else 'abandoned'

                all_matches.append({
                    'match_id': str(uuid.uuid4()),
                    'user_id': user['user_id'],
                    'mode': 'premier' if user['has_prime'] else 'casual',
                    'result': match_res,
                    'timestamp': ts
                })

                if is_finished and random.random() < SCENARIO_CONFIG['case_drop_chance']:
                    ts += timedelta(seconds=10)
                    all_events.append({'user_id': user['user_id'], 'event_name': 'case_drop_received', 'timestamp': ts,
                                       'properties': {'case_type': 'Kilowatt Case'}})

                    # Просмотр кейса
                    if random.random() < SCENARIO_CONFIG['inspect_case_rate']:
                        ts += timedelta(seconds=15)
                        all_events.append(
                            {'user_id': user['user_id'], 'event_name': 'inventory_inspect', 'timestamp': ts})

                        if random.random() < SCENARIO_CONFIG['click_buy_key_rate']:
                            ts += timedelta(seconds=5)
                            all_events.append(
                                {'user_id': user['user_id'], 'event_name': 'store_checkout_start', 'timestamp': ts})

                            if random.random() < SCENARIO_CONFIG['payment_success_rate']:
                                ts += timedelta(seconds=10)
                                all_transactions.append({
                                    'trans_id': str(uuid.uuid4()),
                                    'user_id': user['user_id'],
                                    'item': 'case_key',
                                    'amount_usd': SCENARIO_CONFIG['price_key'],
                                    'timestamp': ts
                                })
                                all_events.append(
                                    {'user_id': user['user_id'], 'event_name': 'case_opened', 'timestamp': ts})
                            else:
                                all_events.append(
                                    {'user_id': user['user_id'], 'event_name': 'payment_error', 'timestamp': ts})

        if not user['has_prime'] and day > 3 and day < 10:
            if random.random() < 0.05:
                ts += timedelta(minutes=5)
                all_transactions.append({
                    'trans_id': str(uuid.uuid4()),
                    'user_id': user['user_id'],
                    'item': 'prime_status',
                    'amount_usd': SCENARIO_CONFIG['price_prime'],
                    'timestamp': ts
                })
                user['has_prime'] = True

print("Шаг 3/4: Формирование датафреймов...")

df_events = pd.DataFrame(all_events)
df_transactions = pd.DataFrame(all_transactions)
df_matches = pd.DataFrame(all_matches)

print("Шаг 4/4: Сохранение CSV файлов...")

df_players.to_csv('cs2_players.csv', index=False)
df_events.to_csv('cs2_events_log.csv', index=False)
df_transactions.to_csv('cs2_transactions.csv', index=False)
df_matches.to_csv('cs2_matches.csv', index=False)

print("\nГЕНЕРАЦИЯ ЗАВЕРШЕНА!")
print(f"Игроков: {len(df_players)}")
print(f"Событий: {len(df_events)}")
print(f"Транзакций: {len(df_transactions)}")
print(f"Матчей: {len(df_matches)}")
print("\nФайлы сохранены в текущей директории. Можете использовать их для построения графиков в Главе 3.")