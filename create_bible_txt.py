import os
import sys

def concatenate_text_files(input_dir, output_file):
    all_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                all_files.append(os.path.join(root, file))

    all_files.sort()

    concatenated = []
    for file_path in all_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            concatenated.append(file_content)

    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write('\n\n'.join(concatenated))

input_directory = "bible_texts/"
output_file_name = "bible.txt"
output_file_path = os.path.join(input_directory, '../', output_file_name)

if __name__ == '__main__':
    from time import perf_counter
    
    start = perf_counter()
    
    concatenate_text_files(input_directory, output_file_path)

    print(f"Concatenation complete. Output file: {output_file_path}")
    
    elapsed_time = perf_counter() - start
    print(f'Elapsed time: {elapsed_time * 1e3:.0f} milisecs.')
