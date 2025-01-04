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
                margin: 1cm;
            }}
            body {{
                font-family: 'Georgia', serif;
                color: #2F2F2F;
                line-height: 1.5;
                margin: 0;
                padding: 0;
            }}
            .container {{
                padding: 20px;
                max-width: 800px;
                margin: auto;
            }}
            h1 {{
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                color: #1A1A1A;
                margin: 10px 0;
                letter-spacing: 1px;
            }}
            h2 {{
                font-size: 18px;
                font-weight: 600;
                color: #8C8C8C;
                border-bottom: 2px solid #D3A34D;
                padding-bottom: 4px;
                margin: 15px 0 10px 0;
            }}
            p {{
                font-size: 14px;
                color: #555;
                margin: 5px 0;
            }}
            table {{
                width: 100%;
                margin: 10px 0;
                border-collapse: collapse;
            }}
            th, td {{
                font-size: 14px;
                text-align: left;
                padding: 8px 10px;
                border: 1px solid #EAEAEA;
            }}
            th {{
                background-color: #F4F4F4;
                color: #555;
                font-weight: bold;
            }}
            .note {{
                background-color: #FFF0F0;
                padding: 10px;
                border-left: 5px solid #FF0000;
                margin: 15px 0;
                font-style: italic;
                font-size: 14px;
                color: #FF0000;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #8C8C8C;
                margin-top: 15px;
                line-height: 1.2;
            }}
            .footer p {{
                margin: 2px 0;
            }}
            .highlight {{
                color: #D3A34D;
                font-weight: bold;
            }}
            .bank-details {{
                background-color: #FAFAFA;
                padding: 10px;
                border: 1px solid #EAEAEA;
                border-radius: 8px;
                margin-top: 10px;
                font-size: 14px;
                line-height: 1.4;
            }}
            .bank-details p {{
                margin: 3px 0;
            }}
            .contact-details {{
                line-height: 1.3;
                margin: 5px 0;
            }}
            .contact-details p {{
                margin: 3px 0;
            }}
            .welcome-text {{
                text-align: center;
                font-size: 16px;
                color: #666;
                margin: 10px 0;
            }}
            a {{
                color: #D3A34D;
                text-decoration: none;
            }}
            .page-break {{
                page-break-before: always;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Achillion Hotel Booking Confirmation</h1>

            <p class="welcome-text">
                <strong>Your booking has been confirmed!</strong> Thank you for choosing <span class="highlight">Achillion Hotel</span>.
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
                    <th>Check-in Date</th>
                    <td>{data['check_in']}</td>
                </tr>
                <tr>
                    <th>Check-out Date</th>
                    <td>{data['check_out']}</td>
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

            <div class="page-break"></div>

            <h2>Hotel Contact Details</h2>
            <div class="contact-details">
                <p><strong>Address:</strong> 6, Nikis Str., Paralia Katerinis, Pieria, Greece | <strong>Coordinates:</strong> 40.267814, 22.596908</p>
                <p><strong>Email:</strong> <a href="mailto:achillion.paralia@gmail.com">achillion.paralia@gmail.com</a> | <strong>Phone:</strong> +30 2351061320, +30 6946 552892 | <strong>Website:</strong> <a href="http://www.achillion-paralia.gr">www.achillion-paralia.gr</a></p>
            </div>

            <h2>Bank Details</h2>
            <div class="bank-details">
                <p><strong>Bank:</strong> Alpha Bank | <strong>IBAN:</strong> GR5601408400840002002023605 | <strong>BIC:</strong> CRBAGRAA</p>
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

    # Form Inputs
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
