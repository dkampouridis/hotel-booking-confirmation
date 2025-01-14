import streamlit as st
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime

def generate_pdf(data):
    # Fresh, elegant CSS design with subtle styling
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
                background-color: #F9FBFD; /* Soft background */
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: auto;
                background-color: #FFFFFF;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-radius: 8px;
                padding: 25px 30px;
            }}
            h1 {{
                font-size: 28px;
                font-weight: 700;
                color: #2C3E50;
                margin-bottom: 6px;
                text-align: center;
                letter-spacing: 1px;
            }}
            .subheader {{
                text-align: center;
                color: #7F8C8D;
                font-size: 16px;
                margin-bottom: 30px;
            }}
            h2 {{
                font-size: 18px;
                color: #2C3E50;
                margin: 24px 0 12px;
                position: relative;
            }}
            h2::after {{
                content: "";
                display: block;
                width: 60px;
                height: 3px;
                background-color: #ADCBE3;
                margin-top: 6px;
            }}
            .welcome-text {{
                text-align: center;
                font-size: 16px;
                margin-bottom: 20px;
                color: #34495E;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
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
                background-color: #F0F4F8; /* Subtle, blending background */
                padding: 12px;
                border-left: 4px solid #3498DB; /* Thin accent on the left */
                margin: 15px 0;
                font-size: 14px;
                color: #555; /* Subtler text color */
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #999;
                margin-top: 30px;
            }}
            .footer p {{
                margin: 2px 0;
            }}
            .highlight {{
                color: #3498DB;
                font-weight: bold;
            }}
            .bank-details {{
                background-color: #F4F8FA;
                padding: 14px;
                border: 1px solid #ECECEC;
                border-radius: 6px;
                margin-top: 10px;
                font-size: 14px;
                line-height: 1.4;
            }}
            .contact-details {{
                line-height: 1.4;
                margin: 8px 0;
                font-size: 14px;
            }}
            .contact-details p {{
                margin: 4px 0;
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
            <div class="subheader">Booking Confirmation</div>

            <p class="welcome-text">
                <strong>Thank you for choosing <span class="highlight">Achillion Hotel</span>!</strong><br>
                We look forward to welcoming you soon.
            </p>

            <h2>Guest Details</h2>
            <table>
                <tr>
                    <th>Guest Name</th>
                    <td>{data['guest_name']}</td>
                </tr>
                <tr>
                    <th>Room Type</th>
                    <td>{data['room_type']}</td>
                </tr>
                <tr>
                    <th>Number of Guests</th>
                    <td>{data['guests']}</td>
                </tr>
            </table>

            <h2>Booking Details</h2>
            <table>
                <tr>
                    <th>Check-In / Check-Out</th>
                    <td>
                        {data['check_in']} (15:00 - 23:00) &nbsp;—&nbsp; 
                        {data['check_out']} (08:00 - 11:00)
                    </td>
                </tr>
                <tr>
                    <th>Total Nights</th>
                    <td>{data['nights']}</td>
                </tr>
                <tr>
                    <th>Price (incl. Tax)</th>
                    <td>{data['price']} €</td>
                </tr>
                <tr>
                    <th>Environment Tax</th>
                    <td>{data['environment_tax']} €</td>
                </tr>
                <tr>
                    <th>Total Charge</th>
                    <td>{data['total_charge']} €</td>
                </tr>
                <tr>
                    <th>Payment Status</th>
                    <td>{data['payment_status']}</td>
                </tr>
            </table>

            <div class="note">
                <strong>Note:</strong> Please be informed that parking services are not available at the facility.
            </div>

            <h2>Hotel Contact Details</h2>
            <div class="contact-details">
                <p>
                    <strong>Address:</strong> 6, Nikis Str., Paralia Katerinis, Pieria, Greece<br>
                    <strong>Coordinates:</strong> 40.267814, 22.596908
                </p>
                <p>
                    <strong>Email:</strong> <a href="mailto:achillion.paralia@gmail.com">achillion.paralia@gmail.com</a><br>
                    <strong>Phone:</strong> +30 2351061320, +30 6946 552892<br>
                    <strong>Website:</strong> <a href="http://www.achillion-paralia.gr">www.achillion-paralia.gr</a>
                </p>
            </div>

            <h2>Bank Details</h2>
            <div class="bank-details">
                <p><strong>Bank:</strong> Alpha Bank</p>
                <p><strong>IBAN:</strong> GR5601408400840002002023605</p>
                <p><strong>BIC:</strong> CRBAGRAA</p>
            </div>

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

            # Create filename using guest name and dates
            clean_guest_name = "".join(c for c in guest_name if c.isalnum() or c.isspace()).replace(" ", "_")
            filename = f"{clean_guest_name}_{check_in.strftime('%d-%m-%Y')}_{check_out.strftime('%d-%m-%Y')}.pdf"
            
            st.download_button(
                "Download Confirmation PDF",
                pdf_buffer,
                filename,
                "application/pdf"
            )
