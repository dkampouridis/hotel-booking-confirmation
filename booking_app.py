import streamlit as st
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime


def generate_pdf(data):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @page {{
                size: A4;
                margin: 1.5cm;
            }}
            body {{
                margin: 0;
                padding: 0;
                font-family: "Helvetica", Arial, sans-serif;
                background-color: #F9FBFD;
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: auto;
                background-color: #FFFFFF;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-radius: 8px;
                padding: 25px 30px;
                page-break-inside: avoid;
            }}
            h1 {{
                font-size: 28px;
                font-weight: 700;
                color: #2C3E50;
                text-align: center;
                margin-bottom: 5px;
                letter-spacing: 1px;
            }}
            .welcome-text {{
                text-align: center;
                font-size: 16px;
                margin-bottom: 16px;
                color: #34495E;
            }}
            .highlight {{
                color: #3498DB;
                font-weight: bold;
            }}
            h2 {{
                font-size: 18px;
                color: #2C3E50;
                margin: 16px 0 8px;
                position: relative;
            }}
            h2::after {{
                content: "";
                display: block;
                width: 50px;
                height: 2px;
                background-color: #ADCBE3;
                margin-top: 4px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 16px;
            }}
            th, td {{
                border: 1px solid #ECECEC;
                padding: 10px 12px;
                font-size: 14px;
                vertical-align: top;
            }}
            th {{
                background-color: #FAFAFA;
                font-weight: 600;
                color: #555;
                width: 30%;
            }}
            .note {{
                background-color: #F0F4F8;
                padding: 8px 10px;
                border-left: 4px solid #3498DB;
                margin: 10px 0 15px;
                font-size: 14px;
                color: #555;
            }}
            .info-sections {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                align-items: flex-start;
                margin-bottom: 10px;
            }}
            .info-section {{
                flex: 1 1 350px;
            }}
            .contact-details p,
            .bank-details p {{
                margin: 4px 0;
            }}
            .bank-details, .contact-details {{
                background-color: #F4F8FA;
                border: 1px solid #ECECEC;
                border-radius: 6px;
                padding: 10px 12px;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #999;
                margin-top: 5px;
            }}
            a {{
                color: #3498DB;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Achillion Hotel</h1>
            <p class="welcome-text">
                <strong>Thank you for choosing <span class="highlight">Achillion Hotel</span>!</strong><br>
                We look forward to welcoming you soon.
            </p>

            <h2>Guest Details</h2>
            <table>
                <tr><th>Guest Name</th><td>{data['guest_name']}</td></tr>
                <tr><th>Room Type</th><td>{data['room_type']}</td></tr>
                <tr><th>Number of Guests</th><td>{data['guests']}</td></tr>
            </table>

            <h2>Booking Details</h2>
            <table>
                <tr><th>Check-In / Check-Out</th><td>{data['check_in']} (15:00–23:00) &#8212; {data['check_out']} (08:00–11:00)</td></tr>
                <tr><th>Total Nights</th><td>{data['nights']}</td></tr>
                <tr><th>Price (incl. Tax)</th><td>{data['price']} €</td></tr>
                <tr><th>Environment Tax</th><td>{data['environment_tax']} €</td></tr>
                <tr><th>Total Charge</th><td>{data['total_charge']} €</td></tr>
                <tr><th>Payment Status</th><td>{data['payment_status']}</td></tr>
            </table>

            <div class="note">
                <strong>Note:</strong> Please be informed that parking services are not available at the facility.
            </div>

            <h2>Terms & Conditions</h2>
            <p>For complete terms and conditions, please visit our website: 
               <a href="http://www.achillion-paralia.gr/terms">www.achillion-paralia.gr/terms</a>
            </p>

            <div class="info-sections">
                <div class="info-section">
                    <h2>Hotel Contact Details</h2>
                    <div class="contact-details">
                        <p><strong>Address:</strong> 6, Nikis Str., Paralia Katerinis, Pieria, Greece</p>
                        <p><strong>Coordinates:</strong> 40.267814, 22.596908</p>
                        <p><strong>Email:</strong> <a href="mailto:achillion.paralia@gmail.com">achillion.paralia@gmail.com</a></p>
                        <p><strong>Phone:</strong> +30 2351061320, +30 6946 552892</p>
                        <p><strong>Website:</strong> <a href="http://www.achillion-paralia.gr">www.achillion-paralia.gr</a></p>
                    </div>
                </div>
                <div class="info-section">
                    <h2>Bank Details</h2>
                    <div class="bank-details">
                        <p><strong>Bank:</strong> Alpha Bank</p>
                        <p><strong>IBAN:</strong> GR5601408400840002002023605</p>
                        <p><strong>BIC:</strong> CRBAGRAA</p>
                    </div>
                </div>
            </div>

            <h2>Cancellation Policy</h2>
            <p>There are no refunds for cancellations within <strong>14 days</strong> prior to arrival.</p>

            <div class="footer">
                <p>Confirmed by: <strong>Kampouridis Dimitris</strong>, Hotel Manager</p>
                <p>© 2025 Achillion Hotel - Apartments. All Rights Reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Generate PDF
    pdf_buffer = BytesIO()
    pisa.CreatePDF(html_template, dest=pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer


if __name__ == "__main__":
    st.title("Achillion Hotel Booking Confirmation")

    st.header("Provide your booking details:")
    guest_name = st.text_input("Guest Name", placeholder="Enter guest's full name")
    room_type = st.text_input("Room Type (Custom)")
    
    check_in = st.date_input("Check-in Date", value=datetime.now())
    check_out = st.date_input("Check-out Date", value=datetime.now())
    nights = (check_out - check_in).days if check_out > check_in else 0
    guests = st.text_input("Number of Guests", placeholder="e.g., 2 adults, 1 child")
    
    price = st.number_input("Price (incl. Tax, €)", min_value=0.0, step=0.01)
    environment_tax = st.number_input("Environment Tax (€)", min_value=0.0, step=0.01)
    payment_status = st.text_input("Payment Status", placeholder="e.g., Paid in full, Pending")

    # Calculate total charge
    total_charge = price + environment_tax

    # Generate PDF
    if st.button("Generate PDF"):
        if not guest_name or not guests or nights <= 0:
            st.error("Please fill out all fields correctly.")
        else:
            data = {
                "guest_name": guest_name,
                "room_type": room_type,
                "check_in": check_in.strftime("%d-%m-%Y"),
                "check_out": check_out.strftime("%d-%m-%Y"),
                "nights": nights,
                "guests": guests,
                "price": f"{price:,.2f}",
                "environment_tax": f"{environment_tax:,.2f}",
                "total_charge": f"{total_charge:,.2f}",
                "payment_status": payment_status,
            }
            pdf_buffer = generate_pdf(data)

            clean_guest_name = "".join(
                c for c in guest_name if c.isalnum() or c.isspace()
            ).replace(" ", "_")
            filename = f"{clean_guest_name}_{check_in.strftime('%d-%m-%Y')}_{check_out.strftime('%d-%m-%Y')}.pdf"
            
            st.download_button(
                "Download Confirmation PDF",
                pdf_buffer,
                filename,
                "application/pdf"
            )
