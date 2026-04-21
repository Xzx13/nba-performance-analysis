from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

OUTPUT_PDF = r"C:\Users\xuzhe\Desktop\IS1520\nba_report.pdf"
FIGURE_PATH = r"C:\Users\xuzhe\Desktop\IS1520\nba_figure.png"

doc = SimpleDocTemplate(
    OUTPUT_PDF, pagesize=letter,
    rightMargin=0.9*inch, leftMargin=0.9*inch,
    topMargin=0.9*inch, bottomMargin=0.9*inch
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('T', parent=styles['Title'], fontSize=20, spaceAfter=6,
    textColor=colors.HexColor('#1D428A'), alignment=TA_CENTER, fontName='Helvetica-Bold')
subtitle_style = ParagraphStyle('S', parent=styles['Normal'], fontSize=12, spaceAfter=4,
    textColor=colors.HexColor('#444444'), alignment=TA_CENTER, fontName='Helvetica')
section_style = ParagraphStyle('H', parent=styles['Heading2'], fontSize=12, spaceBefore=14,
    spaceAfter=5, textColor=colors.HexColor('#1D428A'), fontName='Helvetica-Bold')
body_style = ParagraphStyle('B', parent=styles['Normal'], fontSize=10, spaceAfter=6,
    leading=15, alignment=TA_JUSTIFY, fontName='Helvetica')
bullet_style = ParagraphStyle('BL', parent=styles['Normal'], fontSize=10, spaceAfter=4,
    leading=14, leftIndent=16, fontName='Helvetica')
caption_style = ParagraphStyle('Cap', parent=styles['Normal'], fontSize=8.5,
    textColor=colors.grey, alignment=TA_CENTER, spaceAfter=8, leading=12)

story = []

# Title
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("NBA Team Performance Analysis (2015–2022)", title_style))
story.append(Paragraph("Zhexi Xu", subtitle_style))
story.append(Paragraph("INFSCI 1400 &nbsp;|&nbsp; Spring 2025-2026", subtitle_style))
story.append(Spacer(1, 0.18*inch))

# Figure
story.append(Image(FIGURE_PATH, width=6.4*inch, height=5.0*inch))
story.append(Paragraph(
    "<i>Figure 1: (Top) Average home points scored per game for the top 15 NBA teams (2020–2022). "
    "(Bottom-left) NBA scoring trend by season from 2015 to 2022 for home and away teams. "
    "(Bottom-right) Home court win rate by season.</i>", caption_style))

# Legend
story.append(Paragraph("Legend", section_style))
story.append(Paragraph(
    "In the bar chart (top), bars are colored by rank: "
    "<b>dark blue</b> = top 5 highest-scoring teams, <b>medium blue</b> = ranks 6–10, "
    "<b>light blue</b> = ranks 11–15. "
    "In the scoring trend chart (bottom-left), the <b>blue line with circles</b> represents the "
    "home team average points per game, and the <b>red line with squares</b> represents the away team. "
    "The shaded area between them shows the scoring gap. "
    "In the home win rate chart (bottom-right), <b>red bars</b> above the dashed 50% line "
    "indicate that home teams win more than half of all games.", body_style))

# Findings
story.append(Paragraph("Key Findings", section_style))
findings = [
    "The <b>Utah Jazz (UTA)</b> had the highest average home points scored at <b>117.2 points per game</b> from 2020–2022, followed closely by Denver (DEN) and Milwaukee (MIL).",
    "NBA scoring has increased significantly over the years — average points per game rose from around <b>104 in 2015 to over 114 in 2022</b>, showing the league has shifted toward a faster, more offensive style of play.",
    "Home teams consistently score more than away teams every season, with a gap of roughly <b>2–3 points per game</b> on average.",
    "Home court advantage is real — home teams won between <b>53.7% and 59.4%</b> of games every season from 2015 to 2022.",
    "The 2019 season had the lowest home win rate at <b>53.7%</b>, possibly affected by the NBA bubble games played without fans.",
    "The most recent season (2022) shows home teams winning <b>58.9%</b> of games, suggesting home court advantage has returned strongly after the pandemic era.",
]
for f in findings:
    story.append(Paragraph(f"• {f}", bullet_style))

story.append(PageBreak())

# Data and Methods
story.append(Paragraph("Data and Methods", section_style))
story.append(Paragraph(
    "<b>Data Source:</b> I used the NBA Games dataset from Kaggle, which contains data on over "
    "26,000 NBA games from 2003 to 2022. For this analysis I focused on seasons 2015–2022 "
    "to look at more recent trends. The dataset includes columns like game date, home and away "
    "team IDs, points scored, and win/loss results.", body_style))
story.append(Paragraph(
    "<b>Data Cleaning:</b> I filtered the data to only include seasons between 2015 and 2022. "
    "I merged the games data with the teams file to get team abbreviations. "
    "For the top 15 chart, I only used 2020–2022 data to focus on recent performance.", body_style))
story.append(Paragraph(
    "<b>Analysis:</b> I grouped the data by team to calculate average home points scored. "
    "For the scoring trend, I grouped by season and computed the mean home and away scores. "
    "For the win rate chart, I calculated the percentage of games won by the home team each season.", body_style))
story.append(Paragraph(
    "<b>Tools:</b> All charts were made in Python using pandas for data processing and "
    "matplotlib for visualization. The report was created using reportlab.", body_style))

# Significance
story.append(Paragraph("Significance Statement", section_style))
story.append(Paragraph(
    "I picked this topic because I enjoy watching NBA games and was curious whether home court "
    "advantage is actually real or just something people say. The data clearly shows it is real — "
    "home teams win more than 50% of games in every single season from 2015 to 2022.", body_style))
story.append(Paragraph(
    "Another thing I found interesting is how much NBA scoring has gone up over the years. "
    "The average team went from scoring around 104 points per game in 2015 to over 114 in 2022. "
    "<b>That's a 10-point increase in just 7 years</b>, which is pretty significant. "
    "This reflects how the modern NBA has moved toward three-point shooting and faster pace of play.", body_style))
story.append(Paragraph(
    "This kind of analysis is useful for fans trying to understand trends in the game, "
    "and also for teams and coaches thinking about scheduling or game strategy. "
    "It also shows that playing at home still matters a lot, even in today's NBA.", body_style))

# GitHub
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("GitHub Repository", section_style))
story.append(Paragraph(
    "Code, data sources, and this report are archived at: "
    "<b>https://github.com/Xzx13/nba-performance-analysis</b>", body_style))

doc.build(story)
print("PDF saved to:", OUTPUT_PDF)
