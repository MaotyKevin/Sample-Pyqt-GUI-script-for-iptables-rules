import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTableWidget, QHBoxLayout, QStackedLayout, QMessageBox, QDialog, QTableWidgetItem , QTextEdit , QListWidget

import subprocess

"""class ModifyRuleDialog(QDialog):
    def __init__(self, rule_number, parent=None):
        super().__init__(parent)
        
        self.rule_number = rule_number
        
        self.protocol_input = QLineEdit()
        self.source_ip_input = QLineEdit()
        self.destination_ip_input = QLineEdit()
        self.port_input = QLineEdit()
        
        self.modify_button = QPushButton("Modify")
        self.modify_button.clicked.connect(self.modify_rule)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Modifying rule number: {rule_number}"))
        layout.addWidget(QLabel("Protocol:"))
        layout.addWidget(self.protocol_input)
        layout.addWidget(QLabel("Source IP:"))
        layout.addWidget(self.source_ip_input)
        layout.addWidget(QLabel("Destination IP:"))
        layout.addWidget(self.destination_ip_input)
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.port_input)
        layout.addWidget(self.modify_button)
        
        self.setLayout(layout)
        
    def modify_rule(self):
        new_protocol = self.protocol_input.text()
        new_source_ip = self.source_ip_input.text()
        new_destination_ip = self.destination_ip_input.text()
        new_port = self.port_input.text()
        
        # Construct and execute the iptables command to modify the rule
        command = f"sudo iptables -R {self.chain_name} {self.rule_number} -p {new_protocol} -s {new_source_ip} -d {new_destination_ip} --dport {new_port} -j ACCEPT"
        result = self.run_iptables_command(command)
        self.update_table()
        
        self.close()
"""
class RulePage(QWidget):
    def __init__(self, chain_name, run_iptables_command):
        super().__init__()

        self.chain_name = chain_name
        self.run_iptables_command = run_iptables_command

      

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        
        self.add_button = QPushButton("Ajouter une regle")
        self.add_button.clicked.connect(self.add_rule)
       
        layout.addWidget(self.add_button)

        self.rulePageLabel = QLabel("Règles existantes:")
        self.existing_rules_list = QListWidget()
        self.delete_button = QPushButton("Supprimer la règle")
        self.delete_button.clicked.connect(self.delete_rule)
        layout.addWidget(self.rulePageLabel)
        layout.addWidget(self.existing_rules_list)
        layout.addWidget(self.delete_button)
      

        self.setLayout(layout)
        self.update_rules_list()

        
    def add_rule(self):
        dialog = AddRuleDialog(self.chain_name, self.run_iptables_command, self)
        dialog.exec_()

    def update_rules_list(self):
        result = self.run_iptables_command(f"sudo iptables -L {self.chain_name} -n --line-numbers -v")
        lines = result.splitlines()
        existing_rules = [line.strip() for line in lines if line.strip()]
        self.existing_rules_list.clear()
        self.existing_rules_list.addItems(existing_rules)
        
    def delete_rule(self):
        selected_item = self.existing_rules_list.currentItem()
        if selected_item is not None:
            rule_number = selected_item.text().split()[0]
            confirmation = QMessageBox.question(
                self, "Confirmation", "Êtes-vous sûr de vouloir supprimer cette règle ?", QMessageBox.Yes | QMessageBox.No
            )
            if confirmation == QMessageBox.Yes:
                command = f"sudo iptables -D {self.chain_name} {rule_number}"
                result = self.run_iptables_command(command)
                print(result)
                self.update_rules_list()  # Update the list after deleting the rule
                QMessageBox.information(
                    self, "Règle supprimée", "La règle personnalisée a été supprimée avec succès."
                )
        else:
            QMessageBox.warning(self, "Sélection requise", "Veuillez sélectionner une règle à supprimer.")
                    
        
