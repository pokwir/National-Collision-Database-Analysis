import csv
import sys
import os

def create_csv_from_text(input_text, output_filename):
    data = [line.split(maxsplit=1) for line in input_text.strip().split('\n')[1:]]

    output_path = os.path.join(os.getcwd(), output_filename)

    with open(output_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Code", "Description"])
        csv_writer.writerows(data)

if __name__ == "__main__":
    input_text = input("Enter the input text:\n")

    if not input_text:
        print("Input text is empty. Exiting.")
        sys.exit(1)

    output_filename = input("Enter the desired CSV file name (without extension):\n")

    if not output_filename.endswith('.csv'):
        output_filename += '.csv'

    create_csv_from_text(input_text, output_filename)
    print(f"CSV file '{output_filename}' has been created.")