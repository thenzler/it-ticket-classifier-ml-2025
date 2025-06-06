#!/usr/bin/env python3
"""
IT-Ticket Beispieldaten Generator
Erstellt realistische Testdaten für das Machine Learning Modell

ATL - HF Wirtschaftsinformatik
Autor: Benjamin Peter
Datum: 08.06.2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import csv
import os

def generate_realistic_tickets(n_samples=1000):
    """
    Generiert realistische IT-Ticket Beispieldaten
    """
    np.random.seed(42)
    random.seed(42)
    
    # Hardware Issues - Realistische Problembeschreibungen
    hardware_issues = [
        {
            "title": "Laptop won't start - black screen",
            "description": "My laptop shows a black screen when I press the power button. The power LED is on but nothing displays on screen. Tried restarting multiple times but same issue persists.",
            "priority": "High"
        },
        {
            "title": "Printer not working - paper jam error",
            "description": "Office printer shows paper jam error but I can't find any jammed paper. Tried turning off and on but error persists. Multiple users affected.",
            "priority": "Medium"
        },
        {
            "title": "Monitor flickering and display distorted",
            "description": "My monitor keeps flickering and the display is distorted with weird colors. Started happening this morning. Makes it impossible to work.",
            "priority": "High"
        },
        {
            "title": "Keyboard keys not responding properly",
            "description": "Several keys on my keyboard are not working. The 'e', 'r', and spacebar require multiple presses. Need replacement keyboard urgently.",
            "priority": "Medium"
        },
        {
            "title": "Mouse cursor jumping erratically",
            "description": "Mouse cursor moves erratically across screen and sometimes doesn't respond to clicks. Tried different mouse pad but same issue.",
            "priority": "Low"
        },
        {
            "title": "Hard drive making clicking noise",
            "description": "Computer hard drive is making loud clicking noises and system is very slow. Worried about data loss. Please backup and replace urgently.",
            "priority": "Critical"
        },
        {
            "title": "Computer extremely slow performance",
            "description": "Desktop computer takes forever to start up and open programs. Performance has degraded significantly over past week. Need diagnostic.",
            "priority": "Medium"
        },
        {
            "title": "USB ports not recognizing devices",
            "description": "None of the USB ports on my laptop are working. Can't connect mouse, keyboard, or USB drives. Tried different devices but same issue.",
            "priority": "High"
        },
        {
            "title": "Laptop overheating and fan very loud",
            "description": "Laptop gets extremely hot and fan runs at maximum speed constantly. Sometimes shuts down automatically. Affects productivity.",
            "priority": "High"
        },
        {
            "title": "Desktop computer crashes randomly",
            "description": "Desktop computer crashes randomly without warning. Blue screen appears briefly then restarts. Happens 3-4 times per day.",
            "priority": "High"
        }
    ]
    
    # Software Issues
    software_issues = [
        {
            "title": "Outlook not receiving emails",
            "description": "Microsoft Outlook stopped receiving new emails since yesterday. Can send emails but nothing comes in. Checked spam folder already.",
            "priority": "High"
        },
        {
            "title": "Excel file corrupted - cannot open",
            "description": "Important Excel spreadsheet with financial data shows corruption error when trying to open. File worked fine yesterday. Need recovery.",
            "priority": "High"
        },
        {
            "title": "Windows update failed with error",
            "description": "Windows update keeps failing with error code 0x80070005. Update runs for hours then fails. Computer asks to restart repeatedly.",
            "priority": "Medium"
        },
        {
            "title": "Antivirus blocking legitimate software",
            "description": "Antivirus software is blocking our business application from running. Added to exceptions but still blocks. Need configuration help.",
            "priority": "Medium"
        },
        {
            "title": "Chrome browser crashing frequently",
            "description": "Google Chrome crashes every 10-15 minutes especially when opening multiple tabs. Tried reinstalling but same issue persists.",
            "priority": "Medium"
        },
        {
            "title": "Application freezes when saving files",
            "description": "CAD application freezes every time I try to save large files. Have to force close and lose work. Very frustrating and time consuming.",
            "priority": "High"
        },
        {
            "title": "PDF files won't open - error message",
            "description": "All PDF files show error message 'file is damaged and could not be repaired'. Tried different PDF viewers but same error.",
            "priority": "Medium"
        },
        {
            "title": "Software license expired - activation needed",
            "description": "Adobe Creative Suite shows license expired message and won't start. Need to renew license or update activation key.",
            "priority": "Medium"
        },
        {
            "title": "Database connection timeout errors",
            "description": "ERP system shows database connection timeout errors frequently. Takes multiple attempts to connect. Slows down work significantly.",
            "priority": "High"
        },
        {
            "title": "Video conference audio not working",
            "description": "Teams/Zoom audio not working during video calls. Can hear others but they can't hear me. Microphone works in other applications.",
            "priority": "High"
        }
    ]
    
    # Network Issues
    network_issues = [
        {
            "title": "Internet connection very slow",
            "description": "Internet speed is extremely slow. Websites take forever to load and file downloads timeout. Affects entire office building.",
            "priority": "High"
        },
        {
            "title": "WiFi keeps disconnecting frequently",
            "description": "WiFi connection drops every 5-10 minutes and have to reconnect manually. Other devices on same network work fine.",
            "priority": "Medium"
        },
        {
            "title": "Cannot access shared network drives",
            "description": "Cannot connect to shared drives on network. Get access denied error even with correct credentials. Need files for project deadline.",
            "priority": "High"
        },
        {
            "title": "VPN connection fails with authentication error",
            "description": "Cannot connect to company VPN from home. Authentication fails even with correct username and password. Need access for remote work.",
            "priority": "High"
        },
        {
            "title": "Email server not reachable",
            "description": "Cannot connect to email server. Outlook shows server unavailable error. Affects multiple users in department.",
            "priority": "Critical"
        },
        {
            "title": "Company website not loading",
            "description": "Company website shows timeout error and won't load. Other websites work fine. Customers reporting same issue.",
            "priority": "Critical"
        },
        {
            "title": "Network printer not found",
            "description": "Network printer disappeared from available printers list. Cannot print important documents. Other users have same issue.",
            "priority": "Medium"
        },
        {
            "title": "Remote desktop connection failed",
            "description": "Cannot connect to office computer remotely. Remote desktop shows connection error. Need access to files on office machine.",
            "priority": "High"
        },
        {
            "title": "File transfer to server interrupted",
            "description": "Large file transfers to server keep getting interrupted and fail. Tried multiple times but connection drops during upload.",
            "priority": "Medium"
        },
        {
            "title": "DNS resolution not working properly",
            "description": "Some websites work while others don't load. DNS lookup seems to fail for certain domains. Intermittent connectivity issues.",
            "priority": "Medium"
        }
    ]
    
    # Security Issues
    security_issues = [
        {
            "title": "Suspicious phishing email received",
            "description": "Received suspicious email claiming to be from bank asking for login credentials. Looks like phishing attempt. Please investigate immediately.",
            "priority": "High"
        },
        {
            "title": "Password reset not working",
            "description": "Cannot reset my domain password. Reset link in email doesn't work and system shows invalid token error. Need access urgently.",
            "priority": "High"
        },
        {
            "title": "Account locked after multiple login attempts",
            "description": "My account got locked after entering wrong password multiple times. Cannot access any systems. Need account unlocked please.",
            "priority": "Medium"
        },
        {
            "title": "Malware detected on computer",
            "description": "Antivirus detected malware on my computer and quarantined several files. Computer running very slow. Need full system scan.",
            "priority": "Critical"
        },
        {
            "title": "Unauthorized access to file server",
            "description": "Security logs show unauthorized access attempts to file server. Multiple failed login attempts from unknown IP address.",
            "priority": "Critical"
        },
        {
            "title": "Suspicious network activity detected",
            "description": "Network monitoring tools flagging unusual outbound traffic from my computer. Might be compromised. Please investigate.",
            "priority": "Critical"
        },
        {
            "title": "Two-factor authentication not working",
            "description": "2FA app not generating correct codes for login. Tried multiple times but authentication fails. Cannot access work systems.",
            "priority": "High"
        },
        {
            "title": "Security certificate expired warning",
            "description": "Browser shows security certificate expired warning for company intranet. Cannot access internal websites safely.",
            "priority": "Medium"
        },
        {
            "title": "Firewall blocking legitimate application",
            "description": "Company firewall is blocking our new business application from connecting to internet. Need firewall rule configuration.",
            "priority": "Medium"
        },
        {
            "title": "Possible data breach - need investigation",
            "description": "Received notification that company email might be involved in data breach. Need to check if our systems are affected.",
            "priority": "Critical"
        }
    ]
    
    # User Roles und ihre typischen Eigenschaften
    user_roles = [
        {'role': 'end_user', 'weight': 0.6, 'avg_tickets': 2, 'tech_savvy': 0.3},
        {'role': 'admin', 'weight': 0.15, 'avg_tickets': 8, 'tech_savvy': 0.9},
        {'role': 'developer', 'weight': 0.15, 'avg_tickets': 6, 'tech_savvy': 0.85},
        {'role': 'manager', 'weight': 0.08, 'avg_tickets': 1, 'tech_savvy': 0.4},
        {'role': 'intern', 'weight': 0.02, 'avg_tickets': 4, 'tech_savvy': 0.6}
    ]
    
    # Departments
    departments = ['IT', 'HR', 'Finance', 'Sales', 'Marketing', 'Operations', 'Legal']
    dept_weights = [0.25, 0.15, 0.15, 0.15, 0.15, 0.1, 0.05]
    
    # Affected Systems
    systems = ['email', 'erp', 'crm', 'network', 'workstation', 'server', 'database', 'web_app', 'printer']
    
    # Generiere Tickets
    tickets = []
    ticket_counter = 1
    
    for i in range(n_samples):
        # Wähle Kategorie
        categories = ['Hardware', 'Software', 'Network', 'Security']
        category_weights = [0.28, 0.35, 0.22, 0.15]
        category = np.random.choice(categories, p=category_weights)
        
        # Wähle Issue Template basierend auf Kategorie
        if category == 'Hardware':
            issue_template = np.random.choice(hardware_issues)
        elif category == 'Software':
            issue_template = np.random.choice(software_issues)
        elif category == 'Network':
            issue_template = np.random.choice(network_issues)
        else:  # Security
            issue_template = np.random.choice(security_issues)
        
        # Wähle User Role
        role_data = np.random.choice(user_roles, p=[r['weight'] for r in user_roles])
        user_role = role_data['role']
        
        # Department und System
        department = np.random.choice(departments, p=dept_weights)
        affected_system = np.random.choice(systems)
        
        # Time-based attributes
        base_date = datetime.now() - timedelta(days=np.random.randint(0, 180))
        hour_submitted = np.random.choice(range(24), p=[
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01,  # 0-5 Uhr
            0.02, 0.05, 0.08, 0.12, 0.15, 0.15,  # 6-11 Uhr  
            0.12, 0.15, 0.15, 0.12, 0.08, 0.05,  # 12-17 Uhr
            0.02, 0.01, 0.01, 0.01, 0.01, 0.01   # 18-23 Uhr
        ])
        
        is_weekend = 1 if base_date.weekday() >= 5 else 0
        
        # Priority Logic
        base_priority = issue_template['priority']
        priority = base_priority
        
        # Adjustments basierend auf Context
        if user_role in ['admin', 'developer'] and priority == 'Low':
            priority = np.random.choice(['Medium', 'High'], p=[0.7, 0.3])
        
        if (hour_submitted < 8 or hour_submitted > 18) and priority != 'Critical':
            if priority == 'Low':
                priority = 'Medium'
            elif priority == 'Medium' and np.random.random() < 0.3:
                priority = 'High'
        
        if affected_system in ['server', 'database', 'email'] and priority == 'High':
            if np.random.random() < 0.2:
                priority = 'Critical'
        
        # Previous tickets (User History)
        base_tickets = role_data['avg_tickets']
        previous_tickets = max(0, int(np.random.poisson(base_tickets)))
        
        # Variiere Beschreibung leicht
        title = issue_template['title']
        description = issue_template['description']
        
        # Füge gelegentlich zusätzliche Details hinzu
        additional_details = [
            "This is urgent and blocking my work.",
            "Please help as soon as possible.",
            "Multiple users are affected by this issue.",
            "This started happening after the latest update.",
            "I tried restarting but the problem persists.",
            "Error message appears intermittently.",
            "This never happened before today.",
            "Colleagues have reported similar issues.",
            "Need this resolved before end of day.",
            "This is affecting our project deadline."
        ]
        
        if np.random.random() < 0.4:
            description += " " + np.random.choice(additional_details)
        
        # Erstelle Ticket
        ticket = {
            'ticket_id': f'TICK-2025-{ticket_counter:05d}',
            'title': title,
            'description': description,
            'category': category,
            'priority': priority,
            'user_role': user_role,
            'department': department,
            'affected_system': affected_system,
            'hour_submitted': hour_submitted,
            'is_weekend': is_weekend,
            'previous_tickets_30d': previous_tickets,
            'created_date': base_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': np.random.choice(['Open', 'In Progress', 'Resolved'], p=[0.3, 0.4, 0.3]),
            'resolution_time_hours': np.random.lognormal(2, 1) if np.random.random() < 0.7 else None
        }
        
        tickets.append(ticket)
        ticket_counter += 1
    
    return pd.DataFrame(tickets)

def create_sample_files():
    """
    Erstellt verschiedene Beispieldateien
    """
    print("🎫 Generiere IT-Ticket Beispieldaten...")
    
    # Erstelle data Verzeichnisse falls sie nicht existieren
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # Generiere verschiedene Datensätze
    datasets = {
        'data/raw/training_data.csv': 15000,
        'data/raw/test_data.csv': 3000,
        'data/raw/demo_data.csv': 100
    }
    
    for filename, size in datasets.items():
        print(f"📄 Erstelle {filename} mit {size:,} Tickets...")
        df = generate_realistic_tickets(size)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        # Zeige Statistiken
        print(f"   ✓ Kategorien: {df['category'].value_counts().to_dict()}")
        print(f"   ✓ Prioritäten: {df['priority'].value_counts().to_dict()}")
        print(f"   ✓ Benutzerrollen: {df['user_role'].value_counts().to_dict()}")
        print()
    
    # Erstelle auch ein kleines Demo-Dataset als JSON
    demo_df = generate_realistic_tickets(20)
    demo_df.to_json('data/raw/demo_tickets.json', orient='records', indent=2)
    
    print("📋 Beispiel-Tickets (erste 5):")
    print("=" * 80)
    for i, (_, ticket) in enumerate(demo_df.head().iterrows()):
        print(f"\n🎫 TICKET #{i+1} ({ticket['ticket_id']}):")
        print(f"   Titel: {ticket['title']}")
        print(f"   Kategorie: {ticket['category']} | Priorität: {ticket['priority']}")
        print(f"   Benutzer: {ticket['user_role']} aus {ticket['department']}")
        print(f"   System: {ticket['affected_system']}")
        print(f"   Beschreibung: {ticket['description'][:100]}...")
    
    print(f"\n✅ Beispieldaten erfolgreich erstellt!")
    print(f"📁 Dateien:")
    print(f"   - data/raw/training_data.csv (15,000 Tickets für Training)")
    print(f"   - data/raw/test_data.csv (3,000 Tickets für Testing)")  
    print(f"   - data/raw/demo_data.csv (100 Tickets für Demos)")
    print(f"   - data/raw/demo_tickets.json (20 Tickets als JSON)")

if __name__ == "__main__":
    print("🎯 IT-Ticket Beispieldaten Generator")
    print("=" * 50)
    
    # Erstelle Hauptdatensätze
    create_sample_files()
    
    print(f"\n📊 DATASET ÜBERSICHT:")
    print(f"=" * 30)
    print(f"✓ Training Dataset: 15,000 Tickets")
    print(f"✓ Test Dataset: 3,000 Tickets") 
    print(f"✓ Demo Dataset: 100 Tickets")
    print(f"\n🎯 Ready für Machine Learning Training!")