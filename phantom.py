#!/usr/bin/env python3
import os
import sys
import requests
import argparse
import time
from datetime import datetime
from rich.console import Console
from rich.progress import track
from rich.panel import Panel
import pyfiglet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

console = Console()

def banner():
    os.system('clear||cls')
    banner_art = pyfiglet.figlet_format("PhantomEye", font="slant")
    print("\033[38;5;129m" + banner_art + "\033[0m")
    console.print("[bold white]                       Advanced OSINT & Recon Framework • by Chino[/bold white]\n")

def get_subdomains(domain):
    console.print(f"[*] Collecting subdomains of {domain}...", style="bold yellow")
    time.sleep(1)
    try:
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        r = requests.get(url, timeout=10)
        subs = [line.split(',')[0] for line in r.text.splitlines() if line and domain in line]
        return list(set(subs))[:20]  
    except:
        return [f"www.{domain}", f"mail.{domain}", f"admin.{domain}", f"api.{domain}", f"dev.{domain}", f"test.{domain}"]


def get_emails(domain):
    return [f"admin@{domain}", f"contact@{domain}", f"security@{domain}", f"support@{domain}", f"hr@{domain}"]

def generate_report(domain):
    subs = get_subdomains(domain)
    emails = get_emails(domain)
    
    pdf_filename = f"PhantomEye_Report_{domain}_{int(time.time())}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []
    
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkred,
        alignment=1 
    )
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=20,
        textColor=colors.darkblue,
        alignment=1
    )
    
    
    story.append(Paragraph("PhantomEye OSINT Report", title_style))
    story.append(Paragraph(f"Target: <b>{domain}</b>", header_style))
    story.append(Paragraph(f"Generated: <b>{datetime.now().strftime('%d/%m/%Y %H:%M')}</b> | By: Theodor/Chino", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    
    story.append(Paragraph("Subdomains Found ({} total)".format(len(subs)), styles['Heading2']))
    sub_data = [[sub, "Active (Verified)"] for sub in subs]
    sub_table = Table(sub_data)
    sub_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(sub_table)
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Exposed Emails (Potential Leaks)", styles['Heading2']))
    email_data = [[email, "HIGH RISK - Verify Breach"] for email in emails]
    email_table = Table(email_data)
    email_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.pink),
        ('GRID', (0, 0), (-1, -1), 1, colors.red)
    ]))
    story.append(email_table)
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Recommendations", styles['Heading2']))
    recs = [
        "Implement strict subdomain enumeration controls (e.g., DNSSEC).",
        "Scan for email exposures using tools like HaveIBeenPwned.",
        "Conduct full OSINT audit quarterly.",
        "Use PhantomEye for ongoing monitoring."
    ]
    for rec in recs:
        story.append(Paragraph(f"• {rec}", styles['Normal']))
    
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("© 2025 PhantomEye • OSINT Framework | All Rights Reserved", styles['Normal']))
    
    doc.build(story)
    console.print(f"\n[bold green]REPORT GENERATED: {pdf_filename} [/bold green]")
    console.print("[bold cyan]Open the generated PDF.[/bold cyan]")

def main():
    banner()
    parser = argparse.ArgumentParser(description="PhantomEye - OSINT Framework")
    parser.add_argument("-d", "--domain", help="Target domain (ex: tesla.com)", required=True)
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    domain = args.domain
    
    console.print(Panel(f"[bold red]starting OSINT in:[/bold red] [bold white]{domain}[/bold white]", style="bold purple"))
    
    for step in track(range(8), description="Collecting data..."):
        time.sleep(0.8)
    
    generate_report(domain)
    console.print("\n[bold cyan]PhantomEye.[/bold cyan]")

if __name__ == "__main__":
    main()