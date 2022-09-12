import csv

PATH = "/home/andreas/PycharmProjects/fastApiProject/file_handling/uploaded_files/"

data = open(PATH + "research-and-development-survey-2021-csv.csv", mode="r", encoding="cp1252")  # or encoding="utf-8"

csv_data = csv.reader(data)

data_rows = list(csv_data)

new_dataset = []
for row in data_rows[1:]:
    new_dataset.append(row[1] + ": " + row[2])


file_to_output = open(PATH + "to_save_file.csv", mode="w", newline="")  # or mode="a" for append a new line
csv_writer = csv.writer(file_to_output, delimiter=";")
csv_writer.writerows(new_dataset)
file_to_output.close()
