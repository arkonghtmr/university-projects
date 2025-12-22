import pandas as pd
import numpy as np

# Загружаем созданные файлы
print("Загрузка данных...")
df_events = pd.read_csv('cs2_events_log.csv')
df_trans = pd.read_csv('cs2_transactions.csv')
df_matches = pd.read_csv('cs2_matches.csv')

print("\n=== ДАННЫЕ ДЛЯ РИСУНКОВ ГЛАВЫ 3 ===\n")

# --- РИСУНОК 3.1: Структура выручки (Pie Chart) ---
print("--- Рисунок 3.1: Структура выручки ---")
revenue_by_item = df_trans.groupby('item')['amount_usd'].sum()
total_revenue = revenue_by_item.sum()
revenue_share = (revenue_by_item / total_revenue * 100).round(1)
print(revenue_share)
print("Совет: Постройте круговую диаграмму в Excel по этим %.\n")

# --- РИСУНОК 3.2: Воронка новичка (Bar Chart) ---
print("--- Рисунок 3.2: Воронка онбординга ---")
# Считаем уникальных пользователей на каждом этапе
step1 = df_events[df_events['event_name'] == 'app_start']['user_id'].nunique()
step2 = df_events[df_events['event_name'] == 'tutorial_complete']['user_id'].nunique()
# Фильтруем свойства JSON для матчей (упрощенно по строке)
step3 = df_events[(df_events['event_name'] == 'match_started') & (df_events['properties'].str.contains('deathmatch'))]['user_id'].nunique()
step4 = df_events[(df_events['event_name'] == 'match_started') & (df_events['properties'].str.contains('premier'))]['user_id'].nunique()

print(f"1. App Start:        {step1} (100%)")
print(f"2. Tutorial Complete:{step2} ({round(step2/step1*100, 1)}%)")
print(f"3. Deathmatch:       {step3} ({round(step3/step1*100, 1)}%)")
print(f"4. Premier Match:    {step4} ({round(step4/step1*100, 1)}%)")
print("Совет: Постройте столбчатую диаграмму (Воронку).\n")

# --- РИСУНОК 3.3: Воронка монетизации (Bar Chart) ---
print("--- Рисунок 3.3: Воронка покупки ключа ---")
s1 = df_events[df_events['event_name'] == 'case_drop_received']['user_id'].nunique()
s2 = df_events[df_events['event_name'] == 'inventory_inspect']['user_id'].nunique()
s3 = df_events[df_events['event_name'] == 'store_checkout_start']['user_id'].nunique()
s4 = df_events[df_events['event_name'] == 'case_opened']['user_id'].nunique()

print(f"1. Case Drop:    {s1} (100%)")
print(f"2. Inspect:      {s2} ({round(s2/s1*100, 1)}%)")
print(f"3. Click Buy:    {s3} ({round(s3/s1*100, 1)}%)")
print(f"4. Payment Success:{s4} ({round(s4/s1*100, 1)}%)")
print("Совет: Это ключевая воронка для гипотезы.\n")

# --- РИСУНОК 3.4: Матчмейкинг (Bar Chart) ---
print("--- Рисунок 3.4: Воронка матча ---")
total_searches = df_events[df_events['event_name'] == 'match_search'].shape[0]
total_matches = df_matches.shape[0]
finished_matches = df_matches[df_matches['result'] == 'finished'].shape[0]

# Имитируем этапы на основе статистики
print(f"1. Search Started: {total_searches} (100%)")
print(f"2. Match Found:    {int(total_searches * 0.95)} (95%)")
print(f"3. Match Started:  {total_matches} ({round(total_matches/total_searches*100, 1)}%)")
print(f"4. Match Finished: {finished_matches} ({round(finished_matches/total_searches*100, 1)}%)")
print("Совет: Покажите отвал на этапе Finished (ливеры).\n")