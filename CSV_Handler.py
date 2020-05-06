import csv
from pathlib import Path

class CSV_Handler():
    
    
    def __init__(self, main):
        
        self.main = main
        self.file_name = Path(str(self.main.dir) + "/result_table.csv")
        
        
    def create_csv(self):
        
        with open(self.file_name,'a', newline = '') as f:
                
                writer = csv.writer(f)
                writer.writerow(["Total Count, Dart Count, X, Y"])
        
        
    def count_lines(self):
        
        if self.file_name.exists() == False:
            
            self.main.text_display.print_to_display("CSV was not found!")
            
            self.create_csv()
   
            self.main.text_display.print_to_display("Created new CSV file")
            
            self.count_lines()

        else:
            
            self.main.total_count = sum(1 for row in open(self.file_name)) - 1
            self.main.frame_UI_right.entry_total_count.delete(0,8)
            self.main.frame_UI_right.entry_total_count.insert(0, str(self.main.total_count))