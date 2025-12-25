import streamlit as st
from io import BytesIO
from datetime import date, datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)


def _money(v: float) -> str:
    try:
        return f"{float(v):,.2f}"
    except Exception:
        return "0.00"


def generate_pdf(data: dict) -> BytesIO:
    buf = BytesIO()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="Achillion Hotel Booking Confirmation",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        textColor=colors.HexColor("#2C3E50"),
        alignment=1,  # center
        spaceAfter=6,
    )
    subtitle = ParagraphStyle(
        "subtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        textColor=colors.HexColor("#34495E"),
        alignment=1,
        spaceAfter=12,
        leading=14,
    )
    h2 = ParagraphStyle(
        "h2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=colors.HexColor("#2C3E50"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body = ParagraphStyle(
        "body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.HexColor("#333333"),
        leading=13,
    )
    small = ParagraphStyle(
        "small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.HexColor("#555555"),
        leading=12,
    )
    note_style = ParagraphStyle(
        "note",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        textColor=colors.HexColor("#555555"),
        leading=12,
    )

    def make_kv_table(rows):
        t = Table(rows, colWidths=[5.0 * cm, 11.0 * cm])
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#ECECEC")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#333333")),
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#FAFAFA")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        return t

    story = []
    story.append(Paragraph("Achillion Hotel", title))
    story.append(
        Paragraph(
            "<b>Thank you for choosing <font color='#3498DB'>Achillion Hotel</font>!</b><br/>"
            "We look forward to welcoming you soon.",
            subtitle,
        )
    )

    # Guest Details
    story.append(Paragraph("Guest Details", h2))
    guest_rows = [
        ["Guest Name", data["guest_name"]],
        ["Room Type", data["room_type"]],
        ["Number of Guests", data["guests"]],
    ]
    story.append(make_kv_table(guest_rows))
    story.append(Spacer(1, 10))

    # Booking Details
    story.append(Paragraph("Booking Details", h2))
    booking_rows = [
        [
            "Check-In / Check-Out",
            f"{data['check_in']} (15:00–23:00) — {data['check_out']} (08:00–11:00)",
        ],
        ["Total Nights", str(data["nights"])],
        ["Price (incl. Tax)", f"{data['price']} €"],
        ["Environment Tax", f"{data['environment_tax']} €"],
        ["Total Charge", f"{data['total_charge']} €"],
        ["Payment Status", data["payment_status"] or "—"],
    ]
    story.append(make_kv_table(booking_rows))

    story.append(Spacer(1, 10))

    # Note box
    note_table = Table(
        [[Paragraph("<b>Note:</b> Please be informed that parking services are not available at the facility.", note_style)]],
        colWidths=[16.0 * cm],
    )
    note_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F0F4F8")),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#ECECEC")),
                ("LINEBEFORE", (0, 0), (0, 0), 4, colors.HexColor("#3498DB")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(note_table)
    story.append(Spacer(1, 10))

    # Terms
    story.append(Paragraph("Terms & Conditions", h2))
    story.append(
        Paragraph(
            "For complete terms and conditions, please visit our website: "
            "<font color='#3498DB'>www.achillion-paralia.gr/terms</font>",
            body,
        )
    )
    story.append(Spacer(1, 8))

    # Contact + Bank side-by-side
    story.append(Paragraph("Hotel Contact Details & Bank Details", h2))

    contact_box = Table(
        [[
            Paragraph(
                "<b>Hotel Contact Details</b><br/>"
                "Address: 6, Nikis Str., Paralia Katerinis, Pieria, Greece<br/>"
                "Coordinates: 40.267814, 22.596908<br/>"
                "Email: achillion.paralia@gmail.com<br/>"
                "Phone: +30 2351061320, +30 6946 552892<br/>"
                "Website: www.achillion-paralia.gr",
                small,
            )
        ]],
        colWidths=[7.8 * cm],
    )
    bank_box = Table(
        [[
            Paragraph(
                "<b>Bank Details</b><br/>"
                "Bank: Alpha Bank<br/>"
                "IBAN: GR5601408400840002002023605<br/>"
                "BIC: CRBAGRAA<br/>"
                "Name: Kampouridis Dimitris",
                small,
            )
        ]],
        colWidths=[7.8 * cm],
    )

    for box in (contact_box, bank_box):
        box.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F8FA")),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#ECECEC")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

    two_col = Table([[contact_box, bank_box]], colWidths=[8.0 * cm, 8.0 * cm], hAlign="LEFT")
    two_col.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    story.append(two_col)
    story.append(Spacer(1, 10))

    # Cancellation
    story.append(Paragraph("Cancellation Policy", h2))
    story.append(Paragraph("There are no refunds for cancellations within <b>14 days</b> prior to arrival.", body))
    story.append(Spacer(1, 14))

    # Footer
    story.append(
        Paragraph(
            "Confirmed by: <b>Kampouridis Dimitris</b>, Hotel Manager",
            ParagraphStyle("footer", parent=small, alignment=1, textColor=colors.HexColor("#999999")),
        )
    )

    doc.build(story)
    buf.seek(0)
    return buf


st.set_page_config(page_title="Achillion Hotel Booking Confirmation", page_icon="🏨", layout="centered")

st.title("Achillion Hotel Booking Confirmation")
st.header("Provide your booking details:")

guest_name = st.text_input("Guest Name", placeholder="Enter guest's full name")
room_type = st.text_input("Room Type (Custom)")

check_in = st.date_input("Check-in Date", value=date.today())
check_out = st.date_input("Check-out Date", value=date.today())

nights = (check_out - check_in).days if check_out and check_in else 0

guests = st.text_input("Number of Guests", placeholder="e.g., 2 adults, 1 child")

price = st.number_input("Price (incl. Tax, €)", min_value=0.0, step=0.01)
environment_tax = st.number_input("Environment Tax (€)", min_value=0.0, step=0.01)
payment_status = st.text_input("Payment Status", placeholder="e.g., Paid in full, Pending")

total_charge = price + environment_tax

if st.button("Generate PDF"):
    if not guest_name.strip() or not guests.strip() or nights <= 0:
        st.error("Please fill out Guest Name, Number of Guests, and ensure Check-out is after Check-in.")
    else:
        data = {
            "guest_name": guest_name.strip(),
            "room_type": room_type.strip() or "—",
            "check_in": check_in.strftime("%d-%m-%Y"),
            "check_out": check_out.strftime("%d-%m-%Y"),
            "nights": nights,
            "guests": guests.strip(),
            "price": _money(price),
            "environment_tax": _money(environment_tax),
            "total_charge": _money(total_charge),
            "payment_status": payment_status.strip(),
        }

        pdf_buffer = generate_pdf(data)

        clean_guest_name = "".join(c for c in guest_name if c.isalnum() or c.isspace()).strip()
        clean_guest_name = clean_guest_name.replace(" ", "_") or "Guest"
        filename = f"{clean_guest_name}_{check_in.strftime('%d-%m-%Y')}_{check_out.strftime('%d-%m-%Y')}.pdf"

        st.download_button(
            "Download Confirmation PDF",
            data=pdf_buffer,
            file_name=filename,
            mime="application/pdf",
        )
