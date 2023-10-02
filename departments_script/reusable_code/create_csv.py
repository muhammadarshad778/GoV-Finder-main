import csv
def create_csv(data, filename, header):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)  # Write the header row
            for row in data:
                csv_writer.writerow(row)
        print(f"Data saved to '{filename}'.")
    except Exception as e:
        print(f"Error: {e}")