def extract_unique_ordered(input_file, output_file):
    unique_ids = []
    seen = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and line != "Идентификатор" and line not in seen:
                seen.add(line)
                unique_ids.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        for id_value in unique_ids:
            f.write(id_value + '\n')

    print(f"Уникальных значений: {len(unique_ids)}")


# Использование
extract_unique_ordered("Идентификаторы.txt", "unique_ids_ordered.txt")