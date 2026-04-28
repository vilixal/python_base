def remove_every_second_symbol_streaming(input_file, output_file):
    """Обрабатывает большой файл построчно"""
    with open(input_file, 'r', encoding='utf-8') as fin, \
            open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            # Удаляем каждый второй символ в строке
            processed_line = line[1::2]
            fout.write(processed_line)


remove_every_second_symbol_streaming(r'D:\temp\pochta\sovc\file.txt', r'D:\temp\pochta\sovc\file_out2.txt')