class ReadFilePage(QWidget):
    def __init__(self):
        super().__init__()
        self.text_edit = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        
        self.button1 = QPushButton("Button 1")
        self.button1.clicked.connect(self.button1_clicked)
        
        self.button2 = QPushButton("Button 2")
        self.button2.clicked.connect(self.button2_clicked)
        
        self.button3 = QPushButton("Button 3")
        self.button3.clicked.connect(self.button3_clicked)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        
        self.setLayout(layout)
    
    def display_file_content(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_edit.setPlainText(content)
        except Exception as e:
            self.text_edit.setPlainText(str(e))
            
    def button1_clicked(self):
        pass
    
    def button2_clicked(self):
        pass
    
    def button3_clicked(self):
        pass

class AddRuleDialog(QDialog):
    def __init__(self, chain_name, run_iptables_command, parent=None):
        super().__init__(parent)
        
        self.chain_name = chain_name
        self.run_iptables_command = run_iptables_command
        
        self.protocol_input = QLineEdit()
        self.source_ip_input = QLineEdit()
        self.destination_ip_input = QLineEdit()
        self.port_input = QLineEdit()
        
        self.add_button = QPushButton("Ajouter")
        self.add_button.clicked.connect(self.add_rule)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Ajout de nouvelle regle {chain_name}"))
        layout.addWidget(QLabel("Protocol:"))
        layout.addWidget(self.protocol_input)
        layout.addWidget(QLabel("Source IP:"))
        layout.addWidget(self.source_ip_input)
        layout.addWidget(QLabel("Destination IP:"))
        layout.addWidget(self.destination_ip_input)
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.port_input)
        layout.addWidget(self.add_button)
        
        self.setLayout(layout)
        
    def add_rule(self):
        new_protocol = self.protocol_input.text()
        new_source_ip = self.source_ip_input.text()
        new_destination_ip = self.destination_ip_input.text()
        new_port = self.port_input.text()
        
        # Construct and execute the iptables command to add the new rule
        command = f"sudo iptables -A {self.chain_name} -p {new_protocol} -s {new_source_ip} -d {new_destination_ip} --dport {new_port} -j ACCEPT"
        result = self.run_iptables_command(command)
        self.parent().update_table()
        
        self.close()
        
class AddCustomRulePage(QWidget):
    def __init__(self, chain_name, run_iptables_command):
        super().__init__()

        self.chain_name = chain_name
        self.run_iptables_command = run_iptables_command

        self.rule_input = QTextEdit()
        self.add_button = QPushButton("Ajouter la règle")
        self.add_button.clicked.connect(self.add_custom_rule)

        self.existing_rules_label = QLabel("Règles existantes:")
        self.existing_rules_list = QListWidget()
        self.delete_button = QPushButton("Supprimer la règle")
        self.delete_button.clicked.connect(self.delete_custom_rule)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Ajouter une règle personnalisée à la chaîne {chain_name}"))
        layout.addWidget(QLabel("Entrez la règle:"))
        layout.addWidget(self.rule_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.existing_rules_label)
        layout.addWidget(self.existing_rules_list)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

        # Populate existing rules list
        self.update_existing_rules_list()

    def update_existing_rules_list(self):
        result = self.run_iptables_command(f"sudo iptables -L {self.chain_name} -n --line-numbers -v")
        lines = result.splitlines()
        existing_rules = [line.strip() for line in lines if line.strip()]
        self.existing_rules_list.clear()
        self.existing_rules_list.addItems(existing_rules)

    def add_custom_rule(self):
        new_rule = self.rule_input.toPlainText()
        # Construct the iptables command without executing it
        command = f"sudo iptables -A {self.chain_name} {new_rule}"
        print("Executing command:", command)  # Print the command for debugging
        result = self.run_iptables_command(command)
        print(result)
        self.update_existing_rules_list()  # Update the list after adding the new rule
        QMessageBox.information(self, "Règle ajoutée", "La règle personnalisée a été ajoutée avec succès.")
        self.rule_input.clear()

    def delete_custom_rule(self):
        selected_item = self.existing_rules_list.currentItem()
        if selected_item is not None:
            rule_number = selected_item.text().split()[0]
            command = f"sudo iptables -D {self.chain_name} {rule_number}"
            result = self.run_iptables_command(command)
            print(result)
            self.update_existing_rules_list()  # Update the list after deleting the rule
            QMessageBox.information(self, "Règle supprimée", "La règle personnalisée a été supprimée avec succès.")
        else:
            QMessageBox.warning(self, "Sélection requise", "Veuillez sélectionner une règle à supprimer.")


class FirewallGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestion de pare feu")
        self.setGeometry(100, 100, 800, 400)
        
        self.setStyleSheet("QMainWindow {background-color: white;} QPushButton {background-color: #1B1B1B; color: white; border: none; padding: 5px 10px; border-radius: 3px;} QListWidget {background-color: white;} QMainWindow::title {background-color: red; color: black; padding: 5px; border: none;}")

        self.input_page = RulePage("INPUT", self.run_iptables_command)
        self.forward_page = RulePage("FORWARD", self.run_iptables_command)
        self.output_page = RulePage("OUTPUT", self.run_iptables_command)
        self.read_file_page = ReadFilePage()
        self.custom_page = AddCustomRulePage("CUSTOM" , self.run_iptables_command)
        
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.input_page)
        self.stacked_layout.addWidget(self.forward_page)
        self.stacked_layout.addWidget(self.output_page)
        self.stacked_layout.addWidget(self.read_file_page)
        
        # Create navigation buttons
        self.input_button = QPushButton("Input")
        self.forward_button = QPushButton("Forward")
        self.output_button = QPushButton("Output")
        #self.refresh_button = QPushButton("Refresh")
        self.dmz_button = QPushButton("DMZ")
        self.custom_rule_button = QPushButton("Règle personnalisée")
        self.custom_rule_button.clicked.connect(self.show_custom_rule_page)
        
        
        self.dmz_button.clicked.connect(lambda: self.show_read_file_page(file_path = "coucou.txt"))
        
      
        
        self.input_button.clicked.connect(self.show_input_page)
        self.forward_button.clicked.connect(self.show_forward_page)
        self.output_button.clicked.connect(self.show_output_page)
     
        #self.refresh_button.clicked.connect(self.refresh_current_page)
        
        nav_layout = QVBoxLayout()
        nav_layout.addWidget(self.input_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.output_button)
        nav_layout.addWidget(self.dmz_button)
        nav_layout.addWidget(self.custom_rule_button)
        #nav_layout.addWidget(self.refresh_button)
        
        main_layout = QHBoxLayout()
        main_layout.addLayout(nav_layout)
        main_layout.addLayout(self.stacked_layout)
        
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        self.show_input_page()  # Show the input page by default
        
    def show_custom_rule_page(self):
        custom_rule_page = AddCustomRulePage("CUSTOM", self.run_iptables_command)
        self.stacked_layout.addWidget(custom_rule_page)
        self.stacked_layout.setCurrentWidget(custom_rule_page)

        
    def show_read_file_page(self, file_path):
        self.stacked_layout.setCurrentWidget(self.read_file_page)
        self.read_file_page.display_file_content(file_path)
        
    def show_input_page(self):
        self.stacked_layout.setCurrentWidget(self.input_page)
        self.refresh_current_page()
        
    def show_forward_page(self):
        self.stacked_layout.setCurrentWidget(self.forward_page)
        self.refresh_current_page()
        
    def show_output_page(self):
        self.stacked_layout.setCurrentWidget(self.output_page)
        self.refresh_current_page()
    
  
        
        
    def run_iptables_command(self, command):
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return result.stderr
        except Exception as e:
            return str(e)
        
    def refresh_current_page(self):
        current_page = self.stacked_layout.currentWidget()
        if isinstance(current_page, RulePage):
            current_page.update_rules_list()

def main():
    app = QApplication(sys.argv)
    window = FirewallGUI()
    window.show()
    
    
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
