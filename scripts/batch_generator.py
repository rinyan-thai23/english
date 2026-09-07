"""
NGSL 2800 段階的3例文生成・更新ユーティリティ
Usage:
  python scripts/batch_generator.py --status
  python scripts/batch_generator.py --list 21 40
  python scripts/batch_generator.py --update examples_batch.json
"""

import argparse
import csv
import json
import os
import sys

# WindowsコンソールのUTF-8対応
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ngsl_2800.csv')

def get_status():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))

    total = len(reader)
    with_examples = sum(1 for r in reader if r.get('example_1_en', '').strip())
    
    print(f"========================================")
    print(f" NGSL 2,800語 例文進捗ステータス")
    print(f"========================================")
    print(f" 総単語数: {total} 語")
    print(f" 例文作成済み: {with_examples} 語 ({(with_examples/total*100):.1f}%)")
    print(f" 未作成: {total - with_examples} 語")
    
    # 最初の未作成単語番号
    first_missing = None
    for r in reader:
        if not r.get('example_1_en', '').strip():
            first_missing = r['id']
            break
    if first_missing:
        print(f" 次に作成すべき単語番号: #{first_missing}")
    print(f"========================================")

def list_words(start_id, end_id):
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))

    print(f"--- 単語リスト #{start_id} 〜 #{end_id} ---")
    for r in reader:
        w_id = int(r['id'])
        if start_id <= w_id <= end_id:
            has_ex = "✓" if r.get('example_1_en', '').strip() else " "
            print(f"[{has_ex}] #{w_id:4d}: {r['word']:15s} ({r['part_of_speech']:10s}) - {r['meaning_ja']}")

def update_examples_from_json(json_file):
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found.")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    updated_count = 0
    for r in rows:
        w_id_str = str(r['id'])
        w_word = r['word'].lower()
        
        entry = data.get(w_id_str) or data.get(w_word)
        if entry:
            r['example_1_en'] = entry.get('example_1_en', r['example_1_en'])
            r['example_1_ja'] = entry.get('example_1_ja', r['example_1_ja'])
            r['example_2_en'] = entry.get('example_2_en', r['example_2_en'])
            r['example_2_ja'] = entry.get('example_2_ja', r['example_2_ja'])
            r['example_3_en'] = entry.get('example_3_en', r['example_3_en'])
            r['example_3_ja'] = entry.get('example_3_ja', r['example_3_ja'])
            updated_count += 1

    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully updated {updated_count} words in {CSV_PATH}")

def main():
    parser = argparse.ArgumentParser(description="NGSL 2800 段階的3例文生成・更新ツール")
    parser.add_argument('--status', action='store_true', help="現在の例文作成進捗を表示")
    parser.add_argument('--list', nargs=2, type=int, metavar=('START', 'END'), help="指定番号範囲の単語を一覧表示")
    parser.add_argument('--update', type=str, metavar='JSON_FILE', help="JSONファイルから3例文を一括反映")
    args = parser.parse_args()

    if args.status:
        get_status()
    elif args.list:
        list_words(args.list[0], args.list[1])
    elif args.update:
        update_examples_from_json(args.update)
    else:
        get_status()

if __name__ == '__main__':
    main()
